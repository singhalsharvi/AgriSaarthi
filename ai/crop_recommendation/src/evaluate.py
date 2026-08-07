import os
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def evaluate_models(trained_results, X_test, y_test, label_encoder, output_dir="ai/crop_recommendation/reports"):
    """
    Evaluates all trained models on the holdout test set.
    Calculates Accuracy, Precision, Recall, F1 Score, Latency, Confusion Matrix, Classification Report.
    Generates comparison report and automatically selects the best model.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "plots"), exist_ok=True)

    metrics_list = []
    classification_reports = {}
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None

    class_names = label_encoder.classes_.tolist()

    for model_name, res in trained_results.items():
        model = res['model']

        # Measure prediction latency
        t0 = time.time()
        y_pred = model.predict(X_test)
        pred_time_total = time.time() - t0
        latency_ms = (pred_time_total / len(X_test)) * 1000.0

        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
        prec_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
        rec_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
        f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        clf_rep = classification_report(y_test, y_pred, target_names=class_names, output_dict=True, zero_division=0)
        classification_reports[model_name] = clf_rep

        row = {
            "Model": model_name,
            "Accuracy": round(acc, 4),
            "Precision (Macro)": round(prec_macro, 4),
            "Precision (Weighted)": round(prec_weighted, 4),
            "Recall (Macro)": round(rec_macro, 4),
            "Recall (Weighted)": round(rec_weighted, 4),
            "F1 Score (Macro)": round(f1_macro, 4),
            "F1 Score (Weighted)": round(f1_weighted, 4),
            "CV Mean F1": round(res['cv_mean'], 4),
            "CV Std F1": round(res['cv_std'], 4),
            "Training Time (s)": round(res['fit_time'], 4),
            "Prediction Latency (ms/sample)": round(latency_ms, 4)
        }
        metrics_list.append(row)

        if f1_weighted > best_f1:
            best_f1 = f1_weighted
            best_model_name = model_name
            best_model_obj = model

    comparison_df = pd.DataFrame(metrics_list).sort_values(by="F1 Score (Weighted)", ascending=False)
    csv_report_path = os.path.join(output_dir, "model_comparison_report.csv")
    comparison_df.to_csv(csv_report_path, index=False)

    clf_rep_path = os.path.join(output_dir, "classification_reports.json")
    with open(clf_rep_path, 'w') as f:
        json.dump(classification_reports, f, indent=2)

    # Plot Confusion Matrix for Best Model
    best_pred = best_model_obj.predict(X_test)
    cm = confusion_matrix(y_test, best_pred)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title(f"Confusion Matrix - Best Model ({best_model_name})", fontsize=14, fontweight='bold')
    plt.xlabel("Predicted Crop", fontsize=12)
    plt.ylabel("True Crop", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    cm_plot_path = os.path.join(output_dir, "plots", "confusion_matrix_best.png")
    plt.savefig(cm_plot_path, dpi=300)
    plt.close()

    # Plot Model Comparison Bar Chart
    plt.figure(figsize=(12, 6))
    x_indices = np.arange(len(comparison_df))
    plt.bar(x_indices - 0.2, comparison_df['F1 Score (Weighted)'], width=0.4, label='Holdout Test F1', color='#2b5c8f')
    plt.bar(x_indices + 0.2, comparison_df['CV Mean F1'], width=0.4, label='5-Fold CV Mean F1', color='#4ba3e3')
    plt.xticks(x_indices, comparison_df['Model'], rotation=15, ha='right', fontsize=11)
    plt.ylabel("F1 Score", fontsize=12)
    plt.title("Model Performance Comparison (F1 Score & Cross-Validation)", fontsize=14, fontweight='bold')
    plt.ylim(0.85, 1.02)
    plt.legend(fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    comp_plot_path = os.path.join(output_dir, "plots", "model_comparison.png")
    plt.savefig(comp_plot_path, dpi=300)
    plt.close()

    explanation = (
        f"The best performing model is '{best_model_name}' achieving a Weighted F1-Score of {best_f1:.4f} "
        f"on the holdout test set and a 5-Fold Cross-Validation score of {trained_results[best_model_name]['cv_mean']:.4f} "
        f"(±{trained_results[best_model_name]['cv_std']:.4f}). "
        f"It balances strong multi-class decision boundaries with low prediction latency "
        f"({comparison_df.loc[comparison_df['Model']==best_model_name, 'Prediction Latency (ms/sample)'].values[0]:.4f} ms/sample), "
        f"making it ideal for production FastAPI serving."
    )

    return {
        "best_model_name": best_model_name,
        "best_model_obj": best_model_obj,
        "best_f1": best_f1,
        "comparison_df": comparison_df,
        "explanation": explanation
    }

def generate_eda_visualizations(df: pd.DataFrame, output_dir="ai/crop_recommendation/reports/plots"):
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")

    num_cols = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']

    # 1. Feature Distributions
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    axes = axes.flatten()
    for idx, col in enumerate(num_cols):
        sns.histplot(df[col], kde=True, ax=axes[idx], color='#2b5c8f')
        axes[idx].set_title(f"Distribution of {col}", fontsize=11, fontweight='bold')
    # Remove unused subplots
    for idx in range(len(num_cols), len(axes)):
        fig.delaxes(axes[idx])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "feature_distributions.png"), dpi=300)
    plt.close()

    # 2. Correlation Matrix
    plt.figure(figsize=(10, 8))
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
    plt.title("Correlation Matrix of Soil & Environmental Features", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_matrix.png"), dpi=300)
    plt.close()

    # 3. Class Distribution
    plt.figure(figsize=(14, 6))
    order = df['Crop'].value_counts().index
    sns.countplot(data=df, x='Crop', order=order, palette='viridis')
    plt.title("Target Crop Class Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Crop Label", fontsize=12)
    plt.ylabel("Sample Count", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "class_distribution.png"), dpi=300)
    plt.close()
