/*users_raw-->clean_users*/
CREATE OR REPLACE VIEW clean_users AS
SELECT
    user_id,
    signup_date,
    COALESCE(country, 'Unknown') AS country,
    CASE
        WHEN LOWER(acquisition_channel) LIKE '%organic%' THEN 'Organic'
        WHEN LOWER(acquisition_channel) LIKE '%paid%' THEN 'Paid Ads'
        WHEN LOWER(acquisition_channel) LIKE '%referral%' THEN 'Referral'
        WHEN LOWER(acquisition_channel) LIKE '%partner%' THEN 'Partnership'
        ELSE 'Unknown'
    END AS acquisition_channel
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY signup_date) AS rn
    FROM users_raw
) t
WHERE rn = 1;

CREATE OR REPLACE VIEW clean_users AS
SELECT
    user_id,
    signup_date,
    CASE
        WHEN country IS NULL OR TRIM(country) = '' THEN 'Others'
        ELSE country
    END AS country,
    acquisition_channel
FROM users_raw;

SELECT COUNT(*) FROM clean_users;

/*subscriptions_raw ---> subscriptions_clean */
select * from subscriptions_raw;
select count(1) from subscriptions_raw;

create or replace view clean_subscriptions as 
select subscription_id,user_id,
		case when lower(plan_type) like '%free%' then 'Free' 
			 when lower(plan_type) like '%pro%' then 'Pro'
             when lower(plan_type) like '%team%' then 'Team'
             else 'Free' end as plan_type,
             start_date,end_date,
             case when lower(status) like '%cancelled%' then 'Cancelled' 
             else 'Active' end as status
from subscriptions_raw;   

select * from clean_subscriptions;
select count(*) from clean_subscriptions;
select distinct plan_type from clean_subscriptions;         


/*sessions_raw --> clean_sessions*/
select count(1) from sessions_raw;
select * from sessions_raw;

create or replace view  clean_sessions as
select session_id,user_id,session_start,session_end,
		case when lower(device_type) like '%mobile%' then 'Mobile' 
			 when lower(device_type) like '%tablet%' then 'Tablet' 
             when lower(device_type) like '%web%' then 'Web' 
             else 'Unknown'
             end as device_type
from sessions_raw;  

select count(1) from clean_sessions ;
select  * from clean_sessions;
select distinct device_type from clean_sessions;           



/*feature_usage_raw ---> clean_feature_usage */
select count(1) from feature_usage_raw;
select * from feature_usage_raw;

CREATE OR REPLACE VIEW clean_feature_usage AS
SELECT
    usage_id,
    session_id,

    CASE
        WHEN LOWER(feature_name) LIKE '%chat%' THEN 'AI_Chat'
        WHEN LOWER(feature_name) LIKE '%rewrite%' THEN 'AI_Rewrite'
        WHEN LOWER(feature_name) LIKE '%summarize%' THEN 'AI_Summarize'
        WHEN LOWER(feature_name) LIKE '%grammar%' THEN 'Grammar_Check'
        WHEN LOWER(feature_name) LIKE '%plagiarism%' THEN 'Plagiarism_Check'
        WHEN LOWER(feature_name) LIKE '%export%' THEN 'Export_PDF'
        WHEN LOWER(feature_name) LIKE '%setting%' THEN 'Settings'
        ELSE 'Other'
    END AS feature_name,

    usage_count
FROM feature_usage_raw
WHERE usage_count > 0;

select  distinct feature_name from clean_feature_usage;


/*error_logs_raw ---> clean_error_logs*/
select count(1) from error_logs_raw;
select * from error_logs_raw;

CREATE OR REPLACE VIEW clean_error_logs AS
SELECT
    error_id,
    session_id,

    CASE
        WHEN LOWER(error_type) LIKE '%timeout%' THEN 'Timeout'
        WHEN LOWER(error_type) LIKE '%rate%' THEN 'Rate_Limit'
        WHEN LOWER(error_type) LIKE '%model%' THEN 'Model_Error'
        WHEN LOWER(error_type) LIKE '%ui%' THEN 'UI_Bug'
        ELSE 'Other'
    END AS error_type,

    error_time

FROM error_logs_raw;

select distinct error_type from clean_error_logs;

/*feedback_raw --- > clean_feedback*/
select count(1) from feedback_raw;
select * from feedback_raw;

CREATE OR REPLACE VIEW clean_feedback AS
SELECT
    feedback_id,
    user_id,

    CASE
        WHEN rating BETWEEN 1 AND 5 THEN rating
        ELSE NULL
    END AS rating,

    CASE
        WHEN comment IS NULL OR TRIM(comment) = '' THEN 'No Comment'
        ELSE comment
    END AS comment,

    feedback_date

FROM feedback_raw;

SELECT MIN(rating), MAX(rating) FROM clean_feedback;
select * from clean_feedback ;
