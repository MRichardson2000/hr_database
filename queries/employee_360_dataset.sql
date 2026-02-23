WITH employee_details AS (
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        e.hire_date,
        d.name AS department_name,
        j.title AS job_title,
        s.effective_date,
        s.amount AS salary,
        l.country,
        l.city
    FROM employees e
    LEFT JOIN departments d ON e.department_id = d.department_id
    LEFT JOIN jobs j ON e.job_id = j.job_id
    LEFT JOIN salaries s ON e.employee_id = s.employee_id
    LEFT JOIN locations l ON d.location_id = l.location_id
),

latest_salary AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY employee_id
            ORDER BY effective_date DESC
        ) AS rn
    FROM employee_details
),

filtered_latest AS (
    SELECT
        employee_id,
        first_name,
        last_name,
        hire_date,
        department_name,
        job_title,
        effective_date AS salary_effective_date,
        salary AS latest_salary,
        country,
        city
    FROM latest_salary
    WHERE rn = 1
),

salary_band AS (
    SELECT
        *,
        CASE 
            WHEN latest_salary > 80000 THEN 'Band 1'
            WHEN latest_salary BETWEEN 45000 AND 79000 THEN 'Band 2'
            WHEN latest_salary BETWEEN 30000 AND 44000 THEN 'Band 3'
            ELSE 'Band 4'
        END AS salary_band
    FROM filtered_latest
),

performance_metrics AS (
    SELECT
        employee_id,
        AVG(score) AS avg_performance_score,
        MAX(review_date) AS last_review_date
    FROM performance
    GROUP BY employee_id
),

last_score AS (
    SELECT
        p.employee_id,
        p.score AS last_performance_score
    FROM performance p
    INNER JOIN (
        SELECT employee_id, MAX(review_date) AS max_date
        FROM performance
        GROUP BY employee_id
    ) x ON p.employee_id = x.employee_id
       AND p.review_date = x.max_date
),

performance_trend AS (
    SELECT
        p.employee_id,
        CASE
            WHEN (SELECT AVG(score) 
                  FROM performance p2 
                  WHERE p2.employee_id = p.employee_id 
                    AND p2.review_date >= date('now', '-180 day'))
                 >
                 (SELECT AVG(score) 
                  FROM performance p3 
                  WHERE p3.employee_id = p.employee_id 
                    AND p3.review_date < date('now', '-180 day'))
            THEN 'Improving'
            WHEN (SELECT AVG(score) 
                  FROM performance p2 
                  WHERE p2.employee_id = p.employee_id 
                    AND p2.review_date >= date('now', '-180 day'))
                 <
                 (SELECT AVG(score) 
                  FROM performance p3 
                  WHERE p3.employee_id = p.employee_id 
                    AND p3.review_date < date('now', '-180 day'))
            THEN 'Declining'
            ELSE 'Stable'
        END AS performance_trend
    FROM performance p
    GROUP BY p.employee_id
),

attendance_metrics AS (
    SELECT
        employee_id,
        SUM(CASE WHEN status = 'Present' AND date >= date('now', '-90 day') THEN 1 ELSE 0 END) AS days_present_last_90,
        SUM(CASE WHEN status = 'Absent' AND date >= date('now', '-90 day') THEN 1 ELSE 0 END) AS days_absent_last_90,
        SUM(CASE WHEN status = 'Remote' AND date >= date('now', '-90 day') THEN 1 ELSE 0 END) AS days_remote_last_90,
        ROUND(
            CAST(SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS FLOAT) /
            NULLIF(COUNT(*), 0), 2
        ) AS attendance_rate
    FROM attendance
    GROUP BY employee_id
),

training_metrics AS (
    SELECT
        employee_id,
        COUNT(*) AS total_courses_completed,
        MAX(completion_date) AS last_training_date,
        CASE 
            WHEN MAX(completion_date) >= date('now', '-180 day') THEN 1
            ELSE 0
        END AS has_recent_training
    FROM training
    GROUP BY employee_id
),

project_metrics AS (
    SELECT
        employee_id,
        COUNT(*) AS number_of_projects,
        MAX(end_date) AS last_project_end_date
    FROM projects
    LEFT JOIN employees e ON projects.department_id = e.department_id
    GROUP BY employee_id
),

benefit_flags AS (
    SELECT
        employee_id,
        MAX(CASE WHEN benefit_type = 'Health' THEN 1 ELSE 0 END) AS has_health,
        MAX(CASE WHEN benefit_type = 'Dental' THEN 1 ELSE 0 END) AS has_dental,
        MAX(CASE WHEN benefit_type = 'Vision' THEN 1 ELSE 0 END) AS has_vision,
        MAX(CASE WHEN benefit_type = 'Retirement' THEN 1 ELSE 0 END) AS has_retirement
    FROM benefits
    GROUP BY employee_id
)

SELECT
    sb.*,
    pm.avg_performance_score,
    ls.last_performance_score,
    pt.performance_trend,
    am.days_present_last_90,
    am.days_absent_last_90,
    am.days_remote_last_90,
    am.attendance_rate,
    tm.total_courses_completed,
    tm.last_training_date,
    tm.has_recent_training,
    pr.number_of_projects,
    pr.last_project_end_date,
    bf.has_health,
    bf.has_dental,
    bf.has_vision,
    bf.has_retirement
FROM salary_band sb
LEFT JOIN performance_metrics pm ON sb.employee_id = pm.employee_id
LEFT JOIN last_score ls ON sb.employee_id = ls.employee_id
LEFT JOIN performance_trend pt ON sb.employee_id = pt.employee_id
LEFT JOIN attendance_metrics am ON sb.employee_id = am.employee_id
LEFT JOIN training_metrics tm ON sb.employee_id = tm.employee_id
LEFT JOIN project_metrics pr ON sb.employee_id = pr.employee_id
LEFT JOIN benefit_flags bf ON sb.employee_id = bf.employee_id;