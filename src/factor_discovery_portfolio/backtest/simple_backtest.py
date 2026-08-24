import pandas as pd



def monthly_top_quantile(
    df,
    score_col="factor_score",
    top_pct=0.2
):


    data = df.copy()


    data["date"] = pd.to_datetime(
        data["date"]
    )


    # 月份

    data["month"] = (
        data["date"]
        .dt.to_period("M")
    )


    # =========================
    # 每个月取最后交易日
    # =========================

    monthly = (
        data
        .sort_values("date")
        .groupby(
            [
                "month",
                "ts_code"
            ]
        )
        .tail(1)
    )


    portfolio=[]


    for month, group in monthly.groupby(
        "month"
    ):

        n = int(len(group) * top_pct)
        
        selected = (
            group.sort_values(score_col,ascending=False).head(n))


        portfolio.append(

            selected[
                [
                    "month",
                    "ts_code",
                    score_col
                ]
            ]

        )


    return pd.concat(
        portfolio,
        ignore_index=True
    )