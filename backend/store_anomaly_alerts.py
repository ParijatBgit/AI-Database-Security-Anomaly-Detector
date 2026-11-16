import pandas as pd
from pathlib import Path

def classify_risk(row):
    if row["delete_count"] >= 15 or row["login_failures"] >= 5 or row["access_denied_count"] >= 5:
        return "HIGH"
    if row["queries_per_hour"] >= 80 or row["after_hours_login"] == 1:
        return "MEDIUM"
    return "LOW"

def store_anomaly_alerts(connection):
    project_root = Path(__file__).resolve().parents[1]
    results_path = project_root / "data" / "processed" / "oracle_prediction_results.csv"
    df = pd.read_csv(results_path)
    anomalies = df[df["predicted_label"] == 1]
    print("Total anomalies detected:", len(anomalies))

    cursor = connection.cursor()
    inserted_count = 0
    updated_count = 0
    skipped_count = 0

    check_query = """
        SELECT ALERT_ID FROM ANOMALY_ALERTS
        WHERE USER_ID = :1 AND ACTIVITY_TYPE = :2 AND DESCRIPTION = :3
    """
    insert_query = """
        INSERT INTO ANOMALY_ALERTS (USER_ID, ACTIVITY_TYPE, DESCRIPTION, RISK_LEVEL)
        VALUES (:1, :2, :3, :4)
    """
    update_query = "UPDATE ANOMALY_ALERTS SET RISK_LEVEL = :1 WHERE ALERT_ID = :2"

    try:
        required_columns = {
            "user_id", "predicted_label", "anomaly_score",
            "queries_per_hour", "login_failures", "delete_count",
            "access_denied_count", "after_hours_login"
        }
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing prediction columns: {missing}")
        for _, row in anomalies.iterrows():
            user_id = int(row["user_id"])
            risk_level = classify_risk(row)
            description = (
                f"Anomaly detected using {row.get('detection_method', 'Isolation Forest')}. "
                f"Anomaly score: {row['anomaly_score']:.4f}. "
                f"Queries per hour: {row['queries_per_hour']}. "
                f"Login failures: {row['login_failures']}. "
                f"DELETE operations: {row['delete_count']}. "
                f"Access denied: {row['access_denied_count']}."
            )
            activity_type = "ML_DETECTED_ANOMALY"
            cursor.execute(check_query, (user_id, activity_type, description))
            existing_alerts = cursor.fetchall()

            if existing_alerts:
                for alert in existing_alerts:
                    cursor.execute(update_query, (risk_level, alert[0]))
                updated_count += len(existing_alerts)
                print(f"Existing alert updated: User {user_id}, Risk: {risk_level}")
            else:
                cursor.execute(insert_query, (user_id, activity_type, description, risk_level))
                inserted_count += 1
                print(f"New alert inserted: User {user_id}, Risk: {risk_level}")
                
        print("\n========== ALERT SUMMARY ==========")
        print("Anomalies detected:", len(anomalies))
        print("New alerts inserted:", inserted_count)
        print("Existing alerts updated:", updated_count)
        print("Records skipped:", skipped_count)
        print("Risk classification completed successfully!")
    finally:
        cursor.close()
