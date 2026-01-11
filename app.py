import streamlit as st
import pandas as pd
from rule_engine import run_rule_engine, compute_kpis

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Retail Business Rule Engine",
    layout="wide"
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("Upload Retail CSV", type=["csv"])

# THEME TOGGLE
dark_mode = st.sidebar.toggle("Dark Mode")

# ------------------ THEME STYLES ------------------
if dark_mode:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
            h1, h2, h3, h4 {
                color: #ffffff;
            }
            .metric-card {
                background: #1c1f26;
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.6);
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #f5f7fb;
                color: #000000;
            }
            h1, h2, h3, h4 {
                color: #000000;
            }
            .metric-card {
                background: #ffffff;
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.08);
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

# ------------------ MAIN TITLE ------------------
st.markdown("<h1 style='font-size:42px; font-weight:800;'>Retail Business Rule Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px;'>Automated detection of business risks and performance insights</p>", unsafe_allow_html=True)

# =================================================
# MAIN LOGIC
# =================================================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # ---------- FILTERS ----------
    st.sidebar.subheader("Filters")

    selected_regions = st.sidebar.multiselect(
        "Region",
        sorted(df["Region"].unique())
    )

    selected_products = st.sidebar.multiselect(
        "Product",
        sorted(df["Product"].unique())
    )

    # ---------- THRESHOLDS ----------
    st.sidebar.subheader("Rule Thresholds")

    sales_threshold = st.sidebar.slider("High Sales Threshold", 1000, 20000, 5000, 500)
    profit_threshold = st.sidebar.slider("Low Profit Threshold", 0, 500, 100, 10)
    discount_threshold = st.sidebar.slider("High Discount Percentage", 0, 50, 15, 1) / 100

    if not selected_regions or not selected_products:
        st.info("Select at least one region and product")
        st.stop()

    filtered_df = df[
        (df["Region"].isin(selected_regions)) &
        (df["Product"].isin(selected_products))
    ]

    # ---------- KPIs ----------
    total_sales, total_profit, top_products = compute_kpis(filtered_df)
    all_alerts = run_rule_engine(filtered_df, sales_threshold, profit_threshold, discount_threshold)

    forecast_alerts = [a for a in all_alerts if a["type"] == "FORECAST_PROFIT_RISK"]
    alerts = [a for a in all_alerts if a["type"] != "FORECAST_PROFIT_RISK"]

    st.markdown("<h2 style='font-size:32px; font-weight:700;'>Key Performance Indicators</h2>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>Total Sales</h3><h2>{total_sales:,.0f}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3>Total Profit</h3><h2>{total_profit:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h3>Total Alerts</h3><h2>{len(all_alerts)}</h2></div>", unsafe_allow_html=True)

    # ---------- EXECUTIVE SUMMARY ----------
    st.markdown("<h2 style='font-size:32px; font-weight:700;'>Executive Summary</h2>", unsafe_allow_html=True)

    high_risk = sum(1 for a in alerts if a["severity"] == "High")
    medium_risk = sum(1 for a in alerts if a["severity"] == "Medium")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Alerts", len(alerts))
    c2.metric("High Risk", high_risk)
    c3.metric("Products Impacted", len({a["entity"] for a in alerts if a["group"] == "Product"}))
    c4.metric("Regions Impacted", len({a["entity"] for a in alerts if a["group"] == "Region"}))

    # ---------- SEVERITY HEATMAP ----------
    if alerts:
        st.markdown("<h2 style='font-size:32px; font-weight:700;'>Risk Severity Overview</h2>", unsafe_allow_html=True)
        heatmap_df = pd.DataFrame(alerts)
        pivot = heatmap_df.groupby(["group", "severity"]).size().unstack(fill_value=0)
        st.dataframe(pivot, use_container_width=True)

    # ---------- ALERTS ----------
    st.markdown("<h2 style='font-size:32px; font-weight:700;'>Business Risk Alerts</h2>", unsafe_allow_html=True)

    for alert in alerts:
        st.markdown(f"""
            <div class='metric-card' style='margin-bottom:18px; text-align:left;'>
                <h3>{alert['group']} : {alert['entity']}</h3>
                <p style='font-size:17px;'><strong>Severity:</strong> {alert['severity']}</p>
                <p style='font-size:17px;'>{alert['message']}</p>
                <p style='font-size:17px;'><strong>Recommendation:</strong> {alert['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)

    # ---------- FORECAST ----------
    if forecast_alerts:
        st.markdown("<h2 style='font-size:32px; font-weight:700;'>Forecast Risk Assessment</h2>", unsafe_allow_html=True)
        for alert in forecast_alerts:
            st.markdown(f"""
                <div class='metric-card' style='border-left:6px solid #ff9800; text-align:left;'>
                    <h3>{alert['entity']}</h3>
                    <p style='font-size:17px;'>{alert['message']}</p>
                    <p style='font-size:17px;'><strong>Recommendation:</strong> {alert['recommendation']}</p>
                </div>
            """, unsafe_allow_html=True)

    # ---------- TREND ----------
    st.markdown("<h2 style='font-size:32px; font-weight:700;'>Profit Trend Over Time</h2>", unsafe_allow_html=True)

    trend_df = (
        filtered_df
        .groupby(pd.to_datetime(filtered_df["Date"]).dt.to_period("M"))["Profit"]
        .sum()
        .reset_index()
    )
    trend_df["Date"] = trend_df["Date"].astype(str)
    st.line_chart(trend_df, x="Date", y="Profit")

else:
    st.info("Upload a retail CSV file to begin analysis")
