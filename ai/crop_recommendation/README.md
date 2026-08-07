# Smart Farming Crop Recommendation Machine Learning System

A production-grade, multiclass Crop Recommendation Machine Learning pipeline engineered for high-precision agricultural advisory systems. Built with Optuna hyperparameter optimization, 5-Fold Stratified Cross-Validation, SHAP interpretability, and robust leakage-free preprocessing.

Designed for seamless integration into a FastAPI backend with future Weather API, Soil Knowledge Base, RAG, and Gemini LLM integration.

---

## 📁 Repository & Project Architecture

```
ai/
└── crop_recommendation/
    ├── data/
    │   └── Crop_recommendation.csv        # Preprocessed agricultural dataset
    ├── notebooks/
    │   └── exploratory_data_analysis.ipynb # EDA summary and visualization notebook
    ├── src/
    │   ├── __init__.py
    │   ├── preprocess.py                 # Feature cleaning, Variety evaluation & pipeline transformer
    │   ├── train.py                      # Optuna hyperparameter tuning across 6 algorithms
    │   ├── evaluate.py                   # Metrics calculation & plot generation
    │   ├── explain.py                    # Feature importance & SHAP diagnostics
    │   └── pipeline.py                   # End-to-end training orchestrator
    ├── models/
    │   ├── best_model.pkl                # Exported best-performing model artifact
    │   ├── preprocessing_pipeline.pkl    # Exported Feature Scaler & OneHotEncoder
    │   └── label_encoder.pkl             # Exported target LabelEncoder
    ├── reports/
    │   ├── model_comparison_report.csv   # Comprehensive benchmark comparison report
    │   ├── classification_reports.json   # Full precision/recall per class breakdown
    │   ├── explainability_diagnostics.json# Fit status, train/test gap & recommendations
    │   └── plots/
    │       ├── correlation_matrix.png     # Feature correlation heatmap
    │       ├── feature_distributions.png  # KDE distribution histograms
    │       ├── class_distribution.png     # Target sample count per crop
    │       ├── confusion_matrix_best.png  # Multi-class confusion matrix
    │       ├── model_comparison.png       # Holdout F1 vs 5-Fold CV F1 comparison bar chart
    │       ├── feature_importance.png     # Gini/Gain feature importance bar chart
    │       └── shap_summary.png           # Multi-class SHAP feature impact plot
    ├── main.py                           # Training execution entrypoint
    ├── prediction.py                     # Production inference API module
    ├── requirements.txt                  # Python dependencies
    └── README.md                         # Technical documentation
```

---

## 📊 Dataset & Features

- **Target Label**: `Crop` (22 unique crop categories: *rice, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee*)
- **Input Features**:
  1. `Nitrogen`: Soil Nitrogen ratio (N)
  2. `Phosphorus`: Soil Phosphorus ratio (P)
  3. `Potassium`: Soil Potassium ratio (K)
  4. `Temperature`: Ambient temperature (°C)
  5. `Humidity`: Relative humidity (%)
  6. `pH_Value`: Soil pH level (0 - 14)
  7. `Rainfall`: Rainfall level (mm)
  8. `Soil_Type`: Soil category (*Clay, Loam, Sandy, Black, Alluvial, Laterite, etc.*)
  9. `Variety`: Evaluated & dropped due to zero variance (constant feature carrying 0 bits of information).

---

## 🤖 Models Trained & Evaluated

1. **XGBoost** (`XGBClassifier`)
2. **CatBoost** (`CatBoostClassifier`)
3. **LightGBM** (`LGBMClassifier`)
4. **Random Forest** (`RandomForestClassifier`)
5. **Extra Trees** (`ExtraTreesClassifier`)
6. **HistGradientBoostingClassifier**

### Optimization & Evaluation Setup
- **Hyperparameter Optimization**: Optuna (TPE Sampler)
- **Validation Scheme**: 5-Fold Stratified Cross Validation
- **Holdout Test Split**: 20% Stratified Split
- **Metrics Evaluated**: Accuracy, Precision (Macro/Weighted), Recall (Macro/Weighted), F1-Score (Macro/Weighted), 5-Fold CV Mean & Std Dev, Training Time, Latency (ms/sample).

---

## 🚀 Quickstart & Training

### 1. Installation
```bash
pip install -r ai/crop_recommendation/requirements.txt
```

### 2. Run Full Training & Evaluation Pipeline
```bash
python ai/crop_recommendation/main.py
```

---

## 💡 Production Inference API (`prediction.py`)

The inference function `predict_crop()` accepts individual parameters and returns the Top-3 crop recommendations along with confidence scores and class probability vector.

### Code Example:
```python
from ai.crop_recommendation.prediction import predict_crop

result = predict_crop(
    Nitrogen=90,
    Phosphorus=42,
    Potassium=43,
    Temperature=20.87,
    Humidity=82.0,
    pH_Value=6.5,
    Rainfall=202.93,
    Soil_Type="Clay"
)

print(result["top_3_predictions"])
# Output:
# [
#   {"crop": "rice", "confidence_score": 0.9852, "probability": 0.9852},
#   {"crop": "jute", "confidence_score": 0.0114, "probability": 0.0114},
#   {"crop": "papaya", "confidence_score": 0.0021, "probability": 0.0021}
# ]
```

---

## 📄 License & Attribution
Developed for the Smart Farming AI System project.
