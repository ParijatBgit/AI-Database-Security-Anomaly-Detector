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
    skipped_count = 0
    check_query = """
        SELECT COUNT(*)
        FROM ANOMALY_ALERTS
        WHERE USER_ID = :1
          AND ACTIVITY_TYPE = :2
          AND DESCRIPTION = :3
    """
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
            print("Skipping: User ID not identified.")
            skipped_count += 1
            continue
        description = (
            f"ML detected suspicious activity. "
            f"Anomaly score: {row['anomaly_score']:.4f}. "
            f"Queries per hour: {row['queries_per_hour']}. "
            f"Login failures: {row['login_failures']}. "
            f"DELETE operations: {row['delete_count']}. "
            f"Access denied: {row['access_denied_count']}."
        )
        activity_type = "ML_DETECTED_ANOMALY"
        cursor.execute(
            check_query,
            (int(user_id), activity_type, description)
        )
        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            print(f"Duplicate alert skipped for user {user_id}")
            skipped_count += 1
            continue
        cursor.execute(
            insert_query,
            (
                int(user_id),
                activity_type,
                description,
                "MEDIUM"
            )
        )
        inserted_count += 1

    connection.commit()
    print("\n========== ALERT INSERTION SUMMARY ==========")
    print("Anomalies detected:", len(anomalies))
    print("New alerts inserted:", inserted_count)
    print("Duplicate alerts skipped:", skipped_count)
    print("\nOracle alert processing completed!")
    cursor.close()

except Exception as error:
    if connection:
        connection.rollback()
    print("\nAlert processing failed!")
    print("Error:", error)
finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")
