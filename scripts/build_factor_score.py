import pandas as pd
from scipy.stats import zscore


input_path = (
    "data/processed/"
    "csi800_factors.parquet"
)


output_path = (
    "data/processed/"
    "csi800_factor_score.parquet"
)



df = pd.read_parquet(
    input_path
)


print("Loaded:")
print(df.shape)



# ==========================
# Cross-sectional zscore
# ==========================

print("Standardizing factors...")


df["momentum_z"] = (
    df
    .groupby("date")["momentum"]
    .transform(
        lambda x:
        zscore(x, nan_policy="omit")
    )
)


df["low_volatility_z"] = (
    df
    .groupby("date")["volatility"]
    .transform(
        lambda x:
        -zscore(x, nan_policy="omit")
    )
)


df["reversal_z"] = (
    df
    .groupby("date")["reversal"]
    .transform(
        lambda x:
        zscore(x, nan_policy="omit")
    )
)



# ==========================
# Composite score
# ==========================


df["factor_score"] = (
    0.5 * df["low_volatility_z"]
    +
    0.3 * df["momentum_z"]
    +
    0.2 * df["reversal_z"]
)



df.to_parquet(
    output_path,
    index=False
)



print("\nSaved:")
print(output_path)


print(df[
    [
        "ts_code",
        "date",
        "momentum_z",
        "low_volatility_z",
        "reversal_z",
        "factor_score"
    ]
].head())