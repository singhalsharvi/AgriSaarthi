import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai.government_schemes.scripts.filter_schemes import get_eligible_schemes
from ai.government_schemes.scripts.retrieve_schemes import retrieve_schemes
from ai.crop_recommendation.scripts.retrieve_crop_knowledge import retrieve_crop_knowledge
from backend.services.rag.crop_retriever import CropRetriever
from backend.services.rag.disease_retriever import DiseaseRetriever
from backend.services.rag.gemini_service import GeminiService
from backend.services.rag.government_retriever import GovernmentSchemeRetriever


def test_1_verify_government_chromadb_count():
    print("\n--- Test 1: Verifying Existing Government Schemes ChromaDB Collection Count ---")
    import chromadb

    persist_dir = PROJECT_ROOT / "ai" / "government_schemes" / "chroma_db"
    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_collection(name="government_schemes")
    count = collection.count()
    print(f"ChromaDB Collection 'government_schemes' contains {count} items.")
    assert count == 20, f"Expected 20 documents in government_schemes ChromaDB, found {count}"
    print("SUCCESS: Existing Government Schemes ChromaDB collection count is exactly 20.")


def test_2_verify_crop_chromadb_count():
    print("\n--- Test 2: Verifying Crop Knowledge ChromaDB Collection Count ---")
    import chromadb

    persist_dir = PROJECT_ROOT / "ai" / "crop_recommendation" / "chroma_db"
    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_collection(name="crop_knowledge")
    count = collection.count()
    print(f"ChromaDB Collection 'crop_knowledge' contains {count} items.")
    assert count >= 22, f"Expected at least 22 crop documents in crop_knowledge ChromaDB, found {count}"
    print("SUCCESS: Crop Knowledge ChromaDB collection count is valid.")


def test_3_government_schemes_rag():
    print("\n--- Test 3: Government Schemes RAG Pipeline ---")
    retriever = GovernmentSchemeRetriever()
    result = retriever.retrieve(
        query="I need credit facilities and low interest loan for small farmers in Karnataka",
        state="Karnataka",
        crop="rice",
        farmer_category="Small and marginal farmer families",
        annual_income=60000,
        landholding=1.5,
        age=42,
        gender="male",
        top_k=3,
    )

    eligible = result.get("eligible_schemes", [])
    docs = result.get("retrieved_docs", [])

    print(f"Eligible Scheme Count: {len(eligible)}")
    print(f"Retrieved Context Documents Count: {len(docs)}")
    assert len(docs) > 0, "Retrieved government scheme docs should not be empty"
    print("SUCCESS: Government Scheme RAG Pipeline executed cleanly.")


def test_4_crop_knowledge_vector_retrieval():
    print("\n--- Test 4: Crop Knowledge Vector Retrieval ---")
    crops_to_test = ["rice", "jute", "maize"]
    retrieved = retrieve_crop_knowledge(crop_names=crops_to_test, query="water and fertilizer requirements")
    print(f"Retrieved {len(retrieved)} crop knowledge documents for {crops_to_test}:")
    for r in retrieved:
        print(f"  - Crop: {r['crop_name']} | Title: {r['scheme_name']}")
    assert len(retrieved) >= 3, "Expected at least 3 crop knowledge docs"
    print("SUCCESS: Crop Knowledge Vector Retrieval working correctly.")


