import pandas as pd
import joblib
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
model_path = project_root / "ml_model" / "isolation_forest_model.pkl"

data_path = (
    project_root / "data" / "processed" /
    "database_activity_processed.csv"
)

model = joblib.load(model_path)
print("Trained model loaded successfully!")
df = pd.read_csv(data_path)
actual_labels = df["anomaly_label"]
X = df.drop(columns=["anomaly_label"])
X = X.reindex(columns=model.feature_names_in_)
print("Activity records loaded:", len(X))

predictions = model.predict(X)
predicted_labels = [1 if p == -1 else 0 for p in predictions]
anomaly_scores = -model.decision_function(X)
results = pd.DataFrame({
    "Actual": actual_labels,
    "Predicted": predicted_labels,
    "Anomaly_Score": anomaly_scores
})
results["Detection_Status"] = results["Predicted"].map({
    0: "NORMAL",
    1: "ANOMALY"
})
print("\n========== PREDICTION RESULTS ==========")
print(results.head(15).to_string(index=False))
normal_count = (results["Predicted"] == 0).sum()
anomaly_count = (results["Predicted"] == 1).sum()
print("\n========== DETECTION SUMMARY ==========")
print("Total records:", len(results))
print("Normal activities detected:", normal_count)
print("Anomalies detected:", anomaly_count)

output_path = (
    project_root / "data" / "processed" /
    "prediction_results.csv"
)
results.to_csv(output_path, index=False)
print("\nPrediction results saved at:", output_path)
