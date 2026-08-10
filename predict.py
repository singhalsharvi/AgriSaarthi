import argparse
import json
import os
import sys
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from src.model import PlantDiseaseClassifier, load_model_artifact

IMG_SIZE = (224, 224)

def load_class_indices(json_path="class_indices.json"):
    """Loads class mapping from index to disease class name."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Class mapping file '{json_path}' not found. Please train model first.")
    with open(json_path, "r") as f:
        mapping = json.load(f)
    return {int(k): v for k, v in mapping.items()}

def get_inference_transform():
    """Returns torchvision preprocessing transforms for inference."""
    return transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def predict_leaf_disease(image_path, model_path="plant_disease_model.keras", json_path="class_indices.json"):
    """Predicts plant disease and confidence percentage for a given leaf image."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Leaf image not found at path: {image_path}")

    class_indices = load_class_indices(json_path)
    num_classes = len(class_indices)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Reconstruct model and load weights
    model = PlantDiseaseClassifier(num_classes=num_classes, freeze_backbone=False)
    model = load_model_artifact(model, filepath=model_path, device=device)
    model.eval()

    # Preprocess image
    image = Image.open(image_path).convert("RGB")
    transform = get_inference_transform()
    tensor_img = transform(image).unsqueeze(0).to(device) # Shape: (1, 3, 224, 224)

    # Inference
    with torch.no_grad():
        outputs = model(tensor_img)
        probs = F.softmax(outputs, dim=1).squeeze(0).cpu().numpy()

    top_idx = int(np.argmax(probs))
    predicted_disease = class_indices.get(top_idx, f"Unknown_Class_{top_idx}")
    confidence_pct = float(probs[top_idx] * 100.0)

    print("\n" + "="*60)
    print("                PLANT DISEASE PREDICTION RESULT")
    print("="*60)
    print(f"  * Input Image:        {os.path.basename(image_path)}")
    print(f"  * Predicted Disease:  {predicted_disease}")
    print(f"  * Confidence Level:   {confidence_pct:.2f}%")
    print("="*60)

    # Top 3 Candidate Predictions
    top_3_indices = np.argsort(probs)[-3:][::-1]
    print("\nTop 3 Candidate Diseases:")
    for rank, idx in enumerate(top_3_indices, start=1):
        disease_name = class_indices.get(int(idx), f"Class_{idx}")
        score = float(probs[idx] * 100.0)
        print(f"  {rank}. {disease_name:<42} ({score:.2f}%)")
    print("\n")

    return {
        "disease": predicted_disease,
        "confidence": confidence_pct,
        "probs": probs
    }

def main():
    import numpy as np
    parser = argparse.ArgumentParser(description="Predict Plant Disease from Leaf Image using Trained Model.")
    parser.add_argument("--image", "-i", type=str, help="Path to leaf image file.")
    args = parser.parse_args()

    image_path = args.image
    if not image_path:
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            image_path = sys.argv[1]
        else:
            image_path = input("Enter path to leaf image: ").strip().strip('"')

    try:
        predict_leaf_disease(image_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
