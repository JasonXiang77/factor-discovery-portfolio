import pandas as pd


def calculate_ic(
    df,
    factor,
    target="future_return_20d"
):
    """
    Calculate daily cross-sectional IC

    factor:
        factor column name

    target:
        future return
    """


    ic = (
        df
        .groupby("date")
        .apply(
            lambda x:
            x[factor].corr(
                x[target]
            )
        )
        .reset_index()
    )


    ic.columns = [
        "date",
        "IC"
    ]


    return ic



def ic_statistics(ic):

    mean_ic = ic["IC"].mean()

    std_ic = ic["IC"].std()

    icir = (
        mean_ic /
        std_ic
    )


    result = pd.DataFrame(
        {
            "IC_mean":[mean_ic],
            "IC_std":[std_ic],
            "ICIR":[icir]
        }
    )


    return result