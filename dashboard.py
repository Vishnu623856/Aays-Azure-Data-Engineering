import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AdventureWorks Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load Gold data
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

MONTHLY_PATH = PROJECT_DIR / "output" / "gold" / "monthly_sales"
PRODUCT_PATH = PROJECT_DIR / "output" / "gold" / "product_performance"


@st.cache_data
def load_data():
    monthly = pd.read_parquet(MONTHLY_PATH)
    product = pd.read_parquet(PRODUCT_PATH)

    return monthly, product


monthly_sales, product_performance = load_data()


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 AdventureWorks Sales Dashboard")

st.markdown(
    "Interactive dashboard built from the Gold layer of the "
    "Azure Data Engineering pipeline."
)


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_orders = monthly_sales["TotalOrders"].sum()
total_quantity = monthly_sales["TotalQuantity"].sum()
total_products = product_performance["ProductKey"].nunique()

average_quantity = (
    total_quantity / total_orders
    if total_orders > 0
    else 0
)


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    f"{total_orders:,.0f}"
)

col2.metric(
    "Total Quantity",
    f"{total_quantity:,.0f}"
)

col3.metric(
    "Products",
    f"{total_products:,.0f}"
)

col4.metric(
    "Avg Quantity / Order",
    f"{average_quantity:.2f}"
)


st.divider()


# --------------------------------------------------
# Monthly sales chart
# --------------------------------------------------

st.subheader("Monthly Sales Performance")

monthly_sales["YearMonth"] = (
    monthly_sales["OrderYear"].astype(str)
    + "-"
    + monthly_sales["OrderMonth"].astype(str).str.zfill(2)
)

fig_monthly = px.line(
    monthly_sales,
    x="YearMonth",
    y="TotalQuantity",
    markers=True,
    title="Sales Quantity by Month"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Quantity"
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)


# --------------------------------------------------
# Top products
# --------------------------------------------------

st.subheader("Top 10 Products")

top_products = (
    product_performance
    .sort_values("TotalQuantity", ascending=False)
    .head(10)
    .sort_values("TotalQuantity")
)

fig_products = px.bar(
    top_products,
    x="TotalQuantity",
    y="ProductKey",
    orientation="h",
    title="Top 10 Products by Quantity"
)

fig_products.update_layout(
    xaxis_title="Total Quantity",
    yaxis_title="Product Key"
)

st.plotly_chart(
    fig_products,
    width="stretch"
)


# --------------------------------------------------
# Data tables
# --------------------------------------------------

st.subheader("Monthly Sales Data")

st.dataframe(
    monthly_sales[
        [
            "OrderYear",
            "OrderMonth",
            "TotalOrders",
            "TotalQuantity",
            "TotalLineQuantity",
            "AverageOrderQuantity"
        ]
    ],
    width="stretch"
)


st.subheader("Top Product Performance")

st.dataframe(
    product_performance
    .sort_values("TotalQuantity", ascending=False)
    .head(10),
    width="stretch"
)