import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


INPUT = (
    "reports/"
    "strategy_ic.csv"
)

OUTPUT_DIR = Path(
    "figures"
)


OUTPUT_DIR.mkdir(
    exist_ok=True
)


# =========================
# Load
# =========================

df = pd.read_csv(INPUT)

df["date"] = pd.to_datetime(
    df["date"]
)

df = df.sort_values(
    "date"
)


# =========================
# Cumulative IC
# =========================

df["cumulative_ic"] = (
    df["IC"]
    .cumsum()
)


plt.figure(
    figsize=(10,5)
)

plt.plot(
    df["date"],
    df["cumulative_ic"]
)

plt.title(
    "Cumulative IC Curve"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Cumulative IC"
)

plt.grid(
    True
)

plt.tight_layout()


plt.savefig(
    OUTPUT_DIR /
    "cumulative_ic_curve.png",
    dpi=300
)

plt.close()



# =========================
# IC Distribution
# =========================

plt.figure(
    figsize=(8,5)
)


plt.hist(
    df["IC"].dropna(),
    bins=40
)


plt.title(
    "IC Distribution"
)

plt.xlabel(
    "Daily IC"
)

plt.ylabel(
    "Frequency"
)

plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR /
    "ic_distribution.png",
    dpi=300
)

plt.close()


print(
    "Saved:"
)

print(
    OUTPUT_DIR /
    "cumulative_ic_curve.png"
)

print(
    OUTPUT_DIR /
    "ic_distribution.png"
)