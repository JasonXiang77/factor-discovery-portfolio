import pandas as pd
import os


# =========================
# Config
# =========================

INPUT = "data/processed/csi800_dynamic_icir_score.parquet"

OUTPUT = "data/processed/csi800_dynamic_portfolio.parquet"

TOP_N = 100


# =========================
# Load
# =========================

df = pd.read_parquet(INPUT)

print("="*60)
print("Loaded:")
print(df.shape)

print(df.head())


# =========================
# Date
# =========================

df["date"] = pd.to_datetime(df["date"])


# =========================
# Monthly rebalance date
# =========================

# 每个月最后一个交易日
df["month"] = df["date"].dt.to_period("M")


rebalance_dates = (
    df
    .groupby("month")["date"]
    .max()
    .reset_index()
)


df = df.merge(
    rebalance_dates,
    on=["month", "date"],
    how="inner"
)


print("\nRebalance days:")
print(df["date"].head())

print(df["date"].tail())


# =========================
# Remove missing score
# =========================

df = df.dropna(
    subset=["dynamic_icir_score"]
)


# =========================
# Rank stocks
# =========================

df["rank"] = (
    df
    .groupby("date")["dynamic_icir_score"]
    .rank(
        ascending=False,
        method="first"
    )
)


# =========================
# Select Top N
# =========================

portfolio = (
    df[df["rank"] <= TOP_N]
    [
        [
            "date",
            "ts_code",
            "dynamic_icir_score"
        ]
    ]
)


# =========================
# Equal weight
# =========================

portfolio["weight"] = 1 / TOP_N


# =========================
# Check
# =========================

print("\nPortfolio:")
print(portfolio.head())


print("\nSelected:")
print(
    portfolio
    .groupby("date")["ts_code"]
    .count()
    .head(10)
)


print("\nWeight:")
print(
    portfolio
    .groupby("date")["weight"]
    .sum()
    .head()
)


# =========================
# Save
# =========================

os.makedirs(
    "data/processed",
    exist_ok=True
)


portfolio.to_parquet(
    OUTPUT,
    index=False
)


print("\nSaved:")
print(OUTPUT)