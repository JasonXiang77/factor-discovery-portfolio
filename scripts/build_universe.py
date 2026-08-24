from factor_discovery_portfolio.data.universe import (
    build_csi800_universe
)


dates = [
    "2024-01-31",
    "2024-02-29",
    "2024-03-29"
]


df = build_csi800_universe(
    dates
)


print(df.head())

print(df.shape)

print(
    df.groupby(
        ["universe_date","index"]
    )
    .size()
)