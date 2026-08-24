import pandas as pd
from pathlib import Path


# =====================
# Paths
# =====================

factor_path = (
    "data/processed/"
    "csi800_factor_score.parquet"
)


quality_path = (
    "data/processed/"
    "quality_factor_z.parquet"
)


output_path = (
    "data/processed/"
    "csi800_multifactor_v2.parquet"
)



# =====================
# Load
# =====================

print("Loading...")


factor = pd.read_parquet(
    factor_path
)


quality = pd.read_parquet(
    quality_path
)



print("Factor:")
print(
    factor.shape
)


print("Quality:")
print(
    quality.shape
)



# =====================
# Date convert
# =====================

factor["date"] = pd.to_datetime(
    factor["date"]
)


quality["available_date"] = pd.to_datetime(
    quality["available_date"]
)



# =====================
# Keep columns
# =====================

quality = quality[
    [
        "ts_code",
        "available_date",
        "quality_z"
    ]
]



# =====================
# Sort for merge_asof
# =====================

# 注意：
# merge_asof要求left_on/right_on整体排序

factor = (
    factor
    .sort_values(
        [
            "date",
            "ts_code"
        ]
    )
    .reset_index(drop=True)
)



quality = (
    quality
    .sort_values(
        [
            "available_date",
            "ts_code"
        ]
    )
    .reset_index(drop=True)
)



print("="*50)

print("Before merge")

print(
    factor[
        [
            "date",
            "ts_code"
        ]
    ].head()
)


print(
    quality[
        [
            "available_date",
            "ts_code"
        ]
    ].head()
)



# =====================
# PIT merge
# =====================

merged = pd.merge_asof(
    factor,
    quality,
    left_on="date",
    right_on="available_date",
    by="ts_code",
    direction="backward"
)



print("="*50)

print("Merged")

print(
    merged[
        [
            "ts_code",
            "date",
            "quality_z"
        ]
    ].head()
)



# =====================
# Missing quality check
# =====================

missing = (
    merged["quality_z"]
    .isna()
    .mean()
)


print(
    "Missing quality ratio:",
    missing
)



# 删除没有财务数据的股票日期

merged = merged.dropna(
    subset=[
        "quality_z"
    ]
)



# =====================
# Build multifactor score
# =====================

merged["factor_score_v2"] = (

      merged["momentum_z"]

    + merged["low_volatility_z"]

    + merged["reversal_z"]

    + merged["quality_z"]

) / 4



# =====================
# Save
# =====================

Path(
    output_path
).parent.mkdir(
    parents=True,
    exist_ok=True
)


merged.to_parquet(
    output_path,
    index=False
)



print("="*50)

print(
    "Final:"
)

print(
    merged.shape
)


print(
    merged[
        [
            "ts_code",
            "date",
            "momentum_z",
            "low_volatility_z",
            "reversal_z",
            "quality_z",
            "factor_score_v2"
        ]
    ].head()
)


print(
    "Saved:"
)

print(
    output_path
)