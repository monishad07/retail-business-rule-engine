


import pandas as pd

REQUIRED_COLUMNS = {"Date", "Product", "Profit", "Sales", "Discount", "Region"}

def validate_columns(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Missing columns: {', '.join(missing)}"
    return True, None


def high_sales_low_profit(df, sales_threshold=5000, profit_threshold=100):
    alerts = []
    filtered = df[(df["Sales"] > sales_threshold) & (df["Profit"] < profit_threshold)]

    for _, row in filtered.iterrows():
        alerts.append(
            f"⚠ High Sales–Low Profit → {row['Product']} | Sales: {row['Sales']} | Profit: {row['Profit']}"
        )
    return alerts


def three_month_decline(df):
    alerts = []
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Product", "Month"])["Profit"].sum().reset_index()

    for product, group in grouped.groupby("Product"):
        profits = group.sort_values("Month")["Profit"].values

        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append(
                    f"📉 {product} profit declined for 3 consecutive months"
                )
                break  # avoid duplicates

    return alerts


def risky_discount(df, profit_threshold=100, discount_threshold=0.15):
    alerts = []
    risky = df[(df["Discount"] >= discount_threshold) & (df["Profit"] < profit_threshold)]

    for _, row in risky.iterrows():
        alerts.append(
            f"⚠ High Discount Risk → {row['Product']} | Discount: {row['Discount']*100:.0f}% | Profit: {row['Profit']}"
        )
    return alerts


def region_risk(df):
    alerts = []
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = df.groupby(["Region", "Month"])["Profit"].sum().reset_index()

    for region, group in grouped.groupby("Region"):
        profits = group.sort_values("Month")["Profit"].values

        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append(
                    f"🌍 Region Risk: {region} profit declining for 3 months"
                )
                break

    return alerts


def run_rule_engine(df):
    valid, error = validate_columns(df)
    if not valid:
        return [error]

    alerts = []
    alerts.extend(high_sales_low_profit(df))
    alerts.extend(three_month_decline(df))
    alerts.extend(risky_discount(df))
    alerts.extend(region_risk(df))

    return list(set(alerts))  # remove duplicates

def compute_kpis(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    top_products = (
        df.groupby("Product")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return total_sales, total_profit, top_products

