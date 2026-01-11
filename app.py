

# import streamlit as st
# import pandas as pd
# from rule_engine import run_rule_engine, compute_kpis

# # ---------- Page Config ----------
# st.set_page_config(
#     page_title="Retail Business Rule Engine",
#     layout="wide"
# )

# # ---------- Sidebar ----------
# st.sidebar.title("Controls")
# uploaded_file = st.sidebar.file_uploader(
#     "Upload Retail CSV",
#     type=["csv"]
# )

# # ---------- Main Title ----------
# st.title("Retail Business Rule Engine")
# st.caption("Upload a retail dataset to automatically detect business risks and insights")

# # =========================================================
# # MAIN LOGIC
# # =========================================================
# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     df["Date"] = pd.to_datetime(df["Date"])

#     # ---------- Filters ----------
#     st.sidebar.subheader("Filters")

#     regions = sorted(df["Region"].unique())
#     products = sorted(df["Product"].unique())

#     selected_regions = st.sidebar.multiselect(
#         "Select Region",
#         options=regions
#     )

#     selected_products = st.sidebar.multiselect(
#         "Select Product",
#         options=products
#     )

#     # ---------- Stop until user selects ----------
#     if not selected_regions or not selected_products:
#         st.info("👈 Please select at least one Region and one Product to view insights.")
#         st.stop()

#     filtered_df = df[
#         (df["Region"].isin(selected_regions)) &
#         (df["Product"].isin(selected_products))
#     ]

#     # ---------- KPIs ----------
#     total_sales, total_profit, top_products = compute_kpis(filtered_df)
#     alerts = run_rule_engine(filtered_df)

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Sales", f"{total_sales:,.0f}")
#     col2.metric("Total Profit", f"{total_profit:,.0f}")
#     col3.metric("Total Alerts", len(alerts))

#     st.divider()

#     # ---------- Alerts Section ----------
#     st.subheader("🚨 Business Risk Alerts")

#     if alerts:
#         for alert in alerts:
#             severity = alert.get("severity", "Low")
#             message = alert.get("message", "Unknown alert")

#             if severity == "High":
#                 st.error(message)
#             elif severity == "Medium":
#                 st.warning(message)
#             else:
#                 st.info(message)
#     else:
#         st.success("No risks detected. Business performance looks healthy.")

#     st.divider()

#     # ---------- Line Chart ----------
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

    alerts = run_rule_engine(
        filtered_df,
        sales_threshold,
        profit_threshold,
        discount_threshold
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Total Profit", f"{total_profit:,.0f}")
    col3.metric("Total Alerts", len(alerts))

    st.divider()

    # ---------- ALERTS ----------
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
        alert_df = pd.DataFrame(alerts)
        st.download_button(
            "⬇️ Download Alerts CSV",
            data=alert_df.to_csv(index=False),
            file_name="retail_business_alerts.csv",
            mime="text/csv"
        )
    else:
        st.success("No risks detected. Business performance looks healthy.")

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


