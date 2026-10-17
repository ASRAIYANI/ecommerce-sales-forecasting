from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "ecommerce_orders.csv"
FORECAST_PATH = BASE / "reports" / "revenue_forecast.csv"
MODEL_COMPARISON_PATH = BASE / "reports" / "forecast_model_comparison.csv"

st.set_page_config(
    page_title="E-commerce Sales Analytics",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv(
        DATA_PATH,
        parse_dates=["order_date"],
    )
    return data


@st.cache_data
def load_forecast():
    return pd.read_csv(
        FORECAST_PATH,
        parse_dates=["month"],
    )


@st.cache_data
def load_model_comparison():
    return pd.read_csv(MODEL_COMPARISON_PATH)


df = load_data()
forecast = load_forecast()
model_comparison = load_model_comparison()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("E-commerce Sales Analytics & Forecasting")

st.caption(
    "Interactive portfolio dashboard for business performance "
    "analysis and revenue forecasting using synthetic e-commerce data."
)


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date


categories = sorted(df["category"].unique())

selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
)


regions = sorted(df["region"].unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
)


channels = sorted(df["sales_channel"].unique())

selected_channels = st.sidebar.multiselect(
    "Sales Channel",
    options=channels,
    default=channels,
)


# --------------------------------------------------
# Apply filters
# --------------------------------------------------

filtered = df[
    (df["order_date"].dt.date >= start_date)
    & (df["order_date"].dt.date <= end_date)
    & (df["category"].isin(selected_categories))
    & (df["region"].isin(selected_regions))
    & (df["sales_channel"].isin(selected_channels))
].copy()


if filtered.empty:
    st.warning(
        "No data matches the selected filters. "
        "Please change the sidebar selections."
    )
    st.stop()


# --------------------------------------------------
# Executive KPIs
# --------------------------------------------------

total_revenue = filtered["revenue"].sum()
total_profit = filtered["profit"].sum()
total_orders = filtered["order_id"].nunique()
units_sold = filtered["quantity"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue
    else 0
)

average_order_value = (
    total_revenue / total_orders
    if total_orders
    else 0
)


st.subheader("Executive Overview")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Revenue",
    f"{total_revenue:,.2f}",
)

c2.metric(
    "Profit",
    f"{total_profit:,.2f}",
)

c3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%",
)


c4, c5, c6 = st.columns(3)

c4.metric(
    "Orders",
    f"{total_orders:,}",
)

c5.metric(
    "Units Sold",
    f"{units_sold:,}",
)

c6.metric(
    "Average Order Value",
    f"{average_order_value:,.2f}",
)


# --------------------------------------------------
# Monthly performance
# --------------------------------------------------

st.divider()
st.header("Sales Trends")

monthly = (
    filtered.set_index("order_date")
    .resample("MS")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    .reset_index()
)


trend_long = monthly.melt(
    id_vars="order_date",
    value_vars=["revenue", "profit"],
    var_name="Metric",
    value_name="Amount",
)

trend_chart = px.line(
    trend_long,
    x="order_date",
    y="Amount",
    color="Metric",
    markers=True,
    title="Monthly Revenue and Profit",
)

st.plotly_chart(
    trend_chart,
    use_container_width=True,
)


# --------------------------------------------------
# Yearly performance
# --------------------------------------------------

filtered["year"] = filtered["order_date"].dt.year

yearly = (
    filtered.groupby("year", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
    )
)

yearly["revenue_growth_pct"] = (
    yearly["revenue"].pct_change() * 100
)

st.subheader("Yearly Performance")

