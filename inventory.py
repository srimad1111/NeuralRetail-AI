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

    # Product Revenue

    inventory = (

        df.groupby("Description")["Revenue"]

        .sum()

        .sort_values(

            ascending=False

        )

        .reset_index()

    )

    inventory.columns = [

        "Product",

        "Revenue"

    ]

    inventory["Revenue %"] = (

        inventory["Revenue"] /

        inventory["Revenue"].sum()

    ) * 100

    inventory["Cumulative %"] = (

        inventory["Revenue %"]

        .cumsum()

    )

    inventory["Category"] = "C"

    inventory.loc[

        inventory["Cumulative %"] <= 80,

        "Category"

    ] = "A"

    inventory.loc[

        (inventory["Cumulative %"] > 80) &
        (inventory["Cumulative %"] <= 95),

        "Category"

    ] = "B"

    st.subheader("📊 ABC Analysis")

    fig = px.bar(

        inventory.head(30),

        x="Product",

        y="Revenue",

        color="Category",

        color_discrete_map={

            "A":"red",

            "B":"orange",

            "C":"green"

        }

    )

    fig.update_layout(

        template="plotly_white",

        height=500,

        xaxis_tickangle=-90

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")