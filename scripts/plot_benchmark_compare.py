import pandas as pd
import matplotlib.pyplot as plt


# =====================================
# Config
# =====================================

BENCHMARK_PATH = (
    "data/raw/csi800_index.parquet"
)

V1_PATH = (
    "data/processed/dynamic_optimizer_result.parquet"
)

V14_PATH = (
    "data/processed/dynamic_optimizer_v14_result.parquet"
)


NAV_OUTPUT = (
    "results/nav_benchmark_compare.png"
)

DD_OUTPUT = (
    "results/drawdown_benchmark_compare.png"
)



# =====================================
# Load
# =====================================

benchmark = pd.read_parquet(
    BENCHMARK_PATH
)

v1 = pd.read_parquet(
    V1_PATH
)

v14 = pd.read_parquet(
    V14_PATH
)


for df in [benchmark, v1, v14]:
    df["date"] = pd.to_datetime(
        df["date"]
    )



# =====================================
# Benchmark NAV
# =====================================

benchmark = (
    benchmark
    .sort_values("date")
    .reset_index(drop=True)
)


benchmark["nav"] = (
    (1 + benchmark["daily_return"])
    .cumprod()
)



# =====================================
# Align date
# =====================================

start = max(
    benchmark["date"].min(),
    v1["date"].min(),
    v14["date"].min()
)

end = min(
    benchmark["date"].max(),
    v1["date"].max(),
    v14["date"].max()
)


benchmark = benchmark[
    (benchmark["date"] >= start)
    &
    (benchmark["date"] <= end)
]


v1 = v1[
    (v1["date"] >= start)
    &
    (v1["date"] <= end)
]


v14 = v14[
    (v14["date"] >= start)
    &
    (v14["date"] <= end)
]



# =====================================
# NAV Comparison
# =====================================

plt.figure(
    figsize=(12,5)
)


plt.plot(
    benchmark["date"],
    benchmark["nav"],
    label="CSI800 Benchmark"
)


plt.plot(
    v1["date"],
    v1["nav"],
    label="V1 Baseline Factor Portfolio"
)


plt.plot(
    v14["date"],
    v14["v14_nav"],
    label="V14 Risk-Controlled Optimizer"
)


plt.title(
    "NAV Comparison"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "NAV"
)


plt.legend()

plt.grid(
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    NAV_OUTPUT,
    dpi=300
)


plt.close()



# =====================================
# Drawdown
# =====================================


def calc_drawdown(nav):

    high = nav.cummax()

    return nav / high - 1



benchmark["drawdown"] = calc_drawdown(
    benchmark["nav"]
)


v1["drawdown"] = calc_drawdown(
    v1["nav"]
)


v14["drawdown"] = calc_drawdown(
    v14["v14_nav"]
)



plt.figure(
    figsize=(12,5)
)


plt.plot(
    benchmark["date"],
    benchmark["drawdown"],
    label="CSI800"
)


plt.plot(
    v1["date"],
    v1["drawdown"],
    label="V1"
)


plt.plot(
    v14["date"],
    v14["drawdown"],
    label="V14"
)


plt.title(
    "Drawdown Comparison"
)


plt.xlabel(
    "Date"
)


plt.ylabel(
    "Drawdown"
)


plt.legend()

plt.grid(
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    DD_OUTPUT,
    dpi=300
)


plt.close()



print("Saved:")
print(NAV_OUTPUT)
print(DD_OUTPUT)