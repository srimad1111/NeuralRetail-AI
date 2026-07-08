import pandas as pd
import streamlit as st


# Load Dataset
@st.cache_data
def load_data():

    df = pd.read_csv(
        "online_retail_II.csv",
        encoding="ISO-8859-1"
    )

    return df


def kpi_card(title, value, color="#2563EB"):
    html = f"""
    <div style="
        background:#ffffff;
        border-left:8px solid {color};
        border-radius:16px;
        padding:20px;
        height:150px;
        box-shadow:0 4px 12px rgba(0,0,0,0.12);
        display:flex;
        flex-direction:column;
        justify-content:space-between;
    ">
        <div style="font-size:22px;font-weight:600;color:#6B7280;">
            {title}
        </div>

        <div style="font-size:36px;font-weight:700;color:#111827;">
            {value}
        </div>
    </div>
    """
    st.html(html)

# Data Cleaning
def clean_data(df):

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

    return df


# KPI Calculation
def calculate_kpis(df):

    total_revenue = df["Revenue"].sum()

    total_orders = df["Invoice"].nunique()

    total_customers = df["Customer ID"].nunique()

    average_order_value = (
        total_revenue /
        total_orders
    )

    return {

        "Revenue": total_revenue,

        "Orders": total_orders,

        "Customers": total_customers,

        "AOV": average_order_value

    }


# Monthly Sales
def monthly_sales(df):

    monthly = (

        df.groupby(

            df["InvoiceDate"].dt.to_period("M")

        )["Revenue"]

        .sum()

        .reset_index()

    )

    monthly["InvoiceDate"] = (

        monthly["InvoiceDate"]

        .astype(str)

    )

    return monthly


# Daily Sales
def daily_sales(df):

    daily = (

        df.groupby(

            df["InvoiceDate"].dt.date

        )["Revenue"]

        .sum()

        .reset_index()

    )

    daily.columns = [

        "Date",

        "Revenue"

    ]

    return daily


# Country Sales
def country_sales(df):

    country = (

        df.groupby("Country")["Revenue"]

        .sum()

        .sort_values(

            ascending=False

        )

        .reset_index()

    )

    return country


# Product Sales
def product_sales(df):

    products = (

        df.groupby("Description")["Revenue"]

        .sum()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    return products


# RFM Dataset
def create_rfm(df):

    snapshot_date = (

        df["InvoiceDate"].max()

        + pd.Timedelta(days=1)

    )

    rfm = (

        df.groupby("Customer ID")

        .agg({

            "InvoiceDate":
            lambda x:
            (snapshot_date - x.max()).days,

            "Invoice": "nunique",

            "Revenue": "sum"

        })

    )

    rfm.columns = [

        "Recency",

        "Frequency",

        "Monetary"

    ]

    return rfm


# Prophet Dataset
def prophet_dataset(df):

    prophet_df = (

        df.assign(

            Date=df["InvoiceDate"].dt.date

        )

        .groupby("Date")["Revenue"]

        .sum()

        .reset_index()

    )

    prophet_df.columns = [

        "ds",

        "y"

    ]

    prophet_df["ds"] = pd.to_datetime(

        prophet_df["ds"]

    )

    return prophet_df