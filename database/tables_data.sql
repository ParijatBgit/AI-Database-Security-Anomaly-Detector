INSERT INTO DB_USERS
(username, user_role, department, account_status)
VALUES ('Rahul', 'STUDENT', 'CSE', 'ACTIVE');
INSERT INTO DB_USERS
(username, user_role, department, account_status)
VALUES ('Amit', 'FACULTY', 'IT', 'ACTIVE');
INSERT INTO DB_USERS
(username, user_role, department, account_status)
VALUES ('Priya', 'STUDENT', 'ECE', 'ACTIVE');
INSERT INTO DB_USERS
(username, user_role, department, account_status)
VALUES ('Sneha', 'RESEARCHER', 'CSE', 'ACTIVE');
INSERT INTO DB_USERS
(username, user_role, department, account_status)
VALUES ('Admin', 'ADMIN', 'ADMINISTRATION', 'ACTIVE');
INSERT INTO DB_USERS
(username, user_role, department, account_status)
VALUES ('Rohan', 'STUDENT', 'CSE', 'ACTIVE');


INSERT INTO LOGIN_HISTORY
(user_id, login_time, logout_time, ip_address)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    SYSDATE-1, SYSDATE-1+1/24, '192.168.1.10'
);
INSERT INTO LOGIN_HISTORY
(user_id, login_time, logout_time, ip_address)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Amit'),
    SYSDATE-2, SYSDATE-2+2/24, '192.168.1.11'
);
INSERT INTO LOGIN_HISTORY
(user_id, login_time, logout_time, ip_address)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Priya'),
    SYSDATE-1/2, SYSDATE-1/2+1/24, '192.168.1.12'
);
INSERT INTO LOGIN_HISTORY
(user_id, login_time, logout_time, ip_address)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Sneha'),
    SYSDATE-3, SYSDATE-3+3/24, '192.168.1.13'
);
INSERT INTO LOGIN_HISTORY
(user_id, login_time, logout_time, ip_address)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Admin'),
    SYSDATE-1/4, SYSDATE-1/4+2/24, '192.168.1.14'
);
INSERT INTO LOGIN_HISTORY
(user_id, login_time, logout_time, ip_address)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rohan'),
    SYSDATE-2, SYSDATE-2+1/24, '192.168.1.15'
);


INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    'STUDENTS', 'SELECT'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    'MARKS', 'SELECT'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Amit'),
    'STUDENTS', 'SELECT'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Amit'),
    'STUDENTS', 'UPDATE'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Priya'),
    'STUDENTS', 'SELECT'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Sneha'),
    'RESEARCH', 'SELECT'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Admin'),
    'STUDENTS', 'ALL'
);
INSERT INTO USER_PERMISSIONS
(user_id, object_name, permission_type)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rohan'),
    'STUDENTS', 'SELECT'
);



INSERT INTO LOGIN_FAILURES
(user_id, attempted_username, failure_reason)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    'Rahul', 'Incorrect Password'
);
INSERT INTO LOGIN_FAILURES
(user_id, attempted_username, failure_reason)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Amit'),
    'Amit', 'Incorrect Password'
);
INSERT INTO LOGIN_FAILURES
(user_id, attempted_username, failure_reason)
VALUES (
    NULL, 'UnknownUser', 'Invalid Username'
);
INSERT INTO LOGIN_FAILURES
(user_id, attempted_username, failure_reason)
VALUES (
    NULL, 'UnknownUser', 'Invalid Username'
);


INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    'SELECT', 'STUDENTS', 'SELECT * FROM STUDENTS',
    10, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    'SELECT', 'MARKS', 'SELECT * FROM MARKS',
    5, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Amit'),
    'UPDATE', 'STUDENTS', 'UPDATE STUDENTS SET STATUS=1',
    3, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Priya'),
    'SELECT', 'STUDENTS', 'SELECT NAME FROM STUDENTS',
    8, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Sneha'),
    'SELECT', 'RESEARCH', 'SELECT * FROM RESEARCH',
    20, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Admin'),
    'DELETE', 'STUDENTS', 'DELETE FROM STUDENTS WHERE ID=5',
    1, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rohan'),
    'SELECT', 'STUDENTS', 'SELECT * FROM STUDENTS',
    10, 'SUCCESS'
);
INSERT INTO QUERY_LOGS
(user_id, query_type, object_name, query_text,
 rows_affected, access_status)
VALUES (
    (SELECT user_id FROM DB_USERS WHERE username='Rahul'),
    'SELECT', 'STUDENTS', 'SELECT ID FROM STUDENTS',
    10, 'SUCCESS'
);
