import logging
from typing import Any, Dict, Optional
import urllib.parse
import urllib.request
import json

LOG = logging.getLogger("location_service")

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Enables meaningful, location-specific recommendations when a device is offline
# or the geocoding provider is temporarily unavailable.  Coordinates are state
# reference points, not a claim that the entered village is the state capital.
OFFLINE_STATE_LOCATIONS = {
    "andhra pradesh": (15.9129, 79.7400),
    "gujarat": (22.2587, 71.1924),
    "karnataka": (15.3173, 75.7139),
    "madhya pradesh": (22.9734, 78.6569),
    "maharashtra": (19.7515, 75.7139),
    "punjab": (31.1471, 75.3412),
    "rajasthan": (27.0238, 74.2179),
    "tamil nadu": (11.1271, 78.6569),
    "telangana": (18.1124, 79.0193),
    "uttar pradesh": (26.8467, 80.9462),
    "west bengal": (22.9868, 87.8550),
}


def offline_location_fallback(location_name: str) -> Dict[str, Any]:
    """Return a state-aware fallback instead of one identical India location."""
    normalized = location_name.casefold()
    for state, (latitude, longitude) in OFFLINE_STATE_LOCATIONS.items():
        if state in normalized:
            return {
                "latitude": latitude,
                "longitude": longitude,
                "name": location_name,
                "state": state.title(),
                "country": "India",
                "is_fallback": True,
            }
    return {
        "latitude": 20.5937,
        "longitude": 78.9629,
        "name": location_name,
        "state": "India",
        "country": "India",
        "is_fallback": True,
    }


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
            return offline_location_fallback(location_name)

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
        return offline_location_fallback(location_name)
