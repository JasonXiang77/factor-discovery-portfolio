import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


input_path = (
    "data/processed/"
    "portfolio_returns.parquet"
)


output_dir = Path(
    "figures"
)

output_dir.mkdir(
    exist_ok=True
)



# =====================
# Load
# =====================

df = pd.read_parquet(
    input_path
)

df = df.dropna()


df["date"] = pd.to_datetime(
    df["date"]
)


print(df.head())



# =====================
# NAV Curve
# =====================

plt.figure(
    figsize=(10,5)
)


plt.plot(
    df["date"],
    df["nav"]
)


plt.title(
    "Multi-factor Portfolio NAV"
)


plt.xlabel(
    "Date"
)


plt.ylabel(
    "NAV"
)


plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    output_dir /
    "nav_curve.png",
    dpi=300
)


plt.close()



# =====================
# Drawdown
# =====================


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



plt.figure(
    figsize=(10,5)
)


plt.plot(
    df["date"],
    drawdown
)


plt.title(
    "Portfolio Drawdown"
)


plt.xlabel(
    "Date"
)


plt.ylabel(
    "Drawdown"
)


plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    output_dir /
    "drawdown.png",
    dpi=300
)


plt.close()



print(
    "Saved figures:"
)

print(
    output_dir /
    "nav_curve.png"
)

print(
    output_dir /
    "drawdown.png"
)