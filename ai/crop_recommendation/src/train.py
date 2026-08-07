import os
import time
import joblib
import numpy as np
import pandas as pd
import optuna
from optuna.samplers import TPESampler
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier

optuna.logging.set_verbosity(optuna.logging.WARNING)

def tune_random_forest(X, y, n_trials=10, random_state=42):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 5, 25),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 5),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy']),
            'random_state': random_state,
            'n_jobs': -1
        }
        model = RandomForestClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=-1)
        return scores.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=random_state))
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def tune_extra_trees(X, y, n_trials=10, random_state=42):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 5, 25),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 5),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy']),
            'random_state': random_state,
            'n_jobs': -1
        }
        model = ExtraTreesClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=-1)
        return scores.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=random_state))
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def tune_xgboost(X, y, num_classes, n_trials=10, random_state=42):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.03, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.7, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.7, 1.0),
            'objective': 'multi:softprob',
            'num_class': num_classes,
            'random_state': random_state,
            'n_jobs': 2,
            'verbosity': 0
        }
        model = XGBClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=2)
        return scores.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=random_state))
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def tune_lightgbm(X, y, n_trials=10, random_state=42):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'num_leaves': trial.suggest_int('num_leaves', 15, 63),
            'learning_rate': trial.suggest_float('learning_rate', 0.03, 0.3, log=True),
            'subsample': trial.suggest_float('subsample', 0.7, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.7, 1.0),
            'random_state': random_state,
            'n_jobs': 2,
            'verbose': -1,
            'verbosity': -1
        }
        model = LGBMClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=2)
        return scores.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=random_state))
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def tune_catboost(X, y, n_trials=8, random_state=42):
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 50, 150),
            'depth': trial.suggest_int('depth', 4, 8),
            'learning_rate': trial.suggest_float('learning_rate', 0.03, 0.3, log=True),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1e-2, 10.0, log=True),
            'random_seed': random_state,
            'verbose': 0,
            'allow_writing_files': False
        }
        model = CatBoostClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=-1)
        return scores.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=random_state))
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def tune_hist_gradient_boosting(X, y, n_trials=10, random_state=42):
    def objective(trial):
        params = {
            'max_iter': trial.suggest_int('max_iter', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.03, 0.3, log=True),
            'l2_regularization': trial.suggest_float('l2_regularization', 1e-4, 10.0, log=True),
            'random_state': random_state
        }
        model = HistGradientBoostingClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=-1)
        return scores.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=random_state))
    study.optimize(objective, n_trials=n_trials)
    return study.best_params


def train_and_tune_all_models(X_train, y_train, num_classes, n_trials=10, random_state=42):
    models_config = {
        'Random Forest': (tune_random_forest, RandomForestClassifier),
        'Extra Trees': (tune_extra_trees, ExtraTreesClassifier),
        'XGBoost': (lambda X, y, n_trials=10, random_state=42: tune_xgboost(X, y, num_classes, n_trials, random_state), XGBClassifier),
        'LightGBM': (tune_lightgbm, LGBMClassifier),
        'CatBoost': (tune_catboost, CatBoostClassifier),
        'HistGradientBoosting': (tune_hist_gradient_boosting, HistGradientBoostingClassifier)
    }

    trained_results = {}

    for model_name, (tuner_fn, model_class) in models_config.items():
        print(f"--- Tuning {model_name} with Optuna (5-Fold Stratified CV) ---", flush=True)
        t0 = time.time()
        best_params = tuner_fn(X_train, y_train, n_trials=n_trials, random_state=random_state)
        tuning_time = time.time() - t0

        final_params = best_params.copy()
        final_params['random_state'] = random_state
        if model_name in ['Random Forest', 'Extra Trees', 'LightGBM']:
            final_params['n_jobs'] = -1
        elif model_name == 'XGBoost':
            final_params['n_jobs'] = -1
            final_params['verbosity'] = 0
            final_params['objective'] = 'multi:softprob'
            final_params['num_class'] = num_classes
        elif model_name == 'CatBoost':
            final_params['verbose'] = 0
            final_params['thread_count'] = -1
            final_params['allow_writing_files'] = False
            if 'random_state' in final_params:
                final_params['random_seed'] = final_params.pop('random_state')
        elif model_name == 'HistGradientBoosting':
            if 'n_jobs' in final_params:
                del final_params['n_jobs']

        final_model = model_class(**final_params)
        fit_t0 = time.time()
        final_model.fit(X_train, y_train)
        fit_time = time.time() - fit_t0

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        cv_scores = cross_val_score(final_model, X_train, y_train, cv=cv, scoring='f1_weighted', n_jobs=-1)

        trained_results[model_name] = {
            'model': final_model,
            'best_params': best_params,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'fit_time': fit_time,
            'total_tuning_time': tuning_time
        }
        print(f"[OK] {model_name} Tuned | 5-Fold CV F1: {cv_scores.mean():.4f} (+/-{cv_scores.std():.4f}) | Fit Time: {fit_time:.2f}s", flush=True)

    return trained_results
