import pandas as pd
import numpy as np
import os


# =========================
# Config
# =========================

FILE = (
    "data/processed/"
    "dynamic_backtest_result.parquet"
)


# =========================
# Load
# =========================

df = pd.read_parquet(
    FILE
)


df["date"] = pd.to_datetime(
    df["date"]
)


df = df.sort_values(
    "date"
)


print("="*60)

print("Loaded:")
print(df.shape)

print(df.head())



# =========================
# Basic
# =========================


returns = (
    df["net_return"]
    .dropna()
)


nav = (
    df["nav"]
    .dropna()
)



# =========================
# Performance
# =========================


total_return = (
    nav.iloc[-1]
    -
    1
)



years = (
    (df["date"].iloc[-1]
     -
     df["date"].iloc[0])
    .days
    /
    365
)



annual_return = (
    (nav.iloc[-1])
    **
    (1 / years)
    -
    1
)



annual_vol = (
    returns.std()
    *
    np.sqrt(252)
)



sharpe = (
    annual_return
    /
    annual_vol
)



# =========================
# Drawdown
# =========================


rolling_max = (
    nav
    .cummax()
)


drawdown = (
    nav
    /
    rolling_max
    -
    1
)



max_drawdown = (
    drawdown.min()
)



calmar = (
    annual_return
    /
    abs(max_drawdown)
)



# =========================
# Win rate
# =========================


win_rate = (
    (returns > 0)
    .mean()
)



# =========================
# Monthly
# =========================


monthly = (
    df
    .set_index("date")
    ["net_return"]
    .resample("ME")
    .apply(
        lambda x:
        (1+x).prod()-1
    )
)



# =========================
# Output
# =========================


result = pd.DataFrame(
    {
        "Metric":
        [
            "Total Return",
            "Annual Return",
            "Annual Volatility",
            "Sharpe Ratio",
            "Max Drawdown",
            "Calmar Ratio",
            "Win Rate"
        ],

        "Value":
        [
            total_return,
            annual_return,
            annual_vol,
            sharpe,
            max_drawdown,
            calmar,
            win_rate
        ]
    }
)



print("\n")
print("="*60)
print("Dynamic ICIR Strategy Performance")
print("="*60)


print(result)



print("\nMonthly Return:")
print(monthly.head())

print(monthly.tail())



# save

output = (
    "data/processed/"
    "dynamic_performance.csv"
)


result.to_csv(
    output,
    index=False
)


monthly.to_csv(
    "data/processed/"
    "dynamic_monthly_return.csv"
)



print("\nSaved:")
print(output)