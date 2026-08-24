import pandas as pd
import numpy as np


PATH = (
    "data/processed/dynamic_optimizer_v3_result.parquet"
)


df = pd.read_parquet(PATH)


print("="*60)

print(df.head())


# =====================
# Metrics
# =====================

total_return = (
    df["nav"].iloc[-1]-1
)


years = (
    len(df)/252
)


annual_return = (
    (df["nav"].iloc[-1])
    **
    (1/years)
    -
    1
)



volatility = (

    df["net_return"]
    .std()
    *
    np.sqrt(252)

)



sharpe = (

    annual_return
    /
    volatility

)



# drawdown

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



calmar = (

    annual_return
    /
    abs(max_drawdown)

)



win_rate = (

    (
        df["net_return"]>0
    )
    .mean()

)



avg_turnover = (

    df["turnover"]
    .mean()

)



annual_cost = (

    df["cost"]
    .sum()
    /
    years

)



result = pd.DataFrame(

[
[
"Total Return",
total_return
],

[
"Annual Return",
annual_return
],

[
"Volatility",
volatility
],

[
"Sharpe Ratio",
sharpe
],

[
"Max Drawdown",
max_drawdown
],

[
"Calmar Ratio",
calmar
],

[
"Win Rate",
win_rate
],

[
"Average Turnover",
avg_turnover
],

[
"Annual Cost",
annual_cost
]

],

columns=[
"Metric",
"Value"
]

)


print("="*60)

print(
result
)


result.to_csv(
"data/processed/dynamic_optimizer_v3_performance.csv",
index=False
)


print("Saved")