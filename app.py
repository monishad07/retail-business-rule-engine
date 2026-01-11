

# import streamlit as st
# import pandas as pd
# from rule_engine import run_rule_engine, compute_kpis

# # ------------------ PAGE CONFIG ------------------
# st.set_page_config(
#     page_title="Retail Business Rule Engine",
#     layout="wide"
# )

# # ------------------ SIDEBAR ------------------
# st.sidebar.title("Controls")
# uploaded_file = st.sidebar.file_uploader("Upload Retail CSV", type=["csv"])

# # ------------------ MAIN TITLE ------------------
# st.title("Retail Business Rule Engine")
# st.caption("Upload a retail dataset to automatically detect business risks and insights")

# # =================================================
# # MAIN LOGIC
# # =================================================
# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     df["Date"] = pd.to_datetime(df["Date"])

#     # ---------- FILTERS ----------
#     st.sidebar.subheader("Filters")

#     selected_regions = st.sidebar.multiselect(
#         "Select Region",
#         sorted(df["Region"].unique())
#     )

#     selected_products = st.sidebar.multiselect(
#         "Select Product",
#         sorted(df["Product"].unique())
#     )

#     # ---------- THRESHOLDS ----------
#     st.sidebar.subheader("Rule Thresholds")

#     sales_threshold = st.sidebar.slider(
#         "High Sales Threshold",
#         1000, 20000, 5000, 500
#     )

#     profit_threshold = st.sidebar.slider(
#         "Low Profit Threshold",
#         0, 500, 100, 10
#     )

#     discount_threshold = st.sidebar.slider(
#         "High Discount %",
#         0, 50, 15, 1
#     ) / 100

#     if not selected_regions or not selected_products:
#         st.info("👈 Please select at least one Region and Product.")
#         st.stop()

#     filtered_df = df[
#         (df["Region"].isin(selected_regions)) &
#         (df["Product"].isin(selected_products))
#     ]


#     # ---------- KPIs ----------
#     total_sales, total_profit, top_products = compute_kpis(filtered_df)

#     alerts = run_rule_engine(
#         filtered_df,
#         sales_threshold,
#         profit_threshold,
#         discount_threshold
#     )

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Sales", f"{total_sales:,.0f}")
#     col2.metric("Total Profit", f"{total_profit:,.0f}")
#     col3.metric("Total Alerts", len(alerts))

#     st.divider()

#     # ---------- EXECUTIVE SUMMARY ----------
#     st.subheader("📊 Executive Summary")

#     high_risk = sum(1 for a in alerts if a["severity"] == "High")
#     medium_risk = sum(1 for a in alerts if a["severity"] == "Medium")

#     products_impacted = {
#         a["entity"] for a in alerts if a["group"] == "Product"
#     }

#     regions_impacted = {
#         a["entity"] for a in alerts if a["group"] == "Region"
#     }

#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("Total Alerts", len(alerts))
#     c2.metric("High Risk", high_risk)
#     c3.metric("Products Impacted", len(products_impacted))
#     c4.metric("Regions Impacted", len(regions_impacted))

#     # ---------- ALERTS ----------
#     st.subheader("🚨 Business Risk Alerts")

#     if alerts:
#         grouped = {}
#         for alert in alerts:
#             key = f"{alert['group']}: {alert['entity']}"
#             grouped.setdefault(key, []).append(alert)

#         for header, items in grouped.items():
#             st.markdown(f"### 🔹 {header}")
#             for alert in items:
#                 if alert["severity"] == "High":
#                     st.error(alert["message"])
#                 elif alert["severity"] == "Medium":
#                     st.warning(alert["message"])
#                 else:
#                     st.info(alert["message"])

#         # ---------- DOWNLOAD ----------
#         alert_df = pd.DataFrame(alerts)
#         st.download_button(
#             "⬇️ Download Alerts CSV",
#             data=alert_df.to_csv(index=False),
#             file_name="retail_business_alerts.csv",
#             mime="text/csv"
#         )
#     else:
#         st.success("No risks detected. Business performance looks healthy.")

#     st.divider()

#     # ---------- TREND ----------
#     st.subheader("📈 Profit Trend Over Time")

#     trend_df = (
#         filtered_df
#         .groupby(pd.to_datetime(filtered_df["Date"]).dt.to_period("M"))["Profit"]
#         .sum()
#         .reset_index()
#     )

