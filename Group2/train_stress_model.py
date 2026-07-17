import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "Student_Stress", "StressLevelDataset.csv")
SAVE_DIR = os.path.join(os.path.dirname(__file__), "models")

df = pd.read_csv(DATA_PATH)
X = df.drop("stress_level", axis=1)
y = df["stress_level"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)

model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    loss_function="MultiClass",
    eval_metric="TotalF1",
    random_seed=42,
    verbose=False,
)
model.fit(X_train, y_train)

os.makedirs(SAVE_DIR, exist_ok=True)
joblib.dump(model, os.path.join(SAVE_DIR, "stress_model.pkl"))
joblib.dump(list(X.columns), os.path.join(SAVE_DIR, "stress_features.pkl"))

from sklearn.metrics import accuracy_score, classification_report
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=["Low", "Medium", "High"]))
print("Saved stress_model.pkl and stress_features.pkl")