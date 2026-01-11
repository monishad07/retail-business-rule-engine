import streamlit as st
import pandas as pd
from rule_engine import run_rule_engine, compute_kpis
from ml_forecast import forecast_profit_risk

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Retail Business Rule Engine",
    layout="wide"
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("Upload Retail CSV", type=["csv"])
dark_mode = st.sidebar.toggle("Dark Mode")

# ------------------ MAIN TITLE ------------------
st.markdown("<h1>Retail Business Rule Engine</h1>", unsafe_allow_html=True)
st.markdown("<p>Automated detection of business risks and performance insights</p>", unsafe_allow_html=True)

# =================================================
# MAIN LOGIC
# =================================================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    st.sidebar.subheader("Filters")
    selected_regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
    selected_products = st.sidebar.multiselect("Product", sorted(df["Product"].unique()))

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

    total_sales, total_profit, _ = compute_kpis(filtered_df)

    rule_alerts = run_rule_engine(
        filtered_df,
        sales_threshold,
        profit_threshold,
        discount_threshold
    )

    ml_alerts, ml_forecasts = forecast_profit_ml(filtered_df, profit_threshold)

    all_alerts = rule_alerts + ml_alerts

    forecast_alerts = [a for a in all_alerts if a["type"] == "FORECAST_PROFIT_RISK"]
    alerts = [a for a in all_alerts if a["type"] != "FORECAST_PROFIT_RISK"]

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Risk Analysis", "Forecast", "Trends"])

    # ================= OVERVIEW =================
    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Sales", f"{total_sales:,.0f}")
        c2.metric("Total Profit", f"{total_profit:,.0f}")
        c3.metric("Total Alerts", len(all_alerts))

    # ================= RISK ANALYSIS =================
    with tab2:
        if alerts:
            df_heat = pd.DataFrame(alerts)
            pivot = (
                df_heat.groupby(["group", "severity"])
                .size()
                .unstack(fill_value=0)
            )

            for sev in ["High", "Medium"]:
                if sev not in pivot.columns:
                    pivot[sev] = 0

            pivot = pivot[["High", "Medium"]]
            st.dataframe(pivot, use_container_width=True)

        for alert in alerts:
            st.markdown(f"""
                **{alert['group']} : {alert['entity']}**  
                Severity: {alert['severity']}  
                {alert['message']}  
                Recommendation: {alert['recommendation']}
            """)

    # ================= FORECAST =================
    with tab3:
        for f in ml_forecasts:
            st.subheader(f"{f['Product']} ({f['Region']})")

            chart_df = pd.DataFrame({
                "Month": f["Months"],
                "Actual Profit": f["ActualProfit"]
            })

            st.line_chart(chart_df.set_index("Month"))

            st.markdown(
                f"""
                **Next Month Prediction:** {f['PredictedProfit']:.0f}  
                **95% Confidence Range:** {f['LowerBound']:.0f} – {f['UpperBound']:.0f}
                """
            )

    # ================= TRENDS =================
    with tab4:
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
