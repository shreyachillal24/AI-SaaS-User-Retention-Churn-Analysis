/*total_users,churned_users,churn rate*/ /*uage-->KPI CARDS*/
CREATE OR REPLACE VIEW vw_churn_overview AS
SELECT 
    COUNT(*) AS total_users,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS churned_users,
    ROUND(
        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM clean_subscriptions;


/*CHURN BY PLAN*/
CREATE OR REPLACE VIEW vw_churn_by_plan AS
SELECT 
    plan_type,
    COUNT(*) AS total_users,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS churned_users,
    ROUND(
        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM clean_subscriptions
GROUP BY plan_type;


/*ACTIVITY LEVEL OF ACTIVE AND CHURNED USER*/
CREATE OR REPLACE VIEW vw_engagement_by_status AS
SELECT 
    s.status,
    COUNT(DISTINCT s.user_id) AS total_users,
    COUNT(cs.session_id) AS total_sessions,
    ROUND(
        COUNT(cs.session_id) * 1.0 / COUNT(DISTINCT s.user_id),
        2
    ) AS avg_sessions_per_user
FROM clean_subscriptions s
LEFT JOIN clean_sessions cs 
    ON s.user_id = cs.user_id
GROUP BY s.status;

/*FEATURE USAGE BY STATUS*/
CREATE OR REPLACE VIEW vw_feature_usage_by_status AS
SELECT 
    s.status,
    SUM(cf.usage_count) AS total_usage,
    COUNT(DISTINCT s.user_id) AS total_users,
    ROUND(
        SUM(cf.usage_count) * 1.0 / COUNT(DISTINCT s.user_id),
        2
    ) AS avg_usage_per_user
FROM clean_subscriptions s
LEFT JOIN clean_sessions cs 
    ON s.user_id = cs.user_id
LEFT JOIN clean_feature_usage cf 
    ON cs.session_id = cf.session_id
GROUP BY s.status;


/*ERROR PER USER COMPARISION */
CREATE OR REPLACE VIEW vw_error_impact_by_status AS
SELECT 
    s.status,
    COUNT(ce.error_id) AS total_errors,
    COUNT(DISTINCT s.user_id) AS total_users,
    ROUND(
        COUNT(ce.error_id) * 1.0 / COUNT(DISTINCT s.user_id),
        2
    ) AS errors_per_user
FROM clean_subscriptions s
LEFT JOIN clean_sessions cs 
    ON s.user_id = cs.user_id
LEFT JOIN clean_error_logs ce 
    ON cs.session_id = ce.session_id
GROUP BY s.status;

/*total errors per total sessions*/
CREATE OR REPLACE VIEW vw_errors_per_session_by_status AS
SELECT 
    s.status,
    COUNT(DISTINCT cs.session_id) AS total_sessions,
    COUNT(ce.error_id) AS total_errors,
    ROUND(
        COUNT(ce.error_id) * 1.0 / COUNT(DISTINCT cs.session_id),
        3
    ) AS errors_per_session
FROM clean_subscriptions s
LEFT JOIN clean_sessions cs 
    ON s.user_id = cs.user_id
LEFT JOIN clean_error_logs ce 
    ON cs.session_id = ce.session_id
GROUP BY s.status;

/*user_dimension*/
CREATE OR REPLACE VIEW vw_user_dimension AS
SELECT 
    u.user_id,
    u.country,
    s.status,
    s.plan_type
FROM clean_users u
JOIN clean_subscriptions s
ON u.user_id = s.user_id;

/*feature usage*/
CREATE OR REPLACE VIEW vw_feature_usage_by_feature_status AS
SELECT 
    cf.feature_name,
    s.status,
    SUM(cf.usage_count) AS total_usage
FROM clean_feature_usage cf
JOIN clean_sessions cs 
    ON cf.session_id = cs.session_id
JOIN clean_subscriptions s 
    ON cs.user_id = s.user_id
GROUP BY cf.feature_name, s.status;


SELECT * FROM vw_churn_overview;
SELECT * FROM vw_churn_by_plan;
SELECT * FROM vw_engagement_by_status;
SELECT * FROM vw_feature_usage_by_status;
SELECT * FROM vw_error_impact_by_status;
SELECT * FROM vw_errors_per_session_by_status;
SELECT * FROM vw_user_dimension;
SELECT * FROM vw_feature_usage_by_feature_status;
