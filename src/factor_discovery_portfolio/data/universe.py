import pandas as pd
import baostock as bs


def convert_code(code):
    """
    Baostock:
        sh.600000
        sz.000001

    Tushare:
        600000.SH
        000001.SZ
    """

    market, symbol = code.split(".")

    if market == "sh":
        return f"{symbol}.SH"

    elif market == "sz":
        return f"{symbol}.SZ"

    else:
        return None



def get_index_members(
        index,
        date
):
    """
    Get historical index constituents
    """

    if index == "CSI300":

        rs = bs.query_hs300_stocks(
            date=date
        )

    elif index == "CSI500":

        rs = bs.query_zz500_stocks(
            date=date
        )

    else:

        raise ValueError(
            "Unsupported index"
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


    df["ts_code"] = (
        df["code"]
        .apply(convert_code)
    )


    df["index"] = index


    df.rename(
        columns={
            "code_name":"name",
            "updateDate":"universe_date"
        },
        inplace=True
    )


    return df[
        [
            "index",
            "universe_date",
            "ts_code",
            "name"
        ]
    ]



def build_csi800_universe(
        dates
):

    """
    Build historical CSI800 universe

    dates:
        list of str
        example:
        ["2015-01-30"]
    """


    bs.login()


    universe=[]


    for date in dates:


        print(
            f"Downloading {date}"
        )


        csi300 = get_index_members(
            "CSI300",
            date
        )


        csi500 = get_index_members(
            "CSI500",
            date
        )


        df = pd.concat(
            [
                csi300,
                csi500
            ],
            ignore_index=True
        )


        universe.append(df)



    bs.logout()


    result = pd.concat(
        universe,
        ignore_index=True
    )


    # remove duplicate stocks
    result = (
        result
        .drop_duplicates(
            [
                "universe_date",
                "ts_code"
            ]
        )
    )


    return result