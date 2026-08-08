from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.rag.disease_retriever import DiseaseRetriever
from backend.services.rag.gemini_service import GeminiService

router = APIRouter(prefix="/disease", tags=["Disease Detection & Recommendation"])

disease_retriever = DiseaseRetriever()
gemini_service = GeminiService()


class DiseaseAnalysisRequest(BaseModel):
    crop_name: Optional[str] = Field(None, example="Tomato")
    symptoms: Optional[str] = Field(None, example="Yellow spots on leaves with brown margins")
    user_query: Optional[str] = Field(None, example="How to treat these yellow leaf spots?")


class DiseaseAnalysisResponse(BaseModel):
    status: str
    disease_status: str
    ai_explanation: str


@router.post("/analyze", response_model=DiseaseAnalysisResponse)
def analyze_disease(request: DiseaseAnalysisRequest) -> DiseaseAnalysisResponse:
    """Analyze crop disease symptoms and generate advisory via Gemini service."""
    try:
        retrieval_result = disease_retriever.retrieve(
            query=request.symptoms or request.user_query or "",
            crop_name=request.crop_name,
        )

        retrieved_docs = retrieval_result.get("retrieved_docs", [])

        ai_explanation = gemini_service.generate_response(
            user_query=request.user_query or f"Symptoms on {request.crop_name or 'crop'}: {request.symptoms}",
            domain="disease_detection",
            retrieved_docs=retrieved_docs,
            structured_metadata={"crop_name": request.crop_name, "symptoms": request.symptoms},
        )

        return DiseaseAnalysisResponse(
            status="success",
            disease_status=retrieval_result.get("disease_status", "placeholder"),
            ai_explanation=ai_explanation,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Disease analysis error: {str(exc)}")
