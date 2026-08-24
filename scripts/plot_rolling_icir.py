import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


INPUT = (
    "reports/"
    "strategy_ic.csv"
)


OUTPUT = (
    "figures/"
    "rolling_icir.png"
)


Path(
    "figures"
).mkdir(
    exist_ok=True
)


# =========================
# Load IC
# =========================

df = pd.read_csv(
    INPUT
)


df["date"] = pd.to_datetime(
    df["date"]
)


df = df.sort_values(
    "date"
)


# =========================
# Rolling ICIR
# =========================

window = 60


rolling_mean = (
    df["IC"]
    .rolling(window)
    .mean()
)


rolling_std = (
    df["IC"]
    .rolling(window)
    .std()
)


df["rolling_ICIR"] = (
    rolling_mean /
    rolling_std
)


# =========================
# Plot
# =========================

plt.figure(
    figsize=(10,5)
)


plt.plot(
    df["date"],
    df["rolling_ICIR"]
)


plt.axhline(
    y=0,
    linestyle="--"
)


plt.title(
    "Rolling 60-Day ICIR"
)


plt.xlabel(
    "Date"
)


plt.ylabel(
    "ICIR"
)


plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    OUTPUT,
    dpi=300
)


plt.close()


print(
    "Saved:"
)

print(
    OUTPUT
)