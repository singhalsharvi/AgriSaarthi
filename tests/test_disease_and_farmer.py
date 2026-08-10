import os
import sys
import io
import json
import unittest
from pathlib import Path
from PIL import Image
import torch
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai.disease_detection.prediction import predict_disease, parse_class_name
from ai.disease_detection.scripts.retrieve_disease_knowledge import retrieve_disease_knowledge
from backend.services.db_service import db_service
from backend.main import app

client = TestClient(app)

class TestDiseaseAndFarmerPipeline(unittest.TestCase):

    def setUp(self):
        # Create a mock 128x128 green image in memory for testing
        self.mock_image_bytes = io.BytesIO()
        img = Image.new("RGB", (128, 128), color="green")
        img.save(self.mock_image_bytes, format="JPEG")
        self.mock_image_bytes.seek(0)

    def test_1_class_name_parsing(self):
        print("\n--- Test 1: Class Name Parsing ---")
        c1, d1 = parse_class_name("Pepper__bell___Bacterial_spot")
        self.assertEqual(c1, "Pepper bell")
        self.assertEqual(d1, "Bacterial Spot")

        c2, d2 = parse_class_name("Potato___Early_blight")
        self.assertEqual(c2, "Potato")
        self.assertEqual(d2, "Early Blight")

        c3, d3 = parse_class_name("Tomato_healthy")
        self.assertEqual(c3, "Tomato")
        self.assertEqual(d3, "Healthy")
        print("SUCCESS: Class name parsing is correct.")

    def test_2_model_inference(self):
        print("\n--- Test 2: Model Loading and Inference ---")
        img = Image.open(self.mock_image_bytes)
        res = predict_disease(img)
        self.assertIn("top_3_predictions", res)
        self.assertEqual(len(res["top_3_predictions"]), 3)
        
        best = res["top_3_predictions"][0]
        self.assertIn("crop", best)
        self.assertIn("disease", best)
        self.assertIn("confidence", best)
        print(f"SUCCESS: Model loaded and mock image classified successfully. Top match: {best['crop']} — {best['disease']}")

    def test_3_disease_rag_retrieval(self):
        print("\n--- Test 3: Disease RAG Vector Retrieval ---")
        docs = retrieve_disease_knowledge(crop_name="Tomato", disease_name="Late Blight", query="symptoms")
        self.assertGreater(len(docs), 0)
        first_doc = docs[0]
        self.assertIn("document_text", first_doc)
        self.assertEqual(first_doc["crop"], "Tomato")
        self.assertEqual(first_doc["disease"], "Late Blight")
        print(f"SUCCESS: ChromaDB query returned {len(docs)} documents for Tomato Late Blight.")

    def test_4_db_service_farmer_profile(self):
        print("\n--- Test 4: SQLite Database Profile Upsert and Get ---")
        test_id = "test.farmer@agrisaarthi.in"
        profile_data = {
            "name": "Sharvi Singhal",
            "location": "Meerut, Uttar Pradesh",
            "landholding": "5.0 Acres",
            "soilType": "Alluvial Clay"
        }
        
        # Upsert
        upserted = db_service.upsert_farmer_profile(test_id, profile_data)
        self.assertEqual(upserted["name"], "Sharvi Singhal")
        self.assertEqual(upserted["location"], "Meerut, Uttar Pradesh")
        self.assertEqual(upserted["land_size"], "5.0 Acres")
        self.assertEqual(upserted["soil_type"], "Alluvial Clay")

        # Get
        retrieved = db_service.get_farmer_profile(test_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Sharvi Singhal")
        print("SUCCESS: Database profile upsert and retrieval verified successfully.")

    def test_5_db_service_activities(self):
        print("\n--- Test 5: SQLite Database Activity Logging ---")
        test_id = "test.farmer@agrisaarthi.in"
        activity_type = "disease_analysis"
        details = {
            "crop": "Tomato",
            "disease": "Late Blight",
            "confidence": "95.50%"
        }
        
        log_id = db_service.log_activity(test_id, activity_type, details)
        self.assertGreater(log_id, 0)
        
        activities = db_service.get_activities(test_id)
        self.assertGreater(len(activities), 0)
        self.assertEqual(activities[0]["activity_type"], "disease_analysis")
        self.assertEqual(activities[0]["details"]["crop"], "Tomato")
        print("SUCCESS: Farmer activity successfully logged and retrieved from database.")

    def test_6_api_endpoints_farmer(self):
        print("\n--- Test 6: FastAPI Farmer Profile Endpoints ---")
        payload = {
            "farmer_id": "api.test@agrisaarthi.in",
            "name": "Ramesh Kumar API Test",
            "location": "Mandya, Karnataka",
            "preferred_language": "kn"
        }
        
        # POST /farmer/profile
        res = client.post("/farmer/profile", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")
        self.assertEqual(res.json()["profile"]["name"], "Ramesh Kumar API Test")

        # GET /farmer/profile/{farmer_id}
        res_get = client.get("/farmer/profile/api.test@agrisaarthi.in")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["profile"]["location"], "Mandya, Karnataka")
        print("SUCCESS: FastAPI profile endpoints verified successfully.")

    def test_7_api_endpoint_disease_json(self):
        print("\n--- Test 7: FastAPI Disease Analysis JSON Endpoint (Text Fallback) ---")
        payload = {
            "crop_name": "Pepper bell",
            "symptoms": "Bacterial Spot",
            "user_query": "How to treat yellow leaf spots?"
        }
        
        res = client.post("/disease/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        self.assertEqual(res_json["status"], "success")
        self.assertEqual(res_json["crop"], "Pepper bell")
        self.assertEqual(res_json["disease"], "Bacterial Spot")
        self.assertIn("ai_explanation", res_json)
        print("SUCCESS: JSON text-only diagnostics endpoint verified successfully.")

    def test_8_api_endpoint_disease_multipart(self):
        print("\n--- Test 8: FastAPI Disease Analysis Multipart Upload Endpoint ---")
        self.mock_image_bytes.seek(0)
        files = {
            "image": ("leaf.jpg", self.mock_image_bytes, "image/jpeg")
        }
        data = {
            "crop_name": "Potato",
            "symptoms": "Brown spots with concentric rings",
            "farmer_id": "test.farmer@agrisaarthi.in"
        }
        
        res = client.post("/disease/analyze", data=data, files=files)
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        self.assertEqual(res_json["status"], "success")
        self.assertIn("crop", res_json)
        self.assertIn("disease", res_json)
        self.assertIn("confidence", res_json)
        self.assertIn("top_matches", res_json)
        self.assertIn("ai_explanation", res_json)
        print("SUCCESS: Multipart image upload diagnostics endpoint verified successfully.")


if __name__ == "__main__":
    unittest.main()
