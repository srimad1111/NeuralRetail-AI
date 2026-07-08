import streamlit as st
from churn import churn_dashboard
from utils import load_data, clean_data
from executive import executive_dashboard
from inventory import inventory_dashboard
from sales import sales_dashboard
from customer import customer_dashboard
from forecast import forecast_dashboard
 

st.set_page_config(
    page_title="NeuralRetail AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.spinner("Loading Dashboard..."):
    df = load_data()
    df = clean_data(df)

st.sidebar.image(
    "assets/logo.png",
    width=180     
)

st.sidebar.title("NeuralRetail AI")
st.sidebar.caption("Retail Intelligence Platform")

PAGES = {
    "Executive Overview": executive_dashboard,
    "Sales Analytics": sales_dashboard,
    "Customer Hub": customer_dashboard,
    "Demand Explorer": forecast_dashboard,
    "Churn Prediction": churn_dashboard,
    "Inventory Optimization": inventory_dashboard,
}

page = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys())
)

st.sidebar.markdown("---")
st.sidebar.caption("NeuralRetail AI v1.0")


st.title("🛒 NeuralRetail AI")
st.caption("AI Powered Retail Sales Intelligence Dashboard")
st.markdown("---")

# Open selected page
PAGES[page](df)

st.markdown("---")

st.caption(
    "© 2026 NeuralRetail AI | By Srimad Snehashis | Made with ❤️"
)