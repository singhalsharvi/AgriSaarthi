import os
import sys
import json
import math
from PIL import Image

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pth")
METADATA_PATH = os.path.join(BASE_DIR, "model", "metadata.json")

# Fallback for older model artifacts.  The checkpoint metadata is the source of
# truth and is loaded below so a future re-trained model cannot silently be
# decoded with the wrong label order.
DEFAULT_CLASSES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# Global instances for fast API warm-start
_model = None
_metadata = None


def load_metadata() -> dict:
    """Load and validate the training metadata shipped with the checkpoint."""
    global _metadata
    if _metadata is not None:
        return _metadata

    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as handle:
            metadata = json.load(handle)

    classes = metadata.get("classes", DEFAULT_CLASSES)
    if not isinstance(classes, list) or not classes or not all(isinstance(item, str) for item in classes):
        raise ValueError("Disease model metadata has an invalid 'classes' list.")

    preprocessing = metadata.get("preprocessing", {})
    image_size = preprocessing.get("image_size", [128, 128])
    normalization = preprocessing.get("normalization", {})
    mean = normalization.get("mean", [0.485, 0.456, 0.406])
    std = normalization.get("std", [0.229, 0.224, 0.225])
    if len(image_size) != 2 or len(mean) != 3 or len(std) != 3:
        raise ValueError("Disease model metadata has invalid preprocessing settings.")

    _metadata = {
        "classes": classes,
        "image_size": tuple(int(value) for value in image_size),
        "mean": [float(value) for value in mean],
        "std": [float(value) for value in std],
    }
    return _metadata


def build_inference_transform(metadata: dict):
    from torchvision import transforms
    return transforms.Compose([
        transforms.Resize(metadata["image_size"]),
        transforms.ToTensor(),
        transforms.Normalize(mean=metadata["mean"], std=metadata["std"]),
    ])

def load_model():
    """Loads and caches the trained PyTorch MobileNetV2 model."""
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model checkpoint not found at: {MODEL_PATH}")

    metadata = load_metadata()
    num_classes = len(metadata["classes"])

    import torch
    import torch.nn as nn
    import torchvision.models as models

    # Rebuild MobileNetV2 architecture
    try:
        model = models.mobilenet_v2(weights=None)
    except Exception:
        model = models.mobilenet_v2()

    num_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Linear(num_features, 128),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(128, num_classes)
    )

    # Load weights
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()

    _model = model
    return _model


def parse_class_name(class_name: str):
    """Parses raw dataset class name (e.g. Pepper__bell___Bacterial_spot)

    into clean Crop and Disease names.
    """
    if "___" in class_name:
        crop_raw, disease_raw = class_name.split("___", 1)
    else:
        # PlantVillage uses both Tomato_Early_blight and Tomato__Target_Spot.
        # Split only at the crop boundary, then trim the separator run.
        if "_" in class_name:
            crop_raw, disease_raw = class_name.split("_", 1)
            disease_raw = disease_raw.lstrip("_")
        else:
            crop_raw = class_name
            disease_raw = "healthy"

    crop = " ".join(crop_raw.replace("_", " ").split()).title()
    disease = " ".join(disease_raw.replace("_", " ").split()).title()

    # Special cleanups
    if crop == "Pepper Bell":
        crop = "Pepper bell"
    if "Yellowleaf" in disease:
        disease = "Tomato Yellow Leaf Curl Virus"
    if "Mosaic" in disease:
        disease = "Tomato Mosaic Virus"
    if "Spider Mites" in disease:
        disease = "Spider Mites (Two-spotted Spider Mite)"

    return crop, disease


def predict_disease(image_pil: Image.Image) -> dict:
    """Takes a PIL Image and runs inference using the MobileNetV2 CNN model.

    Returns:
        Dict containing top predictions and probabilities.
    """
    if not isinstance(image_pil, Image.Image):
        raise TypeError("A decoded PIL image is required for disease prediction.")
    if image_pil.width < 64 or image_pil.height < 64:
        raise ValueError("Image is too small. Upload a clear leaf photo at least 64×64 pixels.")

    import torch

    model = load_model()
    metadata = load_metadata()

    # Ensure RGB format
    if image_pil.mode != "RGB":
        image_pil = image_pil.convert("RGB")

    # Preprocess image
    tensor_img = build_inference_transform(metadata)(image_pil).unsqueeze(0)

    with torch.no_grad():
        outputs = model(tensor_img)
        probs = torch.softmax(outputs, dim=1).squeeze(0)

    # Get top 3 predictions
    top_probs, top_indices = probs.topk(3)

    top_3_predictions = []
    for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
        cls_name = metadata["classes"][idx]
        crp, dis = parse_class_name(cls_name)
        top_3_predictions.append({
            "class_name": cls_name,
            "crop": crp,
            "disease": dis,
            "confidence": round(prob, 4)
        })

    # Expose entropy for diagnostics. A softmax classifier is forced to choose
    # one of its trained classes even for an unsupported crop, so its top label
    # alone must not be treated as a diagnosis.
    entropy = -sum(float(prob) * math.log(float(prob) + 1e-12) for prob in probs.tolist())
    normalized_entropy = entropy / math.log(len(metadata["classes"]))
    confidence_margin = float(top_probs[0].item() - top_probs[1].item()) if len(top_probs) > 1 else float(top_probs[0].item())

    return {
        "top_3_predictions": top_3_predictions,
        "raw_probabilities": probs.tolist(),
        "normalized_entropy": round(normalized_entropy, 4),
        "confidence_margin": round(confidence_margin, 4),
        "supported_classes": metadata["classes"],
    }
