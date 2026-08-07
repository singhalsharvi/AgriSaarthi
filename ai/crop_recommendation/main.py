import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai.crop_recommendation.src.pipeline import run_full_pipeline

def main():
    print("Launching Crop Recommendation Production Training Pipeline...")
    run_full_pipeline(
        data_path="ai/crop_recommendation/data/Crop_recommendation.csv",
        models_dir="ai/crop_recommendation/models",
        reports_dir="ai/crop_recommendation/reports",
        optuna_trials=10,  # 10 trials per model for fast thorough optimization
        random_state=42
    )

if __name__ == "__main__":
    main()
