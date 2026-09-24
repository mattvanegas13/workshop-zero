"""
Reusuable bits and pieces used during the data pre-processing portion of our qr endeavors
"""
import pandas as pd


def realized_volatility_df(close_prices_df):
    """
    Given a dataframe with close prices - construct a copy of a dataframe
    that calculates the realized volatility of the last 20 days using
    the averaged squared returns
    """

    rv_df = close_prices_df.copy()
    rv_df["date"] = pd.to_datetime(rv_df["date"])
    rv_df = rv_df.sort_values("date")
    rv_df["returns"] = rv_df["close"].pct_change()
    rv_df["squared_return"] = rv_df["returns"] ** 2
    rv_df["RV_20"] = rv_df["squared_return"].rolling(20).mean()
    rv_df["r^2_{t+1}"] = rv_df["squared_return"].shift(-1)
    rv_df["target_date"] = rv_df["date"].shift(-1)

    # given that we are using a rolling window - the first 20 rows in
    # RV_20 are going to be NaN's since we dont have enough data to compute
    # further more we will have a NAN in the final row because there is
    # no t+1 observation after the final day
    return rv_df.dropna(subset=["RV_20", "r^2_{t+1}", "target_date"])
