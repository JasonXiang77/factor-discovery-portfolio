import pandas as pd


def zscore(
    x
):
    """
    Cross-sectional z-score
    """

    return (
        x - x.mean()
    ) / x.std()



def normalize_factors(
    df,
    factors
):
    """
    Daily cross-sectional normalization
    """


    result = df.copy()


    for factor in factors:

        z_name = factor + "_z"


        result[z_name] = (
            result
            .groupby("date")[factor]
            .transform(
                zscore
            )
        )


    return result