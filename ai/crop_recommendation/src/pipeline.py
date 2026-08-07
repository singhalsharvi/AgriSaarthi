import os
import joblib
import json
import pandas as pd
from ai.crop_recommendation.src.preprocess import (
    prepare_preprocessed_data,
    save_preprocessing_artifacts
)
from ai.crop_recommendation.src.train import train_and_tune_all_models
from ai.crop_recommendation.src.evaluate import (
    evaluate_models,
    generate_eda_visualizations
)
from ai.crop_recommendation.src.explain import analyze_explainability_and_diagnostics

def run_full_pipeline(
    data_path="ai/crop_recommendation/data/Crop_recommendation.csv",
    models_dir="ai/crop_recommendation/models",
    reports_dir="ai/crop_recommendation/reports",
    optuna_trials=15,
    random_state=42
):
    """
    Executes the complete production ML training, tuning, evaluation, explainability,
    and artifact export pipeline.
    """
    print("=" * 80)
    print("STARTING CROP RECOMMENDATION ML PRODUCTION PIPELINE")
    print("=" * 80)

    # 1. Load Raw Dataset & Generate EDA Visualizations
    raw_df = pd.read_csv(data_path)
    print(f"\n[STEP 1/6] Loaded raw dataset with shape: {raw_df.shape}")
    generate_eda_visualizations(raw_df, output_dir=os.path.join(reports_dir, "plots"))
    print("[OK] EDA visualizations generated successfully.")

    # 2. Data Preprocessing & Leakage Prevention
    print("\n[STEP 2/6] Running data preprocessing & train/test split...")
    prep_data = prepare_preprocessed_data(data_path, test_size=0.2, random_state=random_state)
    summary_info = prep_data["summary_info"]
    print(f"[OK] Deduplicated rows: {summary_info['clean_rows']} (Removed {summary_info['duplicates_removed']} duplicates)")
    print(f"[OK] Feature Evaluation for Variety: {summary_info['variety_eval']['justification']}")

    # 3. Save Preprocessing & Label Encoder Artifacts
    pipe_path, le_path = save_preprocessing_artifacts(
        prep_data["preprocessor"], prep_data["label_encoder"], output_dir=models_dir
    )
    print(f"[OK] Saved preprocessing pipeline -> {pipe_path}")
    print(f"[OK] Saved label encoder -> {le_path}")

    # 4. Model Training & Optuna Tuning
    print(f"\n[STEP 3/6] Tuning 6 Models using Optuna & 5-Fold Stratified Cross Validation...")
    X_train = prep_data["X_train"]
    y_train = prep_data["y_train"]
    X_test = prep_data["X_test"]
    y_test = prep_data["y_test"]
    num_classes = summary_info["num_classes"]

    trained_results = train_and_tune_all_models(
        X_train, y_train, num_classes=num_classes, n_trials=optuna_trials, random_state=random_state
    )

    # 5. Model Evaluation & Best Model Selection
    print("\n[STEP 4/6] Evaluating all models on Holdout Test Set...")
    eval_results = evaluate_models(
        trained_results, X_test, y_test, prep_data["label_encoder"], output_dir=reports_dir
    )

    best_model_name = eval_results["best_model_name"]
    best_model_obj = eval_results["best_model_obj"]
    print(f"\n[BEST MODEL SELECTED]: {best_model_name} (Holdout F1: {eval_results['best_f1']:.4f})")
    print(f"Explanation: {eval_results['explanation']}")

    # Save Best Model Artifact
    best_model_path = os.path.join(models_dir, "best_model.pkl")
    joblib.dump(best_model_obj, best_model_path)
    print(f"[OK] Saved best model artifact -> {best_model_path}")

    # 6. Model Explainability & Overfitting Diagnostics
    print("\n[STEP 5/6] Generating Model Explainability & Overfitting Diagnostics...")
    feature_names = prep_data["preprocessor"].feature_names_out
    diagnostics, feat_imp, perm_imp = analyze_explainability_and_diagnostics(
        best_model_obj, X_train, y_train, X_test, y_test, feature_names, output_dir=reports_dir
    )
    print(f"[OK] Diagnostic fit status: {diagnostics['fit_status']}")
    print(f"[OK] Train F1: {diagnostics['train_f1_score']} | Test F1: {diagnostics['test_f1_score']} | Gap: {diagnostics['train_test_gap']}")

    # 7. Summary Log Export
    print("\n[STEP 6/6] Writing pipeline execution summary report...")
    summary_report = {
        "dataset_info": summary_info,
        "best_model": best_model_name,
        "best_holdout_f1": eval_results["best_f1"],
        "selection_explanation": eval_results["explanation"],
        "diagnostics": diagnostics,
        "model_comparison": eval_results["comparison_df"].to_dict(orient="records")
    }

    summary_file = os.path.join(reports_dir, "pipeline_execution_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary_report, f, indent=2)

    print(f"[OK] Saved pipeline summary -> {summary_file}")
    print("\n" + "=" * 80)
    print("SUCCESS: CROP RECOMMENDATION TRAINING PIPELINE COMPLETED!")
    print("=" * 80)

    return summary_report

if __name__ == "__main__":
    run_full_pipeline()
