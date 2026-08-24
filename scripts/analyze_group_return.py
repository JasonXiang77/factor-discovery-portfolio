import pandas as pd
from pathlib import Path


from factor_discovery_portfolio.evaluation.portfolio import (
    factor_quantile_return,
    long_short_return
)



INPUT_PATH = (
    "data/processed/"
    "csi800_factors.parquet"
)


OUTPUT_DIR = Path(
    "reports"
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)



def main():


    print("Loading factors...")


    df = pd.read_parquet(
        INPUT_PATH
    )


    factors = [
        "momentum",
        "volatility",
        "reversal",
        "volume_ratio"
    ]


    summary = []


    for factor in factors:


        print(
            "\nTesting:",
            factor
        )


        group = factor_quantile_return(
            df,
            factor
        )


        # 保存分组收益

        group.to_csv(
            OUTPUT_DIR /
            f"{factor}_quantile_return.csv"
        )


        ls = long_short_return(
            group
        )


        stats = {

            "factor":factor,

            "Q1_mean":
            group.iloc[:,0].mean(),

            "Q5_mean":
            group.iloc[:,-1].mean(),

            "long_short_mean":
            ls.mean(),

            "long_short_std":
            ls.std()

        }


        summary.append(
            stats
        )


    result = pd.DataFrame(
        summary
    )


    result.to_csv(
        OUTPUT_DIR /
        "factor_quantile_summary.csv",
        index=False
    )


    print("\n================")
    print("Quantile Summary")
    print("================")


    print(result)



if __name__=="__main__":

    main()