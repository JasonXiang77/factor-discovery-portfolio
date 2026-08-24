import pandas as pd
import numpy as np


# ==================================================
# Config
# ==================================================

PORTFOLIO_PATH = (
    "data/processed/csi800_dynamic_icir_score.parquet"
)

FACTOR_PATH = (
    "data/processed/csi800_multifactor_v2.parquet"
)


OUTPUT_PATH = (
    "data/processed/dynamic_optimizer_result.parquet"
)


TOP_N = 100
VOL_WINDOW = 20


print("=" * 60)
print("Dynamic Optimizer V1")


# ==================================================
# Load
# ==================================================

portfolio = pd.read_parquet(
    PORTFOLIO_PATH
)

factor = pd.read_parquet(
    FACTOR_PATH
)


print("Portfolio")
print(portfolio.shape)


print("Factor")
print(factor.shape)



# ==================================================
# Date clean
# ==================================================

portfolio["date"] = pd.to_datetime(
    portfolio["date"]
)


factor["date"] = pd.to_datetime(
    factor["date"]
)



# ==================================================
# Select Top N by Dynamic ICIR
# ==================================================

portfolio = (
    portfolio
    .sort_values(
        [
            "date",
            "dynamic_icir_score"
        ],
        ascending=[
            True,
            False
        ]
    )
)



selected = (
    portfolio
    .groupby("date")
    .head(TOP_N)
    .copy()
)


selected = selected.reset_index(
    drop=True
)



print("Selected")
print(selected.shape)



# ==================================================
# Merge Return
# ==================================================

price = factor[
    [
        "ts_code",
        "date",
        "daily_return"
    ]
].copy()



price = price.rename(
    columns={
        "daily_return":
        "stock_return"
    }
)



data = selected.merge(
    price,
    on=[
        "ts_code",
        "date"
    ],
    how="left"
)



data = data.reset_index(
    drop=True
)



print("After return merge")
print(data.shape)



# ==================================================
# Volatility Estimation
# ==================================================

vol = factor[
    [
        "ts_code",
        "date",
        "daily_return"
    ]
].copy()



vol = vol.sort_values(
    [
        "ts_code",
        "date"
    ]
)



vol["vol20"] = (
    vol
    .groupby("ts_code")
    ["daily_return"]
    .rolling(
        VOL_WINDOW,
        min_periods=5
    )
    .std()
    .reset_index(
        level=0,
        drop=True
    )
)



data = data.merge(
    vol[
        [
            "ts_code",
            "date",
            "vol20"
        ]
    ],
    on=[
        "ts_code",
        "date"
    ],
    how="left"
)



data = data.reset_index(
    drop=True
)



data["vol20"] = (
    data["vol20"]
    .fillna(
        data["vol20"].median()
    )
)



# ==================================================
# Optimizer Score
# ==================================================

# Dynamic ICIR + volatility adjustment

data["optimizer_score"] = (
    data["dynamic_icir_score"]
    /
    (1 + data["vol20"])
)



# ==================================================
# Weight
# ==================================================

data["raw_weight"] = (
    data["optimizer_score"]
    .clip(lower=0)
)



data["weight"] = (
    data
    .groupby("date")
    ["raw_weight"]
    .transform(
        lambda x:
        x / x.sum()
        if x.sum() != 0
        else 1 / len(x)
    )
)



print("Weight check")


print(
    data
    .groupby("date")
    ["weight"]
    .sum()
    .head()
)



# ==================================================
# Portfolio Return
# ==================================================

daily = (
    data
    .groupby("date")
    .apply(
        lambda x:
        np.sum(
            x["weight"]
            *
            x["stock_return"].fillna(0)
        ),
        include_groups=False
    )
    .reset_index()
)



daily.columns = [
    "date",
    "portfolio_return"
]



daily["nav"] = (
    (1 + daily["portfolio_return"])
    .cumprod()
)



# ==================================================
# Performance Metrics
# ==================================================

daily["high_water"] = (
    daily["nav"]
    .cummax()
)



daily["drawdown"] = (
    daily["nav"]
    /
    daily["high_water"]
    -
    1
)



total_return = (
    daily["nav"]
    .iloc[-1]
    -
    1
)



years = (
    len(daily)
    /
    252
)



annual_return = (
    (1 + total_return)
    **
    (1 / years)
    -
    1
)



volatility = (
    daily["portfolio_return"]
    .std()
    *
    np.sqrt(252)
)



sharpe = (
    annual_return
    /
    volatility
)



max_drawdown = (
    daily["drawdown"]
    .min()
)



# ==================================================
# Print Result
# ==================================================

print("=" * 60)

print(
    "V1 Performance"
)


performance = pd.DataFrame(
    {
        "Metric":
        [
            "Total Return",
            "Annual Return",
            "Volatility",
            "Sharpe Ratio",
            "Max Drawdown"
        ],

        "Value":
        [
            total_return,
            annual_return,
            volatility,
            sharpe,
            max_drawdown
        ]
    }
)



print(performance)



print("=" * 60)


print(
    daily.head()
)


print(
    daily.tail()
)



# ==================================================
# Save
# ==================================================

daily.to_parquet(
    OUTPUT_PATH
)



print("=" * 60)

print("Saved:")
print(OUTPUT_PATH)