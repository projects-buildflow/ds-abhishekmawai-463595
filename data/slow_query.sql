-- Deliberately inefficient query for Task 3.3: Query Optimization
-- Your job: identify the performance problems and create an optimized version.
--
-- This query attempts to find high-value customers with their order history
-- and product preferences. It has multiple performance issues.

SELECT *
FROM customers c
WHERE c.customer_id IN (
    SELECT o.customer_id
    FROM orders o
    WHERE o.total > (
        SELECT AVG(o2.total)
        FROM orders o2
        WHERE DATE(o2.order_date) >= DATE('2023-01-01')
    )
    AND o.order_id IN (
        SELECT oi.order_id
        FROM order_items oi
        WHERE oi.product_id IN (
            SELECT p.id
            FROM products p
            WHERE p.category_id IN (
                SELECT cat.id
                FROM categories cat
                WHERE cat.name LIKE '%Electronics%'
            )
        )
    )
)
AND DATE(c.signup_date) >= DATE('2022-01-01')
ORDER BY (
    SELECT SUM(o3.total)
    FROM orders o3
    WHERE o3.customer_id = c.customer_id
) DESC;
