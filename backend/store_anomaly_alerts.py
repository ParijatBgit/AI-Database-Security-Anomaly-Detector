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

def classify_risk(row):
    if (
        row["delete_count"] >= 15
        or row["login_failures"] >= 5
        or row["access_denied_count"] >= 5
    ):
        return "HIGH"
    elif (
        row["queries_per_hour"] >= 80
        or row["after_hours_login"] == 1
    ):
        return "MEDIUM"
    else:
        return "LOW"

connection = None
try:
    connection = get_connection()
    cursor = connection.cursor()
    inserted_count = 0
    updated_count = 0
    check_query = """
        SELECT ALERT_ID
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
            :1, :2, :3, :4
        )
    """
    update_query = """
        UPDATE ANOMALY_ALERTS
        SET RISK_LEVEL = :1
        WHERE ALERT_ID = :2
    """
    for _, row in anomalies.iterrows():
        user_id = None
        for uid in range(1, 7):
            if row[f"user_{uid}"] == 1:
                user_id = uid
                break
        if user_id is None:
            print("Skipping: User ID not identified.")
            continue
        risk_level = classify_risk(row)
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
        existing_alerts = cursor.fetchall()
        if existing_alerts:
            for alert in existing_alerts:
                cursor.execute(
                    update_query,
                    (risk_level, alert[0])
                )
            updated_count += len(existing_alerts)
            print(
                f"Existing alert updated: User {user_id}, "
                f"Risk: {risk_level}"
            )
        else:
            cursor.execute(
                insert_query,
                (
                    int(user_id),
                    activity_type,
                    description,
                    risk_level
                )
            )
            inserted_count += 1
            print(
                f"New alert inserted: User {user_id}, "
                f"Risk: {risk_level}"
            )
    connection.commit()
    print("\n========== RISK CLASSIFICATION SUMMARY ==========")
    print("Anomalies detected:", len(anomalies))
    print("New alerts inserted:", inserted_count)
    print("Existing alerts updated:", updated_count)
    print("\nRisk classification completed successfully!")
    cursor.close()
except Exception as error:
    if connection:
        connection.rollback()
    print("\nRisk classification failed!")
    print("Error:", error)
finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")
