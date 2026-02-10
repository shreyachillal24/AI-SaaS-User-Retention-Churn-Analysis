CREATE DATABASE ai_saas_analytics;
USE ai_saas_analytics;

drop table subscriptions_raw;
CREATE TABLE users_raw (
    user_id INT,
    signup_date DATETIME,
    country VARCHAR(50),
    acquisition_channel VARCHAR(50)
);
SET GLOBAL local_infile = 0;

DROP TABLE IF EXISTS subscriptions_raw;

CREATE TABLE subscriptions_raw (
    subscription_id INT,
    user_id INT,
    plan_type VARCHAR(20),
    start_date DATETIME,
    end_date VARCHAR(30),   -- TEMPORARY, ON PURPOSE
    status VARCHAR(20)
);


CREATE TABLE sessions_raw (
    session_id INT,
    user_id INT,
    session_start DATETIME,
    session_end DATETIME,
    device_type VARCHAR(20)
);
CREATE TABLE feature_usage_raw (
    usage_id INT,
    session_id INT,
    feature_name VARCHAR(50),
    usage_count INT
);
CREATE TABLE error_logs_raw (
    error_id INT,
    session_id INT,
    error_type VARCHAR(50),
    error_time DATETIME
);


CREATE TABLE feedback_raw (
    feedback_id INT,
    user_id INT,
    rating INT,
    comment TEXT,
    feedback_date DATETIME
);
/*Data import using the table wizard */
select count(*) from users_raw;
select count(*) from subscriptions_raw;


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/subscriptions_raw.csv'
INTO TABLE subscriptions_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

UPDATE subscriptions_raw
SET end_date = NULL
WHERE end_date = '' OR end_date = 'NaT';

ALTER TABLE subscriptions_raw
MODIFY end_date DATETIME NULL;


DROP TABLE IF EXISTS sessions_raw;

CREATE TABLE sessions_raw (
    session_id INT,
    user_id INT,
    session_start DATETIME,
    session_end VARCHAR(30),   -- TEMPORARY ON PURPOSE
    device_type VARCHAR(20)
);

SHOW VARIABLES LIKE 'secure_file_priv';



LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sessions_raw.csv'
INTO TABLE sessions_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SET SQL_SAFE_UPDATES = 0;
UPDATE sessions_raw
SET session_end = NULL
WHERE session_end = '' OR session_end = 'NaT';
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE sessions_raw
MODIFY session_end DATETIME NULL;

select count(1) from sessions_raw;


LOAD DATA INFILE
"C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/feature_usage_raw.csv"
INTO TABLE feature_usage_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

select count(1) from feature_usage_raw;



DROP TABLE IF EXISTS error_logs_raw;

CREATE TABLE error_logs_raw (
    error_id INT,
    session_id INT,
    error_type VARCHAR(50),
    error_time VARCHAR(30)   -- TEMPORARY ON PURPOSE
);

LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/error_logs_raw.csv'
INTO TABLE error_logs_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SET SQL_SAFE_UPDATES = 0;

UPDATE error_logs_raw
SET error_time = NULL
WHERE error_time = '' OR error_time = 'NaT';

SET SQL_SAFE_UPDATES = 1;

ALTER TABLE error_logs_raw
MODIFY error_time DATETIME NULL;

SELECT
    COUNT(*) AS total_rows,
    SUM(error_time IS NULL) AS null_error_times
FROM error_logs_raw;


drop table if exists feedback_raw;
CREATE TABLE feedback_raw (
    feedback_id INT,
    user_id INT,
    rating INT,
    comment TEXT,
    feedback_date varchar(50)
);


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/feedback_raw.csv'
INTO TABLE feedback_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


SET SQL_SAFE_UPDATES = 0;

UPDATE feedback_raw
SET feedback_date = NULL
WHERE feedback_date = '' OR feedback_date = 'NaT';

SET SQL_SAFE_UPDATES = 1;

ALTER TABLE feedback_raw
MODIFY feedback_date DATETIME NULL;

select count(1) from feedback_raw;

