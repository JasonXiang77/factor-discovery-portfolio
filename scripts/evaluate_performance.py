import pandas as pd
import numpy as np


path = (
    "data/processed/"
    "portfolio_returns.parquet"
)


df = pd.read_parquet(path)


df = df.dropna()


print("="*40)
print("Performance Evaluation")
print("="*40)


# ---------------------
# Total Return
# ---------------------

total_return = (
    df["nav"].iloc[-1] - 1
)



# ---------------------
# Annual Return
# ---------------------

days = (
    df["date"].iloc[-1]
    -
    df["date"].iloc[0]
).days


years = days / 365


annual_return = (
    df["nav"].iloc[-1]
    **
    (1 / years)
    -
    1
)



# ---------------------
# Volatility
# 月收益年化
# ---------------------

annual_vol = (
    df["portfolio_return"]
    .std()
    *
    np.sqrt(12)
)



# ---------------------
# Sharpe
# ---------------------

sharpe = (
    annual_return
    /
    annual_vol
)



# ---------------------
# Max Drawdown
# ---------------------

rolling_max = (
    df["nav"]
    .cummax()
)


drawdown = (
    df["nav"]
    /
    rolling_max
    -
    1
)


max_drawdown = (
    drawdown.min()
)



print(
    f"Period: {df['date'].min()} - {df['date'].max()}"
)

print(
    f"Total Return: {total_return:.2%}"
)

print(
    f"Annual Return: {annual_return:.2%}"
)

print(
    f"Annual Volatility: {annual_vol:.2%}"
)

print(
    f"Sharpe Ratio: {sharpe:.3f}"
)

print(
    f"Max Drawdown: {max_drawdown:.2%}"
)