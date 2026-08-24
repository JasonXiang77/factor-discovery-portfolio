import pandas as pd
from pathlib import Path


from factor_discovery_portfolio.backtest.simple_backtest import (
    monthly_top_quantile
)


INPUT = (
"data/processed/"
"csi800_multifactor.parquet"
)



def main():


    print(
        "Loading..."
    )


    df = pd.read_parquet(
        INPUT
    )


    df["date"] = pd.to_datetime(
        df["date"]
    )


    print(
        df.shape
    )


    portfolio = monthly_top_quantile(
        df
    )


    print(
        "\nPortfolio:"
    )


    print(
        portfolio.head()
    )


    print(
        "\nSelected stocks:"
    )


    print(
        portfolio.groupby(
            "month"
        )
        .size()
        .head()
    )


    Path(
        "reports"
    ).mkdir(
        exist_ok=True
    )


    portfolio.to_csv(
        "reports/monthly_portfolio.csv",
        index=False
    )


    print(
        "Saved portfolio"
    )



if __name__=="__main__":
    main()