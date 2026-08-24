import pandas as pd
import numpy as np
import os


# ==============================
# Load
# ==============================

factor_path = "data/processed/csi800_multifactor_v2.parquet"

weight_path = "data/processed/dynamic_icir_weights.parquet"


factor = pd.read_parquet(factor_path)

weights = pd.read_parquet(weight_path)


print("==============================")
print("Factor:")
print(factor.shape)

print("Weights:")
print(weights.shape)


# ==============================
# Date format
# ==============================

factor["date"] = pd.to_datetime(
    factor["date"]
)

weights["date"] = pd.to_datetime(
    weights["date"]
)


# ==============================
# Prepare weights
# ==============================


weights = weights.sort_values(
    "date"
)


print("\nWeight dates:")
print(
    weights.head()
)

print(
    weights.tail()
)


# ==============================
# Merge asof
# ==============================

factor = factor.sort_values(
    "date"
)

merged = pd.merge_asof(
    factor,
    weights,
    on="date",
    direction="backward"
)


print("\nAfter merge")

print(
    merged[
        [
            "date",
            "momentum_z_weight",
            "low_volatility_z_weight",
            "quality_z_weight"
        ]
    ].head(20)
)


# ==============================
# Check missing
# ==============================


weight_cols = [
    "momentum_z_weight",
    "low_volatility_z_weight",
    "quality_z_weight"
]


print("\nMissing weight ratio")

print(
    merged[weight_cols]
    .isna()
    .mean()
)


# ==============================
# Remove early period
# ==============================


merged = merged.dropna(
    subset=weight_cols
)


# ==============================
# Dynamic score
# ==============================


merged["dynamic_icir_score"] = (

    merged["momentum_z"]
    *
    merged["momentum_z_weight"]

    +

    merged["low_volatility_z"]
    *
    merged["low_volatility_z_weight"]

    +

    merged["quality_z"]
    *
    merged["quality_z_weight"]

)


print("\nScore")

print(
    merged[
        [
            "ts_code",
            "date",
            "dynamic_icir_score"
        ]
    ].head()
)


print(
    merged["dynamic_icir_score"]
    .describe()
)



# ==============================
# Save
# ==============================


out = (
    "data/processed/"
    "csi800_dynamic_icir_score.parquet"
)


merged.to_parquet(
    out,
    index=False
)


print("\nSaved:")
print(out)