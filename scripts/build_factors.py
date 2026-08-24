import pandas as pd
from pathlib import Path

from factor_discovery_portfolio.factors.basic import (
    add_momentum,
    add_volatility,
    add_reversal,
    add_volume_ratio
)


INPUT_PATH = "data/processed/csi800_returns.parquet"

OUTPUT_PATH = "data/processed/csi800_factors.parquet"



def build_factors():

    print("=" * 50)
    print("Loading returns data...")
    print("=" * 50)


    df = pd.read_parquet(
        INPUT_PATH
    )


    print("Raw shape:")
    print(df.shape)


    print("\nColumns:")
    print(df.columns)



    # 确保排序
    df = df.sort_values(
        [
            "ts_code",
            "date"
        ]
    )


    print("\nBuilding momentum...")
    df = add_momentum(df)


    print("Building volatility...")
    df = add_volatility(df)


    print("Building reversal...")
    df = add_reversal(df)


    print("Building volume ratio...")
    df = add_volume_ratio(df)



    # 删除无法计算因子的早期数据
    factor_columns = [
        "momentum",
        "volatility",
        "reversal",
        "volume_ratio"
    ]


    df = df.dropna(
        subset=factor_columns
    )


    # 保存

    Path(
        OUTPUT_PATH
    ).parent.mkdir(
        parents=True,
        exist_ok=True
    )


    df.to_parquet(
        OUTPUT_PATH,
        index=False
    )


    print("=" * 50)
    print("Factor building finished")
    print("=" * 50)


    print("\nSaved:")
    print(OUTPUT_PATH)


    print("\nShape:")
    print(df.shape)


    print("\nFactor columns:")
    print(
        df[factor_columns].head()
    )



if __name__ == "__main__":

    build_factors()