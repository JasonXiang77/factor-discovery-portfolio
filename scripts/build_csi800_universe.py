import pandas as pd

from factor_discovery_portfolio.data.universe import (
    build_csi800_universe
)



# monthly rebalance dates
dates = pd.date_range(
    start="2015-01-30",
    end="2025-12-31",
    freq="ME"
)


dates = [
    x.strftime("%Y-%m-%d")
    for x in dates
]


print(
    f"Total dates: {len(dates)}"
)


df = build_csi800_universe(
    dates
)


print(df.head())


print(
    df.groupby(
        [
            "universe_date",
            "index"
        ]
    )
    .size()
)



df.to_parquet(
    "data/processed/csi800_universe.parquet"
)


print(
    "Universe saved!"
)