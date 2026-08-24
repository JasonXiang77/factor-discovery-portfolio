import pandas as pd
import numpy as np


# ==================================================
# Path
# ==================================================

input_path = (
    "data/processed/"
    "csi800_multifactor_v2.parquet"
)



# ==================================================
# Load
# ==================================================

df = pd.read_parquet(
    input_path
)


print("=" * 60)

print("Loaded:")
print(df.shape)



# ==================================================
# Check columns
# ==================================================

print("\nColumns:")

print(df.columns.tolist())



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
# Factors
# ==================================================

factors = [
    "momentum_z",
    "low_volatility_z",
    "quality_z"
]



# ==================================================
# Daily IC
# ==================================================

daily_ic = []


for date, group in df.groupby("date"):

    row = {
        "date": date
    }


    for factor in factors:

        ic = (
            group[factor]
            .corr(
                group["future_return_20d"]
            )
        )


        row[
            factor
        ] = ic


    daily_ic.append(row)



ic_df = pd.DataFrame(
    daily_ic
)



print("\nDaily IC sample:")

print(
    ic_df.head()
)



# ==================================================
# Statistics
# ==================================================

print("\n")
print("="*60)

print("Factor Direction")

print("="*60)


result = []


for factor in factors:

    ic_series = (
        ic_df[factor]
        .dropna()
    )


    mean_ic = (
        ic_series
        .mean()
    )


    std_ic = (
        ic_series
        .std()
    )


    icir = (
        mean_ic /
        std_ic
    )


    positive_ratio = (
        ic_series > 0
    ).mean()


    result.append(
        {
            "factor": factor,
            "IC_mean": mean_ic,
            "IC_std": std_ic,
            "ICIR": icir,
            "positive_IC_ratio": positive_ratio
        }
    )



result_df = pd.DataFrame(
    result
)



print(
    result_df
)



# ==================================================
# Save optional
# ==================================================

output_path = (
    "data/processed/"
    "factor_direction_check.parquet"
)


result_df.to_parquet(
    output_path,
    index=False
)


print("\nSaved:")
print(output_path)