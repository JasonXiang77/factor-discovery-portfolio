import pandas as pd
from pathlib import Path


input_path = (
    "data/processed/"
    "quality_factor.parquet"
)


output_path = (
    "data/processed/"
    "quality_factor_z.parquet"
)



df = pd.read_parquet(
    input_path
)


print("="*50)

print(df.shape)


def winsorize(x):

    low = x.quantile(0.01)
    high = x.quantile(0.99)

    return x.clip(
        low,
        high
    )



# ==========================
# Cross sectional winsorize
# ==========================

df["roe_winsor"] = (
    df.groupby(
        "available_date"
    )["roe"]
    .transform(
        winsorize
    )
)



# ==========================
# Cross sectional z-score
# ==========================

df["quality_z"] = (
    df.groupby(
        "available_date"
    )["roe_winsor"]
    .transform(
        lambda x:
        (
            x-x.mean()
        )
        /
        x.std()
    )
)



# ==========================
# Save
# ==========================

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



print(df.head())


print(
    df["quality_z"]
    .describe()
)


print(
    "Saved:",
    output_path
)