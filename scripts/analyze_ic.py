import pandas as pd
import numpy as np


input_path = (
    "data/processed/"
    "csi800_factors.parquet"
)


df = pd.read_parquet(
    input_path
)


print("Loaded:")
print(df.shape)



# ==========================
# Factor list
# ==========================

factors = [
    "momentum",
    "volatility",
    "reversal",
    "volume_ratio"
]


target = "future_return_20d"



results = []



# ==========================
# Daily IC
# ==========================

for factor in factors:

    print(
        "Analyzing:",
        factor
    )

    ic = (
        df
        .groupby("date")
        .apply(
            lambda x:
            x[factor]
            .corr(
                x[target],
                method="spearman"
            )
        )
    )


    results.append(
        {
            "factor": factor,
            "IC_mean": ic.mean(),
            "IC_std": ic.std(),
            "ICIR": ic.mean()/ic.std()
        }
    )



result = pd.DataFrame(
    results
)


print("\nIC Summary")

print(result)



result.to_csv(
    "data/processed/ic_summary.csv",
    index=False
)