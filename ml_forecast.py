import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_profit_ml(df, profit_threshold):
    alerts = []

    df = df.copy()
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    monthly = (
        df.groupby(["Product", "Month"])["Profit"]
        .sum()
        .reset_index()
    )

    for product, group in monthly.groupby("Product"):

        if len(group) < 4:
            continue  # not enough history

        group = group.sort_values("Month")
        group["month_index"] = range(len(group))

        X = group[["month_index"]]
        y = group["Profit"]

        model = LinearRegression()
        model.fit(X, y)

        next_month_index = [[group["month_index"].max() + 1]]
        predicted_profit = model.predict(next_month_index)[0]

        if predicted_profit < profit_threshold:
            alerts.append({
                "type": "ML_FORECAST_PROFIT_RISK",
                "group": "Product",
                "entity": product,
                "message": (
                    f"ML forecast predicts low profit next month "
                    f"({predicted_profit:.2f})"
                ),
                "severity": "High",
                "recommendation": (
                    "Review pricing, cost structure, and promotions "
                    "based on ML forecast."
                )
            })

    return alerts

