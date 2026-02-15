## Original Problems

1. **Deeply nested IN subqueries (lines 4-18):** The original
   query had 4 levels of nested IN subqueries to connect customers →
   orders → order_items → products → categories. Each level forces
   the database to re-execute the inner query for every row in the
   outer query, resulting in redundant full table scans.

2. **Correlated subquery in ORDER BY (lines 19-22):** The ORDER BY
   clause contained a subquery that recalculated `SUM(o3.total)` for
   every customer row. This means the orders table was scanned once
   per result row just for sorting.

3. **SELECT \* on the outer query (line 2):** Using `SELECT *`
   retrieves all columns from the customers table, including ones not
   needed. This increases I/O and memory usage.

4. **DATE() function on indexed columns (lines 7, 14):** Wrapping
   `signup_date` and `order_date` in `DATE()` prevents the database
   from using indexes on those columns, forcing full table scans
   instead of efficient index lookups.

5. **Redundant AVG calculation:** The average order total was
   computed inside a WHERE clause subquery, meaning it could be
   recalculated for each row comparison rather than once.

## Changes Made

1. **Replaced nested subqueries with CTEs and JOINs:** Broke the
   query into five logical CTEs (`avg_order_total`,
   `electronics_products`, `electronics_orders`,
   `high_value_customers`, `customer_totals`). Each CTE is computed
   once and referenced by name, eliminating redundant table scans.

2. **Pre-computed the AVG in its own CTE:** The average order
   total is now calculated once in `avg_order_total` and joined via
   CROSS JOIN, instead of being recalculated inside a WHERE clause.

3. **Pre-computed customer totals:** Moved the correlated ORDER BY
   subquery into the `customer_totals` CTE, which computes the sum
   once per customer using GROUP BY instead of per-row.

4. **Replaced SELECT \* with explicit columns:** Only selecting
   `customer_id`, `name`, `email`, and `signup_date`.

5. **Removed DATE() wrapping:** Changed `DATE(c.signup_date) >=
DATE('2022-01-01')` to `c.signup_date >= '2022-01-01'`, allowing
   index usage on the column.

## Expected Performance Improvement

The original query performs multiple correlated scans of the
orders table (once per nesting level, plus once per row for
sorting). The optimized version scans each table at most once via
CTEs and JOINs. On large datasets this should reduce execution
time from 30+ seconds to under 1 second.
