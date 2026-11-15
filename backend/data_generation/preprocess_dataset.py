import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "generated" / "database_activity.csv"
output_path = project_root / "data" / "processed" / "database_activity_processed.csv"

df = pd.read_csv(input_path)
print("Original dataset shape:", df.shape)
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()
print("Duplicates removed:", duplicate_count)
missing_count = df.isnull().sum().sum()
if missing_count > 0:
    raise ValueError("Dataset contains missing values. Handle them before proceeding.")
print("Missing values:", missing_count)
labels = df["anomaly_label"]
features = df.drop(columns=["anomaly_label"])
features = pd.get_dummies(
    features,
    columns=["user_id"],
    prefix="user",
    dtype=int
)
processed_df = pd.concat(
    [features, labels.reset_index(drop=True)],
    axis=1
)
output_path.parent.mkdir(parents=True, exist_ok=True)
processed_df.to_csv(output_path, index=False)

print("\nPreprocessing completed successfully!")
print("Processed dataset shape:", processed_df.shape)
print("Normal records:", (processed_df["anomaly_label"] == 0).sum())
print("Abnormal records:", (processed_df["anomaly_label"] == 1).sum())
print("Saved at:", output_path)
print("\nProcessed columns:")
print(processed_df.columns.tolist())
print("\nFirst five processed records:")
print(processed_df.head())
