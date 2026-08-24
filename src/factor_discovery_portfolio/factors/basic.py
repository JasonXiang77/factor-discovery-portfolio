import pandas as pd


def add_momentum(
    df,
    window_long=252,
    skip=21
):
    """
    12-1 Momentum
    """

    df = df.copy()

    df["momentum"] = (
        df
        .groupby("ts_code")["close"]
        .shift(skip)
        /
        df
        .groupby("ts_code")["close"]
        .shift(window_long)
        - 1
    )

    return df



def add_volatility(
    df,
    window=20
):
    """
    rolling volatility
    """

    df = df.copy()

    df["volatility"] = (
        df
        .groupby("ts_code")["daily_return"]
        .rolling(window)
        .std()
        .reset_index(level=0,drop=True)
    )

    return df



def add_reversal(
    df,
    window=5
):

    df=df.copy()

    df["reversal"] = (
        df
        .groupby("ts_code")["close"]
        .pct_change(window)
    )

    return df



def add_volume_ratio(
    df,
    window=20
):

    df=df.copy()

    avg_volume = (
        df
        .groupby("ts_code")["volume"]
        .rolling(window)
        .mean()
        .reset_index(level=0,drop=True)
    )

    df["volume_ratio"] = (
        df["volume"] /
        avg_volume
    )

    return df