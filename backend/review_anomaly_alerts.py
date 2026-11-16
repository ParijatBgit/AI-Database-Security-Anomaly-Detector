import pandas as pd
from pathlib import Path
from oracle_conn import get_connection
connection = None

try:
    connection = get_connection()
    cursor = connection.cursor()
    print("\nConnected to Oracle successfully!")

    query = """
        SELECT
            A.ALERT_ID,
            A.USER_ID,
            U.USERNAME,
            A.ACTIVITY_TYPE,
            A.DESCRIPTION,
            A.RISK_LEVEL,
            A.DETECTED_AT,
            A.ALERT_STATUS
        FROM ANOMALY_ALERTS A
        LEFT JOIN DB_USERS U
        ON A.USER_ID = U.USER_ID
        ORDER BY A.DETECTED_AT DESC
    """
    cursor.execute(query)
    columns = [
        column[0].lower()
        for column in cursor.description
    ]
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=columns)

    print("\n========== ANOMALY ALERTS ==========")
    if df.empty:
        print("No anomaly alerts found.")
    else:
        print(df.to_string(index=False))
    print("\n========== RISK LEVEL SUMMARY ==========")
    if not df.empty:
        print(df["risk_level"].value_counts())
        print("\n========== ALERT STATUS SUMMARY ==========")
        print(df["alert_status"].value_counts())
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "oracle_alert_report.csv"
    df.to_csv(output_path, index=False)
    print("\nTotal alerts retrieved:", len(df))
    print("Alert report saved at:", output_path)
    cursor.close()
except Exception as error:
    print("\nAlert retrieval failed!")
    print("Error:", error)
finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")
