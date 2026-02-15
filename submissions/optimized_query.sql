   
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
