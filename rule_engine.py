import pandas as pd

def high_sales_low_profit(df, sales_threshold=5000, profit_threshold=100):
    alerts = []
    df_filtered = df[(df['Sales'] > sales_threshold) & (df['Profit'] < profit_threshold)]
    for _, row in df_filtered.iterrows():
        alerts.append(
            f"{row['Date']} | {row['Product']} | Sales: {row['Sales']} | Profit: {row['Profit']}"
        )
    return alerts


def three_month_decline(df):
    alerts = []
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_profit = df.groupby(['Product', 'Month'])['Profit'].sum().reset_index()

    for product in monthly_profit['Product'].unique():
        temp = monthly_profit[monthly_profit['Product'] == product].sort_values('Month')
        profits = temp['Profit'].values

        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append(
                    f"{product} profit declined for 3 consecutive months"
                )
    return alerts


def risky_discount(df, profit_threshold=100, discount_threshold=0.15):
    alerts = []
    df_filtered = df[
        (df['Discount'] >= discount_threshold) &
        (df['Profit'] < profit_threshold)
    ]

    for _, row in df_filtered.iterrows():
        alerts.append(
            f"{row['Product']} | Discount: {row['Discount'] * 100}% | Profit: {row['Profit']}"
        )
    return alerts


def region_risk(df):
    alerts = []
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_region_profit = df.groupby(['Region', 'Month'])['Profit'].sum().reset_index()

    for region in monthly_region_profit['Region'].unique():
        temp = monthly_region_profit[
            monthly_region_profit['Region'] == region
        ].sort_values('Month')

        profits = temp['Profit'].values

        for i in range(len(profits) - 2):
            if profits[i] > profits[i + 1] > profits[i + 2]:
                alerts.append(
                    f"{region} region profit declined for 3 months"
                )
    return alerts


def run_rule_engine(df):
    alerts = []
    alerts.extend(high_sales_low_profit(df))
    alerts.extend(three_month_decline(df))
    alerts.extend(risky_discount(df))
    alerts.extend(region_risk(df))
    return alerts
