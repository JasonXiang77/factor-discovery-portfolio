import pandas as pd
import numpy as np


# =====================================================
# Config
# =====================================================

INPUT_PATH = (
    "data/processed/dynamic_optimizer_v13_result.parquet"
)

OUTPUT_PATH = (
    "data/processed/dynamic_optimizer_v14_result.parquet"
)


TARGET_VOL = 0.12

VOL_WINDOW = 20

FAST_WINDOW = 20

SLOW_WINDOW = 60

SMOOTH_WINDOW = 5


MAX_EXPOSURE = 1.10

MIN_EXPOSURE = 0.45



# =====================================================
# Load
# =====================================================

print("=" * 60)

print("Dynamic Optimizer V14 Adaptive Risk")



df = pd.read_parquet(
    INPUT_PATH
)


print("Loaded")

print(df.shape)

print(df.head())



# =====================================================
# Prepare
# =====================================================


df["date"] = pd.to_datetime(
    df["date"]
)


df = (
    df
    .sort_values("date")
    .reset_index(drop=True)
)



# =====================================================
# Base Return
# =====================================================


if "v13_return" in df.columns:

    base_col = "v13_return"

elif "v8_return" in df.columns:

    base_col = "v8_return"

elif "base_return" in df.columns:

    base_col = "base_return"

else:

    raise Exception(
        "No return column found"
    )



df["base_return"] = (
    df[base_col]
)



# =====================================================
# NAV
# =====================================================


df["base_nav"] = (
    (1 + df["base_return"])
    .cumprod()
)



# =====================================================
# Trend Signal
# =====================================================


df["fast_ma"] = (
    df["base_nav"]
    .rolling(
        FAST_WINDOW
    )
    .mean()
)



df["slow_ma"] = (
    df["base_nav"]
    .rolling(
        SLOW_WINDOW
    )
    .mean()
)



# =====================================================
# Drawdown
# =====================================================


df["high_water"] = (
    df["base_nav"]
    .cummax()
)



df["drawdown"] = (

    df["base_nav"]
    /
    df["high_water"]
    -
    1

)



# =====================================================
# Volatility
# =====================================================


df["realized_vol"] = (

    df["base_return"]
    .rolling(
        VOL_WINDOW
    )
    .std()

    *
    np.sqrt(252)

)



median_vol = (
    df["realized_vol"]
    .median()
)



vol80 = (
    df["realized_vol"]
    .quantile(0.8)
)



df["realized_vol"] = (

    df["realized_vol"]
    .fillna(
        median_vol
    )

)



# =====================================================
# Volatility Target
# =====================================================


df["vol_scale"] = (

    TARGET_VOL
    /
    df["realized_vol"]

)



df["vol_scale"] = (

    df["vol_scale"]
    .replace(
        [np.inf,-np.inf],
        np.nan
    )
    .fillna(1)

)



df["vol_scale"] = (

    df["vol_scale"]
    .clip(
        0.7,
        1.15
    )

)



# =====================================================
# Regime Detection
# =====================================================


def regime(row):


    # Crisis

    if (

        row["drawdown"] < -0.20

        and

        row["realized_vol"] > vol80

    ):

        return 0.45



    # Bear

    if (

        row["drawdown"] < -0.10

        or

        row["fast_ma"] < row["slow_ma"]

    ):

        return 0.70



    # Bull

    if (

        row["fast_ma"] >
        row["slow_ma"]

        and

        row["drawdown"] > -0.05

    ):

        return 1.05



    # Normal

    return 0.95




df["regime_scale"] = (

    df.apply(
        regime,
        axis=1
    )

)



# =====================================================
# Combined Exposure
# =====================================================


df["raw_exposure"] = (

    df["vol_scale"]

    *

    df["regime_scale"]

)



df["raw_exposure"] = (

    df["raw_exposure"]
    .clip(
        MIN_EXPOSURE,
        MAX_EXPOSURE
    )

)



# =====================================================
# Smooth Exposure
# =====================================================


df["exposure"] = (

    df["raw_exposure"]

    .ewm(
        span=SMOOTH_WINDOW,
        adjust=False
    )
    .mean()

)



df["exposure"] = (

    df["exposure"]
    .clip(
        MIN_EXPOSURE,
        MAX_EXPOSURE
    )

)



# =====================================================
# V14 Return
# =====================================================


df["v14_return"] = (

    df["base_return"]

    *

    df["exposure"]

)



df["v14_nav"] = (

    (1 + df["v14_return"])
    .cumprod()

)



df["v14_high"] = (

    df["v14_nav"]
    .cummax()

)



df["v14_drawdown"] = (

    df["v14_nav"]
    /
    df["v14_high"]

    -
    1

)



# =====================================================
# Metrics
# =====================================================


total_return = (

    df["v14_nav"]
    .iloc[-1]

    -

    1

)



years = (

    len(df)

    /

    252

)



annual_return = (

    (1 + total_return)

    **

    (1 / years)

    -

    1

)



volatility = (

    df["v14_return"]
    .std()

    *

    np.sqrt(252)

)



sharpe = (

    annual_return

    /

    volatility

)



max_dd = (

    df["v14_drawdown"]
    .min()

)



avg_exposure = (

    df["exposure"]
    .mean()

)



print("=" * 60)


print("V14 Performance")


performance = pd.DataFrame({

    "Metric":[

        "Total Return",

        "Annual Return",

        "Volatility",

        "Sharpe",

        "Max Drawdown",

        "Average Exposure"

    ],


    "Value":[

        total_return,

        annual_return,

        volatility,

        sharpe,

        max_dd,

        avg_exposure

    ]

})


print(performance)



# =====================================================
# Preview
# =====================================================


print("=" * 60)


print(

df[

[
"date",
"base_return",
"vol_scale",
"regime_scale",
"exposure",
"v14_return",
"v14_nav",
"v14_drawdown"
]

]

.head()

)



print(

df.tail()

)



# =====================================================
# Save
# =====================================================


output = df[

[
"date",

"base_return",

"vol_scale",

"regime_scale",

"raw_exposure",

"exposure",

"v14_return",

"v14_nav",

"v14_drawdown"

]

]


output.to_parquet(

    OUTPUT_PATH

)



print("=" * 60)

print("Saved:")

print(OUTPUT_PATH)