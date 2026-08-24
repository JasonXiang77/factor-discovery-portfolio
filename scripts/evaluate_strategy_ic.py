import pandas as pd


INPUT = (
    "data/processed/"
    "csi800_dynamic_icir_score.parquet"
)


df = pd.read_parquet(INPUT)


df["date"] = pd.to_datetime(
    df["date"]
)


# =========================
# Daily IC
# =========================

daily_ic = []


for date, group in df.groupby("date"):

    ic = (
        group["dynamic_icir_score"]
        .corr(
            group["future_return_20d"]
        )
    )

    daily_ic.append(
        {
            "date": date,
            "IC": ic
        }
    )


ic_df = pd.DataFrame(
    daily_ic
)


# =========================
# Statistics
# =========================

ic_mean = (
    ic_df["IC"]
    .mean()
)

ic_std = (
    ic_df["IC"]
    .std()
)

icir = (
    ic_mean /
    ic_std
)


positive_ratio = (
    (ic_df["IC"] > 0)
    .mean()
)


print("====================")
print("Strategy IC Result")
print("====================")

print(
    f"IC Mean: {ic_mean:.4f}"
)

print(
    f"IC Std: {ic_std:.4f}"
)

print(
    f"ICIR: {icir:.4f}"
)

print(
    f"Positive IC Ratio: {positive_ratio:.2%}"
)


ic_df.to_csv(
    "reports/strategy_ic.csv",
    index=False
)