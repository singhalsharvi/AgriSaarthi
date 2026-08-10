import os
import sys
import json
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pth")
METADATA_PATH = os.path.join(BASE_DIR, "model", "metadata.json")

# Classes list in alphabetical order (as verified during evaluation)
CLASSES = [
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

# Normalization constants (ImageNet standards, 128x128 resolution)
IMG_SIZE = (128, 128)
INFERENCE_TRANSFORM = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Global instances for fast API warm-start
_model = None

def load_model():
    """Loads and caches the trained PyTorch MobileNetV2 model."""
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model checkpoint not found at: {MODEL_PATH}")

    num_classes = len(CLASSES)

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
        parts = class_name.split("_")
        if len(parts) >= 2:
            crop_raw = parts[0]
            disease_raw = "_".join(parts[1:])
        else:
            crop_raw = class_name
            disease_raw = "healthy"

    crop = crop_raw.replace("__", " ").replace("_", " ").title()
    disease = disease_raw.replace("_", " ").title()

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
    model = load_model()

    # Ensure RGB format
    if image_pil.mode != "RGB":
        image_pil = image_pil.convert("RGB")

    # Preprocess image
    tensor_img = INFERENCE_TRANSFORM(image_pil).unsqueeze(0) # Add batch dimension

    with torch.no_grad():
        outputs = model(tensor_img)
        probs = torch.softmax(outputs, dim=1).squeeze(0)

    # Get top 3 predictions
    top_probs, top_indices = probs.topk(3)

    top_3_predictions = []
    for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
        cls_name = CLASSES[idx]
        crp, dis = parse_class_name(cls_name)
        top_3_predictions.append({
            "class_name": cls_name,
            "crop": crp,
            "disease": dis,
            "confidence": round(prob, 4)
        })

    return {
        "top_3_predictions": top_3_predictions,
        "raw_probabilities": probs.tolist()
    }
