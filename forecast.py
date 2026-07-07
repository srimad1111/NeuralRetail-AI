import streamlit as st
import plotly.express as px

from prophet import Prophet

from utils import prophet_dataset
import joblib
import os


# Demand Forecasting
def forecast_dashboard(df):

    st.header("🔮 Demand Forecasting")

    st.caption(
        "Predict future sales using Meta Prophet."
    )

    st.markdown("---")

    # Prepare Dataset
    prophet_df = prophet_dataset(df)

    # Train Prophet Model

    model = Prophet(

        yearly_seasonality=True,

        weekly_seasonality=True,

        daily_seasonality=False

    )

    model.fit(prophet_df)

    future = model.make_future_dataframe(
        periods=90
    )

    joblib.dump(model, "models/prophet.pkl")

    forecast = model.predict(future)

    # Forecast Chart

    st.subheader("📈 90-Day Sales Forecast")

    fig = px.line(

        forecast,

        x="ds",

        y="yhat",

        title="Predicted Revenue"

    )

    fig.update_traces(

        line_color="#F97316",

        line_width=4

    )

    fig.update_layout(

        template="plotly_white",

        height=500,

        xaxis_title="Date",

        yaxis_title="Revenue"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    # Forecast Components

    st.subheader("📊 Trend Components")

    components = model.plot_components(
        forecast
    )

    st.pyplot(
        components
    )

    st.markdown("---")

    # Forecast Table

    st.subheader("📅 Next 90 Days")

    forecast_table = forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ].tail(90)

    forecast_table.columns = [
        "Date",
        "Predicted Revenue",
        "Lower Bound",
        "Upper Bound"
    ]

    st.dataframe(
        forecast_table,
        use_container_width=True
    )

    st.markdown("---")

    # Forecast Summary

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Forecast Days",
        "90"
    )

    c2.metric(
        "Average Forecast",
        f"₹ {forecast_table['Predicted Revenue'].mean():,.2f}"
    )

    c3.metric(
        "Maximum Forecast",
        f"₹ {forecast_table['Predicted Revenue'].max():,.2f}"
    )