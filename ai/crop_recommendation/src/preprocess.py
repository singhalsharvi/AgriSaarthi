import os
import joblib
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

NUMERICAL_FEATURES = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']
CATEGORICAL_FEATURES = ['Soil_Type']
TARGET_COL = 'Crop'

class CropFeatureTransformer(BaseEstimator, TransformerMixin):
    """
    Custom transformer that handles feature selection (e.g. evaluating and dropping Variety),
    missing value imputation, and numerical/categorical preprocessing.
    """
    def __init__(self, remove_variety=True):
        self.remove_variety = remove_variety
        self.column_transformer = None
        self.feature_names_out = None

    def fit(self, X, y=None):
        X_copy = X.copy()
        if self.remove_variety and 'Variety' in X_copy.columns:
            X_copy = X_copy.drop(columns=['Variety'])

        num_cols = [c for c in NUMERICAL_FEATURES if c in X_copy.columns]
        cat_cols = [c for c in CATEGORICAL_FEATURES if c in X_copy.columns]

        num_pipeline = Pipeline([
            ('scaler', StandardScaler())
        ])

        cat_pipeline = Pipeline([
            ('onehot', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
        ])

        self.column_transformer = ColumnTransformer(
            transformers=[
                ('num', num_pipeline, num_cols),
                ('cat', cat_pipeline, cat_cols)
            ]
        )

        self.column_transformer.fit(X_copy, y)

        # Get feature names out
        cat_encoder = self.column_transformer.named_transformers_['cat'].named_steps['onehot']
        cat_encoded_names = cat_encoder.get_feature_names_out(cat_cols).tolist()
        self.feature_names_out = num_cols + cat_encoded_names
        return self

    def transform(self, X):
        X_copy = X.copy()
        if self.remove_variety and 'Variety' in X_copy.columns:
            X_copy = X_copy.drop(columns=['Variety'])
        
        transformed_arr = self.column_transformer.transform(X_copy)
        return pd.DataFrame(transformed_arr, columns=self.feature_names_out, index=X_copy.index)

def evaluate_variety_feature(df: pd.DataFrame) -> dict:
    """
    Evaluates the 'Variety' feature for variance, uniqueness, and predictive value.
    Returns statistical evaluation dictionary.
    """
    if 'Variety' not in df.columns:
        return {"status": "Not present", "keep": False, "justification": "Variety column not in dataset."}

    n_unique = df['Variety'].nunique()
    val_counts = df['Variety'].value_counts(normalize=True).to_dict()
    
    # Check variance / entropy
    if n_unique <= 1:
        justification = (
            f"Variety contains only {n_unique} unique value ({list(val_counts.keys())}). "
            "Zero variance feature carries 0 bits of mutual information for classification and must be dropped."
        )
        return {"n_unique": n_unique, "keep": False, "justification": justification, "val_counts": val_counts}
    
    top_freq = max(val_counts.values())
    if top_freq > 0.99:
        justification = (
            f"Variety is quasi-constant with top category taking {top_freq*100:.2f}% of samples. "
            "Near-zero variance feature contributes minimal signal and risks overfitting."
        )
        return {"n_unique": n_unique, "keep": False, "justification": justification, "val_counts": val_counts}

    return {"n_unique": n_unique, "keep": True, "justification": "Variety has sufficient variance across samples.", "val_counts": val_counts}

def prepare_preprocessed_data(data_path: str, test_size=0.2, random_state=42):
    """
    Loads raw CSV, cleans duplicates/missing values, evaluates Variety,
    splits into Stratified Train/Test sets without data leakage, fits preprocessing pipeline,
    and returns processed feature matrices & label encoder.
    """
    df = pd.read_csv(data_path)
    
    # 1. Deduplication
    initial_len = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    dedup_len = len(df)
    
    # 2. Missing value handling
    df = df.dropna().reset_index(drop=True)

    # 3. Variety evaluation
    variety_eval = evaluate_variety_feature(df)

    # 4. Target encoding
    label_encoder = LabelEncoder()
    df['Crop_encoded'] = label_encoder.fit_transform(df[TARGET_COL])

    X = df.drop(columns=[TARGET_COL, 'Crop_encoded'])
    y = df['Crop_encoded']

    # 5. Stratified Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # 6. Fit preprocessing pipeline on X_train only to prevent data leakage
    preprocessor = CropFeatureTransformer(remove_variety=not variety_eval.get('keep', False))
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    summary_info = {
        "initial_rows": initial_len,
        "clean_rows": len(df),
        "duplicates_removed": initial_len - dedup_len,
        "variety_eval": variety_eval,
        "classes": label_encoder.classes_.tolist(),
        "num_classes": len(label_encoder.classes_)
    }

    return {
        "X_train_raw": X_train,
        "X_test_raw": X_test,
        "X_train": X_train_processed,
        "X_test": X_test_processed,
        "y_train": y_train,
        "y_test": y_test,
        "preprocessor": preprocessor,
        "label_encoder": label_encoder,
        "summary_info": summary_info
    }

def save_preprocessing_artifacts(preprocessor, label_encoder, output_dir="ai/crop_recommendation/models"):
    os.makedirs(output_dir, exist_ok=True)
    pipe_path = os.path.join(output_dir, "preprocessing_pipeline.pkl")
    le_path = os.path.join(output_dir, "label_encoder.pkl")
    
    joblib.dump(preprocessor, pipe_path)
    joblib.dump(label_encoder, le_path)
    return pipe_path, le_path
