from pathlib import Path
import pandas as pd


BASE = Path(__file__).resolve().parents[1]

DATA_PATH = BASE / "data" / "ecommerce_orders.csv"
REPORTS = BASE / "reports"


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["order_date"]
)

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.to_period("M").astype(str)


# --------------------------------------------------
# 2. Overall business KPIs
# --------------------------------------------------

total_orders = df["order_id"].nunique()
total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
total_quantity = df["quantity"].sum()

profit_margin = (
    total_profit / total_revenue * 100
)

average_order_value = (
    total_revenue / total_orders
)

average_items_per_order = (
    total_quantity / total_orders
)


print("=" * 60)
print("E-COMMERCE BUSINESS PERFORMANCE")
print("=" * 60)

print(f"Total Orders: {total_orders:,}")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Units Sold: {total_quantity:,}")
print(f"Average Order Value: {average_order_value:,.2f}")
print(
    f"Average Items per Order: "
    f"{average_items_per_order:.2f}"
)


# --------------------------------------------------
# 3. Yearly performance
# --------------------------------------------------

yearly = (
    df.groupby("year")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
    .reset_index()
)

yearly["profit_margin_pct"] = (
    yearly["profit"] /
    yearly["revenue"] * 100
)

yearly["revenue_growth_pct"] = (
    yearly["revenue"]
    .pct_change() * 100
)

yearly["profit_growth_pct"] = (
    yearly["profit"]
    .pct_change() * 100
)

print("\nYEARLY PERFORMANCE")
print("-" * 60)
print(yearly.round(2).to_string(index=False))


# --------------------------------------------------
# 4. Monthly KPIs
# --------------------------------------------------

monthly = (
    df.set_index("order_date")
    .resample("MS")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
)

monthly["profit_margin_pct"] = (
    monthly["profit"] /
    monthly["revenue"] * 100
)

monthly["average_order_value"] = (
    monthly["revenue"] /
    monthly["orders"]
)

monthly["revenue_growth_pct"] = (
    monthly["revenue"]
    .pct_change() * 100
)


# --------------------------------------------------
# 5. Category performance
# --------------------------------------------------

category = (
    df.groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
    .reset_index()
)

category["profit_margin_pct"] = (
    category["profit"] /
    category["revenue"] * 100
)

category["revenue_share_pct"] = (
    category["revenue"] /
    total_revenue * 100
)

category = category.sort_values(
    "revenue",
    ascending=False
)

print("\nCATEGORY PERFORMANCE")
print("-" * 60)
print(category.round(2).to_string(index=False))


# --------------------------------------------------
# 6. Product performance
# --------------------------------------------------

product = (
    df.groupby(["product", "category"])
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
    .reset_index()
)

product["profit_margin_pct"] = (
    product["profit"] /
    product["revenue"] * 100
)

product = product.sort_values(
    "revenue",
    ascending=False
)

print("\nTOP 10 PRODUCTS BY REVENUE")
print("-" * 60)

print(
    product.head(10)
    .round(2)
    .to_string(index=False)
)


# --------------------------------------------------
# 7. Region performance
# --------------------------------------------------

region = (
    df.groupby("region")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
    .reset_index()
)

region["profit_margin_pct"] = (
    region["profit"] /
    region["revenue"] * 100
)

region["revenue_share_pct"] = (
    region["revenue"] /
    total_revenue * 100
)

region = region.sort_values(
    "revenue",
    ascending=False
)

print("\nREGION PERFORMANCE")
print("-" * 60)
print(region.round(2).to_string(index=False))


# --------------------------------------------------
# 8. Sales channel performance
# --------------------------------------------------

channel = (
    df.groupby("sales_channel")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
    .reset_index()
)

channel["profit_margin_pct"] = (
    channel["profit"] /
    channel["revenue"] * 100
)

channel["revenue_share_pct"] = (
    channel["revenue"] /
    total_revenue * 100
)

channel = channel.sort_values(
    "revenue",
    ascending=False
)

print("\nSALES CHANNEL PERFORMANCE")
print("-" * 60)
print(channel.round(2).to_string(index=False))


# --------------------------------------------------
# 9. Discount analysis
# --------------------------------------------------

discount = (
    df.groupby("discount")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
    )
    .reset_index()
)

discount["profit_margin_pct"] = (
    discount["profit"] /
    discount["revenue"] * 100
)

discount = discount.sort_values("discount")

print("\nDISCOUNT PERFORMANCE")
print("-" * 60)
print(discount.round(2).to_string(index=False))


# --------------------------------------------------
# 10. Save reports
# --------------------------------------------------

monthly.to_csv(
    REPORTS / "monthly_kpis.csv"
)

yearly.to_csv(
    REPORTS / "yearly_kpis.csv",
    index=False
)

category.to_csv(
    REPORTS / "category_performance.csv",
    index=False
)

product.to_csv(
    REPORTS / "product_performance.csv",
    index=False
)

region.to_csv(
    REPORTS / "region_performance.csv",
    index=False
)

channel.to_csv(
    REPORTS / "channel_performance.csv",
    index=False
)

discount.to_csv(
    REPORTS / "discount_analysis.csv",
    index=False
)


print("\n" + "=" * 60)
print("REPORTS CREATED SUCCESSFULLY")
print("=" * 60)

print("reports/monthly_kpis.csv")
print("reports/yearly_kpis.csv")
print("reports/category_performance.csv")
print("reports/product_performance.csv")
print("reports/region_performance.csv")
print("reports/channel_performance.csv")
print("reports/discount_analysis.csv")