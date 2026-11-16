import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

project_root = Path(__file__).resolve().parents[1]
data_path = project_root / "data" / "processed" / "database_activity_processed.csv"
df = pd.read_csv(data_path)
feature_columns = [
    "login_hour",
    "login_failures",
    "queries_per_hour",
    "select_count",
    "insert_count",
    "update_count",
    "delete_count",
    "distinct_tables",
    "after_hours_login",
    "access_denied_count",
    "session_duration"
]
missing = set(feature_columns + ["anomaly_label"]) - set(df.columns)
if missing:
    raise ValueError(f"Missing dataset columns: {missing}")
X = df[feature_columns]
y = df["anomaly_label"]
print("Dataset loaded:", df.shape)
print("Features:", X.shape)
print("Labels:", y.shape)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

X_train_normal = X_train[y_train == 0]

print("\nTraining records:", len(X_train_normal))
print("Testing records:", len(X_test))
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X_train_normal)

print("\nModel training completed!")
predictions = model.predict(X_test)
y_pred = [1 if p == -1 else 0 for p in predictions]

print("\n========== MODEL EVALUATION ==========")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall:", recall_score(y_test, y_pred, zero_division=0))
print("F1 Score:", f1_score(y_test, y_pred, zero_division=0))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=["Normal", "Anomaly"],
    zero_division=0
))

model_dir = project_root / "ml_model"
model_dir.mkdir(exist_ok=True)
model_path = model_dir / "isolation_forest_model.pkl"
joblib.dump(model, model_path)
print("\nTrained model saved at:", model_path)
