from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.rag.crop_retriever import CropRetriever
from backend.services.rag.gemini_service import GeminiService

router = APIRouter(prefix="/crop", tags=["Crop Recommendation"])

crop_retriever = CropRetriever()
gemini_service = GeminiService()


class CropRecommendationRequest(BaseModel):
    location: Optional[str] = Field(None, example="Mandya, Karnataka", description="City, District, or State in India")
    season: Optional[str] = Field(None, example="Kharif", description="Cropping season (Kharif, Rabi, Summer)")
    Nitrogen: Optional[float] = Field(None, example=90.0, description="Optional soil Nitrogen content")
    Phosphorus: Optional[float] = Field(None, example=42.0, description="Optional soil Phosphorus content")
    Potassium: Optional[float] = Field(None, example=43.0, description="Optional soil Potassium content")
    Temperature: Optional[float] = Field(None, description="Optional Temperature in °C")
    Humidity: Optional[float] = Field(None, description="Optional Humidity in %")
    pH_Value: Optional[float] = Field(None, description="Optional Soil pH level")
    Rainfall: Optional[float] = Field(None, description="Optional Rainfall in mm")
    Soil_Type: Optional[str] = Field(None, example="Clay", description="Optional Soil type override")
    user_query: Optional[str] = Field(None, example="What crops are best for my region and how should I cultivate them?")


class RecommendedCropItem(BaseModel):
    crop: str
    reason: str
    confidence: str
    source: str


class CropRecommendationResponse(BaseModel):
    location: str
    season: str
    soil: str
    weather: Dict[str, Any]
    ml_confidence: str
    recommendation_source: str
    recommended_crops: List[RecommendedCropItem]
    warning: Optional[str] = None
    explanation: str


@router.post("/recommend", response_model=CropRecommendationResponse)
def recommend_crop(request: CropRecommendationRequest) -> CropRecommendationResponse:
    """Predict crops with 50% ML confidence threshold and location/soil/climate RAG fallback when ML confidence is low."""
    try:
        retrieval_result = crop_retriever.retrieve(
            query=request.user_query or "",
            location=request.location,
            season=request.season,
            Nitrogen=request.Nitrogen,
            Phosphorus=request.Phosphorus,
            Potassium=request.Potassium,
            Temperature=request.Temperature,
            Humidity=request.Humidity,
            pH_Value=request.pH_Value,
            Rainfall=request.Rainfall,
            Soil_Type=request.Soil_Type,
        )

        resolved_loc = retrieval_result.get("resolved_location", {})
        weather_data = retrieval_result.get("weather_data", {})
        soil_data = retrieval_result.get("soil_data", {})
        ml_conf_val = retrieval_result.get("ml_confidence", 0.0)
        rec_source = retrieval_result.get("recommendation_source", "ML")
        rec_crops = retrieval_result.get("recommended_crops", [])
        warning_msg = retrieval_result.get("warning")
        retrieved_docs = retrieval_result.get("retrieved_docs", [])

        location_str = f"{resolved_loc.get('name', '')}, {resolved_loc.get('state', '')}"
        soil_str = f"{soil_data.get('dominant_soil_name', '')} ({soil_data.get('soil_type', '')}), pH: {soil_data.get('ph', '')}"

        meta_context = {
            "resolved_location": resolved_loc,
            "weather_data": weather_data,
            "soil_data": soil_data,
            "recommendation_source": rec_source,
            "ml_confidence": f"{ml_conf_val*100:.2f}%",
            "warning": warning_msg,
        }

        ai_explanation = gemini_service.generate_response(
            user_query=request.user_query or f"Crop recommendation advice for {location_str} in {request.season or 'Kharif'} season",
            domain="crop_recommendation",
            retrieved_docs=retrieved_docs,
            structured_metadata=meta_context,
        )

        return CropRecommendationResponse(
            location=location_str,
            season=request.season or "Kharif",
            soil=soil_str,
            weather={
                "temperature": weather_data.get("temperature"),
                "humidity": weather_data.get("humidity"),
                "precipitation": weather_data.get("precipitation_current"),
                "annual_rainfall_estimate": weather_data.get("annual_rainfall_estimate"),
            },
            ml_confidence=f"{ml_conf_val*100:.2f}%",
            recommendation_source=rec_source,
            recommended_crops=[
                RecommendedCropItem(
                    crop=item["crop"],
                    reason=item["reason"],
                    confidence=item["confidence"],
                    source=item["source"],
                )
                for item in rec_crops
            ],
            warning=warning_msg,
            explanation=ai_explanation,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Crop recommendation error: {str(exc)}")
