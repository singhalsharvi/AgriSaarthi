import os
import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agrisaarthi.db")

class DatabaseService:
    """Service to manage SQLite connection and execute queries for farmer profiles and activities."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        # check_same_thread=False enables sharing connections between request threads in FastAPI safely
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes database schema and creates tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create farmer_profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS farmer_profiles (
                    farmer_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    location TEXT,
                    state TEXT,
                    district TEXT,
                    contact_info TEXT,
                    preferred_language TEXT,
                    land_size TEXT,
                    soil_type TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # Create farmer_activities table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS farmer_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    farmer_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    details TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(farmer_id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def get_farmer_profile(self, farmer_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a farmer profile by farmer_id."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM farmer_profiles WHERE farmer_id = ?", 
                (farmer_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def upsert_farmer_profile(self, farmer_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates or updates a farmer profile."""
        now = datetime.utcnow().isoformat()
        
        # Check if profile already exists to preserve created_at
        existing = self.get_farmer_profile(farmer_id)
        created_at = existing["created_at"] if existing else now
        
        name = profile_data.get("name", "Farmer")
        location = profile_data.get("location", "")
        
        # Parse state and district from location if possible (e.g. "Meerut, Uttar Pradesh")
        state = profile_data.get("state", "")
        district = profile_data.get("district", "")
        if location and not (state or district):
            parts = [p.strip() for p in location.split(",")]
            if len(parts) >= 2:
                district = parts[0]
                state = parts[1]
            elif len(parts) == 1:
                district = parts[0]

        contact_info = profile_data.get("contact_info", profile_data.get("emailOrPhone", ""))
        preferred_language = profile_data.get("preferred_language", profile_data.get("preferredLanguage", "en"))
        land_size = profile_data.get("land_size", profile_data.get("landholding", ""))
        soil_type = profile_data.get("soil_type", profile_data.get("soilType", ""))

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO farmer_profiles (
                    farmer_id, name, location, state, district, contact_info, 
                    preferred_language, land_size, soil_type, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(farmer_id) DO UPDATE SET
                    name=excluded.name,
                    location=excluded.location,
                    state=excluded.state,
                    district=excluded.district,
                    contact_info=excluded.contact_info,
                    preferred_language=excluded.preferred_language,
                    land_size=excluded.land_size,
                    soil_type=excluded.soil_type,
                    updated_at=excluded.updated_at
            """, (
                farmer_id, name, location, state, district, contact_info,
                preferred_language, land_size, soil_type, created_at, now
            ))
            conn.commit()

        return self.get_farmer_profile(farmer_id)

    def log_activity(self, farmer_id: str, activity_type: str, details: Dict[str, Any]) -> int:
        """Logs a farmer activity (e.g., crop recommendation, disease detection, scheme search)."""
        now = datetime.utcnow().isoformat()
        details_str = json.dumps(details)

        # First ensure the farmer profile exists in the DB (insert default if not exists)
        if not self.get_farmer_profile(farmer_id):
            self.upsert_farmer_profile(farmer_id, {
                "name": "Default Farmer",
                "location": "Meerut, Uttar Pradesh"
            })

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO farmer_activities (farmer_id, activity_type, details, created_at)
                VALUES (?, ?, ?, ?)
            """, (farmer_id, activity_type, details_str, now))
            conn.commit()
            return cursor.lastrowid

    def get_activities(self, farmer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent activities logged by a farmer."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM farmer_activities 
                WHERE farmer_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (farmer_id, limit))
            
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item["details"]:
                    try:
                        item["details"] = json.loads(item["details"])
                    except Exception:
                        pass
                results.append(item)
            return results

db_service = DatabaseService()
