# AI-Based Database Security Anomaly Detector

A machine learning-based approach to identifying unusual activities in a database using Oracle SQL/PLSQL and Python.

## About the Project

Databases often contain sensitive information, so keeping track of how users interact with them is an important part of database security.

This project explores how machine learning can help identify unusual database activity by analysing user behaviour.

The system collects activity records from an Oracle database, processes them into meaningful features and uses an **Isolation Forest** model to detect potentially suspicious behaviour. When an anomaly is detected, the system assigns a risk level and stores the corresponding alert in the database.

The main idea is to go beyond simply storing database logs and use them to identify behaviour that may deserve attention.

## What Does the System Monitor?

The system works with different types of database activity, including:

- User login and logout records
- Failed login attempts
- SQL query execution
- Types of queries performed
- Database objects accessed
- Access permissions and denied operations
- Session duration and login time

These records help build a behavioural picture of how different users interact with the database.

## How It Works

The project follows a sequence of steps:

1. **Database setup:** Oracle tables store user details, login history, failed login attempts, query logs and permissions.
2. **Activity collection:** Python connects to Oracle and retrieves the stored activity records.
3. **Feature extraction:** The collected records are processed and converted into numerical features that the ML model can understand.
4. **Model training:** An Isolation Forest model is trained using a generated dataset containing normal and anomalous activity patterns.
5. **Anomaly detection:** The trained model analyses database activity and identifies records that differ from expected behaviour.
6. **Risk classification:** Detected anomalies are assigned risk levels.
7. **Alert generation:** The alerts are stored in the Oracle database for further inspection.

## Machine Learning

The project uses the **Isolation Forest algorithm**, an unsupervised anomaly detection technique.

Instead of learning a fixed list of suspicious activities, the model looks for patterns that appear unusual compared with the rest of the data.

Some of the features used by the model are:

- Login hour
- Number of failed login attempts
- Queries performed per hour
- SELECT, INSERT, UPDATE and DELETE counts
- Number of distinct database tables accessed
- After-hours login indicator
- Number of denied operations
- Session duration
- User identification features

A separate synthetic dataset is used to train and evaluate the model. The trained model is then used to analyse activity extracted from the Oracle database.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Oracle Database | Database storage |
| SQL and PL/SQL | Tables, queries, procedures and triggers |
| Pandas and NumPy | Data processing |
| Scikit-learn | Machine learning and model evaluation |
| Isolation Forest | Anomaly detection |
| Matplotlib and Seaborn | Data visualisation |
| Joblib | Saving and loading the trained model |
| Git and GitHub | Version control |

## Database Design

The Oracle database contains six main tables:

- `DB_USERS` – Stores registered database project users.
- `LOGIN_HISTORY` – Maintains login and logout records.
- `LOGIN_FAILURES` – Records unsuccessful login attempts.
- `QUERY_LOGS` – Stores information about executed queries.
- `USER_PERMISSIONS` – Maintains user permission records.
- `ANOMALY_ALERTS` – Stores suspicious activities detected by the ML model.

SQL constraints, queries, stored procedures and triggers are also used to support database operations and maintain data consistency.

## Project Structure

```text
AI-Database-Security-Anomaly-Detector/
│
├── backend/
│   ├── data_generation/
│   ├── evaluate_model.py
│   ├── feature_extraction.py
│   ├── fetch_database_activity.py
│   ├── oracle_conn.py
│   ├── prepare_oracle_data.py
│   ├── review_anomaly_alerts.py
│   ├── store_anomaly_alerts.py
│   └── testing.sql
│
├── data/
│   ├── generated/
│   └── processed/
│
├── database/
│   ├── procedures.sql
│   ├── tables_constraints.sql
│   ├── tables_created.sql
│   ├── tables_data.sql
│   ├── tables_queries.sql
│   └── tables_triggers.sql
│
├── ml_model/
│   ├── isolation_forest_model.pkl
│   ├── predict_activity.py
│   ├── predict_oracle_activity.py
│   └── train_model.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Requirements

Before running the project, make sure you have:

- Python installed
- Oracle Database installed and configured
- VS Code or another Python development environment
- Git installed

### 1. Clone the Repository

```bash
git clone https://github.com/ParijatBgit/AI-Database-Security-Anomaly-Detector.git
```

Move into the project directory:

```bash
cd AI-Database-Security-Anomaly-Detector
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Configure Oracle Database

- Set up the Oracle database and the `SECURITY_ADMIN` schema.
- Execute the SQL scripts from the `database` folder using the appropriate database connection.
- Configure the Oracle connection details in the Python connection module.
- Make sure the database is running before executing the Python scripts.

Keep database credentials private. Do not upload passwords or personal connection details to GitHub.

### 5. Run the Project

From the root directory, execute:

```bash
python backend/prepare_oracle_data.py
```

This runs the main pipeline, which handles database extraction, feature extraction, ML prediction and alert generation.

## Model Evaluation

The model is evaluated using commonly used classification metrics:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Classification report

Different Isolation Forest contamination settings are also compared to understand how they affect the detection results.

## Results and Outputs

The project generates several outputs during execution, including:

- Extracted database activity in CSV format
- Processed activity features
- Machine learning prediction results
- Model evaluation reports
- Data analysis graphs
- Risk-classified anomaly alerts stored in Oracle

During the latest pipeline validation, the system successfully processed 15 activity records and detected 2 anomalies. Both corresponding alerts were updated in the Oracle database.

These numbers represent one execution of the pipeline and may change as database activity changes.

## Current Status

The core database and machine learning pipeline has been implemented and tested.

The system can currently:

- Extract activity records from Oracle.
- Convert database activity into machine learning features.
- Train and load an Isolation Forest model.
- Predict potentially anomalous activity.
- Assign risk levels to detected anomalies.
- Store and update alerts in Oracle.

## Future Improvements

There is still room to improve the system. Some possible additions include:

- Training with larger and more diverse datasets.
- Improving anomaly detection performance, particularly recall.
- Refining the risk classification logic.
- Preventing duplicate alerts across repeated executions.
- Expanding automated testing.
- Exploring real-time database activity monitoring.

---

**Developed as an academic project exploring the use of machine learning for database security and behavioural anomaly detection.**