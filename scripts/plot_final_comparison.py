import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =====================================================
# Config
# =====================================================

BASE_PATH = "data/processed"

FACTOR_PATH = (
    f"{BASE_PATH}/dynamic_optimizer_result.parquet"
)

OPTIMIZER_PATH = (
    f"{BASE_PATH}/dynamic_optimizer_v14_result.parquet"
)

INDEX_PATH = (
    f"{BASE_PATH}/../raw/csi800_index.parquet"
)


FIG_PATH = (
    "figures/performance_comparison.png"
)

CSV_PATH = (
    f"{BASE_PATH}/final_performance_comparison.csv"
)


# =====================================================
# Load Portfolio
# =====================================================

print("=" * 60)
print("Load Dynamic Factor Portfolio")


factor = pd.read_parquet(
    FACTOR_PATH
)


print(factor.head())
print(factor.columns)


factor["date"] = pd.to_datetime(
    factor["date"]
)


factor = (
    factor
    .sort_values("date")
    .reset_index(drop=True)
)


factor["nav"] = (
    factor["nav"]
    /
    factor["nav"].iloc[0]
)


factor_curve = factor[
    [
        "date",
        "nav"
    ]
].copy()


factor_curve.rename(
    columns={
        "nav":
        "Dynamic Factor Portfolio"
    },
    inplace=True
)



# =====================================================
# Load Dynamic Optimizer
# =====================================================

print("=" * 60)
print("Load Dynamic Optimizer V14")


optimizer = pd.read_parquet(
    OPTIMIZER_PATH
)


print(optimizer.head())
print(optimizer.columns)


optimizer["date"] = pd.to_datetime(
    optimizer["date"]
)


optimizer = (
    optimizer
    .sort_values("date")
    .reset_index(drop=True)
)


optimizer["v14_nav"] = (
    optimizer["v14_nav"]
    /
    optimizer["v14_nav"].iloc[0]
)


optimizer_curve = optimizer[
    [
        "date",
        "v14_nav"
    ]
].copy()


optimizer_curve.rename(
    columns={
        "v14_nav":
        "Dynamic Optimizer V14"
    },
    inplace=True
)



# =====================================================
# Load CSI800 Benchmark
# =====================================================

print("=" * 60)
print("Load CSI800 Benchmark")


index = pd.read_parquet(
    INDEX_PATH
)


print(index.columns)
print(index.head())


# 处理日期字段
if "date" in index.columns:

    index["date"] = pd.to_datetime(
        index["date"]
    )


elif "trade_date" in index.columns:

    index["date"] = pd.to_datetime(
        index["trade_date"]
    )

else:

    raise Exception(
        "No date column found"
    )


index = (
    index
    .sort_values("date")
    .reset_index(drop=True)
)


# 如果有close
if "close" in index.columns:

    index["index_nav"] = (
        index["close"]
        /
        index["close"].iloc[0]
    )

else:

    raise Exception(
        "No close column found"
    )


index_curve = index[
    [
        "date",
        "index_nav"
    ]
].copy()


index_curve.rename(
    columns={
        "index_nav":
        "CSI800 Benchmark"
    },
    inplace=True
)



# =====================================================
# Merge
# =====================================================

data = (
    factor_curve
    .merge(
        optimizer_curve,
        on="date",
        how="outer"
    )
    .merge(
        index_curve,
        on="date",
        how="outer"
    )
)


data = (
    data
    .sort_values("date")
    .reset_index(drop=True)
)


data = data.ffill()


print(data.head())



# =====================================================
# Plot
# =====================================================

plt.figure(
    figsize=(14,7)
)


plt.plot(
    data["date"],
    data["Dynamic Factor Portfolio"],
    label="Dynamic Factor Portfolio",
    linewidth=2
)


plt.plot(
    data["date"],
    data["Dynamic Optimizer V14"],
    label="Dynamic Optimizer V14",
    linewidth=2
)


plt.plot(
    data["date"],
    data["CSI800 Benchmark"],
    label="CSI800 Benchmark",
    linewidth=2
)


plt.title(
    "Dynamic Factor Portfolio vs Dynamic Optimizer vs CSI800 Benchmark",
    fontsize=15
)


plt.xlabel(
    "Date"
)


plt.ylabel(
    "Net Asset Value"
)


plt.grid(
    alpha=0.3
)


plt.legend()


plt.tight_layout()



Path(
    "figures"
).mkdir(
    exist_ok=True
)


plt.savefig(
    FIG_PATH,
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# =====================================================
# Performance Table
# =====================================================


def performance(nav):

    total_return = (
        nav.iloc[-1]
        -
        1
    )


    years = (
        len(nav)
        /
        252
    )


    annual_return = (
        (1+total_return)
        **
        (1/years)
        -
        1
    )


    daily_return = (
        nav
        .pct_change()
        .dropna()
    )


    volatility = (
        daily_return.std()
        *
        np.sqrt(252)
    )


    sharpe = (
        annual_return
        /
        volatility
    )


    high = (
        nav
        .cummax()
    )


    drawdown = (
        nav/high-1
    )


    max_dd = (
        drawdown.min()
    )


    return [
        total_return,
        annual_return,
        volatility,
        sharpe,
        max_dd
    ]



result = pd.DataFrame(
    [
        performance(
            data["Dynamic Factor Portfolio"]
        ),

        performance(
            data["Dynamic Optimizer V14"]
        ),

        performance(
            data["CSI800 Benchmark"]
        )
    ],

    columns=[
        "Total Return",
        "Annual Return",
        "Volatility",
        "Sharpe",
        "Max Drawdown"
    ],

    index=[
        "Dynamic Factor Portfolio",
        "Dynamic Optimizer V14",
        "CSI800 Benchmark"
    ]
)



print("="*60)
print(result)



result.to_csv(
    CSV_PATH
)



print("="*60)

print(
    "Saved Figure:"
)

print(
    FIG_PATH
)


print(
    "Saved Performance:"
)

print(
    CSV_PATH
)