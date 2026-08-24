import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =====================================================
# Config
# =====================================================

INPUT_V3 = (
    "data/processed/"
    "dynamic_optimizer_v3_result.parquet"
)

INPUT_V14 = (
    "data/processed/"
    "dynamic_optimizer_v14_result.parquet"
)


OUTPUT_DIR = Path(
    "reports/dynamic_optimizer"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================================
# Load
# =====================================================

print("="*60)
print("Dynamic Optimizer Research Report")


v3 = pd.read_parquet(
    INPUT_V3
)

v14 = pd.read_parquet(
    INPUT_V14
)


for df in [v3,v14]:

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df.sort_values(
        "date",
        inplace=True
    )



# =====================================================
# Helper
# =====================================================

def performance(
    df,
    ret_col,
    name
):

    nav = (
        (1+df[ret_col])
        .cumprod()
    )

    high = (
        nav
        .cummax()
    )

    dd = (
        nav/high-1
    )


    years = len(df)/252


    total = (
        nav.iloc[-1]-1
    )


    annual = (
        (1+total)
        **
        (1/years)
        -1
    )


    vol = (
        df[ret_col]
        .std()
        *
        np.sqrt(252)
    )


    sharpe = (
        annual/vol
    )


    return pd.Series(
        {
            "Strategy":name,
            "Total Return":total,
            "Annual Return":annual,
            "Volatility":vol,
            "Sharpe Ratio":sharpe,
            "Max Drawdown":dd.min()
        }
    )



# =====================================================
# Metrics
# =====================================================


v3_metric = performance(
    v3,
    "net_return",
    "V3 Base"
)


v14_metric = performance(
    v14,
    "v14_return",
    "V14 Final"
)



summary = pd.DataFrame(
    [
        v3_metric,
        v14_metric
    ]
)



print(summary)



summary.to_csv(
    OUTPUT_DIR /
    "performance_summary.csv",
    index=False
)



# =====================================================
# NAV Curve
# =====================================================


v3_nav = (
    (1+v3["net_return"])
    .cumprod()
)


v14_nav = (
    (1+v14["v14_return"])
    .cumprod()
)


plt.figure(
    figsize=(12,5)
)


plt.plot(
    v3["date"],
    v3_nav,
    label="V3"
)


plt.plot(
    v14["date"],
    v14_nav,
    label="V14"
)


plt.title(
    "Dynamic Optimizer NAV"
)

plt.legend()

plt.grid()


plt.savefig(
    OUTPUT_DIR /
    "nav_curve.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# =====================================================
# Drawdown
# =====================================================


def drawdown(nav):

    return (
        nav/nav.cummax()
        -1
    )



plt.figure(
    figsize=(12,5)
)


plt.plot(
    v3["date"],
    drawdown(v3_nav),
    label="V3"
)


plt.plot(
    v14["date"],
    drawdown(v14_nav),
    label="V14"
)


plt.title(
    "Drawdown Comparison"
)

plt.legend()

plt.grid()


plt.savefig(
    OUTPUT_DIR /
    "drawdown_curve.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# =====================================================
# Rolling Sharpe
# =====================================================


window = 252


rolling_sharpe = (
    v14["v14_return"]
    .rolling(window)
    .mean()
    /
    v14["v14_return"]
    .rolling(window)
    .std()
    *
    np.sqrt(252)
)



plt.figure(
    figsize=(12,5)
)


plt.plot(
    v14["date"],
    rolling_sharpe
)


plt.axhline(
    1,
    linestyle="--"
)


plt.title(
    "V14 Rolling Sharpe"
)

plt.grid()


plt.savefig(
    OUTPUT_DIR /
    "rolling_sharpe.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# =====================================================
# Annual Return
# =====================================================


v14_tmp = v14.copy()

v14_tmp["year"] = (
    v14_tmp["date"]
    .dt.year
)


annual = (
    v14_tmp
    .groupby("year")
    ["v14_return"]
    .apply(
        lambda x:
        (1+x).prod()-1
    )
)



annual.to_csv(
    OUTPUT_DIR /
    "annual_return.csv"
)



# =====================================================
# Final Report Table
# =====================================================


print("="*60)

print(
"Saved:"
)

print(
OUTPUT_DIR
)

print("="*60)