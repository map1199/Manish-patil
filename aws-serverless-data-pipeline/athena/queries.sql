-- Revenue by category
SELECT category, ROUND(SUM(total_amount), 2) AS revenue
FROM sales_db.clean_sales
GROUP BY category
ORDER BY revenue DESC;

-- Monthly revenue
SELECT date_trunc('month', order_date) AS month, ROUND(SUM(total_amount), 2) AS revenue
FROM sales_db.clean_sales
GROUP BY 1
ORDER BY 1;

-- Top 5 cities
SELECT city, ROUND(SUM(total_amount), 2) AS revenue
FROM sales_db.clean_sales
GROUP BY city
ORDER BY revenue DESC
LIMIT 5;
