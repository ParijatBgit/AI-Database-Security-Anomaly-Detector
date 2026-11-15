ALTER TABLE DB_USERS
ADD CONSTRAINT chk_account_status
CHECK (account_status IN ('ACTIVE', 'INACTIVE', 'LOCKED'));
ALTER TABLE DB_USERS
ADD CONSTRAINT chk_user_role
CHECK (user_role IN ('STUDENT', 'FACULTY', 'RESEARCHER', 'ADMIN'));


ALTER TABLE LOGIN_HISTORY
ADD CONSTRAINT chk_login_time
CHECK (logout_time IS NULL OR logout_time >= login_time);


ALTER TABLE QUERY_LOGS
ADD CONSTRAINT chk_query_type
CHECK (query_type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE'));
ALTER TABLE QUERY_LOGS
ADD CONSTRAINT chk_access_status
CHECK (access_status IN ('SUCCESS', 'DENIED'));
ALTER TABLE QUERY_LOGS
ADD CONSTRAINT chk_rows_affected
CHECK (rows_affected IS NULL OR rows_affected >= 0);


ALTER TABLE USER_PERMISSIONS
ADD CONSTRAINT chk_permission_type
CHECK (permission_type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'ALL'));


ALTER TABLE ANOMALY_ALERTS
ADD CONSTRAINT chk_risk_level
CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH'));
ALTER TABLE ANOMALY_ALERTS
ADD CONSTRAINT chk_alert_status
CHECK (alert_status IN ('OPEN', 'RESOLVED'));
