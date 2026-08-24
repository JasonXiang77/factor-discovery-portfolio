import os
import tushare as ts
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TUSHARE_TOKEN")

pro = ts.pro_api(TOKEN)

df = pro.index_daily(
    ts_code="000906.SH",
    start_date="20160201",
    end_date="20251231"
)


df["trade_date"] = pd.to_datetime(
    df["trade_date"]
)


df = df.sort_values(
    "trade_date"
)


Path(
    "data/raw"
).mkdir(
    exist_ok=True
)


df.to_parquet(
    "data/raw/csi800_index.parquet",
    index=False
)


print(df.head())
print(df.shape)