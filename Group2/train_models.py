"""
Training script to export all models for the Student Guidance Dashboard.
Run this script from the Web directory: python train_models.py
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor, CatBoostClassifier
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(MODELS_DIR, exist_ok=True)

def train_career_model():
    """Train and export career prediction model."""
    print("\n" + "="*60)
    print("TRAINING CAREER MODEL")
    print("="*60)

    data_path = os.path.join(PARENT_DIR, 'Student_Carrer', 'career_data.csv')
    df = pd.read_csv(data_path)

    feature_cols = [
        'Math_Score', 'Science_Score', 'Programming_Skill', 'Communication_Skill',
        'Logical_Ability', 'R_score', 'I_score', 'A_score', 'S_score', 'E_score', 'C_score'
    ]

    X = df[feature_cols].values
    y = df['Career'].values

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_scaled, y_encoded)

    joblib.dump(model, os.path.join(MODELS_DIR, 'career_model.pkl'))
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'career_scaler.pkl'))
    joblib.dump(le, os.path.join(MODELS_DIR, 'career_label_encoder.pkl'))

    accuracy = model.score(scaler.transform(X), y_encoded)
    print(f"Training accuracy: {accuracy:.4f}")
    print(f"Model saved to: {MODELS_DIR}/career_model.pkl")
    print(f"Scaler saved to: {MODELS_DIR}/career_scaler.pkl")
    print(f"Label encoder saved to: {MODELS_DIR}/career_label_encoder.pkl")

    return model, scaler, le

def train_performance_model():
    """Train and export student performance prediction model."""
    print("\n" + "="*60)
    print("TRAINING PERFORMANCE MODEL")
    print("="*60)

    data_path = os.path.join(PARENT_DIR, 'Student_performance', 'data_final.csv')
    df = pd.read_csv(data_path)

    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    grade_cols = ['G1', 'G2', 'G3']
    target_col = 'G3'

    X = df.drop(columns=grade_cols)
    y = df[target_col]

    feature_cols = list(X.columns)
    print(f"Number of features: {len(feature_cols)}")
    print(f"Features: {feature_cols[:10]}... (first 10)")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = CatBoostRegressor(
        iterations=500,
        learning_rate=0.03,
        depth=4,
        l2_leaf_reg=3,
        random_seed=42,
        verbose=False
    )
    model.fit(X_scaled, y)

    predictions = model.predict(X_scaled)
    mse = np.mean((predictions - y) ** 2)
    print(f"MSE on training data: {mse:.4f}")

    joblib.dump(model, os.path.join(MODELS_DIR, 'performance_model.pkl'))
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'performance_scaler.pkl'))

    print(f"Model saved to: {MODELS_DIR}/performance_model.pkl")
    print(f"Scaler saved to: {MODELS_DIR}/performance_scaler.pkl")

    return model, scaler

def train_stress_model():
    """Train and export stress level prediction model."""
    print("\n" + "="*60)
    print("TRAINING STRESS MODEL")
    print("="*60)

    data_path = os.path.join(PARENT_DIR, 'Student_Stress', 'StressLevelDataset.csv')
    df = pd.read_csv(data_path)

    X = df.drop('stress_level', axis=1)
    y = df['stress_level']

    feature_cols = list(X.columns)
    print(f"Number of features: {len(feature_cols)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42, stratify=y
    )

    model = CatBoostClassifier(
        iterations=500,
        learning_rate=0.05,
        depth=6,
        loss_function='MultiClass',
        eval_metric='TotalF1',
        random_seed=42,
        verbose=False
    )
    model.fit(X_train, y_train)

    from sklearn.metrics import accuracy_score, classification_report
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred, target_names=['Low', 'Medium', 'High']))

    model.fit(X, y)

    joblib.dump(model, os.path.join(MODELS_DIR, 'stress_model.pkl'))
    joblib.dump(feature_cols, os.path.join(MODELS_DIR, 'stress_features.pkl'))

    print(f"Model saved to: {MODELS_DIR}/stress_model.pkl")
    print(f"Feature list saved to: {MODELS_DIR}/stress_features.pkl")

    return model, feature_cols

def main():
    print("="*60)
    print("STUDENT GUIDANCE DASHBOARD - MODEL TRAINING")
    print("="*60)
    print("\nModels will be saved to: {}".format(MODELS_DIR))

    try:
        train_career_model()
    except Exception as e:
        print(f"Error training career model: {e}")

    try:
        train_performance_model()
    except Exception as e:
        print(f"Error training performance model: {e}")

    try:
        train_stress_model()
    except Exception as e:
        print(f"Error training stress model: {e}")

    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)

    files = os.listdir(MODELS_DIR)
    print(f"\nModels in {MODELS_DIR}:")
    for f in sorted(files):
        size = os.path.getsize(os.path.join(MODELS_DIR, f))
        print(f"  {f}: {size:,} bytes")

if __name__ == '__main__':
    main()