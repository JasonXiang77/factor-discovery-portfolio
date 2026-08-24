import pandas as pd
import matplotlib.pyplot as plt


# ============================
# Config
# ============================

V1_PATH = (
    "data/processed/dynamic_optimizer_result.parquet"
)

V14_PATH = (
    "data/processed/dynamic_optimizer_v14_result.parquet"
)


OUTPUT = (
    "results/v1_vs_v14_nav.png"
)


# ============================
# Load
# ============================

v1 = pd.read_parquet(V1_PATH)

v14 = pd.read_parquet(V14_PATH)


v1["date"] = pd.to_datetime(v1["date"])
v14["date"] = pd.to_datetime(v14["date"])


# ============================
# Plot NAV
# ============================

plt.figure(figsize=(12,5))


plt.plot(
    v1["date"],
    v1["nav"],
    label="V1 Dynamic Factor Portfolio"
)


plt.plot(
    v14["date"],
    v14["v14_nav"],
    label="V14 Risk Controlled Optimizer"
)


plt.title(
    "Portfolio NAV Comparison"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "NAV"
)


plt.legend()

plt.grid(
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    OUTPUT,
    dpi=300
)


plt.close()


print(
    "Saved:",
    OUTPUT
)
# ============================
# Drawdown
# ============================


v1["high_water"] = (
    v1["nav"]
    .cummax()
)


v1["drawdown"] = (
    v1["nav"]
    /
    v1["high_water"]
    -
    1
)


v14["high_water"] = (
    v14["v14_nav"]
    .cummax()
)


v14["drawdown"] = (
    v14["v14_nav"]
    /
    v14["high_water"]
    -
    1
)



plt.figure(figsize=(12,5))


plt.plot(
    v1["date"],
    v1["drawdown"],
    label="V1 Drawdown"
)


plt.plot(
    v14["date"],
    v14["drawdown"],
    label="V14 Drawdown"
)


plt.title(
    "Drawdown Comparison"
)


plt.ylabel(
    "Drawdown"
)


plt.legend()

plt.grid(
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    "results/v1_vs_v14_drawdown.png",
    dpi=300
)


plt.close()
import matplotlib.pyplot as plt
import numpy as np


metrics = [
    "Annual Return",
    "Volatility",
    "Sharpe Ratio",
    "Max Drawdown"
]


v1_values = [
    0.1539,
    0.1875,
    0.8209,
    -0.3425
]


v14_values = [
    0.1787,
    0.1041,
    1.7170,
    -0.1377
]


x = np.arange(len(metrics))

width = 0.35


plt.figure(figsize=(10,5))


plt.bar(
    x-width/2,
    v1_values,
    width,
    label="V1"
)


plt.bar(
    x+width/2,
    v14_values,
    width,
    label="V14"
)


plt.xticks(
    x,
    metrics,
    rotation=20
)


plt.title(
    "Performance Metrics Comparison"
)


plt.legend()

plt.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    "results/v1_vs_v14_metrics.png",
    dpi=300
)


plt.close()