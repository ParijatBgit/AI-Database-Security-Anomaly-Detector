import pandas as pd
from pathlib import Path

def fetch_database_activity(connection):
    queries = {
        "DB_USERS": "SELECT USER_ID, USERNAME, USER_ROLE, DEPARTMENT, ACCOUNT_STATUS FROM DB_USERS",
        "LOGIN_HISTORY": "SELECT LOGIN_ID, USER_ID, LOGIN_TIME, LOGOUT_TIME, IP_ADDRESS FROM LOGIN_HISTORY",
        "LOGIN_FAILURES": "SELECT FAILURE_ID, USER_ID, ATTEMPTED_USERNAME, ATTEMPT_TIME, FAILURE_REASON FROM LOGIN_FAILURES",
        "QUERY_LOGS": "SELECT QUERY_ID, USER_ID, QUERY_TYPE, OBJECT_NAME, EXECUTION_TIME, ROWS_AFFECTED, ACCESS_STATUS FROM QUERY_LOGS",
        "USER_PERMISSIONS": "SELECT PERMISSION_ID, USER_ID, OBJECT_NAME, PERMISSION_TYPE, GRANTED_AT FROM USER_PERMISSIONS"
    }

    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "data" / "generated" / "oracle_extract"
    output_dir.mkdir(parents=True, exist_ok=True)
    cursor = connection.cursor()

    try:
        for table_name, query in queries.items():
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
            output_path = output_dir / f"{table_name.lower()}.csv"
            df.to_csv(output_path, index=False)
            print(f"\n{table_name}: {len(df)} records saved")

        print("\nAll database records fetched successfully!")
    finally:
        cursor.close()
