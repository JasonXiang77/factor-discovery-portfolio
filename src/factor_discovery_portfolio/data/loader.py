import os

import tushare as ts
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TUSHARE_TOKEN")

if not TOKEN:
    raise ValueError("TUSHARE_TOKEN is not set.")

pro = ts.pro_api(TOKEN)


def load_stock_basic():
    """Load A-share stock basic information."""
    df = pro.stock_basic(
        exchange="",
        list_status="",
        fields=(
            "ts_code,symbol,name,area,industry,"
            "market,exchange,list_date,delist_date"
        ),
    )

    return df

def load_daily(
    ts_code: str,
    start_date: str,
    end_date: str,
):
    """Load daily OHLCV data for one stock."""
    return pro.daily(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date,
    )


def load_daily_basic(
    ts_code: str,
    start_date: str,
    end_date: str,
):
    """Load daily market indicators for one stock."""
    return pro.daily_basic(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date,
    )