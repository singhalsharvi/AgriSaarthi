import logging
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

LOG = logging.getLogger("crop_retriever")

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai.crop_recommendation.prediction import predict_crop
from ai.crop_recommendation.scripts.retrieve_crop_knowledge import retrieve_crop_knowledge
from backend.services.fallback_matcher import find_fallback_crops
from backend.services.location_service import resolve_location
from backend.services.rag.base_retriever import BaseRetriever
from backend.services.soil_service import resolve_soil_information
from backend.services.weather_service import get_weather_and_climate


class CropRetriever(BaseRetriever):
    """Confidence-Aware End-to-End Crop Recommendation RAG Pipeline:
    1. Resolves location coordinates (Open-Meteo Geocoding).
    2. Fetches real-time weather & climate (Open-Meteo Weather API).
    3. Resolves soil profile & ICAR/SHC N-P-K nutrient benchmarks.
    4. Runs ML prediction model and evaluates highest prediction score against 50.0% threshold.
    5. IF ML confidence >= 50%: Uses ML predictions as candidate crops (recommendation_source = "ML").
    6. IF ML confidence < 50%: Triggers location + soil + climate fallback engine (recommendation_source = "LOCATION_SOIL_RAG").
    7. IF no suitable crops match conditions: Gracefully flags recommendation_source = "NONE".
    8. Queries Crop ChromaDB vector store for candidate crops and synthesizes evidence-backed response.
    """

    CONFIDENCE_THRESHOLD = 0.50  # 50% model confidence threshold

    def retrieve(
        self,
        query: str = "",
        location: Optional[str] = None,
        season: Optional[str] = None,
        Nitrogen: Optional[float] = None,
        Phosphorus: Optional[float] = None,
        Potassium: Optional[float] = None,
        Temperature: Optional[float] = None,
        Humidity: Optional[float] = None,
        pH_Value: Optional[float] = None,
        Rainfall: Optional[float] = None,
        Soil_Type: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Execute confidence-aware crop recommendation pipeline with location/soil fallback."""
        # Step 1: Location Resolution
        location_input = location if location and location.strip() else "Mandya, Karnataka"
        resolved_loc = resolve_location(location_input)
        lat = resolved_loc["latitude"]
        lon = resolved_loc["longitude"]
        state = resolved_loc["state"]
        active_season = season or "Kharif"

        # Step 2: Real-time Weather & Climate Retrieval
        weather_info = get_weather_and_climate(lat, lon)

        final_temp = float(Temperature) if Temperature is not None else float(weather_info["temperature"])
        final_humidity = float(Humidity) if Humidity is not None else float(weather_info["humidity"])
        final_rainfall = float(Rainfall) if Rainfall is not None else float(weather_info["annual_rainfall_estimate"])

        # Step 3: Soil Knowledge & NPK Resolution
        soil_info = resolve_soil_information(
            state=state,
            soil_type_override=Soil_Type,
            N=Nitrogen,
            P=Phosphorus,
            K=Potassium,
        )

        final_ph = float(pH_Value) if pH_Value is not None else float(soil_info["ph"])
        final_soil_type = soil_info["soil_type"]
        final_N = soil_info["Nitrogen"]
        final_P = soil_info["Phosphorus"]
        final_K = soil_info["Potassium"]

        # Step 4: Construct ML input features & run ML prediction model
        supplied_ml_features = {
            "Nitrogen": final_N,
            "Phosphorus": final_P,
            "Potassium": final_K,
            "Temperature": final_temp,
            "Humidity": final_humidity,
            "pH_Value": final_ph,
            "Rainfall": final_rainfall,
            "Soil_Type": final_soil_type,
        }

        predictions = predict_crop(
            Nitrogen=final_N,
            Phosphorus=final_P,
            Potassium=final_K,
            Temperature=final_temp,
            Humidity=final_humidity,
            pH_Value=final_ph,
            Rainfall=final_rainfall,
            Soil_Type=final_soil_type,
        )

        top_3_ml = predictions.get("top_3_predictions", [])
        top_ml_confidence = float(top_3_ml[0].get("confidence_score", 0.0)) if top_3_ml else 0.0

        recommendation_source = "ML"
        recommended_crops_structured = []
        target_crop_names = []
        warning_msg = None

        # Step 5: Evaluate ML Confidence against 50% threshold
        if top_ml_confidence >= self.CONFIDENCE_THRESHOLD:
            recommendation_source = "ML"
            for p in top_3_ml:
                crop_name = p.get("crop", "")
                conf_val = float(p.get("confidence_score", 0.0))
                recommended_crops_structured.append(
                    {
                        "crop": crop_name,
                        "reason": f"Trained ML model high-confidence prediction ({conf_val*100:.1f}% score)",
                        "confidence": f"{conf_val*100:.1f}%",
                        "source": "Trained Crop ML Model (22 Crops Dataset)",
                    }
                )
                target_crop_names.append(crop_name)
        else:
            # ML confidence < 50%: Switch to Location + Soil Fallback Matcher
            LOG.info("ML top prediction score (%.2f%%) is below 50%% threshold. Activating Location/Soil Fallback Matcher.", top_ml_confidence * 100)
            fallback_res = find_fallback_crops(
                state=state,
                soil_type=final_soil_type,
                ph=final_ph,
                temp=final_temp,
                rainfall=final_rainfall,
                season=active_season,
            )

            if fallback_res["status"] == "LOCATION_SOIL_RAG":
                recommendation_source = "LOCATION_SOIL_RAG"
                warning_msg = (
                    f"The ML model has low confidence ({top_ml_confidence*100:.1f}%) for its 22 trained crops under these environmental conditions. "
                    f"Alternative recommendations are provided from the regional location, soil, and climate knowledge base."
                )
                for fb in fallback_res["recommended_crops"]:
                    recommended_crops_structured.append(
                        {
                            "crop": fb["crop"],
                            "reason": fb["reason"],
                            "confidence": fb["confidence"],
                            "source": fb["source"],
                        }
                    )
                    target_crop_names.append(fb["crop"].split("(")[0].strip())
            else:
                # No suitable crop case
                recommendation_source = "NONE"
                limiting_str = "; ".join(fallback_res.get("limiting_factors", ["Environmental constraints"]))
                warning_msg = f"No suitable crop could be confidently recommended for the provided conditions. Limiting factors: {limiting_str}"

        # Step 6: Query Crop ChromaDB for candidate crops (works for both ML and Fallback crops!)
        search_query = query.strip() if query and query.strip() else f"Agronomic guidelines for {', '.join(target_crop_names or ['crops'])}"
        retrieved_crop_docs = []
        if target_crop_names:
            retrieved_crop_docs = retrieve_crop_knowledge(
                crop_names=target_crop_names,
                query=search_query,
                top_k=4,
            )

        # Build context document
        env_summary = (
            f"FARMER ENVIRONMENT & SYSTEM EVALUATION:\n"
            f"- Location: {resolved_loc['name']}, {state} (Lat: {lat:.4f}, Lon: {lon:.4f})\n"
            f"- Season: {active_season}\n"
            f"- Open-Meteo Weather: Temp: {final_temp}°C, Humidity: {final_humidity}%, Rainfall Estimate: {final_rainfall} mm\n"
            f"- Soil Profile: {soil_info['dominant_soil_name']} ({final_soil_type}), pH: {final_ph}\n"
            f"- Highest ML Model Score: {top_ml_confidence*100:.2f}%\n"
            f"- Recommendation Source Selected: {recommendation_source}\n"
            f"- Warning Message: {warning_msg or 'None'}\n"
        )

        input_doc = {
            "scheme_name": "Farmer Environment & System Evaluation Summary",
            "source_file": "backend/services/rag/crop_retriever.py",
            "official_website": "",
            "document_text": env_summary,
            "distance": 0.0,
        }

        all_context_docs = [input_doc] + retrieved_crop_docs

        return {
            "resolved_location": resolved_loc,
            "weather_data": weather_info,
            "soil_data": soil_info,
            "supplied_ml_features": supplied_ml_features,
            "ml_confidence": round(top_ml_confidence, 4),
            "recommendation_source": recommendation_source,
            "recommended_crops": recommended_crops_structured,
            "warning": warning_msg,
            "predictions": predictions,
            "retrieved_docs": all_context_docs,
        }
