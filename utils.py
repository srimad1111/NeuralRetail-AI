

def clean_data(df):

    # Remove missing Customer IDs
    df = df.dropna(subset=["Customer ID"])

    # Remove cancelled invoices
    df = df[
        ~df["Invoice"].astype(str).str.startswith("C")
    ]

    # Remove invalid Quantity
    df = df[
        df["Quantity"] > 0
    ]

    # Remove invalid Price
    df = df[
        df["Price"] > 0
    ]

    # Convert Date
    df["InvoiceDate"] = pd.to

def calculate_kpis(df):

    total_revenue = df["Revenue"].sum()

    total_orders = df["Invoice"].nunique()

    total_customers = df["Customer ID"].nunique()

    average_order_value = (
        total_revenue /
        total_orders
    )

    return {

        "Revenue": total_revenue,

        "Orders": total_orders,

        "Cus

def monthly_sales(df):

    monthly = (

        df.groupby(

            df["InvoiceDate"].dt.to_period("M")

        )["Revenue"]

        .sum()

        .reset_index()

    )

    monthly["InvoiceDate"] = (

        monthly["InvoiceDa

def country_sales(df):

    country = (

        df.

def product_sales(df):

    products = (

        df.groupby("Description")["Revenue"]

        .sum()

        .sort_values(

            ascending=Fals

def create_rfm(df):

    snapshot_date = (

        df["InvoiceDate"].max()

        + pd.Timedelta(days=1)

    )

    rfm = (

        df.groupby("Customer ID")

        .agg({

            "InvoiceDate":

            lambda x:

            (snapshot_date - x.max()).days,

            "Invoice":"nunique",

            "Revenue":"sum"

        })

    )

    rfm.columns = [

        "Recency",

        "Frequency",

        "Monetary"

    ]

    return rfm


# Prophet Dataset

def prophet_dataset(df):

    prophet_df = (

        df.assign(

            Date=df["InvoiceDate"].dt.date

        )

        .groupby("Date")["Revenue"]

        .sum()

        .reset_index()

    )

    prophet_df.columns = [

        "ds",

        "y"

    ]

    prophet_df["ds"] = pd.to_datetime(

        prophet_df["ds"]

    )

    return prophet_df