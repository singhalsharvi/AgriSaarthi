import logging
from typing import Any, Dict, List, Optional

LOG = logging.getLogger("fallback_matcher")

# Comprehensive regional crop suitability knowledge base
# Grounded in official ICAR & Indian State Agricultural University agronomic recommendations
CROP_SUITABILITY_REGISTRY: List[Dict[str, Any]] = [
    {
        "crop": "Bajra (Pearl Millet)",
        "category": "Millet / Coarse Cereal",
        "suitable_states": ["rajasthan", "gujarat", "haryana", "maharashtra", "uttar pradesh"],
        "suitable_soils": ["sandy", "loam", "desert sandy soil"],
        "min_temp": 20.0,
        "max_temp": 42.0,
        "min_rainfall": 250.0,
        "max_rainfall": 800.0,
        "suitable_seasons": ["kharif", "summer", "all"],
        "drought_tolerant": True,
        "reason": "Drought-hardy nutrient-rich millet suited for arid/semi-arid sandy soils with moderate rainfall.",
        "source": "Location & Soil Knowledge Base (ICAR Arid Zone Research)",
    },
    {
        "crop": "Jowar (Sorghum)",
        "category": "Coarse Cereal",
        "suitable_states": ["maharashtra", "karnataka", "rajasthan", "madhya pradesh", "telangana", "andhra pradesh"],
        "suitable_soils": ["black", "loam", "clay"],
        "min_temp": 20.0,
        "max_temp": 38.0,
        "min_rainfall": 350.0,
        "max_rainfall": 900.0,
        "suitable_seasons": ["kharif", "rabi", "all"],
        "drought_tolerant": True,
        "reason": "Hardy coarse grain ideal for Vertisol black soils and medium rainfall regions.",
        "source": "Location & Soil Knowledge Base (ICAR Indian Institute of Millets Research)",
    },
    {
        "crop": "Ragi (Finger Millet)",
        "category": "Nutri-Cereal",
        "suitable_states": ["karnataka", "tamil nadu", "uttarakhand", "odisha", "andhra pradesh", "maharashtra"],
        "suitable_soils": ["red loam", "sandy loam", "loam", "clay"],
        "min_temp": 18.0,
        "max_temp": 35.0,
        "min_rainfall": 450.0,
        "max_rainfall": 1200.0,
        "suitable_seasons": ["kharif", "all"],
        "drought_tolerant": True,
        "reason": "Nutritious finger millet thriving in red loamy soils under rainfed conditions.",
        "source": "Location & Soil Knowledge Base (UAS Bengaluru / ICAR)",
    },
    {
        "crop": "Wheat",
        "category": "Rabi Cereal Staple",
        "suitable_states": ["punjab", "haryana", "uttar pradesh", "madhya pradesh", "rajasthan", "bihar"],
        "suitable_soils": ["alluvial", "loam", "clay loam"],
        "min_temp": 8.0,
        "max_temp": 28.0,
        "min_rainfall": 400.0,
        "max_rainfall": 900.0,
        "suitable_seasons": ["rabi", "winter"],
        "drought_tolerant": False,
        "reason": "Primary Rabi staple requiring cool winter temperatures and rich Gangetic alluvial/loamy soil.",
        "source": "Location & Soil Knowledge Base (ICAR Indian Institute of Wheat & Barley Research)",
    },
    {
        "crop": "Soybean",
        "category": "Oilseed / Legume",
        "suitable_states": ["madhya pradesh", "maharashtra", "rajasthan", "karnataka", "telangana"],
        "suitable_soils": ["black", "clay loam", "loam"],
        "min_temp": 20.0,
        "max_temp": 35.0,
        "min_rainfall": 600.0,
        "max_rainfall": 1100.0,
        "suitable_seasons": ["kharif"],
        "drought_tolerant": False,
        "reason": "Major Kharif oilseed requiring deep moisture-retentive black Vertisol soils.",
        "source": "Location & Soil Knowledge Base (ICAR Indian Institute of Soybean Research)",
    },
    {
        "crop": "Groundnut (Peanut)",
        "category": "Oilseed",
        "suitable_states": ["gujarat", "rajasthan", "andhra pradesh", "tamil nadu", "karnataka", "telangana"],
        "suitable_soils": ["sandy loam", "sandy", "loam", "red loam"],
        "min_temp": 20.0,
        "max_temp": 33.0,
        "min_rainfall": 450.0,
        "max_rainfall": 1000.0,
        "suitable_seasons": ["kharif", "summer", "all"],
        "drought_tolerant": True,
        "reason": "High-value oilseed thriving in friable sandy loam soils enabling subterranean peg formation.",
        "source": "Location & Soil Knowledge Base (ICAR Directorate of Groundnut Research)",
    },
    {
        "crop": "Mustard",
        "category": "Rabi Oilseed",
        "suitable_states": ["rajasthan", "uttar pradesh", "haryana", "madhya pradesh", "west bengal", "assam"],
        "suitable_soils": ["alluvial", "sandy loam", "loam"],
        "min_temp": 8.0,
        "max_temp": 27.0,
        "min_rainfall": 300.0,
        "max_rainfall": 700.0,
        "suitable_seasons": ["rabi", "winter"],
        "drought_tolerant": True,
        "reason": "Essential Rabi oilseed well-suited for light alluvial and loamy soils under cool winter conditions.",
        "source": "Location & Soil Knowledge Base (ICAR Directorate of Rapeseed-Mustard Research)",
    },
    {
        "crop": "Sugarcane",
        "category": "Commercial Perennial",
        "suitable_states": ["uttar pradesh", "maharashtra", "karnataka", "tamil nadu", "andhra pradesh", "gujarat"],
        "suitable_soils": ["alluvial", "black", "clay loam", "loam"],
        "min_temp": 20.0,
        "max_temp": 38.0,
        "min_rainfall": 1200.0,
        "max_rainfall": 2800.0,
        "suitable_seasons": ["all", "perennial", "kharif", "rabi"],
        "drought_tolerant": False,
        "reason": "High-yielding commercial cash crop requiring heavy soils and abundant irrigation.",
        "source": "Location & Soil Knowledge Base (ICAR Sugarcane Breeding Institute)",
    },
    {
        "crop": "Cotton",
        "category": "Commercial Fiber",
        "suitable_states": ["gujarat", "maharashtra", "telangana", "andhra pradesh", "haryana", "punjab", "karnataka"],
        "suitable_soils": ["black", "clay", "alluvial"],
        "min_temp": 21.0,
        "max_temp": 37.0,
        "min_rainfall": 500.0,
        "max_rainfall": 1100.0,
        "suitable_seasons": ["kharif", "all"],
        "drought_tolerant": True,
        "reason": "Golden fiber crop ideal for moisture-retentive black Vertisol soils.",
        "source": "Location & Soil Knowledge Base (ICAR Central Institute for Cotton Research)",
    },
    {
        "crop": "Turmeric",
        "category": "Spice Crop",
        "suitable_states": ["telangana", "andhra pradesh", "tamil nadu", "karnataka", "kerala", "odisha", "maharashtra"],
        "suitable_soils": ["loam", "sandy loam", "clay loam", "red loam"],
        "min_temp": 19.0,
        "max_temp": 35.0,
        "min_rainfall": 1200.0,
        "max_rainfall": 2400.0,
        "suitable_seasons": ["kharif"],
        "drought_tolerant": False,
        "reason": "High-value spice requiring friable organic loamy soils and warm humid conditions.",
        "source": "Location & Soil Knowledge Base (ICAR Indian Institute of Spices Research)",
    },
    {
        "crop": "Potato",
        "category": "Rabi Tuber / Vegetable",
        "suitable_states": ["uttar pradesh", "west bengal", "bihar", "punjab", "gujarat", "madhya pradesh"],
        "suitable_soils": ["alluvial", "sandy loam", "loam"],
        "min_temp": 10.0,
        "max_temp": 25.0,
        "min_rainfall": 400.0,
        "max_rainfall": 800.0,
        "suitable_seasons": ["rabi", "winter"],
        "drought_tolerant": False,
        "reason": "Short-duration tuber requiring loose fertile alluvial soil and cool night temperatures.",
        "source": "Location & Soil Knowledge Base (ICAR Central Potato Research Institute)",
    },
    {
        "crop": "Onion",
        "category": "Bulb Vegetable",
        "suitable_states": ["maharashtra", "karnataka", "gujarat", "madhya pradesh", "rajasthan", "andhra pradesh"],
        "suitable_soils": ["loam", "sandy loam", "black", "red loam"],
        "min_temp": 13.0,
        "max_temp": 32.0,
        "min_rainfall": 450.0,
        "max_rainfall": 900.0,
        "suitable_seasons": ["rabi", "kharif", "late kharif", "all"],
        "drought_tolerant": False,
        "reason": "Essential vegetable crop performing best in well-drained loams with moderate irrigation.",
        "source": "Location & Soil Knowledge Base (ICAR Directorate of Onion & Garlic Research)",
    },
    {
        "crop": "Sesame (Til)",
        "category": "Oilseed",
        "suitable_states": ["gujarat", "west bengal", "rajasthan", "madhya pradesh", "tamil nadu", "uttar pradesh"],
        "suitable_soils": ["sandy loam", "loam", "sandy"],
        "min_temp": 22.0,
        "max_temp": 37.0,
        "min_rainfall": 300.0,
        "max_rainfall": 700.0,
        "suitable_seasons": ["kharif", "summer", "all"],
        "drought_tolerant": True,
        "reason": "Drought-tolerant oilseed well-suited to light sandy loams in warm climates.",
        "source": "Location & Soil Knowledge Base (ICAR Indian Institute of Oilseeds Research)",
    },
    {
        "crop": "Gram / Chickpea",
        "category": "Rabi Pulse",
        "suitable_states": ["madhya pradesh", "maharashtra", "rajasthan", "uttar pradesh", "karnataka", "andhra pradesh"],
        "suitable_soils": ["black", "loam", "clay loam", "alluvial"],
        "min_temp": 10.0,
        "max_temp": 28.0,
        "min_rainfall": 350.0,
        "max_rainfall": 700.0,
        "suitable_seasons": ["rabi", "winter"],
        "drought_tolerant": True,
        "reason": "Major winter pulse crop thriving in moisture-conserving black and loamy soils.",
        "source": "Location & Soil Knowledge Base (ICAR Indian Institute of Pulses Research)",
    },
]


