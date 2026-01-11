

# import pandas as pd

# REQUIRED_COLUMNS = {"Date", "Product", "Profit", "Sales", "Discount", "Region"}

# # ------------------ VALIDATION ------------------
# def validate_columns(df):
#     missing = REQUIRED_COLUMNS - set(df.columns)
#     if missing:
#         return False, f"Missing columns: {', '.join(missing)}"
#     return True, None


# # ------------------ RULES ------------------
# def high_sales_low_profit(df, sales_threshold, profit_threshold):
#     alerts = []
#     filtered = df[(df["Sales"] > sales_threshold) & (df["Profit"] < profit_threshold)]

#     for product in filtered["Product"].unique():
#         alerts.append({
#             "type": "HIGH_SALES_LOW_PROFIT",
#             "group": "Product",
#             "entity": product,
#             "message": f"High sales (> {sales_threshold}) but low profit (< {profit_threshold})",
#             "severity": "High"
#         })
#     return alerts


# def three_month_decline(df):
#     alerts = []
#     df = df.copy()
#     df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

#     grouped = df.groupby(["Product", "Month"])["Profit"].sum().reset_index()

#     for product, group in grouped.groupby("Product"):
#         profits = group.sort_values("Month")["Profit"].values
#         for i in range(len(profits) - 2):
#             if profits[i] > profits[i + 1] > profits[i + 2]:
#                 alerts.append({
#                     "type": "PRODUCT_PROFIT_DECLINE",
#                     "group": "Product",
#                     "entity": product,
#                     "message": "Profit declining for 3 consecutive months",
#                     "severity": "Medium"
#                 })
#                 break
#     return alerts


# def risky_discount(df, discount_threshold, profit_threshold):
#     alerts = []
#     risky = df[(df["Discount"] >= discount_threshold) & (df["Profit"] < profit_threshold)]

#     for product in risky["Product"].unique():
#         alerts.append({
#             "type": "DISCOUNT_RISK",
#             "group": "Product",
#             "entity": product,
#             "message": f"High discount (≥ {discount_threshold*100:.0f}%) with low profit",
#             "severity": "High"
#         })
#     return alerts


# def region_risk(df):
#     alerts = []
#     df = df.copy()
#     df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

#     grouped = df.groupby(["Region", "Month"])["Profit"].sum().reset_index()

#     for region, group in grouped.groupby("Region"):
#         profits = group.sort_values("Month")["Profit"].values
#         for i in range(len(profits) - 2):
#             if profits[i] > profits[i + 1] > profits[i + 2]:
#                 alerts.append({
#                     "type": "REGION_PROFIT_DECLINE",
#                     "group": "Region",
#                     "entity": region,
#                     "message": "Region profit declining for 3 consecutive months",
#                     "severity": "Medium"
#                 })
#                 break
#     return alerts


# # ------------------ HELPERS ------------------
# def deduplicate_alerts(alerts):
#     seen = set()
#     unique = []

#     for alert in alerts:
#         key = (alert["type"], alert["entity"])
#         if key not in seen:
#             seen.add(key)
#             unique.append(alert)

#     return unique


# # ------------------ ENGINE ------------------
# def run_rule_engine(df, sales_threshold, profit_threshold, discount_threshold):
#     valid, error = validate_columns(df)
#     if not valid:
#         return [{
#             "type": "DATA_ERROR",
#             "group": "System",
#             "entity": "Dataset",
#             "message": error,
#             "severity": "High"
#         }]

#     alerts = []
#     alerts.extend(high_sales_low_profit(df, sales_threshold, profit_threshold))
#     alerts.extend(three_month_decline(df))
#     alerts.extend(risky_discount(df, discount_threshold, profit_threshold))
#     alerts.extend(region_risk(df))

#     return deduplicate_alerts(alerts)


# # ------------------ KPIs ------------------
# def compute_kpis(df):
#     total_sales = float(df["Sales"].sum())
#     total_profit = float(df["Profit"].sum())

#     top_products = (
#         df.groupby("Product")["Profit"]
#         .sum()
#         .sort_values(ascending=False)
#         .head(5)
#         .reset_index()
#     )

