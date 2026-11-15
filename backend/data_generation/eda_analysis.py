import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]

file_path = (
    project_root / "data" / "processed" /
    "database_activity_processed.csv"
)
df = pd.read_csv(file_path)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(7, 5))
sns.countplot(
    data=df,
    x="anomaly_label"
)
plt.title("Normal vs Abnormal Database Activity")
plt.xlabel("Activity (0 = Normal, 1 = Abnormal)")
plt.ylabel("Number of Records")
plt.savefig(project_root / "data" / "processed" / "01_activity_distribution.png")
plt.show()
plt.figure(figsize=(7, 5))
sns.boxplot(
    data=df,
    x="anomaly_label",
    y="login_failures"
)
plt.title("Login Failures: Normal vs Abnormal")
plt.xlabel("Activity (0 = Normal, 1 = Abnormal)")
plt.ylabel("Login Failures")
plt.savefig(project_root / "data" / "processed" / "02_login_failures.png")
plt.show()
plt.figure(figsize=(7, 5))
sns.boxplot(
    data=df,
    x="anomaly_label",
    y="queries_per_hour"
)
plt.title("Query Volume: Normal vs Abnormal")
plt.xlabel("Activity (0 = Normal, 1 = Abnormal)")
plt.ylabel("Queries Per Hour")
plt.savefig(project_root / "data" / "processed" / "03_query_volume.png")
plt.show()
plt.figure(figsize=(7, 5))
sns.boxplot(
    data=df,
    x="anomaly_label",
    y="delete_count"
)
plt.title("DELETE Operations: Normal vs Abnormal")
plt.xlabel("Activity (0 = Normal, 1 = Abnormal)")
plt.ylabel("DELETE Operations")
plt.savefig(project_root / "data" / "processed" / "04_delete_operations.png")
plt.show()

correlation = df.drop(
    columns=["anomaly_label"]
).corr()
plt.figure(figsize=(13, 9))
sns.heatmap(
    correlation,
    cmap="coolwarm",
    annot=False,
    linewidths=0.5
)
plt.title("Database Activity Feature Correlation")
plt.savefig(project_root / "data" / "processed" / "05_correlation.png")
plt.show()

comparison = df.groupby("anomaly_label")[
    [
        "login_failures",
        "queries_per_hour",
        "delete_count",
        "access_denied_count",
        "session_duration"
    ]
].mean()

print("\nAVERAGE NORMAL VS ABNORMAL ACTIVITY")
print(comparison)
print("\nEDA ANALYSIS COMPLETED!")
