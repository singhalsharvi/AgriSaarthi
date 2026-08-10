import json
import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, accuracy_score

def get_class_weights_tensor(labels, num_classes, device='cpu'):
    """
    Computes balanced class weights tensor to handle imbalanced plant disease image distributions.
    """
    classes = np.arange(num_classes)
    weights = compute_class_weight(class_weight='balanced', classes=classes, y=labels)
    weights_tensor = torch.tensor(weights, dtype=torch.float32).to(device)
    return weights_tensor

def save_class_mapping(class_names, output_path="class_indices.json"):
    """
    Saves class index to disease name mapping into a JSON file for inference.
    """
    mapping = {int(i): name for i, name in enumerate(class_names)}
    with open(output_path, "w") as f:
        json.dump(mapping, f, indent=4)
    print(f"[Utils] Saved class index mapping to '{output_path}'.")
    return mapping

def load_class_mapping(input_path="class_indices.json"):
    """Loads class index to disease name mapping JSON."""
    with open(input_path, "r") as f:
        data = json.load(f)
    return {int(k): v for k, v in data.items()}

def evaluate_and_report(model, test_loader, class_names, device='cpu', output_cm_path="confusion_matrix.png"):
    """
    Evaluates trained PyTorch model performance on test dataset and reports:
    - Test accuracy
    - Precision
    - Recall
    - F1-score
    - Confusion Matrix (plots and saves heatmaps)
    """
    print("\n" + "="*80)
    print("                      MODEL EVALUATION & METRICS REPORT")
    print("="*80)
    
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for images, targets in test_loader:
            images = images.to(device)
            outputs = model(images)
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(targets.numpy())

    y_true_test = np.array(all_targets)
    y_pred = np.array(all_preds)

    # Accuracy
    test_acc = accuracy_score(y_true_test, y_pred)
    
    # Weighted & Macro Precision, Recall, F1
    precision_w, recall_w, f1_w, _ = precision_recall_fscore_support(y_true_test, y_pred, average='weighted', zero_division=0)
    precision_m, recall_m, f1_m, _ = precision_recall_fscore_support(y_true_test, y_pred, average='macro', zero_division=0)

    print(f"\n--- OVERALL METRICS SUMMARY ---")
    print(f"Test Accuracy:         {test_acc * 100:.2f}%")
    print(f"Weighted Precision:    {precision_w * 100:.2f}%")
    print(f"Weighted Recall:       {recall_w * 100:.2f}%")
    print(f"Weighted F1-Score:     {f1_w * 100:.2f}%")
    print(f"Macro F1-Score:        {f1_m * 100:.2f}%")

    print("\n--- DETAILED PER-CLASS CLASSIFICATION REPORT ---")
    unique_present_classes = np.unique(np.concatenate([y_true_test, y_pred]))
    target_names = [class_names[i] for i in unique_present_classes]
    
    report_str = classification_report(
        y_true_test, 
        y_pred, 
        labels=unique_present_classes,
        target_names=target_names, 
        digits=4, 
        zero_division=0
    )
    print(report_str)

    # Confusion Matrix
    cm = confusion_matrix(y_true_test, y_pred, labels=np.arange(len(class_names)))
    
    # Plot Confusion Matrix
    plt.figure(figsize=(16, 14))
    sns.heatmap(cm, annot=False, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('PlantDoc Disease Classification - Confusion Matrix', fontsize=16, pad=15)
    plt.xlabel('Predicted Disease Class', fontsize=12)
    plt.ylabel('Actual Ground Truth Class', fontsize=12)
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.savefig(output_cm_path, dpi=300)
    plt.close()
    print(f"[Utils] Confusion matrix plot saved to '{output_cm_path}'.")

    return {
        "test_acc": test_acc,
        "precision": precision_w,
        "recall": recall_w,
        "f1_score": f1_w,
        "confusion_matrix": cm,
        "classification_report": report_str
    }
