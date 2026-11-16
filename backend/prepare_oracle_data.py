import subprocess
import sys
from pathlib import Path
from oracle_conn import get_connection
from fetch_database_activity import fetch_database_activity
from store_anomaly_alerts import store_anomaly_alerts
project_root = Path(__file__).resolve().parents[1]
connection = None

def run_script(name, script):
    print(f"\n========== {name.upper()} ==========", flush=True)
    result = subprocess.run([sys.executable, str(script)], cwd=project_root)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed.")
try:
    connection = get_connection()
    print("\nConnected to Oracle successfully!")
    print("\n========== DATABASE EXTRACTION ==========", flush=True)
    fetch_database_activity(connection)
    run_script("Feature extraction", project_root / "backend" / "feature_extraction.py")
    run_script("ML prediction", project_root / "ml_model" / "predict_oracle_activity.py")
    print("\n========== ALERT GENERATION ==========", flush=True)
    store_anomaly_alerts(connection)
    connection.commit()
    print("\n========== PIPELINE SUMMARY ==========")
    print("Database extraction: SUCCESS")
    print("Feature extraction: SUCCESS")
    print("ML prediction: SUCCESS")
    print("Alert generation: SUCCESS")
    print("\nCOMPLETE ANOMALY DETECTION PIPELINE EXECUTED SUCCESSFULLY!")
except Exception as error:
    if connection:
        connection.rollback()
    print("\nPIPELINE FAILED!")
    print("Error:", error)
    sys.exit(1)
finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")
