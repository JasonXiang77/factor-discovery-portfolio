import pandas as pd


def factor_quantile_return(
    df,
    factor,
    quantiles=5,
    target="future_return_20d"
):
    """
    Calculate quantile portfolio returns

    factor:
        factor name

    target:
        future return
    """


    data = df[
        [
            "date",
            "ts_code",
            factor,
            target
        ]
    ].dropna()


    # 每天横截面分组

    data["group"] = (
        data
        .groupby("date")[factor]
        .transform(
            lambda x:
            pd.qcut(
                x,
                quantiles,
                labels=False,
                duplicates="drop"
            )
        )
    )


    # 计算组合收益

    group_return = (
        data
        .groupby(
            [
                "date",
                "group"
            ]
        )[target]
        .mean()
        .reset_index()
    )


    # pivot

    result = (
        group_return
        .pivot(
            index="date",
            columns="group",
            values=target
        )
    )


    return result



def long_short_return(
    group_return
):
    """
    Highest group - Lowest group
    """

    ls = (
        group_return.iloc[:,-1]
        -
        group_return.iloc[:,0]
    )


    return ls