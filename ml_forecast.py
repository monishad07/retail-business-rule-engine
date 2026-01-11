# ml_forecast.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_profit_risk(df, profit_threshold):
    alerts = []

    df = df.copy()
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = (
        df.groupby(["Product", "Region", "Month"])["Profit"]
        .sum()
        .reset_index()
    )

    for (product, region), data in grouped.groupby(["Product", "Region"]):
        data = data.sort_values("Month")

        # Need at least 3 months for ML
        if len(data) < 3:
            continue

        X = np.arange(len(data)).reshape(-1, 1)
        y = data["Profit"].values

        model = LinearRegression()
        model.fit(X, y)

        next_month_index = np.array([[len(data)]])
        predicted_profit = model.predict(next_month_index)[0]

        if predicted_profit < profit_threshold:
            alerts.append({
                "type": "FORECAST_PROFIT_RISK",
                "group": "Product",
                "entity": f"{product} ({region})",
                "severity": "Medium" if predicted_profit > 0 else "High",
                "message": (
                    f"ML forecast predicts next month profit "
                    f"{predicted_profit:.0f}, below threshold {profit_threshold}"
                ),
                "recommendation": "Review pricing, discounts, and demand drivers"
            })

    return alerts
