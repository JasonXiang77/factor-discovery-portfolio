import pandas as pd
import baostock as bs



def download_daily(
        ts_code,
        start_date,
        end_date
):


    code, market = ts_code.split(".")


    if market=="SH":
        bs_code=f"sh.{code}"

    else:
        bs_code=f"sz.{code}"



    rs = bs.query_history_k_data_plus(

        bs_code,

        fields=
        "date,code,open,high,low,close,volume,amount",

        start_date=start_date,

        end_date=end_date,

        frequency="d",

        adjustflag="3"

    )


    data=[]


    while rs.next():

        data.append(
            rs.get_row_data()
        )


    df=pd.DataFrame(
        data,
        columns=rs.fields
    )


    df["ts_code"]=ts_code


    return df[
        [
            "ts_code",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount"
        ]
    ]