st.dataframe(
    yearly.round(2),
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Category and region analysis
# --------------------------------------------------

st.divider()
st.header("Business Segmentation")

left, right = st.columns(2)


with left:

    category = (
        filtered.groupby(
            "category",
            as_index=False,
        )
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values(
            "revenue",
            ascending=False,
        )
    )

    category_chart = px.bar(
        category,
        x="category",
        y="revenue",
        title="Revenue by Category",
    )

    st.plotly_chart(
        category_chart,
        use_container_width=True,
    )


with right:

    region = (
        filtered.groupby(
            "region",
            as_index=False,
        )
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values(
            "revenue",
            ascending=False,
        )
    )

    region_chart = px.bar(
        region,
        x="region",
        y="revenue",
        title="Revenue by Region",
    )

    st.plotly_chart(
        region_chart,
        use_container_width=True,
    )


# --------------------------------------------------
# Sales channel analysis
# --------------------------------------------------

channel = (
    filtered.groupby(
        "sales_channel",
        as_index=False,
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
    )
    .sort_values(
        "revenue",
        ascending=False,
    )
)

channel_chart = px.bar(
    channel,
    x="sales_channel",
    y="revenue",
    title="Revenue by Sales Channel",
)

st.plotly_chart(
    channel_chart,
    use_container_width=True,
)


# --------------------------------------------------
# Product analysis
# --------------------------------------------------

st.divider()
st.header("Product Performance")

product = (
    filtered.groupby(
        ["product", "category"],
        as_index=False,
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units_sold=("quantity", "sum"),
        orders=("order_id", "nunique"),
    )
)

product["profit_margin_pct"] = (
    product["profit"]
    / product["revenue"]
    * 100
)

product = product.sort_values(
    "revenue",
    ascending=False,
)


top_products_chart = px.bar(
    product.head(10),
    x="product",
    y="revenue",
    color="category",
    title="Top Products by Revenue",
)

st.plotly_chart(
    top_products_chart,
    use_container_width=True,
)


st.subheader("Product Performance Table")

st.dataframe(
    product.round(2),
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Discount analysis
# --------------------------------------------------

st.divider()
st.header("Discount Analysis")

discount = (
    filtered.groupby(
        "discount",
        as_index=False,
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
    )
)

discount["profit_margin_pct"] = (
    discount["profit"]
    / discount["revenue"]
    * 100
)

discount["discount_label"] = (
    discount["discount"]
    .mul(100)
    .round(0)
    .astype(int)
    .astype(str)
    + "%"
)


discount_chart = px.bar(
    discount,
    x="discount_label",
    y="revenue",
    title="Revenue by Discount Level",
)

st.plotly_chart(
    discount_chart,
    use_container_width=True,
)


# --------------------------------------------------
# Forecasting section
# --------------------------------------------------

st.divider()
st.header("Revenue Forecast")

st.info(
    "Forecasting was evaluated separately on the complete "
    "historical monthly revenue series. Four methods were "
    "compared using the final six months as a holdout period."
)


forecast_chart = px.line(
    forecast,
    x="month",
    y="forecast_revenue",
    markers=True,
    title="2026 Revenue Forecast",
)

st.plotly_chart(
    forecast_chart,
    use_container_width=True,
)


forecast_total = forecast["forecast_revenue"].sum()

fc1, fc2, fc3 = st.columns(3)

fc1.metric(
    "Selected Model",
    forecast["forecast_method"].iloc[0],
)

fc2.metric(
    "Validation MAPE",
    f"{forecast['validation_mape_pct'].iloc[0]:.2f}%",
)

fc3.metric(
    "6-Month Forecast Revenue",
    f"{forecast_total:,.2f}",
)


st.subheader("Forecast Details")

st.dataframe(
    forecast,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Forecast model comparison
# --------------------------------------------------

st.subheader("Forecast Model Comparison")

model_comparison_display = (
    model_comparison
    .sort_values("MAPE")
    .copy()
)

st.dataframe(
    model_comparison_display.round(2),
    use_container_width=True,
    hide_index=True,
)


comparison_chart = px.bar(
    model_comparison_display,
    x="Model",
    y="MAPE",
    title="Forecast Model Comparison - Lower MAPE is Better",
)

st.plotly_chart(
    comparison_chart,
    use_container_width=True,
)


# --------------------------------------------------
# Business insights
# --------------------------------------------------

st.divider()
st.header("Key Business Insights")

full_revenue = df["revenue"].sum()

category_full = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_category = category_full.index[0]
top_category_share = (
    category_full.iloc[0]
    / full_revenue
    * 100
)

top_product = (
    df.groupby("product")["revenue"]
    .sum()
    .idxmax()
)

top_region = (
    df.groupby("region")["revenue"]
    .sum()
    .idxmax()
)

top_channel = (
    df.groupby("sales_channel")["revenue"]
    .sum()
    .idxmax()
)


st.markdown(
    f"""
- **{top_category}** is the largest revenue category and contributes approximately **{top_category_share:.2f}%** of total historical revenue.
- **{top_product}** is the highest-revenue product in the dataset.
- **{top_region}** is the highest-revenue region.
- **{top_channel}** is the leading sales channel.
- **Seasonal Naive** produced the strongest holdout forecasting performance with **23.72% MAPE**.
"""
)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "Portfolio project built with Python, Pandas, Plotly, "
    "Statsmodels and Streamlit. Dataset is synthetic and "
    "intended for educational and portfolio use."
)