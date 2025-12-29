import streamlit as st
import pandas as pd

from rule_engine import (
    run_rule_engine,
    compute_kpis
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Retail Business Rule Engine",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 Retail Business Rule Engine")
st.caption("Upload a retail dataset to automatically detect business risks and insights")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Retail CSV",
    type="csv"
)

# ---------------- MAIN LOGIC ----------------
if uploaded_file:

    # Load data
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # ---------- FILTERS ----------
    st.sidebar.subheader("Filters")

    region_filter = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique()
    )

    product_filter = st.sidebar.multiselect(
        "Select Product",
        options=df["Product"].unique()
    )

    if region_filter:
        df = df[df["Region"].isin(region_filter)]

    if product_filter:
        df = df[df["Product"].isin(product_filter)]

    # ---------- KPIs ----------
    total_sales, total_profit, top_products = compute_kpis(df)

    alerts = run_rule_engine(df)
    total_alerts = sum(len(v) for v in alerts.values())

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
    col2.metric("📈 Total Profit", f"{total_profit:,.0f}")
    col3.metric("⚠ Total Alerts", total_alerts)

    st.divider()

    # ---------- ALERTS ----------
    st.subheader("🚨 Business Alerts")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📉 Product Decline",
        "🌍 Region Risk",
        "⚠ Discount Risk",
        "💸 High Sales Low Profit"
    ])

    with tab1:
        if alerts["Product Decline"]:
            for alert in alerts["Product Decline"]:
                st.warning(alert)
        else:
            st.success("No product decline detected")

    with tab2:
        if alerts["Region Risk"]:
            for alert in alerts["Region Risk"]:
                st.error(alert)
        else:
            st.success("No regional risk detected")

    with tab3:
        if alerts["Discount Risk"]:
            for alert in alerts["Discount Risk"]:
                st.info(alert)
        else:
            st.success("No risky discounts detected")

    with tab4:
        if alerts["High Sales Low Profit"]:
            for alert in alerts["High Sales Low Profit"]:
                st.warning(alert)
        else:
            st.success("No high sales–low profit cases detected")

    st.divider()

    # ---------- TOP PRODUCTS ----------
    st.subheader("🏆 Top Products by Profit")
    st.dataframe(top_products)

    st.divider()

    # ---------- DATA PREVIEW ----------
    st.subheader("📄 Dataset Preview (Top 10 rows)")
    st.dataframe(df.head(10))

else:
    st.info("⬅ Upload a retail CSV file from the sidebar to begin analysis")
