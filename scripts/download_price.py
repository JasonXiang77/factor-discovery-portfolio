from factor_discovery_portfolio.data.downloader import (
    download_universe_price
)

download_universe_price(

    universe_path=
    "data/processed/csi800_universe.parquet",


    start_date=
    "2015-01-01",


    end_date=
    "2025-12-31",


    output_path=
    "data/raw/csi800_daily_price.parquet"
)