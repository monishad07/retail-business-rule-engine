# import pandas as pd

# REQUIRED_COLUMNS = {"Date", "Product", "Profit", "Sales", "Discount", "Region"}

# def validate_columns(df):
#     missing = REQUIRED_COLUMNS - set(df.columns)
#     if missing:
#         return False, f"Missing columns: {', '.join(missing)}"
#     return True, None


# def high_sales_low_profit(df, sales_threshold=5000, profit_threshold=100):
#     alerts = []
#     filtered = df[(df["Sales"] > sales_threshold) & (df["Profit"] < profit_threshold)]

#     for _, row in filtered.iterrows():
#         alerts.append(
#             f"High sales but low profit for {row['Product']} "
#             f"(Sales: {row['Sales']}, Profit: {row['Profit']})"
#         )
#     return alerts


# def three_month_decline(df):
#     alerts = []
#     df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

#     grouped = df.groupby(["Product", "Month"])["Profit"].sum().reset_index()

#     for product, group in grouped.groupby("Product"):
#         profits = group.sort_values("Month")["Profit"].values
#         for i in range(len(profits) - 2):
#             if profits[i] > profits[i + 1] > profits[i + 2]:
#                 alerts.append(
#                     f"Profit declining for 3 months for product {product}"
#                 )
#                 break
#     return alerts


# def risky_discount(df, profit_threshold=100, discount_threshold=0.15):
#     alerts = []
#     risky = df[(df["Discount"] >= discount_threshold) & (df["Profit"] < profit_threshold)]

#     for _, row in risky.iterrows():
#         alerts.append(
#             f"High discount risk on {row['Product']} "
#             f"(Discount: {row['Discount']*100:.0f}%, Profit: {row['Profit']})"
#         )
#     return alerts


# def region_risk(df):
#     alerts = []
#     df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

#     grouped = df.groupby(["Region", "Month"])["Profit"].sum().reset_index()

#     for region, group in grouped.groupby("Region"):
#         profits = group.sort_values("Month")["Profit"].values
#         for i in range(len(profits) - 2):
#             if profits[i] > profits[i + 1] > profits[i + 2]:
#                 alerts.append(
#                     f"Profit declining for 3 months in region {region}"
#                 )
#                 break
#     return alerts


# def run_rule_engine(df):
#     valid, error = validate_columns(df)
#     if not valid:
#         return [error]

#     alerts = []
#     alerts.extend(high_sales_low_profit(df))
#     alerts.extend(three_month_decline(df))
#     alerts.extend(risky_discount(df))
#     alerts.extend(region_risk(df))

#     return list(set(alerts))


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

def validate_columns(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Missing columns: {', '.join(missing)}"
    return True, None


def high_sales_low_profit(df):
    alerts = []
    filtered = df[(df["Sales"] > 5000) & (df["Profit"] < 100)]

    for product in filtered["Product"].unique():
        alerts.append({
            "type": "HIGH_SALES_LOW_PROFIT",
            "entity": product,
            "message": f"High sales but low profit for {product}",
            "severity": "High"
        })
    return alerts


def three_month_decline(df):
    alerts = []
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Product", "Month"])["Profit"].sum().reset_index()

    for product, group in grouped.groupby("Product"):
        profits = group.sort_values("Month")["Profit"].values
        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append({
                    "type": "PRODUCT_PROFIT_DECLINE",
                    "entity": product,
                    "message": f"Profit declining for 3 months for product {product}",
                    "severity": "Medium"
                })
                break
    return alerts


def risky_discount(df):
    alerts = []
    risky = df[(df["Discount"] >= 0.15) & (df["Profit"] < 100)]

    for product in risky["Product"].unique():
        alerts.append({
            "type": "DISCOUNT_RISK",
            "entity": product,
            "message": f"High discount risk on {product}",
            "severity": "High"
        })
    return alerts


def region_risk(df):
    alerts = []
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Region", "Month"])["Profit"].sum().reset_index()

    for region, group in grouped.groupby("Region"):
        profits = group.sort_values("Month")["Profit"].values
        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append({
                    "type": "REGION_PROFIT_DECLINE",
                    "entity": region,
                    "message": f"Profit declining for 3 months in region {region}",
                    "severity": "Medium"
                })
                break
    return alerts


def deduplicate_alerts(alerts):
    seen = set()
    unique_alerts = []

    for alert in alerts:
        key = (alert["type"], alert["entity"])
        if key not in seen:
            seen.add(key)
            unique_alerts.append(alert)

    return unique_alerts


def run_rule_engine(df):
    valid, error = validate_columns(df)
    if not valid:
        return [{
            "type": "DATA_ERROR",
            "entity": "Dataset",
            "message": error,
            "severity": "High"
        }]

    alerts = []
    alerts.extend(high_sales_low_profit(df))
    alerts.extend(three_month_decline(df))
    alerts.extend(risky_discount(df))
    alerts.extend(region_risk(df))

    return deduplicate_alerts(alerts)


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

