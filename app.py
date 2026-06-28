# ==========================================================
#          NEURALRETAIL AI SALES INTELLIGENCE PLATFORM
#                 PART 1 : PROJECT SETUP
# ==========================================================

# ==========================================================
# Import Libraries
# ==========================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns

from prophet import Prophet

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(
    page_title="NeuralRetail AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Title
# ==========================================================

st.title("🛒 NeuralRetail AI Sales Intelligence Platform")

st.caption(
    "AI Powered Retail Sales Intelligence Dashboard"
)

st.markdown("---")

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🛒 NeuralRetail")

st.sidebar.caption(
    "AI Powered Retail Intelligence"
)

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Executive Overview",

        "📈 Sales Analytics",

        "👥 Customer Hub",

        "🔮 Demand Explorer",

        "⚠️ Churn Risk",

        "📦 Inventory Health"

    ]

)

st.sidebar.markdown("---")

st.sidebar.info(

"""
Current Version

✔ Executive Dashboard

✔ Sales Analytics

✔ Customer Hub

✔ Demand Forecast

Coming Soon

• Churn Prediction

• Inventory Optimization
"""

)

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0")

# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "online_retail_II.csv",
        encoding="ISO-8859-1"
    )

    return df


df = load_data()

# ==========================================================
# Data Cleaning
# ==========================================================

df = df.dropna(subset=["Customer ID"])

df = df[
    ~df["Invoice"].astype(str).str.startswith("C")
]

df = df[
    df["Quantity"] > 0
]

df = df[
    df["Price"] > 0
]

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)

df["Revenue"] = (
    df["Quantity"] *
    df["Price"]
)

# ==========================================================
# Helper DataFrames
# ==========================================================

monthly_sales = (

    df.groupby(

        df["InvoiceDate"].dt.to_period("M")

    )["Revenue"]

    .sum()

    .reset_index()

)

monthly_sales["InvoiceDate"] = (

    monthly_sales["InvoiceDate"]

    .astype(str)

)

country_sales = (

    df.groupby("Country")["Revenue"]

    .sum()

    .sort_values(ascending=False)

    .reset_index()

)

product_sales = (

    df.groupby("Description")["Revenue"]

    .sum()

    .sort_values(ascending=False)

    .head(10)

    .reset_index()

)

daily_sales = (

    df.groupby(

        df["InvoiceDate"].dt.date

    )["Revenue"]

    .sum()

    .reset_index()

)

daily_sales.columns = [

    "Date",

    "Revenue"

]

# ==========================================================
# Executive KPIs
# ==========================================================

total_revenue = df["Revenue"].sum()

total_orders = df["Invoice"].nunique()

total_customers = df["Customer ID"].nunique()

average_order_value = total_revenue / total_orders

# ==========================================================
# End of Part 1
# ==========================================================

# ==========================================================
# PART 2 : EXECUTIVE OVERVIEW DASHBOARD
# ==========================================================

if page == "🏠 Executive Overview":

    st.header("🚀 Executive Overview")

    st.write(
        "A quick overview of the retail business performance based on the cleaned dataset."
    )

    st.markdown("---")

    # ===========================
    # KPI Cards
    # ===========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Revenue",
        f"₹ {total_revenue:,.2f}"
    )

    col2.metric(
        "🧾 Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "🛒 Avg Order Value",
        f"₹ {average_order_value:,.2f}"
    )

    st.markdown("---")

    # ===========================
    # Revenue by Country
    # ===========================

    left, right = st.columns(2)

    with left:

        st.subheader("🌍 Revenue by Country")

        top_country = country_sales.head(10)

        fig_country = px.bar(
            top_country,
            x="Country",
            y="Revenue",
            color="Revenue",
            text_auto=".2s",
            title="Top 10 Countries"
        )

        fig_country.update_layout(
            height=450,
            xaxis_title="Country",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    # ===========================
    # Monthly Revenue Trend
    # ===========================

    with right:

        st.subheader("📈 Monthly Revenue Trend")

        fig_month = px.line(
            monthly_sales,
            x="InvoiceDate",
            y="Revenue",
            markers=True,
            title="Monthly Revenue"
        )

        fig_month.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )

    st.markdown("---")

    # ===========================
    # Top Products
    # ===========================

    left, right = st.columns(2)

    with left:

        st.subheader("🏆 Top Selling Products")

        fig_products = px.bar(
            product_sales,
            x="Revenue",
            y="Description",
            orientation="h",
            color="Revenue",
            text_auto=".2s"
        )

        fig_products.update_layout(
            height=450,
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

    # ===========================
    # Revenue Distribution
    # ===========================

    with right:

        st.subheader("💰 Revenue Distribution")

        fig_hist = px.histogram(
            df,
            x="Revenue",
            nbins=60,
            title="Revenue Distribution"
        )

        fig_hist.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    st.markdown("---")

    # ===========================
    # Business Summary
    # ===========================

    st.subheader("📌 Business Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            f"Highest Revenue Country : **{country_sales.iloc[0]['Country']}**"
        )

    with c2:
        st.info(
            f"Top Product : **{product_sales.iloc[0]['Description']}**"
        )

    with c3:
        st.info(
            f"Average Order Value : **₹ {average_order_value:,.2f}**"
        )