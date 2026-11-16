import pandas as pd
from pathlib import Path
from oracle_conn import get_connection

project_root = Path(__file__).resolve().parents[1]

results_path = (
    project_root / "data" / "processed" /
    "oracle_prediction_results.csv"
)
df = pd.read_csv(results_path)
anomalies = df[df["predicted_label"] == 1]
print("Total anomalies detected:", len(anomalies))
connection = None

try:
    connection = get_connection()
    cursor = connection.cursor()
    inserted_count = 0
    insert_query = """
        INSERT INTO ANOMALY_ALERTS
        (
            USER_ID,
            ACTIVITY_TYPE,
            DESCRIPTION,
            RISK_LEVEL
        )
        VALUES
        (
            :1,
            :2,
            :3,
            :4
        )
    """
    for _, row in anomalies.iterrows():
        user_id = None
        for uid in range(1, 7):
            if row[f"user_{uid}"] == 1:
                user_id = uid
                break
        if user_id is None:
            print("Skipping record: User ID not identified.")
            continue
        description = (
            f"ML detected suspicious activity. "
            f"Anomaly score: {row['anomaly_score']:.4f}. "
            f"Queries per hour: {row['queries_per_hour']}. "
            f"Login failures: {row['login_failures']}. "
            f"DELETE operations: {row['delete_count']}. "
            f"Access denied: {row['access_denied_count']}."
        )
        cursor.execute(
            insert_query,
            (
                int(user_id),
                "ML_DETECTED_ANOMALY",
                description,
                "MEDIUM"
            )
        )
        inserted_count += 1
    connection.commit()
    print("\n========== ALERT INSERTION ==========")
    print("Anomalies detected:", len(anomalies))
    print("Alerts inserted:", inserted_count)
    print("Oracle ANOMALY_ALERTS updated successfully!")
    cursor.close()

except Exception as error:
    if connection:
        connection.rollback()
    print("\nAlert insertion failed!")
    print("Error:", error)

finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")