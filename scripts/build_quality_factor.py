import pandas as pd
from pathlib import Path


input_path = (
    "data/raw/"
    "financial_indicator_akshare.parquet"
)


output_path = (
    "data/processed/"
    "quality_factor.parquet"
)


# ==========================
# Load
# ==========================

df = pd.read_parquet(
    input_path
)


print("="*50)

print(
    "Original:",
    df.shape
)


# ==========================
# Select fields
# ==========================

df = df[
    [
        "ts_code",
        "日期",
        "加权净资产收益率(%)"
    ]
]


df = df.rename(
    columns={
        "日期":"report_date",
        "加权净资产收益率(%)":"roe"
    }
)



# ==========================
# Date
# ==========================

df["report_date"] = pd.to_datetime(
    df["report_date"]
)



# ==========================
# Remove invalid
# ==========================

df = df.dropna(
    subset=[
        "roe"
    ]
)
# ==========================
# Clean ROE
# ==========================

df = df[
    (df["roe"] > 0)
    &
    (df["roe"] < 100)
]

# ==========================
# Build available date
# ==========================

def get_lag(date):

    month = date.month
    day = date.day


    # annual report
    if month == 12 and day == 31:

        return pd.Timedelta(
            days=90
        )


    # Q1
    elif month == 3:

        return pd.Timedelta(
            days=45
        )


    # Semi annual
    elif month == 6:

        return pd.Timedelta(
            days=60
        )


    # Q3

    elif month == 9:

        return pd.Timedelta(
            days=45
        )


    else:

        return pd.Timedelta(
            days=60
        )



df["available_date"] = (
    df["report_date"]
    +
    df["report_date"]
    .apply(get_lag)
)



# ==========================
# Sort
# ==========================

df = df.sort_values(
    [
        "ts_code",
        "available_date"
    ]
)



# ==========================
# Save
# ==========================

Path(
    output_path
).parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_parquet(
    output_path,
    index=False
)



print("="*50)

print(
    df.head()
)

print(
    df.shape
)


print(
    "Stocks:",
    df["ts_code"].nunique()
)


print(
    "Saved:",
    output_path
)