import pandas as pd
import joblib
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
model_path = project_root / "ml_model" / "isolation_forest_model.pkl"
data_path = project_root / "data" / "processed" / "oracle_activity_features.csv"
output_path = project_root / "data" / "processed" / "oracle_prediction_results.csv"
model = joblib.load(model_path)
df = pd.read_csv(data_path)
print("Isolation Forest model loaded!")
print("Oracle activity records:", len(df))

expected_features = list(model.feature_names_in_)
missing_features = set(expected_features) - set(df.columns)

if missing_features:
    raise ValueError(f"Missing features: {missing_features}")

X = df[expected_features]
ml_predictions = model.predict(X)
anomaly_scores = -model.decision_function(X)
results = df.copy()
results["ml_predicted_label"] = [1 if p == -1 else 0 for p in ml_predictions]
results["rule_detected"] = (
    (results["login_failures"] >= 5) |
    (results["queries_per_hour"] >= 80) |
    (results["delete_count"] >= 15) |
    (results["access_denied_count"] >= 5)
).astype(int)
results["predicted_label"] = (
    (results["ml_predicted_label"] == 1) |
    (results["rule_detected"] == 1)
).astype(int)
results["anomaly_score"] = anomaly_scores
results["detection_method"] = "NORMAL"
results.loc[results["ml_predicted_label"] == 1, "detection_method"] = "ISOLATION_FOREST"
results.loc[results["rule_detected"] == 1, "detection_method"] = "RULE_BASED"
results.loc[
    (results["ml_predicted_label"] == 1) &
    (results["rule_detected"] == 1),
    "detection_method"
] = "ML_AND_RULES"
results["detection_status"] = results["predicted_label"].map({
    0: "NORMAL",
    1: "ANOMALY"
})
print("\n========== ORACLE ACTIVITY PREDICTIONS ==========")
print(results[
    [
        "login_failures",
        "queries_per_hour",
        "delete_count",
        "access_denied_count",
        "ml_predicted_label",
        "rule_detected",
        "predicted_label",
        "detection_method",
        "detection_status"
    ]
].to_string(index=False))
print("\n========== DETECTION SUMMARY ==========")
print("Total records:", len(results))
print("Normal activities:", (results["predicted_label"] == 0).sum())
print("Anomalies detected:", (results["predicted_label"] == 1).sum())
print("ML detections:", (results["ml_predicted_label"] == 1).sum())
print("Rule detections:", (results["rule_detected"] == 1).sum())

results.to_csv(output_path, index=False)
print("\nResults saved at:", output_path)
