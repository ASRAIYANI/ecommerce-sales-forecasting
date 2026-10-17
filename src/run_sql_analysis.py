from pathlib import Path
import sqlite3
import pandas as pd


BASE = Path(__file__).resolve().parents[1]

DATABASE_PATH = BASE / "data" / "ecommerce.db"
REPORTS_PATH = BASE / "reports"


# --------------------------------------------------
# Connect to SQLite database
# --------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

print("=" * 60)
print("SQL BUSINESS ANALYSIS")
print("=" * 60)


# --------------------------------------------------
# 1. Overall KPIs
# --------------------------------------------------

overall_query = """
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
"""

overall = pd.read_sql_query(
    overall_query,
    connection
)

print("\nOVERALL KPIs")
print("-" * 60)
print(overall.to_string(index=False))


# --------------------------------------------------
# 2. Yearly performance + YoY growth
# --------------------------------------------------

yearly_query = """
WITH yearly_sales AS (
    SELECT
        CAST(strftime('%Y', order_date) AS INTEGER) AS year,
        COUNT(DISTINCT order_id) AS orders,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM orders
    GROUP BY year
),

yearly_growth AS (
    SELECT
        *,
        LAG(revenue) OVER (
            ORDER BY year
        ) AS previous_year_revenue
    FROM yearly_sales
)

SELECT
    year,
    orders,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,

    ROUND(
        profit * 100.0 / revenue,
        2
    ) AS profit_margin_pct,

    ROUND(
        (
            (revenue - previous_year_revenue)
            / previous_year_revenue
        ) * 100,
        2
    ) AS yoy_revenue_growth_pct

FROM yearly_growth
ORDER BY year;
"""

yearly = pd.read_sql_query(
    yearly_query,
    connection
)

print("\nYEARLY PERFORMANCE")
print("-" * 60)
print(yearly.to_string(index=False))


# --------------------------------------------------
# 3. Category performance
# --------------------------------------------------

category_query = """
SELECT
    category,

    COUNT(DISTINCT order_id)
        AS orders,

    SUM(quantity)
        AS units_sold,

    ROUND(SUM(revenue), 2)
        AS revenue,

    ROUND(SUM(profit), 2)
        AS profit,

    ROUND(
        SUM(profit) * 100.0
        / SUM(revenue),
        2
    ) AS profit_margin_pct,

    ROUND(
        SUM(revenue) * 100.0
        / (
            SELECT SUM(revenue)
            FROM orders
        ),
        2
    ) AS revenue_share_pct

FROM orders
GROUP BY category
ORDER BY revenue DESC;
"""

category = pd.read_sql_query(
    category_query,
    connection
)

print("\nCATEGORY PERFORMANCE")
print("-" * 60)
print(category.to_string(index=False))


# --------------------------------------------------
# 4. Top products
# --------------------------------------------------

product_query = """
SELECT
    product,
    category,

    COUNT(DISTINCT order_id)
        AS orders,

    SUM(quantity)
        AS units_sold,

    ROUND(SUM(revenue), 2)
        AS revenue,

    ROUND(SUM(profit), 2)
        AS profit,

    ROUND(
        SUM(profit) * 100.0
        / SUM(revenue),
        2
    ) AS profit_margin_pct

FROM orders
GROUP BY product, category
ORDER BY revenue DESC;
"""

products = pd.read_sql_query(
    product_query,
    connection
)

print("\nTOP PRODUCTS")
print("-" * 60)

print(
    products.head(10)
    .to_string(index=False)
)


# --------------------------------------------------
# 5. Regional performance
# --------------------------------------------------

region_query = """
SELECT
    region,

    COUNT(DISTINCT order_id)
        AS orders,

    SUM(quantity)
        AS units_sold,

    ROUND(SUM(revenue), 2)
        AS revenue,

    ROUND(SUM(profit), 2)
        AS profit,

    ROUND(
        SUM(profit) * 100.0
        / SUM(revenue),
        2
    ) AS profit_margin_pct

FROM orders
GROUP BY region
ORDER BY revenue DESC;
"""

region = pd.read_sql_query(
    region_query,
    connection
)

print("\nREGIONAL PERFORMANCE")
print("-" * 60)
print(region.to_string(index=False))


# --------------------------------------------------
# 6. Sales channel performance
# --------------------------------------------------

channel_query = """
SELECT
    sales_channel,

    COUNT(DISTINCT order_id)
        AS orders,

    SUM(quantity)
        AS units_sold,

    ROUND(SUM(revenue), 2)
        AS revenue,

    ROUND(SUM(profit), 2)
        AS profit,

    ROUND(
        SUM(profit) * 100.0
        / SUM(revenue),
        2
    ) AS profit_margin_pct

FROM orders
GROUP BY sales_channel
ORDER BY revenue DESC;
"""

channel = pd.read_sql_query(
    channel_query,
    connection
)

print("\nSALES CHANNEL PERFORMANCE")
print("-" * 60)
print(channel.to_string(index=False))


# --------------------------------------------------
# 7. Monthly performance
# --------------------------------------------------

monthly_query = """
SELECT
    strftime(
        '%Y-%m',
        order_date
    ) AS month,

    COUNT(DISTINCT order_id)
        AS orders,

    SUM(quantity)
        AS units_sold,

    ROUND(SUM(revenue), 2)
        AS revenue,

    ROUND(SUM(profit), 2)
        AS profit

FROM orders
GROUP BY month
ORDER BY month;
"""

monthly = pd.read_sql_query(
    monthly_query,
    connection
)


# --------------------------------------------------
# Save SQL-generated reports
# --------------------------------------------------

overall.to_csv(
    REPORTS_PATH / "sql_overall_kpis.csv",
    index=False
)

yearly.to_csv(
    REPORTS_PATH / "sql_yearly_performance.csv",
    index=False
)

category.to_csv(
    REPORTS_PATH / "sql_category_performance.csv",
    index=False
)

products.to_csv(
    REPORTS_PATH / "sql_product_performance.csv",
    index=False
)

region.to_csv(
    REPORTS_PATH / "sql_region_performance.csv",
    index=False
)

channel.to_csv(
    REPORTS_PATH / "sql_channel_performance.csv",
    index=False
)

monthly.to_csv(
    REPORTS_PATH / "sql_monthly_performance.csv",
    index=False
)


# --------------------------------------------------
# Close connection
# --------------------------------------------------

connection.close()


print("\n" + "=" * 60)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Saved SQL reports:")
print("reports/sql_overall_kpis.csv")
print("reports/sql_yearly_performance.csv")
print("reports/sql_category_performance.csv")
print("reports/sql_product_performance.csv")
print("reports/sql_region_performance.csv")
print("reports/sql_channel_performance.csv")
print("reports/sql_monthly_performance.csv")