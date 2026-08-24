import pandas as pd
import numpy as np



strategy_path = (
    "data/processed/"
    "portfolio_returns.parquet"
)


benchmark_path = (
    "data/raw/"
    "csi800_index.parquet"
)



# =====================
# Load
# =====================

strategy = pd.read_parquet(
    strategy_path
)


benchmark = pd.read_parquet(
    benchmark_path
)



strategy = strategy.dropna()


strategy["date"] = pd.to_datetime(
    strategy["date"]
)


benchmark["trade_date"] = pd.to_datetime(
    benchmark["trade_date"]
)



# =====================
# Benchmark monthly return
# =====================

benchmark = benchmark.sort_values(
    "trade_date"
)


benchmark["month"] = (
    benchmark["trade_date"]
    .dt
    .to_period("M")
)


benchmark_monthly = (
    benchmark
    .groupby("month")
    ["close"]
    .last()
)


benchmark_return = (
    benchmark_monthly
    .pct_change()
    .dropna()
    .reset_index()
)


benchmark_return.columns = [
    "month",
    "benchmark_return"
]


benchmark_return["month"] = (
    benchmark_return["month"]
    .astype(str)
)



# =====================
# Strategy monthly
# =====================

strategy["month"] = (
    strategy["date"]
    .dt
    .to_period("M")
    .astype(str)
)


strategy_monthly = strategy[
    [
        "month",
        "portfolio_return"
    ]
]


# =====================
# Merge
# =====================

df = strategy_monthly.merge(
    benchmark_return,
    on="month",
    how="inner"
)



print(df.head())



# =====================
# Performance function
# =====================

def performance(
    returns
):

    nav = (
        1 + returns
    ).cumprod()


    total_return = (
        nav.iloc[-1] - 1
    )


    years = (
        len(returns)
        /
        12
    )


    annual_return = (
        nav.iloc[-1]
        **
        (1 / years)
        -
        1
    )


    volatility = (
        returns.std()
        *
        np.sqrt(12)
    )


    sharpe = (
        annual_return
        /
        volatility
    )


    drawdown = (
        nav /
        nav.cummax()
        -
        1
    )


    max_dd = drawdown.min()


    return [
        total_return,
        annual_return,
        volatility,
        sharpe,
        max_dd
    ]



# =====================
# Results
# =====================

strategy_result = performance(
    df["portfolio_return"]
)


benchmark_result = performance(
    df["benchmark_return"]
)



result = pd.DataFrame(
    [
        strategy_result,
        benchmark_result
    ],
    columns=[
        "Total Return",
        "Annual Return",
        "Volatility",
        "Sharpe",
        "Max Drawdown"
    ],
    index=[
        "Multi-factor",
        "CSI800"
    ]
)



print("="*60)

print(result)

print("="*60)



# Excess

excess = (
    df["portfolio_return"]
    -
    df["benchmark_return"]
)


information_ratio = (
    excess.mean()
    /
    excess.std()
    *
    np.sqrt(12)
)



print(
    "Information Ratio:",
    round(
        information_ratio,
        3
    )
)