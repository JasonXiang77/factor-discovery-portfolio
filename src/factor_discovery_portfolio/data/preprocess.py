import pandas as pd
from pathlib import Path



def preprocess_price(
        price_path,
        universe_path,
        output_path
):

    print("Loading price...")

    price = pd.read_parquet(
        price_path
    )


    print("Loading universe...")

    universe = pd.read_parquet(
        universe_path
    )


    price["date"] = pd.to_datetime(
        price["date"]
    )

    universe["universe_date"] = pd.to_datetime(
        universe["universe_date"]
    )


    # ==========================
    # CSI800 = CSI300 + CSI500
    # ==========================

    universe = universe[
        universe["index"].isin(
            [
                "CSI300",
                "CSI500"
            ]
        )
    ]


    # 每次调整日形成完整股票池

    universe = (
        universe
        .groupby(
            [
                "universe_date",
                "ts_code"
            ]
        )
        .size()
        .reset_index()
        [
            [
                "universe_date",
                "ts_code"
            ]
        ]
    )


    print(
        "Universe dates:",
        universe["universe_date"].nunique()
    )


    print(
        universe
        .groupby(
            "universe_date"
        )
        ["ts_code"]
        .nunique()
        .head()
    )


    # ==========================
    # 给每天价格匹配最近调仓日
    # ==========================


    price = price.sort_values(
        "date"
    )

    universe = universe.sort_values(
        "universe_date"
    )


    date_map = (
        price[
            ["date"]
        ]
        .drop_duplicates()
        .sort_values(
            "date"
        )
    )


    date_map = pd.merge_asof(
        date_map,
        universe[
            [
                "universe_date"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "universe_date"
        ),

        left_on="date",
        right_on="universe_date",

        direction="backward"
    )


    # 每个交易日对应一个调仓日


    price = price.merge(
        date_map,
        on="date",
        how="left"
    )


    # 加入当天股票池

    price = price.merge(
        universe,
        left_on=[
            "universe_date",
            "ts_code"
        ],

        right_on=[
            "universe_date",
            "ts_code"
        ],

        how="inner"
    )


    price = price.drop(
        columns=[
            "universe_date"
        ]
    )


    price = price.sort_values(
        [
            "ts_code",
            "date"
        ]
    )


    Path(
        output_path
    ).parent.mkdir(
        parents=True,
        exist_ok=True
    )


    price.to_parquet(
        output_path,
        index=False
    )


    print("===================")

    print(
        "Saved:",
        output_path
    )

    print(
        "Shape:",
        price.shape
    )

    print(
        "Stocks:",
        price.ts_code.nunique()
    )

    return price