import logging
from typing import Any, Dict, Optional

LOG = logging.getLogger("soil_service")

# Regional soil database mapped to ICAR / Soil Health Card regional benchmark soil types & nutrient profiles
STATE_SOIL_DATABASE: Dict[str, Dict[str, Any]] = {
    "karnataka": {
        "dominant_soil": "Red Sandy Loam",
        "soil_type_category": "Clay",  # Categorical mapping for model input
        "ph": 6.5,
        "default_N": 90.0,
        "default_P": 42.0,
        "default_K": 43.0,
        "description": "Red Sandy Loam / Clay Loam soils rich in iron, responsive to nitrogen & organic matter.",
    },
    "punjab": {
        "dominant_soil": "Alluvial Soil",
        "soil_type_category": "Alluvial",
        "ph": 7.2,
        "default_N": 110.0,
        "default_P": 50.0,
        "default_K": 45.0,
        "description": "Deep fertile Indo-Gangetic Alluvial soil, highly suitable for intensive wheat & rice rotations.",
    },
    "maharashtra": {
        "dominant_soil": "Black Cotton Soil (Regur)",
        "soil_type_category": "Black",
        "ph": 7.5,
        "default_N": 85.0,
        "default_P": 45.0,
        "default_K": 60.0,
        "description": "Deep Black Vertisol clay soil with high clay content and high moisture retention, ideal for cotton & pulses.",
    },
    "tamil nadu": {
        "dominant_soil": "Red Loam / Coastal Alluvial",
        "soil_type_category": "Loam",
        "ph": 6.2,
        "default_N": 80.0,
        "default_P": 42.0,
        "default_K": 50.0,
        "description": "Red Loamy soil with good permeability, responsive to potassium and organic mulching.",
    },
    "uttar pradesh": {
        "dominant_soil": "Alluvial Soil",
        "soil_type_category": "Alluvial",
        "ph": 7.0,
        "default_N": 100.0,
        "default_P": 48.0,
        "default_K": 45.0,
        "description": "Gangetic Plain Alluvial soil, well-drained and fertile.",
    },
    "rajasthan": {
        "dominant_soil": "Desert Sandy Soil",
        "soil_type_category": "Sandy",
        "ph": 7.8,
        "default_N": 50.0,
        "default_P": 30.0,
        "default_K": 40.0,
        "description": "Sandy desert soil with low organic matter, highly permeable with alkaline pH.",
    },
    "west bengal": {
        "dominant_soil": "Deltaic Alluvial / Silty-Clay",
        "soil_type_category": "Silty-Clay",
        "ph": 6.0,
        "default_N": 95.0,
        "default_P": 45.0,
        "default_K": 50.0,
        "description": "Silty-Clay river delta soil with high moisture retentivity, suitable for paddy and jute.",
    },
    "gujarat": {
        "dominant_soil": "Black Soil / Alluvial",
        "soil_type_category": "Black",
        "ph": 7.6,
        "default_N": 85.0,
        "default_P": 45.0,
        "default_K": 55.0,
        "description": "Medium to deep Black Vertisol soil, suitable for groundnut and cotton.",
    },
    "andhra pradesh": {
        "dominant_soil": "Red Sandy Loam / Black Cotton",
        "soil_type_category": "Loam",
        "ph": 6.6,
        "default_N": 90.0,
        "default_P": 42.0,
        "default_K": 48.0,
        "description": "Red Sandy Loam with good drainage and phosphorus response.",
    },
    "telangana": {
        "dominant_soil": "Red Sandy Soil (Chalka)",
        "soil_type_category": "Loam",
        "ph": 6.5,
        "default_N": 85.0,
        "default_P": 40.0,
        "default_K": 45.0,
        "description": "Red Sandy soil with light texture, responsive to organic manures.",
    },
    "madhya pradesh": {
        "dominant_soil": "Medium & Deep Black Soil",
        "soil_type_category": "Black",
        "ph": 7.4,
        "default_N": 80.0,
        "default_P": 40.0,
        "default_K": 50.0,
        "description": "Black Cotton clay soil with high moisture storage, ideal for soybean and chickpea.",
    },
}

DEFAULT_BENCHMARK = {
    "dominant_soil": "Agricultural Loam Soil",
    "soil_type_category": "Loam",
    "ph": 6.8,
    "default_N": 85.0,
    "default_P": 42.0,
    "default_K": 45.0,
    "description": "Standard fertile Agricultural Loam soil with balanced nutrient response.",
}


def resolve_soil_information(
    state: str,
    soil_type_override: Optional[str] = None,
    N: Optional[float] = None,
    P: Optional[float] = None,
    K: Optional[float] = None,
) -> Dict[str, Any]:
    """Resolve categorical soil type and numerical N-P-K nutrient values for a given state/region.

    Distinguishes transparently between user-provided soil measurements and regional Soil Health Card benchmark averages.

    Args:
        state: Administrative state or region name.
        soil_type_override: Optional explicit soil type provided by user.
        N, P, K: Optional user-measured Nitrogen, Phosphorus, Potassium values.

    Returns:
        Dict containing soil_type, ph, Nitrogen, Phosphorus, Potassium, npk_source, and is_benchmark_derived.
    """
    clean_state = (state or "").lower().strip()

    # Find state entry or fallback
    soil_info = DEFAULT_BENCHMARK
    for s_key in STATE_SOIL_DATABASE:
        if s_key in clean_state or clean_state in s_key:
            soil_info = STATE_SOIL_DATABASE[s_key]
            break

    # Determine final soil type category for ML model
    final_soil_type = soil_type_override if soil_type_override else soil_info["soil_type_category"]

    # Determine N-P-K nutrient values & source tracking
    is_user_n = N is not None
    is_user_p = P is not None
    is_user_k = K is not None

    final_N = float(N) if is_user_n else float(soil_info["default_N"])
    final_P = float(P) if is_user_p else float(soil_info["default_P"])
    final_K = float(K) if is_user_k else float(soil_info["default_K"])

    all_user = is_user_n and is_user_p and is_user_k
    npk_source = "User Measured Input" if all_user else "Regional ICAR / Soil Health Card Benchmark Average"

    return {
        "dominant_soil_name": soil_info["dominant_soil"],
        "soil_type": final_soil_type,
        "ph": soil_info["ph"],
        "Nitrogen": final_N,
        "Phosphorus": final_P,
        "Potassium": final_K,
        "npk_source": npk_source,
        "is_benchmark_derived": not all_user,
        "description": soil_info["description"],
    }
