import streamlit as st
import pandas as pd
import plotly.express as px


# Inventory Dashboard
def inventory_dashboard(df):

    st.header("Inventory Optimization")

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

    st.subheader("ABC Analysis")

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

# EOQ CALCULATION

    st.subheader("Economic Order Quantity (EOQ)")

    annual_demand = st.number_input(

        "Annual Demand",

        value=5000

    )

    ordering_cost = st.number_input(

        "Ordering Cost",

        value=500

    )

    holding_cost = st.number_input(

        "Holding Cost",

        value=50

    )
    if st.button("Calculate EOQ"):

        eoq = (

            (

                2 *

                annual_demand *

                ordering_cost

            )

            /

            holding_cost

        ) ** 0.5

        st.success(

            f"Optimal Order Quantity = {eoq:.2f} units"

        )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Category A",

        (inventory["Category"] == "A").sum()

    )

    c2.metric(

        "Category B",

        (inventory["Category"] == "B").sum()

    )

    c3.metric(

        "Category C",

        (inventory["Category"] == "C").sum()

    )