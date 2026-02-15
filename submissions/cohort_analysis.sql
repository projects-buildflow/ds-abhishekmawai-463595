-- Cohort analysis: group customers by first purchase month, show retention for months 0–5.
-- Compatible with SQLite (use STRFTIME). For PostgreSQL, replace STRFTIME('%Y-%m', x) with TO_CHAR(x, 'YYYY-MM').

WITH first_orders AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date
    FROM orders
    GROUP BY customer_id
),
order_cohorts AS (
    SELECT
        o.customer_id,
        STRFTIME('%Y-%m', fo.first_order_date) AS cohort_month,
        (CAST(STRFTIME('%Y', o.order_date) AS INT) * 12 + CAST(STRFTIME('%m', o.order_date) AS INT))
        - (CAST(STRFTIME('%Y', fo.first_order_date) AS INT) * 12 + CAST(STRFTIME('%m', fo.first_order_date) AS INT)) AS months_since
    FROM orders o
    JOIN first_orders fo ON o.customer_id = fo.customer_id
)
SELECT
    cohort_month,
    COUNT(DISTINCT CASE WHEN months_since = 0 THEN customer_id END) AS month_0,
    COUNT(DISTINCT CASE WHEN months_since = 1 THEN customer_id END) AS month_1,
    COUNT(DISTINCT CASE WHEN months_since = 2 THEN customer_id END) AS month_2,
    COUNT(DISTINCT CASE WHEN months_since = 3 THEN customer_id END) AS month_3,
    COUNT(DISTINCT CASE WHEN months_since = 4 THEN customer_id END) AS month_4,
    COUNT(DISTINCT CASE WHEN months_since = 5 THEN customer_id END) AS month_5
FROM order_cohorts
GROUP BY cohort_month
ORDER BY cohort_month;
