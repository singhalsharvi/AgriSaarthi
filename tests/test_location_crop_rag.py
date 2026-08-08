import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.rag.crop_retriever import CropRetriever
from backend.services.rag.gemini_service import GeminiService


def run_location_crop_test(test_id: int, location: str, season: str, user_query: str = ""):
    print(f"\n================================================================================")
    print(f" TEST {test_id}: Location = '{location}', Season = '{season}'")
    print(f"================================================================================")

    retriever = CropRetriever()
    result = retriever.retrieve(
        location=location,
        season=season,
        query=user_query,
    )

    resolved_loc = result.get("resolved_location", {})
    weather = result.get("weather_data", {})
    soil = result.get("soil_data", {})
    ml_features = result.get("supplied_ml_features", {})
    predictions = result.get("predictions", {})
    top_3 = predictions.get("top_3_predictions", [])
    docs = result.get("retrieved_docs", [])

    print("\n1. RESOLVED LOCATION & COORDINATES (Open-Meteo Geocoding):")
    print(f"   Name: {resolved_loc.get('name')}")
    print(f"   State/Admin Region: {resolved_loc.get('state')}")
    print(f"   Country: {resolved_loc.get('country')}")
    print(f"   Coordinates: Latitude {resolved_loc.get('latitude'):.4f}, Longitude {resolved_loc.get('longitude'):.4f}")

    print("\n2. RETRIEVED REAL-TIME WEATHER & CLIMATE (Open-Meteo Weather API):")
    print(f"   Current Temperature: {weather.get('temperature')} °C")
    print(f"   Relative Humidity: {weather.get('humidity')} %")
    print(f"   Current Precipitation: {weather.get('precipitation_current')} mm")
    print(f"   Annual Rainfall Estimate: {weather.get('annual_rainfall_estimate')} mm")

    print("\n3. SOIL KNOWLEDGE DATABASE RETRIEVAL:")
    print(f"   Dominant Soil Type: {soil.get('dominant_soil_name')} (Categorical Class: '{soil.get('soil_type')}')")
    print(f"   Benchmark pH: {soil.get('ph')}")
    print(f"   NPK Nutrients: N={soil.get('Nitrogen')}, P={soil.get('Phosphorus')}, K={soil.get('Potassium')}")
    print(f"   NPK Data Source: [{soil.get('npk_source')}]")

    print("\n4. EXACT ML INPUT FEATURES SUPPLIED TO TRAINED CROP MODEL:")
    print(f"   {json.dumps(ml_features, indent=2)}")

    print("\n5. TOP 3 ML CROP RECOMMENDATIONS:")
    for idx, p in enumerate(top_3, start=1):
        print(f"   {idx}. Crop: {p.get('crop')} | Confidence Score: {p.get('confidence_score')*100:.2f}%")

    print("\n6. RETRIEVED CROP RAG DOCUMENTS (From Crop ChromaDB):")
    print(f"   Total Retrieved Context Items: {len(docs)}")
    for idx, doc in enumerate(docs, start=1):
        print(f"   [{idx}] {doc.get('scheme_name')} (Source: {doc.get('source_file')})")

    print("\n7. GEMINI / LLM SYNTHESIZED FARMER EXPLANATION:")
    gemini = GeminiService()
    explanation = gemini.generate_response(
        user_query=user_query or f"Crop recommendation for {location} in {season} season",
        domain="crop_recommendation",
        retrieved_docs=docs,
        structured_metadata={"resolved_location": resolved_loc, "predictions": predictions},
    )
    print("\n" + explanation[:600] + "\n...")

    assert resolved_loc.get("latitude") is not None, "Latitude missing"
    assert len(top_3) == 3, "Expected top 3 crop predictions"
    assert len(docs) >= 3, "Expected retrieved crop knowledge docs"
    print(f"\nSUCCESS: Test {test_id} for '{location}' completed 100% successfully.")


def main():
    test_cases = [
        {"id": 1, "location": "Mandya, Karnataka", "season": "Kharif", "query": "What crops are best for my soil and how to manage water?"},
        {"id": 2, "location": "Ludhiana, Punjab", "season": "Rabi", "query": "Best winter crop recommendation and fertilizer schedule."},
        {"id": 3, "location": "Nagpur, Maharashtra", "season": "Kharif", "query": "Commercial crop recommendation for black cotton soil."},
    ]

    for tc in test_cases:
        run_location_crop_test(tc["id"], tc["location"], tc["season"], tc["query"])

    print("\n================================================================================")
    print(" ALL 3 REALISTIC LOCATION & CROP RAG TEST CASES COMPLETED 100% SUCCESSFULLY!")
    print("================================================================================")


if __name__ == "__main__":
    main()
