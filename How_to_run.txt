# How to Run the Project
## AI-Based Database Security Anomaly Detector

This guide explains how to set up and execute the project on a fresh Windows device.

The project uses:
- Python for data processing and machine learning.
- Oracle Database for storing user activity and anomaly alerts.
- SQL and PL/SQL for database operations.
- Isolation Forest and rule-based detection for identifying suspicious activity.

---

## 1. Prerequisites

Install the following software before running the project:

| Software | Purpose |
|---|---|
| Python 3 | Running the backend and ML scripts |
| Oracle Database | Database management and storage |
| Oracle SQL Developer | Executing SQL and PL/SQL scripts |
| Git | Cloning the project repository |

You must also have access to an Oracle database account with permission to create tables, constraints, procedures, triggers and other required database objects.

---

## 2. Clone the Repository

Open PowerShell or the terminal and execute:

```bash
git clone https://github.com/ParijatBgit/AI-Database-Security-Anomaly-Detector.git
```

Navigate into the project directory:

```bash
cd AI-Database-Security-Anomaly-Detector
```

---

## 3. Set Up the Python Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## 4. Configure Oracle Database

1. Start your Oracle Database instance.
2. Create a database user/schema named `SECURITY_ADMIN`, or use an appropriately configured existing schema.
3. Grant the permissions required to create and manage the project's database objects.
4. Open the project in VS Code.
5. Navigate to `backend/oracle_conn.py`.
6. Follow the connection configuration or prompts provided by the script to connect to your Oracle database.

Make sure the connection details, service name, username and password are correct.

**Note:** The project does not automatically create an Oracle Database instance. Oracle must be installed or accessible separately.

---

## 5. Create Database Tables and Objects

Open Oracle SQL Developer and connect using the `SECURITY_ADMIN` schema.

Execute the SQL scripts from the `database/` directory.

Recommended setup sequence:

1. `tables_created.sql` – Creates the database tables.
2. `tables_constraints.sql` – Adds primary key, foreign key and other constraints.
3. `tables_data.sql` – Inserts initial records.
4. `tables_triggers.sql` – Creates database triggers.
5. `procedures.sql` – Creates the stored procedures.

Execute `tables_queries.sql` separately when you want to inspect or run the project's demonstration queries.

Check that the tables, procedures and triggers have been created successfully before proceeding.

---

## 6. Train the Machine Learning Model

Activate the virtual environment and execute:

```bash
python ml_model/train_model.py
```

This script trains the Isolation Forest model using the project's processed synthetic dataset and saves the trained model as:

```text
ml_model/isolation_forest_model.pkl
```

If the processed dataset is not already available, first ensure that the required data-generation and preprocessing scripts have been executed.

**Note:** The model is trained using synthetic activity data. Oracle activity is subsequently used to test the detection pipeline.

---

## 7. Execute the Test Cases

Open:

```text
tests/test_cases.sql
```

Execute the SQL script using Oracle SQL Developer.

The test cases create fresh test users and generate different types of database activity, including:

- Normal database queries.
- Repeated failed login attempts.
- High query volume.
- Denied DELETE operations.

**Important:** The test script registers specific usernames. Execute its user-registration section only once on a fresh test database. Re-running it without cleaning up the existing test records may cause duplicate username errors.

The test cases record activity through the project's SQL/PLSQL workflow. They do not perform actual password guessing or destructive DELETE operations.

---

## 8. Run the Complete Anomaly Detection Pipeline

After configuring Oracle and executing the test cases, run:

```bash
python backend/prepare_oracle_data.py
```

This script coordinates the complete detection workflow:

1. Extracts activity records from Oracle.
2. Performs feature extraction and preprocessing.
3. Generates behavioural features for each user-hour group.
4. Applies Isolation Forest predictions.
5. Applies additional security rules.
6. Combines the detection results.
7. Classifies detected anomalies by risk level.
8. Stores anomaly alerts in the Oracle database.

---

## 9. Verify the Results

After successful execution, open Oracle SQL Developer and inspect the `ANOMALY_ALERTS` table.

You can execute:

```sql
SELECT * FROM ANOMALY_ALERTS;
```

To inspect alerts associated with the test users:

```sql
SELECT *
FROM ANOMALY_ALERTS
WHERE USER_ID IN (
    SELECT USER_ID
    FROM DB_USERS
    WHERE USERNAME IN (
        'TestNormal01',
        'TestFailed01',
        'TestVolume01',
        'TestDelete01'
    )
);
```

The expected test outcomes are:

| Test User | Activity | Expected Result |
|---|---|---|
| TestNormal01 | Normal SELECT queries | No anomaly alert |
| TestFailed01 | Repeated failed logins | HIGH risk |
| TestVolume01 | High query volume | MEDIUM risk |
| TestDelete01 | Repeated denied DELETE operations | HIGH risk |

Actual results may depend on the existing database records and activity included in the same user-hour aggregation.

---

## 10. Troubleshooting

**Oracle connection error**
- Check whether the Oracle Database instance is running.
- Verify the username, password, host, port and service name.
- Ensure the database user has the required permissions.

**Module not found**
- Activate the virtual environment.
- Run `pip install -r requirements.txt` again.

**Model file not found**
- Execute `python ml_model/train_model.py`.
- Ensure the processed training dataset exists.

**Table or procedure does not exist**
- Verify that all required SQL scripts have been executed successfully.
- Check that you are connected to the correct schema.

**Duplicate username error**
- Do not execute the test-user registration section repeatedly without cleaning up the previous test records.

---

## 11. Important Project Notes

- The project is an academic prototype and runs its anomaly-detection pipeline on demand.
- It does not continuously monitor every SQL statement or every Oracle authentication attempt.
- The machine learning model is trained using synthetic data.
- The rule-based detection thresholds are demonstration values and may require adjustment for other workloads.
- The `user_id` field is retained as metadata for identifying the database user and is not used as an ML training feature.

---

## Project Execution Command

Once the initial database setup, Python environment and model training are complete, the main command to execute the project is:

```bash
python backend/prepare_oracle_data.py
```

This runs the complete database activity anomaly-detection pipeline.