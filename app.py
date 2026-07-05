import streamlit as st
from churn import churn_dashboard

from utils import load_data, clean_data

from executive import executive_dashboard
from inventory import inventory_dashboard
from sales import sales_dashboard
from customer import customer_dashboard
from forecast import forecast_dashboard


# Streamlit Configuration
st.set_page_config(
    page_title="NeuralRetail AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load Dataset
df = load_data()
df = clean_data(df)


# Sidebar
st.sidebar.title("🛒 NeuralRetail AI")
st.sidebar.caption("AI Powered Retail Intelligence")

PAGES = {
    "🏠 Executive Overview": executive_dashboard,
    "📈 Sales Analytics": sales_dashboard,
    "👥 Customer Hub": customer_dashboard,
    "🔮 Demand Explorer": forecast_dashboard,
    "🤖 Churn Prediction": churn_dashboard,
    "📦 Inventory Optimization": inventory_dashboard,
}

page = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys())
)

st.sidebar.markdown("---")

st.sidebar.subheader("Current Modules")
st.sidebar.success("✔ Executive Dashboard")
st.sidebar.success("✔ Sales Analytics")
st.sidebar.success("✔ Customer Segmentation")
st.sidebar.success("✔ Demand Forecasting")

st.sidebar.markdown("---")

st.sidebar.subheader("Upcoming Modules")
st.sidebar.info("📌 Churn Prediction")
st.sidebar.info("📌 Inventory Optimization")

st.sidebar.markdown("---")
st.sidebar.caption("NeuralRetail AI v1.0")


# Main Title
st.title("🛒 NeuralRetail AI")
st.caption("AI Powered Retail Sales Intelligence Dashboard")
st.markdown("---")


# Navigation
PAGES[page](df)