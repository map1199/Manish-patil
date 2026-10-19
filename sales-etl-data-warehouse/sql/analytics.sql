-- 1. Monthly revenue
SELECT d.year, d.month, d.month_name, ROUND(SUM(f.total_amount), 2) AS revenue
FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 2. Revenue by product category
SELECT p.category, ROUND(SUM(f.total_amount), 2) AS revenue, SUM(f.quantity) AS units_sold
FROM fact_sales f JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;

-- 3. Top 5 cities by revenue
SELECT c.city, ROUND(SUM(f.total_amount), 2) AS revenue
FROM fact_sales f JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.city
ORDER BY revenue DESC
LIMIT 5;

-- 4. Top 10 customers (window function ranking)
SELECT customer_name, revenue, RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM (
    SELECT c.customer_name, ROUND(SUM(f.total_amount), 2) AS revenue
    FROM fact_sales f JOIN dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_name
)
ORDER BY revenue_rank
LIMIT 10;

-- 5. Month-over-month growth (CTE + LAG)
WITH monthly AS (
    SELECT d.year, d.month, SUM(f.total_amount) AS revenue
    FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year, d.month
)
SELECT year, month, ROUND(revenue, 2) AS revenue,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY year, month))
             * 100.0 / LAG(revenue) OVER (ORDER BY year, month), 2) AS mom_growth_pct
FROM monthly
ORDER BY year, month;
