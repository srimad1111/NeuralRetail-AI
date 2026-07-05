import streamlit as st
import plotly.express as px
import pandas as pd

from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

from utils import create_rfm


# Churn Prediction Dashboard
def churn_dashboard(df):

    st.header("🤖 Customer Churn Prediction")

    st.caption(
        "Predict customers likely to stop purchasing using XGBoost."
    )

    st.markdown("---")

    # Create RFM Dataset
    rfm = create_rfm(df)

    # Create Churn Label

    rfm["Churn"] = (

        rfm["Recency"] > 90

    ).astype(int)

    st.subheader("Churn Distribution")

    churn_count = (

        rfm["Churn"]

        .value_counts()

        .reset_index()

    )

    churn_count.columns = [

        "Churn",

        "Customers"

    ]

    churn_count["Churn"] = churn_count["Churn"].map({

        0:"Active",

        1:"Churned"

    })

    fig = px.pie(

        churn_count,

        names="Churn",

        values="Customers",

        hole=0.45

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")