#     trend_df["Date"] = trend_df["Date"].astype(str)
#     st.line_chart(trend_df, x="Date", y="Profit")

# else:
#     st.info("Please upload a retail CSV file to begin analysis.")

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

# ------------------ MAIN TITLE ------------------
st.title("Retail Business Rule Engine")
st.caption("Upload a retail dataset to automatically detect business risks and insights")

# =================================================
# MAIN LOGIC
# =================================================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # ---------- FILTERS ----------
    st.sidebar.subheader("Filters")

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        sorted(df["Region"].unique())
    )

    selected_products = st.sidebar.multiselect(
        "Select Product",
        sorted(df["Product"].unique())
    )

    # ---------- THRESHOLDS ----------
    st.sidebar.subheader("Rule Thresholds")

    sales_threshold = st.sidebar.slider(
        "High Sales Threshold",
        1000, 20000, 5000, 500
    )

    profit_threshold = st.sidebar.slider(
        "Low Profit Threshold",
        0, 500, 100, 10
    )

    discount_threshold = st.sidebar.slider(
        "High Discount %",
        0, 50, 15, 1
    ) / 100

    if not selected_regions or not selected_products:
        st.info("👈 Please select at least one Region and Product.")
        st.stop()

    filtered_df = df[
        (df["Region"].isin(selected_regions)) &
        (df["Product"].isin(selected_products))
    ]

    # ---------- KPIs ----------
    total_sales, total_profit, top_products = compute_kpis(filtered_df)

    all_alerts = run_rule_engine(
        filtered_df,
        sales_threshold,
        profit_threshold,
        discount_threshold
    )

    # ---------- SPLIT FORECAST vs NORMAL ----------
    forecast_alerts = [a for a in all_alerts if a["type"] == "FORECAST_PROFIT_RISK"]
    alerts = [a for a in all_alerts if a["type"] != "FORECAST_PROFIT_RISK"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Total Profit", f"{total_profit:,.0f}")
    col3.metric("Total Alerts", len(all_alerts))

    st.divider()

    # ---------- EXECUTIVE SUMMARY ----------
    st.subheader("📊 Executive Summary")

    high_risk = sum(1 for a in alerts if a["severity"] == "High")
    medium_risk = sum(1 for a in alerts if a["severity"] == "Medium")

    products_impacted = {a["entity"] for a in alerts if a["group"] == "Product"}
    regions_impacted = {a["entity"] for a in alerts if a["group"] == "Region"}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Alerts", len(alerts))
    c2.metric("High Risk", high_risk)
    c3.metric("Products Impacted", len(products_impacted))
    c4.metric("Regions Impacted", len(regions_impacted))

    # ---------- BUSINESS ALERTS ----------
    st.subheader("🚨 Business Risk Alerts")

    if alerts:
        grouped = {}
        for alert in alerts:
            key = f"{alert['group']}: {alert['entity']}"
            grouped.setdefault(key, []).append(alert)

        for header, items in grouped.items():
            st.markdown(f"### 🔹 {header}")
            for alert in items:
                if alert["severity"] == "High":
                    st.error(alert["message"])
                elif alert["severity"] == "Medium":
                    st.warning(alert["message"])
                else:
                    st.info(alert["message"])

        # ---------- DOWNLOAD ----------
        alert_df = pd.DataFrame(all_alerts)
        st.download_button(
            "⬇️ Download Alerts CSV",
            data=alert_df.to_csv(index=False),
            file_name="retail_business_alerts.csv",
            mime="text/csv"
        )
    else:
        st.success("No risks detected. Business performance looks healthy.")

    # ---------- FORECAST SECTION ----------
    if forecast_alerts:
        st.divider()
        st.markdown("## 🔮 Forecast Risk Warnings")
        st.caption("Predictive insights based on recent profit trends")

        for alert in forecast_alerts:
            st.markdown(
                f"""
                <div style="
                    background-color:#fff4e6;
                    padding:18px;
                    border-left:6px solid #ff9800;
                    border-radius:10px;
                    margin-bottom:14px;
                    box-shadow:0 4px 10px rgba(0,0,0,0.05);
                ">
                    <strong>{alert['group']}:</strong> {alert['entity']}<br>
                    <span style="color:#e65100; font-size:16px;">
                        {alert['message']}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # ---------- TREND ----------
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




