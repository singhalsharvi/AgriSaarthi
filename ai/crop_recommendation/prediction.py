import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
LABEL_ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.pkl")

# Global instances for fast API warm-start
_model = None
_preprocessor = None
_label_encoder = None

def _load_artifacts():
    global _model, _preprocessor, _label_encoder
    if _model is None or _preprocessor is None or _label_encoder is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run training pipeline first.")
        _model = joblib.load(MODEL_PATH)
        _preprocessor = joblib.load(PREPROCESSOR_PATH)
        _label_encoder = joblib.load(LABEL_ENCODER_PATH)

def predict_crop(
    Nitrogen: float,
    Phosphorus: float,
    Potassium: float,
    Temperature: float,
    Humidity: float,
    pH_Value: float,
    Rainfall: float,
    Soil_Type: str
) -> dict:
    """
    Predicts the optimal crop recommendations for given soil and environmental conditions.

    Parameters:
    - Nitrogen: Soil Nitrogen content (N)
    - Phosphorus: Soil Phosphorus content (P)
    - Potassium: Soil Potassium content (K)
    - Temperature: Ambient temperature (°C)
    - Humidity: Relative humidity (%)
    - pH_Value: Soil pH level (0-14)
    - Rainfall: Annual/seasonal rainfall (mm)
    - Soil_Type: Category of soil (e.g., 'Clay', 'Loam', 'Sandy', 'Black', 'Alluvial')

    Returns:
    Dictionary containing:
    - top_3_predictions: List of dicts with 'crop', 'confidence_score', and 'probability'
    - prediction_probabilities: Dict mapping all crop classes to predicted probabilities
    """
    _load_artifacts()

    numeric_features = {
        "Nitrogen": Nitrogen, "Phosphorus": Phosphorus, "Potassium": Potassium,
        "Temperature": Temperature, "Humidity": Humidity, "pH_Value": pH_Value,
        "Rainfall": Rainfall,
    }
    for name, value in numeric_features.items():
        if not np.isfinite(float(value)):
            raise ValueError(f"{name} must be a finite number.")
    if not 0.0 <= float(pH_Value) <= 14.0:
        raise ValueError("pH_Value must be between 0 and 14.")
    if not 0.0 <= float(Humidity) <= 100.0:
        raise ValueError("Humidity must be between 0 and 100.")
    if float(Rainfall) < 0.0:
        raise ValueError("Rainfall cannot be negative.")

    input_data = pd.DataFrame([{
        "Nitrogen": float(Nitrogen),
        "Phosphorus": float(Phosphorus),
        "Potassium": float(Potassium),
        "Temperature": float(Temperature),
        "Humidity": float(Humidity),
        "pH_Value": float(pH_Value),
        "Rainfall": float(Rainfall),
        "Soil_Type": str(Soil_Type)
    }])

    processed_input = _preprocessor.transform(input_data)

    probs = _model.predict_proba(processed_input)[0]
    classes = _label_encoder.classes_

    prob_dict = {crop: round(float(prob), 4) for crop, prob in zip(classes, probs)}

    top_3_indices = np.argsort(probs)[::-1][:3]
    sorted_probs = np.sort(probs)[::-1]
    confidence_margin = float(sorted_probs[0] - sorted_probs[1]) if len(sorted_probs) > 1 else float(sorted_probs[0])
    entropy = -float(np.sum(probs * np.log(np.clip(probs, 1e-12, 1.0))))
    normalized_entropy = entropy / float(np.log(len(probs))) if len(probs) > 1 else 0.0
    top_3_list = []
    for idx in top_3_indices:
        crop_name = classes[idx]
        confidence = float(probs[idx])
        top_3_list.append({
            "crop": crop_name,
            "confidence_score": round(confidence, 4),
            "probability": round(confidence, 4)
        })

    return {
        "top_3_predictions": top_3_list,
        "prediction_probabilities": prob_dict,
        "confidence_margin": round(confidence_margin, 4),
        "normalized_entropy": round(normalized_entropy, 4),
    }

if __name__ == "__main__":
    sample_res = predict_crop(
        Nitrogen=90,
        Phosphorus=42,
        Potassium=43,
        Temperature=20.87,
        Humidity=82.0,
        pH_Value=6.5,
        Rainfall=202.93,
        Soil_Type="Clay"
    )
    print("Sample Prediction Output:")
    print(json.dumps(sample_res, indent=2))
