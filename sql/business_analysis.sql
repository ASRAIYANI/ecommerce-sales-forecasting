-- ============================================================
-- E-commerce Sales Forecasting & Business Analytics
-- SQL Business Analysis
-- ============================================================
-- Database: ecommerce.db
-- Table: orders
-- Dataset: Synthetic portfolio dataset
-- ============================================================


-- ------------------------------------------------------------
-- 1. OVERALL BUSINESS KPIs
-- ------------------------------------------------------------

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM orders;


-- ------------------------------------------------------------
-- 2. YEARLY BUSINESS PERFORMANCE
-- ------------------------------------------------------------

SELECT
    CAST(strftime('%Y', order_date) AS INTEGER) AS year,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY year
ORDER BY year;


-- ------------------------------------------------------------
-- 3. MONTHLY REVENUE AND PROFIT
-- ------------------------------------------------------------

SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM orders
GROUP BY month
ORDER BY month;


-- ------------------------------------------------------------
-- 4. CATEGORY PERFORMANCE
-- ------------------------------------------------------------

SELECT
    category,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct,
    ROUND(
        SUM(revenue) * 100.0 /
        (SELECT SUM(revenue) FROM orders),
        2
    ) AS revenue_share_pct
FROM orders
GROUP BY category
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- 5. TOP PRODUCTS BY REVENUE
-- ------------------------------------------------------------

SELECT
    product,
    category,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 6. REGIONAL PERFORMANCE
-- ------------------------------------------------------------

SELECT
    region,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY region
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- 7. SALES CHANNEL PERFORMANCE
-- ------------------------------------------------------------

SELECT
    sales_channel,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY sales_channel
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- 8. DISCOUNT PERFORMANCE
-- ------------------------------------------------------------

SELECT
    ROUND(discount * 100, 0) AS discount_pct,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY discount
ORDER BY discount;


-- ------------------------------------------------------------
-- 9. TOP 5 MOST PROFITABLE PRODUCTS
-- ------------------------------------------------------------

SELECT
    product,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(revenue),
        2
    ) AS profit_margin_pct
FROM orders
GROUP BY product
ORDER BY profit DESC
LIMIT 5;


-- ------------------------------------------------------------
-- 10. YEAR-OVER-YEAR REVENUE GROWTH
-- Demonstrates SQL window functions using LAG()
-- ------------------------------------------------------------

WITH yearly_sales AS (
    SELECT
        CAST(strftime('%Y', order_date) AS INTEGER) AS year,
        SUM(revenue) AS revenue
    FROM orders
    GROUP BY year
),

growth AS (
    SELECT
        year,
        revenue,
        LAG(revenue) OVER (
            ORDER BY year
        ) AS previous_year_revenue
    FROM yearly_sales
)

SELECT
    year,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_year_revenue, 2)
        AS previous_year_revenue,
    ROUND(
        (
            (revenue - previous_year_revenue)
            / previous_year_revenue
        ) * 100,
        2
    ) AS yoy_revenue_growth_pct
FROM growth
ORDER BY year;