def find_fallback_crops(
    state: str,
    soil_type: str,
    ph: float,
    temp: float,
    rainfall: float,
    season: str,
) -> Dict[str, Any]:
    """Find evidence-backed alternative crop recommendations when ML model confidence is low (< 50%).

    Evaluates location, state, soil category, temperature, rainfall, and season.
    Returns compatible crops OR identifies limiting environmental constraints if no crop is suitable.
    """
    clean_state = (state or "").lower().strip()
    clean_soil = (soil_type or "").lower().strip()
    clean_season = (season or "kharif").lower().strip()

    candidate_matches = []
    limiting_factors = []

    # Check for extreme environmental limitations
    if rainfall < 150.0:
        limiting_factors.append(f"Severely deficient rainfall ({rainfall:.1f} mm) below minimal rainfed threshold")
    if temp > 45.0:
        limiting_factors.append(f"Extreme heat stress ({temp:.1f} °C) exceeding crop tolerance")
    if temp < 4.0:
        limiting_factors.append(f"Extreme frost risk ({temp:.1f} °C) below crop survival limits")
    if ph < 4.0 or ph > 9.0:
        limiting_factors.append(f"Extreme soil pH ({ph:.1f}) outside arable crop range")

    if limiting_factors and rainfall < 150.0:
        return {
            "status": "NONE",
            "recommended_crops": [],
            "limiting_factors": limiting_factors,
            "message": "No suitable crop could be confidently recommended for the provided conditions.",
        }

    for crop_meta in CROP_SUITABILITY_REGISTRY:
        score = 0
        reasons = []

        # 1. State / Regional match check
        state_match = any(st in clean_state or clean_state in st for st in crop_meta["suitable_states"])
        if state_match:
            score += 30
            reasons.append(f"Commonly cultivated in {state.title()} state region")

        # 2. Soil type match check
        soil_match = any(st in clean_soil or clean_soil in st for st in crop_meta["suitable_soils"])
        if soil_match:
            score += 30
            reasons.append(f"Well-suited for {soil_type} soil profile")
        elif "loam" in clean_soil or "clay" in clean_soil:
            score += 15
            reasons.append(f"Adaptable to {soil_type} soil texture")

        # 3. Temperature range check
        if crop_meta["min_temp"] <= temp <= crop_meta["max_temp"]:
            score += 20
            reasons.append(f"Temperature ({temp}°C) falls within optimal growth range ({crop_meta['min_temp']}-{crop_meta['max_temp']}°C)")
        else:
            score -= 20  # Penalty for temperature mismatch

        # 4. Rainfall / Water availability check
        if crop_meta["min_rainfall"] <= rainfall <= crop_meta["max_rainfall"]:
            score += 20
            reasons.append(f"Rainfall ({rainfall:.0f} mm) satisfies water requirements")
        elif rainfall < crop_meta["min_rainfall"] and crop_meta.get("drought_tolerant"):
            score += 15
            reasons.append(f"Drought-tolerant nature accommodates dry rainfall regime ({rainfall:.0f} mm)")
        elif rainfall < crop_meta["min_rainfall"] and not crop_meta.get("drought_tolerant"):
            score -= 25

        # 5. Season check
        if "all" in crop_meta["suitable_seasons"] or any(s in clean_season for s in crop_meta["suitable_seasons"]):
            score += 10
        elif clean_season in ["rabi", "winter"] and "rabi" not in crop_meta["suitable_seasons"]:
            score -= 30  # Heavy penalty for planting Kharif crop in Rabi winter

        if score >= 50:
            candidate_matches.append(
                {
                    "crop": crop_meta["crop"],
                    "category": crop_meta["category"],
                    "match_score": score,
                    "reason": "; ".join(reasons),
                    "confidence": "High" if score >= 80 else "Medium",
                    "source": crop_meta["source"],
                }
            )

    # Sort matches by score descending
    candidate_matches.sort(key=lambda x: x["match_score"], reverse=True)
    top_candidates = candidate_matches[:3]

    if not top_candidates:
        if not limiting_factors:
            limiting_factors.append(f"Incompatible combination of {season} season, {soil_type} soil, and current temperature ({temp}°C)")
        return {
            "status": "NONE",
            "recommended_crops": [],
            "limiting_factors": limiting_factors,
            "message": "No suitable crop could be confidently recommended for the provided conditions.",
        }

    return {
        "status": "LOCATION_SOIL_RAG",
        "recommended_crops": top_candidates,
        "limiting_factors": [],
        "message": "Alternative crop recommendations identified from location, soil, and climate knowledge database.",
    }
