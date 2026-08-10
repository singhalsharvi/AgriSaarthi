import io
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from pydantic import BaseModel, Field
from PIL import Image

from ai.disease_detection.prediction import predict_disease
from backend.services.rag.disease_retriever import DiseaseRetriever
from backend.services.rag.gemini_service import GeminiService
from backend.services.db_service import db_service

LOG = logging.getLogger("disease_router")

router = APIRouter(prefix="/disease", tags=["Disease Detection & Recommendation"])

disease_retriever = DiseaseRetriever()
gemini_service = GeminiService()

CONFIDENCE_THRESHOLD = 0.45  # 45% confidence threshold for CNN model

class DiseaseAnalysisResponse(BaseModel):
    status: str
    disease_status: str
    confidence: str
    top_matches: List[Dict[str, str]]
    ai_explanation: str
    crop: str
    disease: str
    confidence_status: str
    analysis: str
    sources: List[str]


@router.post("/analyze", response_model=DiseaseAnalysisResponse)
async def analyze_disease(request: Request) -> DiseaseAnalysisResponse:
    """Analyze crop disease symptoms and generate advisory via CNN model + RAG + Gemini service.

    Accepts BOTH multipart/form-data (image + optional form fields) and application/json (text query).
    """
    content_type = request.headers.get("content-type", "")
    
    # Defaults
    image_file: Optional[UploadFile] = None
    crop_name: Optional[str] = None
    symptoms: Optional[str] = None
    user_query: Optional[str] = None
    farmer_id: str = "ramesh.farmer@agrisaarthi.in"

    # 1. Parse incoming request based on content-type
    if "multipart/form-data" in content_type:
        try:
            form = await request.form()
            crop_name = form.get("crop_name") or form.get("cropName")
            symptoms = form.get("symptoms")
            user_query = form.get("user_query") or form.get("userQuery")
            farmer_id = form.get("farmer_id") or "ramesh.farmer@agrisaarthi.in"
            
            # File field
            file_obj = form.get("image") or form.get("photo")
            if file_obj and isinstance(file_obj, UploadFile):
                image_file = file_obj
        except Exception as err:
            raise HTTPException(status_code=400, detail=f"Failed to parse form-data: {str(err)}")
    else:
        # Fallback to JSON request
        try:
            body = await request.json()
            crop_name = body.get("crop_name") or body.get("cropName")
            symptoms = body.get("symptoms")
            user_query = body.get("user_query") or body.get("userQuery")
            farmer_id = body.get("farmer_id") or "ramesh.farmer@agrisaarthi.in"
        except Exception:
            # Empty request body
            pass

    # 2. Run inference or execute text-only RAG fallback
    top_predictions = []
    is_low_confidence = False
    confidence_pct = 100.0
    crop_pred = crop_name or "Tomato"
    disease_pred = "Healthy"

    if image_file:
        # Check image file format
        filename = image_file.filename or ""
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in ["jpg", "jpeg", "png", "webp"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Supported: JPG, JPEG, PNG, WEBP.")

        try:
            contents = await image_file.read()
            pil_image = Image.open(io.BytesIO(contents))
            
            # Perform CNN classification
            pred_results = predict_disease(pil_image)
            top_predictions = pred_results["top_3_predictions"]
            
            if top_predictions:
                best_match = top_predictions[0]
                crop_pred = best_match["crop"]
                disease_pred = best_match["disease"]
                confidence_pct = best_match["confidence"] * 100.0
                is_low_confidence = best_match["confidence"] < CONFIDENCE_THRESHOLD
        except Exception as err:
            LOG.error("CNN inference error: %s", err)
            raise HTTPException(status_code=500, detail=f"Model inference failed: {str(err)}")
    else:
        # Text-only diagnostics fallback
        # Map input crop/symptoms to a basic guess
        crop_pred = crop_name or "Tomato"
        disease_pred = symptoms or "Healthy"
        top_predictions = [
            {"crop": crop_pred, "disease": disease_pred, "confidence": 1.0}
        ]

    # 3. Query disease RAG vector database
    retrieval_query = f"{symptoms or ''} {user_query or ''}".strip()
    try:
        retrieval_result = disease_retriever.retrieve(
            query=retrieval_query,
            crop_name=crop_pred,
            disease_name=disease_pred,
            top_k=4
        )
        retrieved_docs = retrieval_result.get("retrieved_docs", [])
    except Exception as err:
        LOG.error("RAG retrieval error: %s", err)
        retrieved_docs = []

    # 4. Invoke grounded Gemini response
    sources = list(set([doc.get("source_file") for doc in retrieved_docs if doc.get("source_file")]))
    
    if not retrieved_docs:
        # Return explicit insufficient information response as required
        ai_explanation = (
            "## Insufficient Information\n\n"
            "The system found no matching verification records in our agricultural knowledge base for this crop disease. "
            "To protect your crops, we cannot provide automated recommendations without verified reference documents. "
            "Please check back later or consult your local extension office."
        )
    else:
        # Formulate query/metadata for Gemini based on confidence level
        if is_low_confidence:
            top3_str = "\n".join([f"- {item['crop']} - {item['disease']} (Confidence: {item['confidence']*100:.1f}%)" for item in top_predictions])
            user_prompt = (
                f"The image uploaded by the farmer could not be classified with high confidence.\n"
                f"Primary Guess: Crop: {crop_pred}, Disease: {disease_pred} (Confidence: {confidence_pct:.2f}%)\n"
                f"Top 3 possibilities:\n"
                f"{top3_str}\n\n"
                f"Retrieved context about the primary guess:\n"
                f"Please draft a supportive, cautious advisory stating the system is uncertain about the diagnosis. "
                f"Advise the farmer to upload a clearer, well-lit image of the leaf symptoms. "
                f"Explain what symptoms they should look for to distinguish between these possibilities. "
                f"Give general cultural advice (irrigation, airflow) and recommend consulting a local extension officer, "
                f"but do NOT prescribe chemical treatments since we are uncertain."
            )
        else:
            user_prompt = (
                f"Crop: {crop_pred}\n"
                f"Detected Disease: {disease_pred}\n"
                f"Model Confidence: {confidence_pct:.2f}%\n"
                f"Symptoms observed: {symptoms or 'None'}\n"
                f"Farmer query: {user_query or 'What treatment or organic remedies are recommended?'}"
            )

        try:
            ai_explanation = gemini_service.generate_response(
                user_query=user_prompt,
                domain="disease_detection",
                retrieved_docs=retrieved_docs,
                structured_metadata={
                    "crop": crop_pred,
                    "disease": disease_pred,
                    "confidence": f"{confidence_pct:.2f}%",
                    "is_low_confidence": is_low_confidence
                }
            )
        except Exception as err:
            LOG.error("Gemini service error: %s", err)
            ai_explanation = f"Error generating explanation from Gemini. Base Disease info: {disease_pred} on {crop_pred}."

    # Format top matches for response
    top_matches_formatted = []
    for item in top_predictions:
        name_str = f"{item['crop']} — {item['disease']}"
        conf_str = f"{item['confidence']*100:.1f}%"
        top_matches_formatted.append({"name": name_str, "confidence": conf_str})

    # If top_matches_formatted is empty, default
    if not top_matches_formatted:
        top_matches_formatted = [{"name": f"{crop_pred} — {disease_pred}", "confidence": f"{confidence_pct:.1f}%"}]

    confidence_status = "low" if is_low_confidence else "high"
    disease_status_str = f"{crop_pred} — {disease_pred}"

    # 5. Log activity in SQLite database
    try:
        db_service.log_activity(
            farmer_id=farmer_id,
            activity_type="disease_analysis",
            details={
                "crop": crop_pred,
                "disease": disease_pred,
                "confidence": f"{confidence_pct:.2f}%",
                "confidence_status": confidence_status,
                "has_image": image_file is not None
            }
        )
    except Exception as err:
        LOG.warning("Failed to log activity in database: %s", err)

    return DiseaseAnalysisResponse(
        status="success",
        disease_status=disease_status_str,
        confidence=f"{confidence_pct:.2f}%",
        top_matches=top_matches_formatted,
        ai_explanation=ai_explanation,
        crop=crop_pred,
        disease=disease_pred,
        confidence_status=confidence_status,
        analysis=ai_explanation,
        sources=sources
    )
