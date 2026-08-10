import os
import sys
import torch
import torch.nn as nn
import numpy as np
from src.dataset import load_and_clean_dataset, build_data_loaders
from src.model import PlantDiseaseClassifier, save_model_artifact, load_model_artifact
from src.utils import get_class_weights_tensor, save_class_mapping, evaluate_and_report

class EarlyStopping:
    """Early Stopping and Model Checkpoint Manager."""
    def __init__(self, patience=5, min_delta=1e-4, filepath="plant_disease_model.keras"):
        self.patience = patience
        self.min_delta = min_delta
        self.filepath = filepath
        self.best_loss = float('inf')
        self.counter = 0
        self.early_stop = False

    def check(self, val_loss, model):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            save_model_artifact(model, self.filepath)
            return True
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
            return False

class ReduceLROnPlateau:
    """Learning Rate Scheduler on Plateau."""
    def __init__(self, optimizer, factor=0.5, patience=3, min_lr=1e-6):
        self.optimizer = optimizer
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        self.best_loss = float('inf')
        self.counter = 0

    def step(self, val_loss):
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.counter = 0
                for param_group in self.optimizer.param_groups:
                    old_lr = param_group['lr']
                    new_lr = max(old_lr * self.factor, self.min_lr)
                    param_group['lr'] = new_lr
                    print(f" -> [LR Scheduler] Reducing learning rate: {old_lr:.2e} -> {new_lr:.2e}")

def run_epoch(model, dataloader, criterion, optimizer=None, device='cpu', is_training=False):
    if is_training:
        model.train()
    else:
        model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.set_grad_enabled(is_training):
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.to(device)

            if is_training:
                optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)

            if is_training:
                loss.backward()
                optimizer.step()

            running_loss += loss.item() * images.size(0)
            preds = torch.argmax(outputs, dim=1)
            correct += torch.sum(preds == labels).item()
            total += labels.size(0)

    epoch_loss = running_loss / total if total > 0 else 0.0
    epoch_acc = correct / total if total > 0 else 0.0
    return epoch_loss, epoch_acc

def main():
    print("="*80)
    print("      PLANTDOC DISEASE IMAGE CLASSIFICATION - MODEL TRAINING PIPELINE")
    print("="*80)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[Hardware] Using Compute Device: {device}")

    # 1. Load Dataset, Clean Data Leakage, Stratified Train/Val Split
    dataset_dir = "PlantDoc-Dataset"
    train_data, val_data, test_data, class_names, class_to_idx = load_and_clean_dataset(
        data_dir=dataset_dir, 
        val_split=0.15
    )
    
    num_classes = len(class_names)
    print(f"\n[Config] Total Agricultural Classes: {num_classes}")

    # 2. Save Class Index Mapping JSON
    save_class_mapping(class_names, output_path="class_indices.json")

    # 3. Compute Class Weights to balance loss function across sparse classes
    train_paths, train_labels = train_data
    val_paths, val_labels = val_data
    test_paths, test_labels = test_data

    class_weights_tensor = get_class_weights_tensor(train_labels, num_classes, device=device)
    print(f"[Class Weights] Computed balanced class weights for {num_classes} classes.")

    # 4. Build DataLoaders
    train_loader, val_loader, test_loader = build_data_loaders(train_data, val_data, test_data, batch_size=32)

    # 5. Build Model Architecture (Phase 1: Backbone Frozen)
    model = PlantDiseaseClassifier(num_classes=num_classes, freeze_backbone=True).to(device)
    
    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    
    model_filename = "plant_disease_model.keras"
    early_stopping = EarlyStopping(patience=5, filepath=model_filename)

    # --- PHASE 1: TRAIN CLASSIFICATION HEAD ---
    print("\n" + "-"*80)
    print("   STAGE 1: TRAINING CLASSIFICATION HEAD (BASE LAYERS FROZEN)")
    print("-"*80)
    
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3, weight_decay=1e-4)
    lr_scheduler = ReduceLROnPlateau(optimizer, factor=0.5, patience=3, min_lr=1e-6)

    phase1_epochs = 12
    last_train_acc, last_val_acc = 0.0, 0.0

    for epoch in range(1, phase1_epochs + 1):
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer, device, is_training=True)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, None, device, is_training=False)
        
        last_train_acc, last_val_acc = train_acc, val_acc
        print(f"Epoch {epoch:02d}/{phase1_epochs:02d} | Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.2f}%")
        
        lr_scheduler.step(val_loss)
        if early_stopping.check(val_loss, model):
            print(" -> [Checkpoint] Saved best model weights!")

    print(f"\n[Stage 1 Completed] Final Stage 1 Train Acc: {last_train_acc*100:.2f}%, Val Acc: {last_val_acc*100:.2f}%")

    # --- PHASE 2: FINE-TUNE UPPER LAYERS ---
    print("\n" + "-"*80)
    print("   STAGE 2: FINE-TUNING UPPER PRETRAINED LAYERS (FINE-TUNING)")
    print("-"*80)

    model.unfreeze_upper_layers(unfreeze_blocks=3)
    
    optimizer_ft = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-5, weight_decay=1e-4)
    lr_scheduler_ft = ReduceLROnPlateau(optimizer_ft, factor=0.5, patience=3, min_lr=1e-7)

    phase2_epochs = 15
    for epoch in range(1, phase2_epochs + 1):
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer_ft, device, is_training=True)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, None, device, is_training=False)
        
        last_train_acc, last_val_acc = train_acc, val_acc
        print(f"Epoch {epoch:02d}/{phase2_epochs:02d} | Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.2f}%")
        
        lr_scheduler_ft.step(val_loss)
        if early_stopping.check(val_loss, model):
            print(" -> [Checkpoint] Saved best fine-tuned model weights!")
        if early_stopping.early_stop:
            print(f" -> [EarlyStopping] Triggered at epoch {epoch}.")
            break

    print(f"\n[Stage 2 Completed] Final Fine-Tuning Train Acc: {last_train_acc*100:.2f}%, Val Acc: {last_val_acc*100:.2f}%")

    # Load best saved weights
    if os.path.exists(model_filename):
        print(f"\n[Model] Loading best saved model weights from '{model_filename}'...")
        model = load_model_artifact(model, filepath=model_filename, device=device)

    # 7. Evaluate on Test Dataset & Generate Comprehensive Report
    eval_results = evaluate_and_report(model, test_loader, class_names, device=device, output_cm_path="confusion_matrix.png")

    print("\n" + "="*80)
    print("                    FINAL MODEL METRICS SUMMARY")
    print("="*80)
    print(f"  * Training Accuracy:   {last_train_acc * 100:.2f}%")
    print(f"  * Validation Accuracy: {last_val_acc * 100:.2f}%")
    print(f"  * Test Accuracy:       {eval_results['test_acc'] * 100:.2f}%")
    print(f"  * Precision (Weighted):{eval_results['precision'] * 100:.2f}%")
    print(f"  * Recall (Weighted):   {eval_results['recall'] * 100:.2f}%")
    print(f"  * F1-Score (Weighted): {eval_results['f1_score'] * 100:.2f}%")
    print("="*80)
    print(f"\nModel artifact successfully saved as '{model_filename}'.")
    print("Label mapping saved as 'class_indices.json'.")

if __name__ == "__main__":
    main()
