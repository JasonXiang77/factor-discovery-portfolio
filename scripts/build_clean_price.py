import pandas as pd
from pathlib import Path
from factor_discovery_portfolio.data.preprocess import clean_price


input_path = (
    "data/raw/"
    "csi800_daily_price.parquet"
)


output_path = (
    "data/processed/"
    "csi800_price_clean.parquet"
)



# =========================
# Load
# =========================

df = pd.read_parquet(
    input_path
)


print("=" * 50)

print("Before cleaning:")
print(df.shape)



# =========================
# Clean
# =========================

df = clean_price(
    df
)


print("\nAfter cleaning:")
print(df.shape)



print("\nData types:")
print(df.dtypes)



print("\nMissing:")
print(df.isna().sum())



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



print(
    "\nSaved:",
    output_path
)



print(
    df.head()
)