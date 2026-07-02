import streamlit as st
import plotly.express as px

from utils import (
    monthly_sales,
    daily_sales,
    country_sales,
    product_sales
)


# Sales Dashboard
def sales_dashboard(df):

    st.header("📈 Sales Analytics")

    st.caption(
        "Analyze sales performance using interactive business dashboards."
    )

    st.markdown("---")

    # Sales KPIs
    total_transactions = len(df)
    total_quantity = int(df["Quantity"].sum())
    highest_sale = df["Revenue"].max()
    average_sale = df["Revenue"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🧾 Transactions",
        f"{total_transactions:,}"
    )

    c2.metric(
        "📦 Units Sold",
        f"{total_quantity:,}"
    )

    c3.metric(
        "💰 Highest Sale",
        f"₹ {highest_sale:,.2f}"
    )

    c4.metric(
        "🛒 Average Sale",
        f"₹ {average_sale:,.2f}"
    )

    st.markdown("---")

    # Sales Trends
    left, right = st.columns(2)

    with left:

        st.subheader("📅 Monthly Revenue Trend")

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

    with right:

        st.subheader("📆 Daily Revenue Trend")

        daily = daily_sales(df)

        fig_day = px.line(
            daily,
            x="Date",
            y="Revenue"
        )

        fig_day.update_traces(
            line_color="#10B981",
            line_width=3
        )

        fig_day.update_layout(
            template="plotly_white",
            height=450
        )

        st.plotly_chart(
            fig_day,
            use_container_width=True
        )

    st.markdown("---")

    # Product & Country Analysis
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

    with right:

        st.subheader("🏆 Top Selling Products")

        products = product_sales(df)

        fig_product = px.bar(
            products,
            x="Revenue",
            y="Description",
            orientation="h",
            color="Revenue",
            color_continuous_scale="Oranges",
            text_auto=".2s"
        )

        fig_product.update_layout(
            template="plotly_white",
            height=450,
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True
        )

    st.markdown("---")

    # Sales Insights
    st.subheader("📌 Sales Insights")

    country = country_sales(df)
    products = product_sales(df)

    highest_country = country.iloc[0]["Country"]
    highest_product = products.iloc[0]["Description"]

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"🌍 Highest Revenue Country : {highest_country}"
        )

        st.info(
            f"💰 Total Revenue : ₹ {df['Revenue'].sum():,.2f}"
        )

    with c2:

        st.success(
            f"🏆 Best Selling Product : {highest_product}"
        )

        st.info(
            f"📦 Total Quantity Sold : {int(df['Quantity'].sum()):,}"
        )