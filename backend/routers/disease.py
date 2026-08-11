import io
import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from PIL import Image, UnidentifiedImageError

from ai.disease_detection.prediction import predict_disease
from backend.services.rag.disease_retriever import DiseaseRetriever
from backend.services.rag.gemini_service import GeminiService
from backend.services.db_service import db_service

LOG = logging.getLogger("disease_router")

router = APIRouter(prefix="/disease", tags=["Disease Detection & Recommendation"])

disease_retriever = DiseaseRetriever()
gemini_service = GeminiService()

CONFIDENCE_THRESHOLD = 0.45  # 45% confidence threshold for CNN model
MIN_CONFIDENCE_MARGIN = 0.10
MAX_NORMALIZED_ENTROPY = 0.72
MAX_IMAGE_BYTES = 10 * 1024 * 1024
SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

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


def is_uncertain_prediction(prediction_result: Dict[str, Any]) -> bool:
    """Reject ambiguous softmax predictions, not only low top-class scores."""
    top_predictions = prediction_result.get("top_3_predictions", [])
    top_confidence = float(top_predictions[0].get("confidence", 0.0)) if top_predictions else 0.0
    return (
        not top_predictions
        or top_confidence < CONFIDENCE_THRESHOLD
        or float(prediction_result.get("confidence_margin", 0.0)) < MIN_CONFIDENCE_MARGIN
        or float(prediction_result.get("normalized_entropy", 1.0)) > MAX_NORMALIZED_ENTROPY
    )


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
            if file_obj and hasattr(file_obj, "read") and hasattr(file_obj, "filename"):
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
        if ext not in ["jpg", "jpeg", "png", "webp"] or image_file.content_type not in SUPPORTED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Supported: JPG, JPEG, PNG, WEBP.")

        try:
            contents = await image_file.read()
            if not contents or len(contents) > MAX_IMAGE_BYTES:
                raise ValueError("Image must be between 1 byte and 10 MB.")
            pil_image = Image.open(io.BytesIO(contents))
            pil_image.verify()  # Reject truncated/corrupt images before inference.
            pil_image = Image.open(io.BytesIO(contents))
            
            # Perform CNN classification
            pred_results = predict_disease(pil_image)
            top_predictions = pred_results["top_3_predictions"]
            
            if top_predictions:
                best_match = top_predictions[0]
                confidence_pct = best_match["confidence"] * 100.0
                is_low_confidence = is_uncertain_prediction(pred_results)
                
                if is_low_confidence:
                    crop_pred = crop_name or "Uncertain Crop"
                    disease_pred = "Uncertain Diagnosis (Low Model Confidence)"
                else:
                    crop_pred = best_match["crop"]
                    disease_pred = best_match["disease"]
        except (UnidentifiedImageError, ValueError) as err:
            raise HTTPException(status_code=400, detail=f"Invalid plant image: {err}")
        except Exception as err:
            LOG.error("CNN inference error: %s", err)
            raise HTTPException(status_code=500, detail=f"Model inference failed: {str(err)}")
    else:
        # Require image for analyze endpoint to avoid confusing text fallbacks when no image is uploaded
        return DiseaseAnalysisResponse(
            status="success",
            disease_status="No Image Uploaded",
            confidence="0.00%",
            top_matches=[{"name": "No Image Uploaded", "confidence": "0.0%"}],
            ai_explanation="Please upload a plant leaf image to perform disease detection.",
            crop="Unknown",
            disease="None",
            confidence_status="low",
            analysis="Please upload a plant leaf image to perform disease detection.",
            sources=[]
        )

    # 3. Query disease RAG vector database
    retrieval_query = f"{symptoms or ''} {user_query or ''}".strip()
    try:
        if is_low_confidence and not crop_name:
            retrieved_docs = []
        else:
            retrieval_result = disease_retriever.retrieve(
                query=retrieval_query,
                crop_name=crop_pred if not is_low_confidence else (crop_name or ""),
                disease_name=disease_pred if not is_low_confidence else "",
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
        ai_explanation = "Verified information is not available for this result."
    else:
        # Formulate query/metadata for Gemini based on confidence level
        if is_low_confidence:
            top3_str = "\n".join([f"- {item['crop']} - {item['disease']} (Confidence: {item['confidence']*100:.1f}%)" for item in top_predictions])
            user_prompt = (
                f"The image uploaded by the farmer could not be classified with high confidence.\n"
                f"Supported CNN Model Classes: Pepper bell, Potato, Tomato (15 disease classes total).\n"
                f"If the uploaded image is of an unlisted crop (such as Banana, Wheat, Rice, Cotton), state clearly that the current disease CNN was not trained on banana/unsupported crop classes, so banana disease detection is outside the model's supported classes.\n\n"
                f"Primary Model Guess: Crop: {top_predictions[0]['crop']}, Disease: {top_predictions[0]['disease']} (Confidence: {confidence_pct:.2f}%)\n"
                f"Top 3 Model Guesses:\n"
                f"{top3_str}\n\n"
                f"Retrieved context about the primary guess:\n"
                f"Please draft a clear, supportive advisory informing the farmer about the supported classes (Pepper bell, Potato, Tomato) and advising them to upload clear images of supported crop leaves for diagnosis."
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
                    "disease_status": f"{crop_pred} — {disease_pred}",
                    "crop": crop_pred,
                    "disease": disease_pred,
                    "confidence": f"{confidence_pct:.2f}%",
                    "confidence_pct": f"{confidence_pct:.2f}%",
                    "is_low_confidence": is_low_confidence
                }
            )
        except Exception as err:
            LOG.error("Gemini service error: %s. Using RAG fallback.", err)
            ai_explanation = gemini_service._generate_fallback_response(
                domain="disease_detection",
                user_query=user_prompt,
                retrieved_docs=retrieved_docs,
                structured_metadata={
                    "disease_status": f"{crop_pred} — {disease_pred}",
                    "confidence_pct": f"{confidence_pct:.2f}%",
                    "is_low_confidence": is_low_confidence
                }
            )

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
    if is_low_confidence:
        disease_status_str = f"{crop_pred} — Low Model Confidence ({confidence_pct:.1f}%)"
    else:
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


