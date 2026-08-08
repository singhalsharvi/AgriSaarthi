from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.rag.gemini_service import GeminiService
from backend.services.rag.government_retriever import GovernmentSchemeRetriever

router = APIRouter(prefix="/government-schemes", tags=["Government Schemes"])

retriever = GovernmentSchemeRetriever()
gemini_service = GeminiService()


class GovernmentSchemeRequest(BaseModel):
    state: Optional[str] = Field(None, example="Karnataka")
    crop: Optional[str] = Field(None, example="rice")
    farmer_category: Optional[str] = Field(None, example="Small and marginal farmer families")
    annual_income: Optional[float] = Field(None, example=50000.0)
    landholding: Optional[float] = Field(None, example=1.5)
    age: Optional[float] = Field(None, example=40.0)
    gender: Optional[str] = Field(None, example="male")
    user_query: Optional[str] = Field(None, example="I need financial support for my rice crop.")
    top_k: int = Field(5, ge=1, le=10)


class SchemeDetail(BaseModel):
    scheme_name: str
    official_website: Optional[str] = None
    source_file: Optional[str] = None
    distance: float
    snippet: str


class GovernmentSchemeResponse(BaseModel):
    status: str
    eligible_schemes: List[str]
    recommended_schemes: List[SchemeDetail]
    ai_explanation: str


@router.post("/recommend", response_model=GovernmentSchemeResponse)
def recommend_government_schemes(request: GovernmentSchemeRequest) -> GovernmentSchemeResponse:
    """Recommend government schemes based on farmer eligibility criteria and natural language query.

    Executes eligibility rule filtering, ChromaDB semantic vector search, and Gemini LLM synthesis.
    """
    try:
        # Step 1: Run RAG retrieval pipeline (Eligibility Filter + ChromaDB Vector Search)
        retrieval_result = retriever.retrieve(
            query=request.user_query or "",
            top_k=request.top_k,
            state=request.state,
            crop=request.crop,
            farmer_category=request.farmer_category,
            annual_income=request.annual_income,
            landholding=request.landholding,
            age=request.age,
            gender=request.gender,
        )

        eligible_schemes = retrieval_result.get("eligible_schemes", [])
        retrieved_docs = retrieval_result.get("retrieved_docs", [])

        # Step 2: Synthesize evidence-backed response using common Gemini layer
        profile_meta = {
            "state": request.state,
            "crop": request.crop,
            "farmer_category": request.farmer_category,
            "annual_income": request.annual_income,
            "landholding": request.landholding,
            "age": request.age,
            "gender": request.gender,
            "eligible_schemes_count": len(eligible_schemes),
        }

        ai_explanation = gemini_service.generate_response(
            user_query=request.user_query or "",
            domain="government_schemes",
            retrieved_docs=retrieved_docs,
            structured_metadata=profile_meta,
        )

        # Format scheme details
        scheme_details = []
        for doc in retrieved_docs:
            scheme_details.append(
                SchemeDetail(
                    scheme_name=doc.get("scheme_name") or "Government Scheme",
                    official_website=doc.get("official_website") or None,
                    source_file=doc.get("source_file") or None,
                    distance=round(doc.get("distance", 0.0), 4),
                    snippet=doc.get("document_text", "")[:250].strip() + "...",
                )
            )

        return GovernmentSchemeResponse(
            status="success",
            eligible_schemes=eligible_schemes,
            recommended_schemes=scheme_details,
            ai_explanation=ai_explanation,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Government scheme recommendation error: {str(exc)}")
