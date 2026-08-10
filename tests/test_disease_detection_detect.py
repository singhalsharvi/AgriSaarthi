import io
import os
import sys
import unittest
from pathlib import Path
from PIL import Image
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app
from ai.disease_detection.storage import get_prediction_history

client = TestClient(app)

class TestDiseaseDetectionDetect(unittest.TestCase):

    def setUp(self):
        # Create a mock 128x128 green image in memory for testing
        self.mock_image_bytes = io.BytesIO()
        img = Image.new("RGB", (128, 128), color="green")
        img.save(self.mock_image_bytes, format="JPEG")
        self.mock_image_bytes.seek(0)

        # Create a blurred gray image to test low confidence/ambiguity
        self.mock_gray_image_bytes = io.BytesIO()
        gray_img = Image.new("RGB", (128, 128), color=(128, 128, 128))
        gray_img.save(self.mock_gray_image_bytes, format="JPEG")
        self.mock_gray_image_bytes.seek(0)

    def test_1_detect_success(self):
        print("\n--- Test 1: POST /disease/detect with valid image ---")
        self.mock_image_bytes.seek(0)
        files = {
            "image": ("leaf.jpg", self.mock_image_bytes, "image/jpeg")
        }
        res = client.post("/disease/detect", files=files)
        self.assertEqual(res.status_code, 200)
        
        res_json = res.json()
        print("Response JSON keys:", list(res_json.keys()))
        
        # Verify required fields
        self.assertIn("crop", res_json)
        self.assertIn("disease", res_json)
        self.assertIn("confidence", res_json)
        self.assertIn("low_confidence", res_json)
        self.assertIn("symptoms", res_json)
        self.assertIn("prevention", res_json)
        self.assertIn("treatment_or_management", res_json)
        self.assertIn("explanation", res_json)
        self.assertIn("image_id", res_json)

        # Validate types
        self.assertIsInstance(res_json["crop"], str)
        self.assertIsInstance(res_json["disease"], str)
        self.assertIsInstance(res_json["confidence"], float)
        self.assertIsInstance(res_json["low_confidence"], bool)
        self.assertIsInstance(res_json["symptoms"], list)
        self.assertIsInstance(res_json["prevention"], list)
        self.assertIsInstance(res_json["treatment_or_management"], list)
        self.assertIsInstance(res_json["explanation"], str)
        self.assertIsInstance(res_json["image_id"], str)
        self.assertTrue(len(res_json["image_id"]) > 0)
        
        print(f"SUCCESS: Detection successful. Crop: {res_json['crop']}, Disease: {res_json['disease']}, Confidence: {res_json['confidence']:.4f}")

    def test_2_serve_image(self):
        print("\n--- Test 2: GET /disease/images/{filename} serving ---")
        # 1. Run detection first to save an image
        self.mock_image_bytes.seek(0)
        files = {
            "image": ("leaf_test.jpg", self.mock_image_bytes, "image/jpeg")
        }
        res = client.post("/disease/detect", files=files)
        self.assertEqual(res.status_code, 200)
        image_id = res.json()["image_id"]
        filename = f"{image_id}.jpg"

        # 2. Get the served image
        img_res = client.get(f"/disease/images/{filename}")
        self.assertEqual(img_res.status_code, 200)
        self.assertEqual(img_res.headers["content-type"], "image/jpeg")
        
        # Verify content length > 0
        self.assertTrue(len(img_res.content) > 0)
        print(f"SUCCESS: Served saved image file safely. Filename: {filename}")

    def test_3_invalid_file_format(self):
        print("\n--- Test 3: POST /disease/detect with invalid file format ---")
        mock_txt = io.BytesIO(b"Hello World")
        files = {
            "image": ("test.txt", mock_txt, "text/plain")
        }
        res = client.post("/disease/detect", files=files)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Invalid image format", res.json()["detail"])
        print("SUCCESS: Rejected invalid format correctly.")

    def test_4_low_confidence_ambiguous_image(self):
        print("\n--- Test 4: POST /disease/detect with ambiguous/blurred image ---")
        self.mock_gray_image_bytes.seek(0)
        files = {
            "image": ("ambiguous.jpg", self.mock_gray_image_bytes, "image/jpeg")
        }
        res = client.post("/disease/detect", files=files)
        self.assertEqual(res.status_code, 200)
        
        res_json = res.json()
        print(f"Ambiguous Image confidence: {res_json['confidence']*100:.2f}% | Low confidence flag: {res_json['low_confidence']}")
        self.assertTrue(res_json["low_confidence"])
        
        self.assertIsInstance(res_json["explanation"], str)
        self.assertTrue(len(res_json["explanation"]) > 0)
        print("SUCCESS: Correctly flagged low confidence and generated cautious advisory.")


if __name__ == "__main__":
    unittest.main()
