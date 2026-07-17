"""
Export stress model from Student_Stress data to joblib format.
This matches the CatBoost approach used in the notebook.
"""

import os
import sys
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'Student_Stress', 'StressLevelDataset.csv')
SAVE_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(SAVE_DIR, exist_ok=True)

print("Loading data...")
df = pd.read_csv(DATA_PATH)

X = df.drop('stress_level', axis=1)
y = df['stress_level']

print(f"Dataset shape: {X.shape}")
print(f"Target distribution: {y.value_counts().to_dict()}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)

print("Training CatBoost model...")
model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    loss_function='MultiClass',
    eval_metric='TotalF1',
    random_seed=42,
    verbose=False,
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {accuracy:.4f}")
print(classification_report(y_test, y_pred, target_names=['Low', 'Medium', 'High']))

print("Exporting model...")
joblib.dump(model, os.path.join(SAVE_DIR, 'stress_model.pkl'))
joblib.dump(list(X.columns), os.path.join(SAVE_DIR, 'stress_features.pkl'))

print(f"Model saved to: {SAVE_DIR}/stress_model.pkl")
print(f"Features saved to: {SAVE_DIR}/stress_features.pkl")