def test_5_crop_rag_pipeline():
    print("\n--- Test 5: Crop Recommendation ML + Crop RAG + Gemini Pipeline ---")
    crop_retriever = CropRetriever()
    res = crop_retriever.retrieve(
        Nitrogen=90,
        Phosphorus=42,
        Potassium=43,
        Temperature=20.87,
        Humidity=82.0,
        pH_Value=6.5,
        Rainfall=202.93,
        Soil_Type="Clay",
        query="What fertilizers and water management do I need for my crop?",
    )

    preds = res.get("predictions", {}).get("top_3_predictions", [])
    docs = res.get("retrieved_docs", [])
    print("ML Top 3 Recommendations:")
    for p in preds:
        print(f"  - {p['crop']}: {p['confidence_score']*100:.2f}%")
    
    print(f"Retrieved {len(docs)} context items (Input Summary + Crop Knowledge Docs).")
    assert len(preds) == 3, "Expected 3 crop ML recommendations"
    assert len(docs) >= 3, "Expected input summary + crop knowledge docs"

    gemini = GeminiService()
    synthesis = gemini.generate_response(
        user_query="What crop should I plant and how to cultivate it?",
        domain="crop_recommendation",
        retrieved_docs=docs,
        structured_metadata={"predictions": res["predictions"]},
    )
    print("\nSynthesized Explanation Output Preview:\n" + synthesis[:450] + "\n...")
    assert len(synthesis) > 50, "Synthesized output is too short"
    print("SUCCESS: Crop ML + Crop RAG + Gemini pipeline executed cleanly.")


def test_6_fastapi_backend_endpoints():
    print("\n--- Test 6: FastAPI Backend Integration Endpoints ---")
    from fastapi.testclient import TestClient
    from backend.main import app

    client = TestClient(app)

    # Test /health
    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json() == {"status": "healthy"}
    print("  [GET /health] Passed.")

    # Test POST /government-schemes/recommend
    gov_payload = {
        "state": "Karnataka",
        "crop": "rice",
        "farmer_category": "Small and marginal farmer families",
        "annual_income": 50000,
        "landholding": 1.5,
        "age": 40,
        "gender": "male",
        "user_query": "I need financial support for growing rice.",
        "top_k": 3,
    }
    res_gov = client.post("/government-schemes/recommend", json=gov_payload)
    assert res_gov.status_code == 200, f"Error: {res_gov.text}"
    gov_json = res_gov.json()
    assert gov_json["status"] == "success"
    assert len(gov_json["recommended_schemes"]) > 0
    assert "ai_explanation" in gov_json
    print(f"  [POST /government-schemes/recommend] Passed. (Got {len(gov_json['recommended_schemes'])} schemes)")

    # Test POST /crop/recommend
    crop_payload = {
        "Nitrogen": 90,
        "Phosphorus": 42,
        "Potassium": 43,
        "Temperature": 20.87,
        "Humidity": 82.0,
        "pH_Value": 6.5,
        "Rainfall": 202.93,
        "Soil_Type": "Clay",
        "user_query": "What crop should I plant and what fertilizer to use?",
    }
    res_crop = client.post("/crop/recommend", json=crop_payload)
    assert res_crop.status_code == 200, f"Error: {res_crop.text}"
    crop_json = res_crop.json()
    assert crop_json["status"] == "success"
    assert len(crop_json["top_3_predictions"]) == 3
    assert "ai_explanation" in crop_json
    print(f"  [POST /crop/recommend] Passed. Top crop: {crop_json['top_3_predictions'][0]['crop']}")

    # Test POST /disease/analyze
    disease_payload = {
        "crop_name": "Tomato",
        "symptoms": "Yellow spots on leaves",
        "user_query": "How to treat yellow spots on tomato leaves?",
    }
    res_dis = client.post("/disease/analyze", json=disease_payload)
    assert res_dis.status_code == 200, f"Error: {res_dis.text}"
    dis_json = res_dis.json()
    assert dis_json["status"] == "success"
    print("  [POST /disease/analyze] Passed.")

    print("\nALL FASTAPI BACKEND TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_1_verify_government_chromadb_count()
    test_2_verify_crop_chromadb_count()
    test_3_government_schemes_rag()
    test_4_crop_knowledge_vector_retrieval()
    test_5_crop_rag_pipeline()
    test_6_fastapi_backend_endpoints()
    print("\n==================================================")
    print(" DUAL RAG PIPELINE & BACKEND TESTS PASSED 100%!")
    print("==================================================")
