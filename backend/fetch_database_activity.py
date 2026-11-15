import pandas as pd
from pathlib import Path
from oracle_conn import get_connection
connection = None
try:
    connection = get_connection()
    print("\nConnected to Oracle successfully!")
    queries = {
        "DB_USERS": """
            SELECT USER_ID, USERNAME, USER_ROLE,
                   DEPARTMENT, ACCOUNT_STATUS
            FROM DB_USERS
        """,
        "LOGIN_HISTORY": """
            SELECT LOGIN_ID, USER_ID, LOGIN_TIME,
                   LOGOUT_TIME, IP_ADDRESS
            FROM LOGIN_HISTORY
        """,
        "LOGIN_FAILURES": """
            SELECT FAILURE_ID, USER_ID, ATTEMPTED_USERNAME,
                   ATTEMPT_TIME, FAILURE_REASON
            FROM LOGIN_FAILURES
        """,
        "QUERY_LOGS": """
            SELECT QUERY_ID, USER_ID, QUERY_TYPE,
                   OBJECT_NAME, EXECUTION_TIME,
                   ROWS_AFFECTED, ACCESS_STATUS
            FROM QUERY_LOGS
        """,
        "USER_PERMISSIONS": """
            SELECT PERMISSION_ID, USER_ID, OBJECT_NAME,
                   PERMISSION_TYPE, GRANTED_AT
            FROM USER_PERMISSIONS
        """
    }

    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "data" / "generated" / "oracle_extract"
    output_dir.mkdir(parents=True, exist_ok=True)
    cursor = connection.cursor()
    for table_name, query in queries.items():
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        records = cursor.fetchall()
        df = pd.DataFrame(records, columns=columns)
        output_path = output_dir / f"{table_name.lower()}.csv"
        df.to_csv(output_path, index=False)
        print(f"\nTable: {table_name}")
        print("Records fetched:", len(df))
        print("Saved:", output_path)
        print("\nFirst 3 records:")
        print(df.head(3))
    cursor.close()
    print("\nAll database records fetched successfully!")
    
except Exception as error:
    print("\nDatabase extraction failed!")
    print("Error:", error)
finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")
