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

    # Features & Target

    X = rfm[

        [

            "Recency",

            "Frequency",

            "Monetary"

        ]

    ]

    y = rfm["Churn"]

    scaler = StandardScaler()

    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42

    )

    model = XGBClassifier(

        random_state=42,

        n_estimators=100,

        max_depth=4,

        learning_rate=0.1,

        eval_metric="logloss"

    )

    model.fit(

        X_train,

        y_train

    )

    prediction = model.predict(

        X_test

    )

    accuracy = accuracy_score(

        y_test,

        prediction

    )

    st.subheader("Model Performance")

    st.metric(

        "Accuracy",

        f"{accuracy*100:.2f}%"

    )

    st.markdown("---")