#     return total_sales, total_profit, top_products

import pandas as pd

REQUIRED_COLUMNS = {"Date", "Product", "Profit", "Sales", "Discount", "Region"}

# ------------------ VALIDATION ------------------
def validate_columns(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Missing columns: {', '.join(missing)}"
    return True, None


# ------------------ RULES ------------------
def high_sales_low_profit(df, sales_threshold, profit_threshold):
    alerts = []
    filtered = df[(df["Sales"] > sales_threshold) & (df["Profit"] < profit_threshold)]

    for product in filtered["Product"].unique():
        alerts.append({
            "type": "HIGH_SALES_LOW_PROFIT",
            "group": "Product",
            "entity": product,
            "message": f"High sales (> {sales_threshold}) but low profit (< {profit_threshold})",
            "severity": "High"
        })
    return alerts


def three_month_decline(df):
    alerts = []
    df = df.copy()
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Product", "Month"])["Profit"].sum().reset_index()

    for product, group in grouped.groupby("Product"):
        profits = group.sort_values("Month")["Profit"].values
        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append({
                    "type": "PRODUCT_PROFIT_DECLINE",
                    "group": "Product",
                    "entity": product,
                    "message": "Profit declining for 3 consecutive months",
                    "severity": "Medium"
                })
                break
    return alerts


def risky_discount(df, discount_threshold, profit_threshold):
    alerts = []
    risky = df[(df["Discount"] >= discount_threshold) & (df["Profit"] < profit_threshold)]

    for product in risky["Product"].unique():
        alerts.append({
            "type": "DISCOUNT_RISK",
            "group": "Product",
            "entity": product,
            "message": f"High discount (≥ {discount_threshold*100:.0f}%) with low profit",
            "severity": "High"
        })
    return alerts


def region_risk(df):
    alerts = []
    df = df.copy()
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Region", "Month"])["Profit"].sum().reset_index()

    for region, group in grouped.groupby("Region"):
        profits = group.sort_values("Month")["Profit"].values
        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append({
                    "type": "REGION_PROFIT_DECLINE",
                    "group": "Region",
                    "entity": region,
                    "message": "Region profit declining for 3 consecutive months",
                    "severity": "Medium"
                })
                break
    return alerts


# 🔮 ------------------ FORECAST RULE ------------------
def forecast_decline_risk(df):
    alerts = []
    df = df.copy()
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Product", "Month"])["Profit"].sum().reset_index()

    for product, group in grouped.groupby("Product"):
        group = group.sort_values("Month")

        if len(group) < 3:
            continue

        last_three = group.tail(3)["Profit"].values

        if last_three[0] > last_three[1] > last_three[2]:
            alerts.append({
                "type": "FORECAST_PROFIT_RISK",
                "group": "Product",
                "entity": product,
                "message": "Forecast warning: profit declining for last 2 months, next month at risk",
                "severity": "High"
            })

    return alerts


# ------------------ HELPERS ------------------
def deduplicate_alerts(alerts):
    seen = set()
    unique = []

    for alert in alerts:
        key = (alert["type"], alert["entity"])
        if key not in seen:
            seen.add(key)
            unique.append(alert)

    return unique


# ------------------ ENGINE ------------------
def run_rule_engine(df, sales_threshold, profit_threshold, discount_threshold):
    valid, error = validate_columns(df)
    if not valid:
        return [{
            "type": "DATA_ERROR",
            "group": "System",
            "entity": "Dataset",
            "message": error,
            "severity": "High"
        }]

    alerts = []
    alerts.extend(high_sales_low_profit(df, sales_threshold, profit_threshold))
    alerts.extend(three_month_decline(df))
    alerts.extend(risky_discount(df, discount_threshold, profit_threshold))
    alerts.extend(region_risk(df))
    alerts.extend(forecast_decline_risk(df))  # 🔮 NEW

    return deduplicate_alerts(alerts)


# ------------------ KPIs ------------------
def compute_kpis(df):
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())

    top_products = (
        df.groupby("Product")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return total_sales, total_profit, top_products


