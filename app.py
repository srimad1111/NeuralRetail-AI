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
