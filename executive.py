# executive.py
# Executive Dashboard

import streamlit as st
import plotly.express as px

from utils import (
    calculate_kpis,
    monthly_sales,
    country_sales
)


# Executive Dashboard
def executive_dashboard(df):

    st.header("🏠 Executive Overview")

    st.caption(
        "Business performance overview using the Online Retail II dataset."
    )

    st.markdown("---")

    # KPIs
    kpi = calculate_kpis(df)

    revenue = kpi["Revenue"]
    orders = kpi["Orders"]
    customers = kpi["Customers"]
    aov = kpi["AOV"]

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Revenue",
        f"₹ {revenue:,.2f}"
    )

    c2.metric(
        "🧾 Orders",
        f"{orders:,}"
    )

    c3.metric(
        "👥 Customers",
        f"{customers:,}"
    )

    c4.metric(
        "🛒 Avg Order Value",
        f"₹ {aov:,.2f}"
    )

    st.markdown("---")

    # Revenue by Country
    left, right = st.columns(2)

    with left:

        st.subheader("🌍 Revenue by Country")

        country = country_sales(df).head(10)

        fig_country = px.bar(
            country,
            x="Country",
            y="Revenue",
            color="Revenue",
            color_continuous_scale="Blues",
            text_auto=".2s"
        )

        fig_country.update_layout(
            template="plotly_white",
            height=450,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    # Monthly Revenue
    with right:

        st.subheader("📈 Monthly Revenue Trend")

        monthly = monthly_sales(df)

        fig_month = px.line(
            monthly,
            x="InvoiceDate",
            y="Revenue",
            markers=True
        )

        fig_month.update_traces(
            line_color="#2563EB",
            line_width=4
        )

        fig_month.update_layout(
            template="plotly_white",
            height=450
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )

    st.markdown("---")

    # Business Insights
    st.subheader("📌 Business Insights")

    highest_country = country.iloc[0]["Country"]

    st.success(
        f"🌍 Highest Revenue generated from **{highest_country}**."
    )

    st.info(
        f"💰 Total Revenue : ₹ {revenue:,.2f}"
    )

    st.info(
        f"👥 Total Customers : {customers:,}"
    )