class DiseaseDetectResponse(BaseModel):
    crop: str
    disease: str
    confidence: float
    low_confidence: bool
    symptoms: List[str]
    prevention: List[str]
    treatment_or_management: List[str]
    explanation: str
    image_id: str


def get_markdown_filepath(crop: str, disease: str) -> Optional[str]:
    filename = f"{crop}_{disease}.md".replace(" ", "_")
    kb_dir = Path(__file__).resolve().parents[2] / "ai" / "disease_detection" / "knowledge_base"
    
    # Try exact match first
    filepath = kb_dir / filename
    if filepath.is_file():
        return str(filepath)
        
    # Try case-insensitive matches
    if kb_dir.is_dir():
        for name in os.listdir(kb_dir):
            if name.lower() == filename.lower():
                return str(kb_dir / name)
    return None


@router.post("/detect", response_model=DiseaseDetectResponse)
async def detect_disease(
    image: UploadFile = File(...),
    farmer_id: str = Form("ramesh.farmer@agrisaarthi.in")
) -> DiseaseDetectResponse:
    # Check image format
    filename = image.filename or ""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in ["jpg", "jpeg", "png", "webp"] or image.content_type not in SUPPORTED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported: JPG, JPEG, PNG, WEBP.")

    try:
        contents = await image.read()
        if not contents or len(contents) > MAX_IMAGE_BYTES:
            raise ValueError("Image must be between 1 byte and 10 MB.")
        pil_image = Image.open(io.BytesIO(contents))
        pil_image.verify()
        pil_image = Image.open(io.BytesIO(contents))
        
        # 1. Run CNN classification
        pred_results = predict_disease(pil_image)
        top_predictions = pred_results["top_3_predictions"]
        
        if not top_predictions:
            raise HTTPException(status_code=500, detail="No predictions produced by CNN model.")
            
        best_match = top_predictions[0]
        confidence = float(best_match["confidence"])
        confidence_pct = confidence * 100.0
        is_low_confidence = is_uncertain_prediction(pred_results)
        
        if is_low_confidence:
            crop_pred = "Uncertain Crop"
            disease_pred = "Uncertain Diagnosis (Low Model Confidence)"
        else:
            crop_pred = best_match["crop"]
            disease_pred = best_match["disease"]
            
        # 2. Save image and log prediction in the isolated sqlite database
        from ai.disease_detection.storage import save_image_and_log
        image_id, ref_path = save_image_and_log(pil_image, crop_pred, disease_pred, confidence)
        
        # 3. Query disease RAG vector database
        try:
            if is_low_confidence:
                retrieved_docs = []
            else:
                retrieval_result = disease_retriever.retrieve(
                    query="",
                    crop_name=crop_pred,
                    disease_name=disease_pred,
                    top_k=4
                )
                retrieved_docs = retrieval_result.get("retrieved_docs", [])
        except Exception as err:
            LOG.error("RAG retrieval error in detect: %s", err)
            retrieved_docs = []
            
        # 4. Invoke grounded Gemini response or fallback
        if not retrieved_docs:
            ai_explanation = "Verified information is not available for this result."
        else:
            if is_low_confidence:
                top3_str = "\n".join([f"- {item['crop']} - {item['disease']} (Confidence: {item['confidence']*100:.1f}%)" for item in top_predictions])
                user_prompt = (
                    f"The image uploaded by the farmer could not be classified with high confidence.\n"
                    f"Supported CNN Model Classes: Pepper bell, Potato, Tomato (15 disease classes total).\n"
                    f"Primary Model Guess: Crop: {top_predictions[0]['crop']}, Disease: {top_predictions[0]['disease']} (Confidence: {confidence_pct:.2f}%)\n"
                    f"Top 3 Model Guesses:\n"
                    f"{top3_str}\n\n"
                    f"Retrieved context about the primary guess:\n"
                    f"Please draft a clear, supportive advisory informing the farmer about the supported classes (Pepper bell, Potato, Tomato) and advising them to upload clear images of supported crop leaves for diagnosis."
                )
            else:
                user_prompt = (
                    f"Crop: {crop_pred}\n"
                    f"Detected Disease: {disease_pred}\n"
                    f"Model Confidence: {confidence_pct:.2f}%\n"
                    f"What treatment or organic remedies are recommended?"
                )

            try:
                ai_explanation = gemini_service.generate_response(
                    user_query=user_prompt,
                    domain="disease_detection",
                    retrieved_docs=retrieved_docs,
                    structured_metadata={
                        "disease_status": f"{crop_pred} — {disease_pred}",
                        "crop": crop_pred,
                        "disease": disease_pred,
                        "confidence": f"{confidence_pct:.2f}%",
                        "confidence_pct": f"{confidence_pct:.2f}%",
                        "is_low_confidence": is_low_confidence
                    }
                )
            except Exception as err:
                LOG.error("Gemini service error in detect: %s. Using RAG fallback.", err)
                ai_explanation = gemini_service._generate_fallback_response(
                    domain="disease_detection",
                    user_query=user_prompt,
                    retrieved_docs=retrieved_docs,
                    structured_metadata={
                        "disease_status": f"{crop_pred} — {disease_pred}",
                        "confidence_pct": f"{confidence_pct:.2f}%",
                        "is_low_confidence": is_low_confidence
                    }
                )

        # 5. Extract structured lists using parser
        from ai.disease_detection.parser import parse_disease_markdown
        kb_path = get_markdown_filepath(best_match["crop"], best_match["disease"])
        parsed_data = parse_disease_markdown(kb_path) if kb_path else {}
        
        symptoms_list = parsed_data.get("symptoms", [])
        prevention_list = parsed_data.get("prevention", [])
        treatment_list = parsed_data.get("treatment_or_management", [])
        
        # 6. Log activity in primary database
        try:
            db_service.log_activity(
                farmer_id=farmer_id,
                activity_type="disease_analysis",
                details={
                    "crop": crop_pred,
                    "disease": disease_pred,
                    "confidence": f"{confidence_pct:.2f}%",
                    "confidence_status": "low" if is_low_confidence else "high",
                    "has_image": True
                }
            )
        except Exception as err:
            LOG.warning("Failed to log activity in primary DB in detect: %s", err)

        return DiseaseDetectResponse(
            crop=crop_pred,
            disease=disease_pred,
            confidence=confidence,
            low_confidence=is_low_confidence,
            symptoms=symptoms_list,
            prevention=prevention_list,
            treatment_or_management=treatment_list,
            explanation=ai_explanation,
            image_id=image_id
        )
        
    except (UnidentifiedImageError, ValueError) as err:
        raise HTTPException(status_code=400, detail=f"Invalid plant image: {err}")
    except Exception as err:
        LOG.error("CNN inference error: %s", err)
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(err)}")


@router.get("/images/{filename}")
async def serve_disease_image(filename: str):
    from ai.disease_detection.storage import get_image_file_path
    physical_path = get_image_file_path(filename)
    if not physical_path or not os.path.exists(physical_path):
        raise HTTPException(status_code=404, detail="Image file not found.")
    return FileResponse(physical_path, media_type="image/jpeg")
