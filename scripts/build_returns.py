import pandas as pd
from pathlib import Path

input_path = (
    "data/processed/"
    "csi800_price_clean.parquet"
)

output_path = (
    "data/processed/"
    "csi800_returns.parquet"
)

# =========================
# Load clean price
# =========================

df = pd.read_parquet(
    input_path
)

print("=" * 50)

print("Original:")
print(df.shape)

# =========================
# Ensure numeric
# =========================

numeric_cols = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "amount"
]


for col in numeric_cols:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )



# =========================
# Sort
# =========================

df = df.sort_values(
    [
        "ts_code",
        "date"
    ]
)

# =========================
# Daily return
# =========================

df["daily_return"] = (
    df
    .groupby("ts_code")["close"]
    .pct_change()
)

# =========================
# Future return
# =========================


# 下一交易日收益

df["future_return_1d"] = (
    df
    .groupby("ts_code")["daily_return"]
    .shift(-1)
)

# 未来20交易日收益

df["future_return_20d"] = (

    df
    .groupby("ts_code")["close"]
    .shift(-20)

    /

    df["close"]

    - 1
)

# =========================
# Remove invalid rows
# =========================

df = df.dropna(
    subset=[
        "daily_return"
    ]
)

# =========================
# Save
# =========================

Path(
    output_path
).parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_parquet(
    output_path,
    index=False
)

print("\nFinal:")
print(df.shape)

print("\nReturn statistics:")

print(
    df[
        [
            "daily_return",
            "future_return_1d",
            "future_return_20d"
        ]
    ]
    .describe()
)

print(
    "\nSaved:",
    output_path
)

print(
    df.head()
)