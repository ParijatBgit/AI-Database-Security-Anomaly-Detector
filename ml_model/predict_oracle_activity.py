import pandas as pd
import joblib
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
model_path = project_root / "ml_model" / "isolation_forest_model.pkl"
data_path = (
    project_root / "data" / "processed" /
    "oracle_activity_features.csv"
)
output_path = (
    project_root / "data" / "processed" /
    "oracle_prediction_results.csv"
)
model = joblib.load(model_path)
df = pd.read_csv(data_path)
print("Isolation Forest model loaded!")
print("Oracle activity records:", len(df))

expected_features = list(model.feature_names_in_)
missing_features = set(expected_features) - set(df.columns)
extra_features = set(df.columns) - set(expected_features)
if missing_features or extra_features:
    raise ValueError(
        f"Feature mismatch. Missing: {missing_features}, "
        f"Extra: {extra_features}"
    )

X = df[expected_features]

predictions = model.predict(X)
anomaly_scores = -model.decision_function(X)
results = df.copy()
results["predicted_label"] = [
    1 if prediction == -1 else 0
    for prediction in predictions
]
results["anomaly_score"] = anomaly_scores
results["detection_status"] = results[
    "predicted_label"
].map({
    0: "NORMAL",
    1: "ANOMALY"
})

print("\n========== ORACLE ACTIVITY PREDICTIONS ==========")
print(
    results[
        ["predicted_label", "anomaly_score", "detection_status"]
    ].to_string(index=False)
)
print("\n========== DETECTION SUMMARY ==========")
print("Total records:", len(results))
print(
    "Normal activities:",
    (results["predicted_label"] == 0).sum()
)
print(
    "Anomalies detected:",
    (results["predicted_label"] == 1).sum()
)

results.to_csv(output_path, index=False)
print("\nResults saved at:", output_path)
