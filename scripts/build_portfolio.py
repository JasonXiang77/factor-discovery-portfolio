import pandas as pd
from pathlib import Path


input_path = (
    "data/processed/"
    "csi800_factor_score.parquet"
)


output_path = (
    "data/processed/"
    "csi800_portfolio.parquet"
)


TOP_N = 100


# =====================
# Load
# =====================

df = pd.read_parquet(
    input_path
)


print("Loading...")
print(df.shape)



df["date"] = pd.to_datetime(
    df["date"]
)



# =====================
# Month
# =====================

df["month"] = (
    df["date"]
    .dt
    .to_period("M")
)



# =====================
# Select last trading day
# =====================

rebalance = (
    df
    .groupby("month")["date"]
    .max()
    .reset_index()
)


df = df.merge(
    rebalance,
    on=["month", "date"],
    how="inner"
)



print(
    "Rebalance days:"
)

print(
    df.head()
)



# =====================
# Rank stocks
# =====================

portfolio = (
    df
    .sort_values(
        [
            "month",
            "factor_score"
        ],
        ascending=[
            True,
            False
        ]
    )
    .groupby("month")
    .head(TOP_N)
)



print("\nPortfolio:")
print(
    portfolio[
        [
            "month",
            "ts_code",
            "factor_score"
        ]
    ].head()
)



print("\nSelected:")
print(
    portfolio
    .groupby("month")
    ["ts_code"]
    .count()
    .head()
)



# =====================
# Save
# =====================

Path(
    output_path
).parent.mkdir(
    exist_ok=True,
    parents=True
)


portfolio.to_parquet(
    output_path,
    index=False
)


print("\nSaved:")
print(output_path)