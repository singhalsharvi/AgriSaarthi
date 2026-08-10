import torch
import torch.nn as nn
from torchvision import models

class PlantDiseaseClassifier(nn.Module):
    """
    Transfer Learning Plant Disease Classifier based on Pretrained EfficientNetV2.
    """
    def __init__(self, num_classes, freeze_backbone=True):
        super(PlantDiseaseClassifier, self).__init__()
        
        # Pretrained backbone
        weights = models.EfficientNet_V2_S_Weights.DEFAULT
        self.backbone = models.efficientnet_v2_s(weights=weights)
        
        # Get in_features from original classifier
        in_features = self.backbone.classifier[1].in_features
        
        # Custom Classification Head
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.4, inplace=True),
            nn.Linear(in_features, 256),
            nn.BatchNorm1d(256),
            nn.SiLU(inplace=True),
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(256, num_classes)
        )
        
        if freeze_backbone:
            self.freeze_backbone()

    def freeze_backbone(self):
        """Phase 1: Freeze backbone feature extraction layers."""
        for param in self.backbone.features.parameters():
            param.requires_grad = False
        print("[Model] Phase 1: Base EfficientNetV2 backbone parameters frozen.")

    def unfreeze_upper_layers(self, unfreeze_blocks=3):
        """Phase 2: Unfreeze top N feature blocks for fine-tuning."""
        # Unfreeze all backbone features parameters
        for param in self.backbone.features.parameters():
            param.requires_grad = False
            
        # Unfreeze top feature blocks (last blocks)
        for block in list(self.backbone.features)[-unfreeze_blocks:]:
            for param in block.parameters():
                param.requires_grad = True
                
        print(f"[Model] Phase 2: Unfrozen top {unfreeze_blocks} backbone blocks for fine-tuning.")

    def forward(self, x):
        return self.backbone(x)

def save_model_artifact(model, filepath="plant_disease_model.keras"):
    """Saves best model state dict to disk."""
    torch.save(model.state_dict(), filepath)
    print(f"[Model] Saved best model weights to '{filepath}'.")

def load_model_artifact(model, filepath="plant_disease_model.keras", device="cpu"):
    """Loads best model state dict from disk."""
    model.load_state_dict(torch.load(filepath, map_location=device, weights_only=True))
    model.to(device)
    print(f"[Model] Loaded model weights from '{filepath}'.")
    return model
