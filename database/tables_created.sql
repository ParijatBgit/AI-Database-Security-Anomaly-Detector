CREATE TABLE DB_USERS (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,
    username VARCHAR2(50) NOT NULL UNIQUE,
    user_role VARCHAR2(30) NOT NULL,
    department VARCHAR2(50),
    account_status VARCHAR2(20) DEFAULT 'ACTIVE',
    created_at DATE DEFAULT SYSDATE
);
CREATE TABLE LOGIN_HISTORY (
    login_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER NOT NULL,
    login_time DATE DEFAULT SYSDATE,
    logout_time DATE,
    ip_address VARCHAR2(50),
    FOREIGN KEY (user_id) REFERENCES DB_USERS(user_id)
);
CREATE TABLE LOGIN_FAILURES (
    failure_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER,
    attempted_username VARCHAR2(50),
    attempt_time DATE DEFAULT SYSDATE,
    failure_reason VARCHAR2(100),
    FOREIGN KEY (user_id) REFERENCES DB_USERS(user_id)
);
CREATE TABLE QUERY_LOGS (
    query_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER NOT NULL,
    query_type VARCHAR2(20),
    object_name VARCHAR2(50),
    query_text VARCHAR2(1000),
    execution_time DATE DEFAULT SYSDATE,
    rows_affected NUMBER,
    access_status VARCHAR2(20),
    FOREIGN KEY (user_id) REFERENCES DB_USERS(user_id)
);
CREATE TABLE USER_PERMISSIONS (
    permission_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER NOT NULL,
    object_name VARCHAR2(50) NOT NULL,
    permission_type VARCHAR2(30) NOT NULL,
    granted_at DATE DEFAULT SYSDATE,
    FOREIGN KEY (user_id) REFERENCES DB_USERS(user_id),
    UNIQUE (user_id, object_name, permission_type)
);
CREATE TABLE ANOMALY_ALERTS (
    alert_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER,
    activity_type VARCHAR2(50),
    description VARCHAR2(500),
    risk_level VARCHAR2(20),
    detected_at DATE DEFAULT SYSDATE,
    alert_status VARCHAR2(20) DEFAULT 'OPEN',
    FOREIGN KEY (user_id) REFERENCES DB_USERS(user_id)
);
