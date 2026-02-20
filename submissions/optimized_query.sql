   
  -- Optimized query for Task 3.3: Query Optimization               
  -- Same logic as data/slow_query.sql, using CTEs and JOINs instead
  --- of nested subqueries.                                            
                  
  WITH avg_order_total AS (
      SELECT AVG(total) AS avg_total
      FROM orders
      WHERE order_date >= '2023-01-01'
  ),
  electronics_products AS (
      SELECT p.id AS product_id
      FROM products p
      INNER JOIN categories cat ON p.category_id = cat.id
      WHERE cat.name LIKE '%Electronics%'
  ),
  electronics_orders AS (
      SELECT DISTINCT oi.order_id
      FROM order_items oi
      INNER JOIN electronics_products ep ON oi.product_id = ep.product_id
  ),
  high_value_customers AS (
      SELECT DISTINCT o.customer_id
      FROM orders o
      INNER JOIN electronics_orders eo ON o.order_id = eo.order_id
      CROSS JOIN avg_order_total aot
      WHERE o.total > aot.avg_total
  ),
  customer_totals AS (
      SELECT o.customer_id, SUM(o.total) AS total_order_value
      FROM orders o
      INNER JOIN high_value_customers hvc ON o.customer_id = hvc.customer_id
      GROUP BY o.customer_id
  )
  SELECT c.customer_id, c.first_name, c.last_name, c.email, c.signup_date
  FROM customers c
  INNER JOIN customer_totals ct ON c.customer_id = ct.customer_id
  WHERE c.signup_date >= '2022-01-01'
  ORDER BY ct.total_order_value DESC
