


import streamlit as st
import pandas as pd
from rule_engine import run_rule_engine, compute_kpis

# ---------- Page Config ----------
st.set_page_config(
    page_title="Retail Business Rule Engine",
    layout="wide"
)

# ---------- Sidebar ----------
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader(
    "Upload Retail CSV",
    type=["csv"]
)

# ---------- Main Title ----------
st.title("Retail Business Rule Engine")
st.caption("Upload a retail dataset to automatically detect business risks and insights")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # ---------- Filters ----------
    st.sidebar.subheader("Filters")

    regions = sorted(df["Region"].unique())
    products = sorted(df["Product"].unique())

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        options=regions,
        default=[]
    )

    selected_products = st.sidebar.multiselect(
        "Select Product",
        options=products,
        default=[]
    )

    # ---------- Stop until user selects ----------
    if not selected_regions or not selected_products:
        st.info("👈 Please select at least one Region and one Product to view insights.")
        st.stop()

    filtered_df = df[
        (df["Region"].isin(selected_regions)) &
        (df["Product"].isin(selected_products))
    ]

    # ---------- KPIs ----------
    total_sales, total_profit, top_products = compute_kpis(filtered_df)
    alerts = run_rule_engine(filtered_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Total Profit", f"{total_profit:,.0f}")
    col3.metric("Total Alerts", len(alerts))

    st.divider()

    # ---------- Alerts Section ----------
    st.subheader("Business Risk Alerts")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No risks detected. Business performance looks healthy.")

    st.divider()

    # ---------- Line Chart: Profit Trend ----------
    st.subheader("📈 Profit Trend Over Time")

    trend_df = (
        filtered_df
        .groupby(pd.to_datetime(filtered_df["Date"]).dt.to_period("M"))["Profit"]
        .sum()
        .reset_index()
    )

    trend_df["Date"] = trend_df["Date"].astype(str)

    st.line_chart(trend_df, x="Date", y="Profit")

else:
    st.info("Please upload a retail CSV file to begin analysis.")
