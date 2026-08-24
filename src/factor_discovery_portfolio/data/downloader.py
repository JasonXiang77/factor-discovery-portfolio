import pandas as pd
from pathlib import Path

from factor_discovery_portfolio.data.market import download_daily
from factor_discovery_portfolio.data.baostock_client import BaostockClient



def download_universe_price(
        universe_path,
        start_date,
        end_date,
        output_path
):


    universe = pd.read_parquet(
        universe_path
    )


    stocks = (
        universe["ts_code"]
        .drop_duplicates()
        .tolist()
    )


    print(
        f"Total stocks: {len(stocks)}"
    )


    # 单股票保存目录

    cache_dir = Path(
        "data/raw/daily"
    )

    cache_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    with BaostockClient():


        for i, stock in enumerate(stocks):


            file_path = cache_dir / f"{stock}.parquet"



            # =====================
            # 断点续传核心
            # =====================

            if file_path.exists():

                print(
                    f"[{i+1}/{len(stocks)}] Skip {stock}"
                )

                continue



            print(
                f"[{i+1}/{len(stocks)}] Download {stock}"
            )


            try:

                df = download_daily(
                    stock,
                    start_date,
                    end_date
                )


                if len(df) > 0:

                    df.to_parquet(
                        file_path,
                        index=False
                    )


            except Exception as e:

                print(
                    "Failed:",
                    stock,
                    e
                )



    print(
        "Download finished"
    )



    # =====================
    # 合并所有股票
    # =====================


    all_files = list(
        cache_dir.glob("*.parquet")
    )


    print(
        f"Files found: {len(all_files)}"
    )


    dfs = []


    for f in all_files:

        dfs.append(
            pd.read_parquet(f)
        )



    price = pd.concat(
        dfs,
        ignore_index=True
    )


    price["date"] = pd.to_datetime(
        price["date"]
    )


    price = price.sort_values(
        [
            "date",
            "ts_code"
        ]
    )


    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )


    price.to_parquet(
        output_path,
        index=False
    )


    print(
        "Saved:",
        output_path
    )


    print(
        price.shape
    )