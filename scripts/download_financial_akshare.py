import akshare as ak
import pandas as pd

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


# ==================================================
# Path
# ==================================================

universe_path = (
    "data/processed/"
    "csi800_universe.parquet"
)


cache_dir = Path(
    "data/raw/"
    "financial_cache"
)

cache_dir.mkdir(
    parents=True,
    exist_ok=True
)


output_path = (
    "data/raw/"
    "financial_indicator_akshare.parquet"
)



# ==================================================
# Load universe
# ==================================================

universe = pd.read_parquet(
    universe_path
)


stocks = (
    universe["ts_code"]
    .drop_duplicates()
    .tolist()
)


print("="*50)
print("Stocks:")
print(len(stocks))
print("="*50)



# ==================================================
# Download one stock
# ==================================================

def download_one(ts_code):

    symbol = ts_code.split(".")[0]


    cache_file = (
        cache_dir /
        f"{symbol}.parquet"
    )


    # --------------------------
    # cache exists
    # --------------------------

    if cache_file.exists():

        try:

            return pd.read_parquet(
                cache_file
            )

        except:

            pass



    # --------------------------
    # download
    # --------------------------

    for retry in range(3):

        try:

            print(
                "Downloading:",
                symbol
            )


            df = (
                ak
                .stock_financial_analysis_indicator(
                    symbol=symbol
                )
            )


            if df is None or len(df)==0:
                return None



            df["ts_code"] = ts_code


            # save cache

            df.to_parquet(
                cache_file,
                index=False
            )


            return df



        except Exception as e:

            print(
                "Retry",
                retry+1,
                symbol,
                e
            )

            time.sleep(
                2
            )



    print(
        "Failed:",
        symbol
    )

    return None



# ==================================================
# Multi-thread download
# ==================================================

results = []


max_workers = 8


with ThreadPoolExecutor(
    max_workers=max_workers
) as executor:


    futures = {

        executor.submit(
            download_one,
            stock
        ): stock

        for stock in stocks

    }



    for i, future in enumerate(
        as_completed(futures)
    ):

        stock = futures[future]


        try:

            data = future.result()


            if data is not None:

                results.append(
                    data
                )


        except Exception as e:

            print(
                "Error:",
                stock,
                e
            )


        print(
            f"[{i+1}/{len(stocks)}]"
            " finished"
        )



# ==================================================
# Merge
# ==================================================

print("="*50)

print(
    "Merging..."
)


financial = pd.concat(
    results,
    ignore_index=True
)



# remove duplicate

financial = (
    financial
    .drop_duplicates()
)



# save

financial.to_parquet(
    output_path,
    index=False
)



print("="*50)

print(
    "Finished"
)


print(
    "Shape:",
    financial.shape
)


print(
    "Stocks:",
    financial["ts_code"]
    .nunique()
)


print(
    financial.head()
)


print(
    "Saved:",
    output_path
)