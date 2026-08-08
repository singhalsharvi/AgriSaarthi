import json
import logging
from typing import Any, Dict
import urllib.parse
import urllib.request

LOG = logging.getLogger("weather_service")

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_and_climate(latitude: float, longitude: float) -> Dict[str, Any]:
    """Retrieve real-time weather and climate parameters (temperature, humidity, precipitation) for given coordinates using Open-Meteo Weather API.

    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.

    Returns:
        Dict containing temperature (°C), humidity (%), precipitation (mm), annual rainfall estimate (mm), and daily max/min temperatures.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }
    url = f"{OPEN_METEO_FORECAST_URL}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AgriculturalAI/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current", {})
        daily = data.get("daily", {})

        temp = float(current.get("temperature_2m", 25.0))
        humidity = float(current.get("relative_humidity_2m", 65.0))
        precip = float(current.get("precipitation", 0.0))

        # Calculate representative daily max/min averages from daily forecast
        daily_max_list = daily.get("temperature_2m_max", [temp])
        daily_min_list = daily.get("temperature_2m_min", [temp - 5])
        precip_sum_list = daily.get("precipitation_sum", [precip])

        avg_max_temp = float(sum(daily_max_list) / len(daily_max_list)) if daily_max_list else temp
        avg_min_temp = float(sum(daily_min_list) / len(daily_min_list)) if daily_min_list else (temp - 5)
        daily_precip_avg = float(sum(precip_sum_list) / len(precip_sum_list)) if precip_sum_list else precip

        # Estimate annual/seasonal cumulative rainfall baseline for agricultural modeling (mm)
        annual_rainfall_estimate = max(200.0, round(daily_precip_avg * 120 + 600.0, 1))

        return {
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2),
            "precipitation_current": round(precip, 2),
            "daily_max_temp": round(avg_max_temp, 2),
            "daily_min_temp": round(avg_min_temp, 2),
            "annual_rainfall_estimate": annual_rainfall_estimate,
            "is_weather_fallback": False,
        }
    except Exception as exc:
        LOG.error("Error connecting to Open-Meteo Weather API: %s. Using regional agricultural baseline.", exc)
        return {
            "temperature": 26.5,
            "humidity": 68.0,
            "precipitation_current": 2.5,
            "daily_max_temp": 31.0,
            "daily_min_temp": 22.0,
            "annual_rainfall_estimate": 850.0,
            "is_weather_fallback": True,
        }
