# ml_forecast.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_profit_risk(df, profit_threshold):
    alerts = []
    forecasts = []

    df = df.copy()
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    grouped = (
        df.groupby(["Product", "Region", "Month"])["Profit"]
        .sum()
        .reset_index()
    )

    for (product, region), data in grouped.groupby(["Product", "Region"]):
        data = data.sort_values("Month")

        if len(data) < 3:
            continue

        X = np.arange(len(data)).reshape(-1, 1)
        y = data["Profit"].values

        model = LinearRegression()
        model.fit(X, y)

        next_x = np.array([[len(data)]])
        predicted = model.predict(next_x)[0]

        # --- Confidence band (simple statistical approximation)
        residuals = y - model.predict(X)
        std = residuals.std() if len(residuals) > 1 else 0

        lower = predicted - 1.96 * std
        upper = predicted + 1.96 * std

        forecasts.append({
            "Product": product,
            "Region": region,
            "Months": data["Month"].astype(str).tolist(),
            "ActualProfit": y.tolist(),
            "PredictedProfit": predicted,
            "LowerBound": lower,
            "UpperBound": upper
        })

        if predicted < profit_threshold:
            alerts.append({
                "type": "FORECAST_PROFIT_RISK",
                "group": "Product",
                "entity": f"{product} ({region})",
                "severity": "High" if predicted < 0 else "Medium",
                "message": (
                    f"ML forecast predicts next month profit "
                    f"{predicted:.0f}, below threshold {profit_threshold}"
                ),
                "recommendation": "Review pricing, discounting, and demand drivers"
            })

    return alerts, forecasts
