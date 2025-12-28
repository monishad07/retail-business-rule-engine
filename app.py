# import streamlit as st
# import pandas as pd
# from rule_engine import run_rule_engine

# # ---------------- Page Config ----------------
# st.set_page_config(
#     page_title="Retail Business Rule Engine",
#     layout="wide"
# )

# # ---------------- Title ----------------
# st.title("📊 Retail Business Rule Engine")
# st.caption("Rule-based risk detection using Python & Streamlit")

# # ---------------- Load Dataset ----------------
# @st.cache_data
# def load_data():
#     return pd.read_csv("data/retail_sample.csv")

# df = load_data()

# # ---------------- Dataset Preview ----------------
# st.subheader("Dataset Preview")
# st.dataframe(df.head())

# # ---------------- Run Rule Engine ----------------
# st.subheader("⚠️ Business Alerts")

# alerts = run_rule_engine(df)

# if alerts:
#     for alert in alerts:
#         st.warning(alert)
# else:
#     st.success("No business risks detected")

# # ---------------- Footer ----------------
# st.markdown("---")
# st.caption("Built using Python rule engine (not possible in BI tools)")


import streamlit as st
import pandas as pd
from rule_engine import run_rule_engine

st.set_page_config(page_title="Retail Business Rule Engine", layout="wide")

st.title("📊 Retail Business Rule Engine")
st.caption("Upload your dataset and detect business risks")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your retail dataset (CSV format)",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("⚠️ Business Alerts")
    alerts = run_rule_engine(df)

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No business risks detected")

else:
    st.info("👆 Upload a CSV file to start analysis")
