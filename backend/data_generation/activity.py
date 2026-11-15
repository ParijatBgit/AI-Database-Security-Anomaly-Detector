import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42) # random data

TOTAL_RECORDS = 10000
ANOMALY_COUNT = 1500

records = []

USER_IDS = [1, 2, 3, 4, 5, 6]
for i in range(TOTAL_RECORDS):
    user_id = np.random.choice(USER_IDS)
    is_anomaly = 1 if i < ANOMALY_COUNT else 0
    login_hour = np.random.randint(8, 20)
    login_failures = np.random.poisson(0.2)
    queries_per_hour = np.random.randint(1, 15)
    select_count = np.random.randint(1, queries_per_hour + 1)
    insert_count = np.random.randint(0, 4)
    update_count = np.random.randint(0, 4)
    delete_count = np.random.randint(0, 2)
    distinct_tables = np.random.randint(1, 5)
    after_hours_login = 0
    access_denied_count = np.random.randint(0, 2)
    session_duration = np.random.randint(5, 121)
    if is_anomaly:
        anomaly_type = np.random.choice([
            "failed_login",
            "query_flood",
            "delete_activity",
            "after_hours",
            "unauthorized_access"
        ])
        if anomaly_type == "failed_login":
            login_failures = np.random.randint(5, 16)
        elif anomaly_type == "query_flood":
            queries_per_hour = np.random.randint(80, 201)
            select_count = int(queries_per_hour * 0.7)
            insert_count = int(queries_per_hour * 0.1)
            update_count = int(queries_per_hour * 0.1)
            delete_count = queries_per_hour - (
                select_count + insert_count + update_count
            )
        elif anomaly_type == "delete_activity":
            delete_count = np.random.randint(15, 51)
            queries_per_hour = delete_count + np.random.randint(1, 15)
        elif anomaly_type == "after_hours":
            login_hour = np.random.choice(
                list(range(0, 6)) + list(range(22, 24))
            )
            after_hours_login = 1
        elif anomaly_type == "unauthorized_access":
            access_denied_count = np.random.randint(5, 16)
    records.append({
        "user_id": user_id,
        "login_hour": login_hour,
        "login_failures": login_failures,
        "queries_per_hour": queries_per_hour,
        "select_count": select_count,
        "insert_count": insert_count,
        "update_count": update_count,
        "delete_count": delete_count,
        "distinct_tables": distinct_tables,
        "after_hours_login": after_hours_login,
        "access_denied_count": access_denied_count,
        "session_duration": session_duration,
        "anomaly_label": is_anomaly
    })
df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
project_root = Path(__file__).resolve().parents[2]
output_path = project_root / "data" / "generated" / "database_activity.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
print("Dataset generated successfully!")
print("Total records:", len(df))
print("Normal records:", (df["anomaly_label"] == 0).sum())
print("Abnormal records:", (df["anomaly_label"] == 1).sum())
print("Dataset saved at:", output_path)
print("\nFirst five records:")
print(df.head())
