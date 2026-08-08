import logging
from typing import Any, Dict, Optional
import urllib.parse
import urllib.request
import json

LOG = logging.getLogger("location_service")

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def resolve_location(location_name: str) -> Dict[str, Any]:
    """Resolve location string (e.g. 'Mandya, Karnataka' or 'Ludhiana, Punjab') to latitude, longitude, and administrative state using Open-Meteo Geocoding API.

    Args:
        location_name: City/District/State string provided by the farmer.

    Returns:
        Dict containing latitude, longitude, name, state, country, and admin region.
    """
    if not location_name or not location_name.strip():
        raise ValueError("Location name cannot be empty.")

    query = location_name.strip()
    encoded_query = urllib.parse.quote(query)
    url = f"{OPEN_METEO_GEOCODING_URL}?name={encoded_query}&count=1&language=en&format=json"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AgriculturalAI/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = data.get("results", [])
        if not results:
            # Fallback retry with primary city/state component if compound string was used
            parts = [p.strip() for p in query.split(",") if p.strip()]
            if len(parts) > 1:
                query_fallback = parts[0]
                encoded_fallback = urllib.parse.quote(query_fallback)
                url_fallback = f"{OPEN_METEO_GEOCODING_URL}?name={encoded_fallback}&count=1&language=en&format=json"
                req_fb = urllib.request.Request(url_fallback, headers={"User-Agent": "AgriculturalAI/1.0"})
                with urllib.request.urlopen(req_fb, timeout=10) as response_fb:
                    data_fb = json.loads(response_fb.read().decode("utf-8"))
                results = data_fb.get("results", [])

        if not results:
            LOG.warning("Location '%s' could not be resolved via Open-Meteo. Using fallback coordinates.", location_name)
            return {
                "latitude": 20.5937,
                "longitude": 78.9629,
                "name": location_name,
                "state": "India",
                "country": "India",
                "is_fallback": True,
            }

        top_match = results[0]
        state = top_match.get("admin1") or top_match.get("admin2") or top_match.get("name") or "India"

        return {
            "latitude": float(top_match.get("latitude")),
            "longitude": float(top_match.get("longitude")),
            "name": top_match.get("name") or location_name,
            "state": state,
            "country": top_match.get("country") or "India",
            "admin1": top_match.get("admin1") or "",
            "is_fallback": False,
        }
    except Exception as exc:
        LOG.error("Error connecting to Open-Meteo Geocoding API: %s. Using default India coordinates.", exc)
        return {
            "latitude": 20.5937,
            "longitude": 78.9629,
            "name": location_name,
            "state": "India",
            "country": "India",
            "is_fallback": True,
        }
