


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

    # ---------- Filters ----------
    st.sidebar.subheader("Filters")

    region_filter = st.sidebar.multiselect(
        "Select Region",
        options=sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

    product_filter = st.sidebar.multiselect(
        "Select Product",
        options=sorted(df["Product"].unique()),
        default=sorted(df["Product"].unique())
    )

    filtered_df = df[
        (df["Region"].isin(region_filter)) &
        (df["Product"].isin(product_filter))
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

    # ---------- Visual Insights ----------
    st.subheader("Top Profitable Products")
    st.bar_chart(
        top_products.set_index("Product")["Profit"]
    )

    st.subheader("Profit by Region")
    region_profit = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(region_profit)

else:
    st.info("Please upload a retail CSV file to begin analysis.")
