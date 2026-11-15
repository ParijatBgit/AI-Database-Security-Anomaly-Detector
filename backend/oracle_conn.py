import oracledb
from getpass import getpass
def get_connection():
    print("Connecting to Oracle Database...")
    host = input("Oracle Host [localhost]: ").strip() or "localhost"
    port = input("Oracle Port [1521]: ").strip() or "1521"
    service = input("Oracle Service Name [FREEPDB1]: ").strip() or "FREEPDB1"
    username = input("Oracle Username [SECURITY_ADMIN]: ").strip() or "SECURITY_ADMIN"
    password = getpass("Enter Oracle Password: ")
    dsn = f"{host}:{port}/{service}"
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )
    return connection
if __name__ == "__main__":
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT USER, SYSDATE
            FROM DUAL
        """)
        result = cursor.fetchone()
        print("\nOracle connection successful!")
        print("Connected user:", result[0])
        print("Database date:", result[1])
        cursor.close()
    except oracledb.Error as error:
        print("\nOracle connection failed!")
        print("Error:", error)
    finally:
        if connection:
            connection.close()
            print("\nDatabase connection closed.")
