import pandas as pd
import numpy as np
from pathlib import Path


# ==================================================
# Path
# ==================================================

input_path = (
    "data/processed/"
    "csi800_multifactor_v2.parquet"
)


output_path = (
    "data/processed/"
    "dynamic_icir_weights.parquet"
)



# ==================================================
# Load
# ==================================================

df = pd.read_parquet(
    input_path
)


print("="*60)

print("Loaded:")
print(df.shape)



# ==================================================
# Factors
# ==================================================

factors = [
    "momentum_z",
    "low_volatility_z",
    "quality_z"
]



# ==================================================
# Sort
# ==================================================

df = df.sort_values(
    [
        "date",
        "ts_code"
    ]
)



# ==================================================
# Daily IC
# ==================================================

daily_ic = []


for date, group in df.groupby("date"):

    row = {
        "date": date
    }


    for factor in factors:

        row[factor] = (
            group[factor]
            .corr(
                group["future_return_20d"]
            )
        )


    daily_ic.append(row)



ic_df = pd.DataFrame(
    daily_ic
)



print("\nDaily IC:")

print(
    ic_df.head()
)



# ==================================================
# Rolling ICIR
# ==================================================

window = 60


icir_df = (
    ic_df[
        ["date"]
    ]
    .copy()
)



for factor in factors:


    mean_ic = (
        ic_df[factor]
        .rolling(window)
        .mean()
    )


    std_ic = (
        ic_df[factor]
        .rolling(window)
        .std()
    )


    icir = (
        mean_ic /
        std_ic
    )


    # 只保留正向预测能力

    icir_df[
        factor
    ] = (
        icir
        .clip(
            lower=0
        )
    )



print("\nRolling ICIR:")

print(
    icir_df.head(70)
)



# ==================================================
# Quality minimum support
# ==================================================

icir_df[
    "quality_z"
] = (
    icir_df["quality_z"]
    +
    0.05
)



# ==================================================
# Calculate weights
# ==================================================

weight_df = (
    icir_df[
        ["date"]
    ]
    .copy()
)



total = (
    icir_df[factors]
    .sum(axis=1)
)



total = (
    total
    .replace(
        0,
        np.nan
    )
)



for factor in factors:

    weight_df[
        factor+"_weight"
    ] = (
        icir_df[factor]
        /
        total
    )



weight_df = (
    weight_df
    .dropna()
    .reset_index(drop=True)
)



# ==================================================
# Weight constraint
# ==================================================

weight_cols = [
    factor+"_weight"
    for factor in factors
]


for col in weight_cols:

    weight_df[col] = (
        weight_df[col]
        .clip(
            lower=0.15,
            upper=0.60
        )
    )



# ==================================================
# Normalize
# ==================================================

weight_sum = (
    weight_df[weight_cols]
    .sum(axis=1)
)


weight_df[weight_cols] = (
    weight_df[weight_cols]
    .div(
        weight_sum,
        axis=0
    )
)



# ==================================================
# Check
# ==================================================

print("\nWeights:")

print(
    weight_df.head()
)



print("\nStatistics:")

print(
    weight_df.describe()
)



print("\nSum check:")

print(
    weight_df[weight_cols]
    .sum(axis=1)
    .describe()
)



# ==================================================
# Save
# ==================================================

Path(
    output_path
).parent.mkdir(
    parents=True,
    exist_ok=True
)


weight_df.to_parquet(
    output_path,
    index=False
)



print("\nSaved:")
print(output_path)