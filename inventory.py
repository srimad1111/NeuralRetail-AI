import streamlit as st
import pandas as pd
import plotly.express as px


# Inventory Dashboard
def inventory_dashboard(df):

    st.header("📦 Inventory Optimization")

    st.caption(
        "ABC Analysis and Economic Order Quantity (EOQ)"
    )

    st.markdown("---")

