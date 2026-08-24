import pandas as pd
from pathlib import Path


from factor_discovery_portfolio.factors.normalize import (
    normalize_factors
)



INPUT = (
    "data/processed/"
    "csi800_factors.parquet"
)


OUTPUT = (
    "data/processed/"
    "csi800_multifactor.parquet"
)



def main():


    print(
        "Loading factors..."
    )


    df = pd.read_parquet(
        INPUT
    )


    print(
        df.shape
    )


    # =====================
    # 因子方向调整
    # =====================


    # 低波动
    df["low_volatility"] = (
        -df["volatility"]
    )


    # 低异常成交
    df["low_volume"] = (
        -df["volume_ratio"]
    )



    factors = [

        "momentum",

        "low_volatility",

        "low_volume"

    ]



    print(
        "Normalizing..."
    )


    df = normalize_factors(
        df,
        factors
    )



    # =====================
    # 多因子合成
    # =====================


    df["factor_score"] = (

        0.5 *
        df["momentum_z"]

        +

        0.3 *
        df["low_volatility_z"]

        +

        0.2 *
        df["low_volume_z"]

    )



    # 删除无效数据

    df = df.dropna(
        subset=[
            "factor_score"
        ]
    )



    Path(
        OUTPUT
    ).parent.mkdir(
        exist_ok=True,
        parents=True
    )


    df.to_parquet(
        OUTPUT,
        index=False
    )


    print(
        "Saved:",
        OUTPUT
    )


    print(
        df[
            [
                "ts_code",
                "date",
                "momentum_z",
                "low_volatility_z",
                "low_volume_z",
                "factor_score"
            ]
        ].head()
    )


    print(
        df.shape
    )



if __name__=="__main__":

    main()