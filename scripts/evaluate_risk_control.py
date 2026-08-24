import pandas as pd
import numpy as np


# ===============================
# Load
# ===============================

path = "data/processed/dynamic_risk_control_result.parquet"

df = pd.read_parquet(path)

print("="*60)
print("Loaded:")
print(df.shape)

print(df.head())


# ===============================
# Basic metrics
# ===============================

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")


nav = df["nav"]


total_return = nav.iloc[-1] - 1


days = len(df)

annual_return = (
    nav.iloc[-1] ** (252 / days)
    - 1
)


annual_vol = (
    df["portfolio_return"]
    .std()
    *
    np.sqrt(252)
)


sharpe = annual_return / annual_vol


# ===============================
# Drawdown
# ===============================

cummax = nav.cummax()

drawdown = nav / cummax - 1

max_dd = drawdown.min()


calmar = annual_return / abs(max_dd)


win_rate = (
    (df["portfolio_return"] > 0)
    .mean()
)


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
            max_dd,
            calmar,
            win_rate
        ]
    }
)


print("="*60)
print("Risk Control Strategy Performance")
print(result)


# ===============================
# Monthly return
# ===============================

monthly = (
    df
    .set_index("date")
    ["portfolio_return"]
    .resample("ME")
    .apply(lambda x:(1+x).prod()-1)
)


print("="*60)
print("Monthly Return")
print(monthly.head())

print(monthly.tail())


# ===============================
# Save
# ===============================

result.to_csv(
    "data/processed/risk_control_performance.csv",
    index=False
)


monthly.to_csv(
    "data/processed/risk_control_monthly_return.csv"
)


print("="*60)
print("Saved")