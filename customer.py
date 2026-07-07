import streamlit as st
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from utils import create_rfm

import joblib
import os


# Customer Dashboard
def customer_dashboard(df):

    st.header("👥 Customer Hub")

    st.caption(
        "Customer Segmentation using RFM Analysis and K-Means Clustering."
    )

    st.markdown("---")

    # Create RFM Dataset
    rfm = create_rfm(df)

    # Standardize Features

    scaler = StandardScaler()

    scaled_rfm = scaler.fit_transform(rfm)

    # Apply K-Means

    kmeans = KMeans(

        n_clusters=4,

        random_state=42,

        n_init=10

    )

    rfm["Cluster"] = kmeans.fit_predict(
        scaled_rfm

    
    )

    os.makedirs("models", exist_ok=True)

    joblib.dump(kmeans, "models/kmeans.pkl")
    joblib.dump(scaler, "models/scaler.pkl")


    cluster_names = {

        0: "Champions",

        1: "Loyal",

        2: "At Risk",

        3: "Hibernating"

    }

    rfm["Segment"] = rfm["Cluster"].map(
        cluster_names
    )

    # Customer KPIs

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Customers",
        len(rfm)
    )

    c2.metric(
        "📅 Avg Recency",
        round(rfm["Recency"].mean(), 1)
    )

    c3.metric(
        "🛒 Avg Frequency",
        round(rfm["Frequency"].mean(), 1)
    )

    c4.metric(
        "💰 Avg Monetary",
        f"₹ {rfm['Monetary'].mean():,.2f}"
    )

    st.markdown("---")

    # Customer Segments

    left, right = st.columns(2)

    with left:

        st.subheader("🥧 Customer Segments")

        segment_count = (

            rfm["Segment"]

            .value_counts()

            .reset_index()

        )

        segment_count.columns = [

            "Segment",

            "Customers"

        ]

        fig_pie = px.pie(

            segment_count,

            names="Segment",

            values="Customers",

            hole=0.5,

            color_discrete_sequence=px.colors.qualitative.Set2

        )

        fig_pie.update_layout(

            template="plotly_white",

            height=450

        )

        st.plotly_chart(

            fig_pie,

            use_container_width=True

        )

    with right:

        st.subheader("📈 Customer Distribution")

        fig_scatter = px.scatter(

            rfm,

            x="Recency",

            y="Monetary",

            color="Segment",

            size="Frequency",

            hover_data=["Frequency"]

        )

        fig_scatter.update_layout(

            template="plotly_white",

            height=450

        )

        st.plotly_chart(

            fig_scatter,

            use_container_width=True

        )

    st.markdown("---")

    # Top Customers

    st.subheader("🏆 Top 10 Valuable Customers")

    top_customers = (

        rfm

        .sort_values(

            "Monetary",

            ascending=False

        )

        .head(10)

    )

    st.dataframe(

        top_customers,

        use_container_width=True

    )

    st.markdown("---")

    # Customer Insights

    st.subheader("📌 Customer Insights")

    champion_count = (

        rfm[

            rfm["Segment"] == "Champions"

        ].shape[0]

    )

    st.success(

        f"⭐ Champions Customers : {champion_count}"

    )

    st.info(

        f"👥 Total Customers : {len(rfm)}"

    )


