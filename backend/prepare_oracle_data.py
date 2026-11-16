import subprocess
import sys
import oracledb
import pandas as pd
from pathlib import Path
from oracle_conn import get_connection
from fetch_database_activity import fetch_database_activity
from store_anomaly_alerts import store_anomaly_alerts
project_root = Path(__file__).resolve().parents[1]
backend_dir = project_root / "backend"
data_dir = project_root / "data" / "processed"
model_path = project_root / "ml_model" / "isolation_forest_model.pkl"
feature_path = data_dir / "oracle_activity_features.csv"
prediction_path = data_dir / "oracle_prediction_results.csv"

connection = None

def check_file(path, name):
    if not path.is_file():
        raise FileNotFoundError(f"{name} not found: {path}")
def run_script(name, script):
    check_file(script, name)
    print(f"\n========== {name.upper()} ==========", flush=True)
    result = subprocess.run([sys.executable, str(script)], cwd=project_root)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {result.returncode}.")
try:
    check_file(backend_dir / "feature_extraction.py", "Feature extraction script")
    check_file(project_root / "ml_model" / "predict_oracle_activity.py", "Prediction script")
    check_file(model_path, "Trained ML model")
    print("\nConnecting to Oracle...")
    connection = get_connection()
    print("Oracle connection successful!")
    print("\n========== DATABASE EXTRACTION ==========")
    fetch_database_activity(connection)
    run_script("Feature extraction", backend_dir / "feature_extraction.py")
    check_file(feature_path, "Extracted feature dataset")
    run_script("ML prediction", project_root / "ml_model" / "predict_oracle_activity.py")
    check_file(prediction_path, "Prediction results")

    results = pd.read_csv(prediction_path)
    required_columns = {"predicted_label", "anomaly_score"}
    if not required_columns.issubset(results.columns):
        raise ValueError("Prediction results have missing required columns.")
    print("\n========== ALERT GENERATION ==========")
    store_anomaly_alerts(connection)
    connection.commit()
    print("\n========== PIPELINE SUMMARY ==========")
    print("Database extraction: SUCCESS")
    print("Feature extraction: SUCCESS")
    print("ML prediction: SUCCESS")
    print("Alert generation: SUCCESS")
    print("\nCOMPLETE ANOMALY DETECTION PIPELINE EXECUTED SUCCESSFULLY!")

except FileNotFoundError as error:
    if connection:
        connection.rollback()
    print("\nFILE ERROR:", error)
    sys.exit(1)

except oracledb.Error as error:
    if connection:
        connection.rollback()
    print("\nORACLE DATABASE ERROR:", error)
    sys.exit(1)

except (RuntimeError, ValueError, pd.errors.ParserError) as error:
    if connection:
        connection.rollback()
    print("\nPIPELINE ERROR:", error)
    sys.exit(1)

except Exception as error:
    if connection:
        connection.rollback()
    print("\nUNEXPECTED ERROR:", error)
    sys.exit(1)

finally:
    if connection:
        connection.close()
        print("\nOracle connection closed.")
