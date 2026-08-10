# storage.py — Isolated image saving and SQLite database logging.

import os
import sqlite3
import uuid
from datetime import datetime
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
IMAGES_DIR = os.path.join(STORAGE_DIR, "images")
DB_PATH = os.path.join(STORAGE_DIR, "disease_detection.db")


def init_storage_db():
    """Initializes the storage folders and isolated SQLite database schema."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS disease_history (
            image_id TEXT PRIMARY KEY,
            timestamp TEXT,
            image_path TEXT,
            predicted_crop TEXT,
            predicted_disease TEXT,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()


def save_image_and_log(image: Image.Image, crop: str, disease: str, confidence: float):
    """
    Saves a plant image to disk and logs the prediction metadata in the SQLite db.
    Returns:
        image_id (str): Unique image identifier
        ref_path (str): Frontend reference path (obscuring server paths)
    """
    init_storage_db()
    
    image_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Save image to storage folder
    filename = f"{image_id}.jpg"
    img_save_path = os.path.join(IMAGES_DIR, filename)
    image.convert("RGB").save(img_save_path, "JPEG")
    
    # The reference path exposed to the frontend (obscuring filesystem details)
    # The endpoint will be /disease/images/<filename>
    ref_path = f"/disease/images/{filename}"
    
    # Log to SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO disease_history (image_id, timestamp, image_path, predicted_crop, predicted_disease, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (image_id, timestamp, ref_path, crop, disease, confidence))
    conn.commit()
    conn.close()
    
    return image_id, ref_path


def get_image_file_path(filename):
    """Retrieves the physical filesystem path of a saved image based on its filename."""
    # Prevent directory traversal attacks
    clean_filename = os.path.basename(filename)
    physical_path = os.path.join(IMAGES_DIR, clean_filename)
    if os.path.exists(physical_path):
        return physical_path
    return None


def get_prediction_history():
    """Retrieves all logged predictions from the isolated database."""
    init_storage_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("SELECT * FROM disease_history ORDER BY timestamp DESC").fetchall()
    results = [dict(r) for r in rows]
    conn.close()
    return results
