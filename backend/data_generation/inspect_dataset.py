import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "generated" / "database_activity.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET OVERVIEW ==========")
print("\nDataset Shape:")
print(df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nDataset Information:")
df.info()
print("\n========== DATA QUALITY ==========")
print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Records:")
print(df.duplicated().sum())
print("\n========== ANOMALY DISTRIBUTION ==========")
print(df["anomaly_label"].value_counts())
print("\nAnomaly Percentage:")
print(df["anomaly_label"].value_counts(normalize=True) * 100)
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())
print("\n========== NORMAL VS ABNORMAL ==========")
print(
    df.groupby("anomaly_label")[
        ["login_failures", "queries_per_hour",
         "delete_count", "access_denied_count",
         "session_duration"]
    ].mean()
)
