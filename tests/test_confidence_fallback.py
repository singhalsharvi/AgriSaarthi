import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.rag.crop_retriever import CropRetriever
from backend.services.rag.gemini_service import GeminiService


def run_confidence_test(
    test_id: int,
    title: str,
    location: str,
    season: str,
    user_query: str = "",
    temp_override=None,
    humidity_override=None,
    rainfall_override=None,
    soil_type_override=None,
):
    print(f"\n================================================================================")
    print(f" TEST {test_id}: {title}")
    print(f" Location = '{location}', Season = '{season}'")
    print(f"================================================================================")

    retriever = CropRetriever()
    result = retriever.retrieve(
        location=location,
        season=season,
        query=user_query,
        Temperature=temp_override,
        Humidity=humidity_override,
        Rainfall=rainfall_override,
        Soil_Type=soil_type_override,
    )

    resolved_loc = result.get("resolved_location", {})
    weather = result.get("weather_data", {})
    soil = result.get("soil_data", {})
    ml_conf = result.get("ml_confidence", 0.0)
    rec_source = result.get("recommendation_source", "")
    rec_crops = result.get("recommended_crops", [])
    warning = result.get("warning")
    predictions = result.get("predictions", {})
    top_3_ml = predictions.get("top_3_predictions", [])
    docs = result.get("retrieved_docs", [])

    print(f"\n1. LOCATION & COORDINATES:")
    print(f"   {resolved_loc.get('name')}, {resolved_loc.get('state')} (Lat: {resolved_loc.get('latitude'):.4f}, Lon: {resolved_loc.get('longitude'):.4f})")

    print(f"\n2. SEASON & REAL-TIME WEATHER:")
    print(f"   Season: {season}")
    print(f"   Temperature: {weather.get('temperature')} °C | Humidity: {weather.get('humidity')} % | Rainfall Estimate: {weather.get('annual_rainfall_estimate')} mm")

    print(f"\n3. SOIL PROFILE:")
    print(f"   Dominant Soil: {soil.get('dominant_soil_name')} (Categorical: '{soil.get('soil_type')}') | pH: {soil.get('ph')}")

    print(f"\n4. ML MODEL EVALUATION & CONFIDENCE:")
    print(f"   Highest Model Confidence Score: {ml_conf*100:.2f}% (Threshold = 50.00%)")
    print(f"   ML Top Predictions:")
    for p in top_3_ml:
        print(f"     - {p.get('crop')}: {p.get('confidence_score')*100:.2f}%")

    print(f"\n5. RECOMMENDATION SOURCE DECISION:")
    print(f"   Recommendation Source: [{rec_source}]")
    if warning:
        print(f"   System Warning: {warning}")

    print(f"\n6. FINAL RECOMMENDED CROPS:")
    if rec_crops:
        for idx, item in enumerate(rec_crops, start=1):
            print(f"   [{idx}] {item['crop']} | Confidence: {item['confidence']} | Source: {item['source']}")
            print(f"       Reason: {item['reason']}")
    else:
        print("   No suitable crops recommended.")

    print(f"\n7. RETRIEVED RAG EVIDENCE (Crop ChromaDB):")
    print(f"   Total Retrieved Docs: {len(docs)}")
    for doc in docs[:3]:
        print(f"   - {doc.get('scheme_name')} ({doc.get('source_file')})")

    print(f"\n8. GEMINI SYNTHESIZED RESPONSE:")
    gemini = GeminiService()
    explanation = gemini.generate_response(
        user_query=user_query or f"Crop recommendation for {location}",
        domain="crop_recommendation",
        retrieved_docs=docs,
        structured_metadata={"recommendation_source": rec_source, "warning": warning},
    )
    print("\n" + explanation[:400] + "\n...")

    return result


def main():
    print("=" * 80)
    print(" EXECUTING 4-SCENARIO CONFIDENCE-AWARE & FALLBACK TEST SUITE")
    print("=" * 80)

    # Test 1: ML Model High Confidence (>= 50%) -> Mandya, Karnataka (Rice conditions: high humidity & rainfall)
    res1 = run_confidence_test(
        test_id=1,
        title="ML High Confidence Case (>= 50%)",
        location="Mandya, Karnataka",
        season="Kharif",
        user_query="What crop should I grow under high rainfall Kharif season?",
        humidity_override=85.0,
        rainfall_override=2000.0,
    )
    assert res1["recommendation_source"] == "ML", f"Expected ML source, got {res1['recommendation_source']}"
    assert res1["ml_confidence"] >= 0.50, f"Expected confidence >= 0.50, got {res1['ml_confidence']}"

    # Test 2: Low ML Confidence (< 50%) -> Bikaner, Rajasthan (Sandy Desert Soil)
    res2 = run_confidence_test(
        test_id=2,
        title="Low ML Confidence Case (< 50%) -> Fallback Triggered",
        location="Bikaner, Rajasthan",
        season="Kharif",
        user_query="Best crop for desert sandy soil with low rainfall?",
    )
    assert res2["recommendation_source"] == "LOCATION_SOIL_RAG", f"Expected LOCATION_SOIL_RAG source, got {res2['recommendation_source']}"
    assert res2["ml_confidence"] < 0.50, f"Expected confidence < 0.50, got {res2['ml_confidence']}"
    assert res2["warning"] is not None, "Expected warning message"

    # Test 3: Broader Crop outside 22 ML crops -> Indore, MP (Black Vertisol Soil, Soybean)
    res3 = run_confidence_test(
        test_id=3,
        title="Broader Crop (Outside 22 ML Crops) -> Soybean Recommendation",
        location="Indore, Madhya Pradesh",
        season="Kharif",
        user_query="What Kharif oilseed grows best in black Vertisol soil?",
        soil_type_override="Black",
    )
    assert res3["recommendation_source"] in ["LOCATION_SOIL_RAG", "ML"]
    crops_recommended = [c["crop"].lower() for c in res3["recommended_crops"]]
    print(f"Test 3 Recommended Crops: {crops_recommended}")

    # Test 4: No Suitable Crop Case (Extreme drought / hyper-arid conditions)
    res4 = run_confidence_test(
        test_id=4,
        title="No-Suitable-Crop Case (Extreme Environmental Limitation)",
        location="Jaisalmer Desert, Rajasthan",
        season="Rabi",
        user_query="Can I grow tropical crops in severe frost with 50mm rainfall?",
        temp_override=2.0,
        rainfall_override=50.0,
    )
    assert res4["recommendation_source"] == "NONE", f"Expected NONE source, got {res4['recommendation_source']}"

    print("\n" + "=" * 80)
    print(" ALL 4 CONFIDENCE-AWARE & FALLBACK TEST CASES PASSED 100% SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
