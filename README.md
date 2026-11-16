# AI-Based Database Security Anomaly Detector

A machine learning-based approach to identifying unusual activities in a database using Oracle SQL/PLSQL and Python.

## About the Project

Databases often contain sensitive information, so keeping track of how users interact with them is an important part of database security.

This project explores how machine learning can help identify unusual database activity by analysing user behaviour.

The system collects activity records from an Oracle database, processes them into meaningful behavioural features and uses an **Isolation Forest** model to detect potentially suspicious behaviour. It also applies predefined security rules to identify specific suspicious activities. When an anomaly is detected, the system assigns a risk level and stores the corresponding alert in the database.

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
3. **Feature extraction:** The collected records are processed and converted into numerical behavioural features that the ML model can understand.
4. **Model training:** An Isolation Forest model is trained using a generated dataset containing normal and anomalous activity patterns.
5. **ML prediction:** The trained model analyses database activity and identifies records that differ from expected behaviour.
6. **Rule-based detection:** Predefined security rules independently check for specific suspicious activities.
7. **Combined detection:** The ML predictions and rule-based results are combined to determine whether an activity should be classified as anomalous.
8. **Risk classification:** Detected anomalies are assigned risk levels.
9. **Alert generation:** The alerts are stored in the Oracle database for further inspection.

The pipeline is executed on demand using a Python script. It does not currently provide continuous, real-time database monitoring.

## Machine Learning and Anomaly Detection

The project uses the **Isolation Forest algorithm**, an unsupervised anomaly detection technique.

Instead of learning a fixed list of suspicious activities, the model looks for patterns that appear unusual compared with the rest of the data.

The model uses 11 behavioural features, including:

- Login hour
- Number of failed login attempts
- Queries performed per hour
- SELECT, INSERT, UPDATE and DELETE counts
- Number of distinct database tables accessed
- After-hours login indicator
- Number of denied operations
- Session duration

User identification is maintained separately as metadata. The database `USER_ID` is not used as an ML training feature, allowing the system to process newly registered users without relying on a fixed set of user IDs.

### Rule-Based Security Detection

Alongside Isolation Forest, the system uses predefined security rules to identify specific suspicious activities.

The current detection thresholds are:

| Security condition | Detection threshold |
|---|---:|
| Failed login attempts | 5 or more |
| Queries per hour | 80 or more |
| DELETE operations | 15 or more |
| Denied operations | 5 or more |

An activity is classified as anomalous if either the ML model or the security rules detect suspicious behaviour.

This hybrid approach helps identify known suspicious patterns even when the Isolation Forest model does not independently flag them.

### Risk Classification

Detected anomalies are assigned one of three risk levels:

- **HIGH:** Repeated failed logins, excessive DELETE operations or multiple denied operations.
- **MEDIUM:** Unusually high query volume or after-hours login activity.
- **LOW:** Other detected anomalies that do not meet the HIGH or MEDIUM thresholds.

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
- `ANOMALY_ALERTS` – Stores suspicious activities detected by the hybrid detection system.

SQL constraints, queries, stored procedures and triggers are also used to support database operations and maintain data consistency.

The trigger helps maintain consistency in failed-login records. It does not automatically intercept every actual Oracle authentication failure; failed attempts are recorded through the project's database procedure.

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
│   └── test_cases.sql
│
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
- Make sure the database is running before executing the Python scripts.
- The Python connection module prompts for the Oracle host, port, service name, username and password when connecting.

Keep database credentials private. Do not upload passwords or personal connection details to GitHub.

### 5. Train the Machine Learning Model

From the project root directory, execute:

```bash
python ml_model/train_model.py
```

This trains the Isolation Forest model using the processed synthetic dataset and saves the trained model in the `ml_model` directory.

### 6. Run the Project

Execute the main pipeline:

```bash
python backend/prepare_oracle_data.py
```

This runs the complete workflow:

- Database activity extraction
- Feature extraction
- Machine learning prediction
- Rule-based security detection
- Risk classification
- Alert generation and storage in Oracle

## Model Evaluation

The model is evaluated using commonly used classification metrics:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Classification report

Different Isolation Forest contamination settings are also compared to understand how they affect the detection results.

The evaluation is performed using a synthetic dataset. Therefore, the reported performance represents results on generated data and should not be interpreted as guaranteed real-world detection performance.

## Results and Outputs

The project generates several outputs during execution, including:

- Extracted database activity in CSV format
- Processed behavioural features
- Machine learning prediction results
- Model evaluation reports
- Data analysis graphs
- Risk-classified anomaly alerts stored in Oracle

During one of the latest pipeline validation runs:

- 19 activity records were processed.
- 5 anomalies were detected.
- 4 records were flagged by Isolation Forest.
- 5 records were flagged by the rule-based detection layer.
- 5 anomaly alerts were inserted into Oracle.

The validation also included four newly registered test users:

- A normal user performing regular queries.
- A user with 15 failed login attempts.
- A user performing 85 SELECT queries.
- A user making 15 denied DELETE attempts.

The three suspicious test users generated alerts with the expected HIGH, MEDIUM and HIGH risk classifications, respectively. The normal test user did not generate an alert.

These numbers represent one particular test execution and may change as database activity changes.

## Current Status

The core database and hybrid anomaly-detection pipeline has been implemented and tested.

The system can currently:

- Register and manage database project users.
- Record login activity and failed login attempts.
- Record SQL query activity.
- Extract activity records from Oracle.
- Convert database activity into 11 behavioural ML features.
- Train and load an Isolation Forest model.
- Detect potentially anomalous activity using ML predictions and predefined security rules.
- Assign HIGH, MEDIUM and LOW risk levels.
- Store and update anomaly alerts in Oracle.
- Process activity from newly registered users.

## Limitations and Future Improvements

The current implementation is an academic prototype and has some limitations.

- Monitoring is performed on demand rather than continuously.
- Failed login attempts are recorded through the project's PL/SQL procedure rather than automatically intercepting every Oracle authentication failure.
- The ML model is trained using synthetic activity data.
- Detection performance can vary with different activity patterns.
- Further testing with real database activity is required.

Possible future improvements include:

- Training with larger and more diverse datasets.
- Improving anomaly detection performance, particularly recall.
- Refining the risk classification logic.
- Improving duplicate-alert handling across repeated executions.
- Expanding automated testing.
- Exploring real-time database activity monitoring.

---

**Developed as an academic project exploring the use of machine learning and behavioural analysis for database security and anomaly detection.**