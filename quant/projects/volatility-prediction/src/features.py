"""
Code that helps us select input features that will be fed into our models
"""
import pandas as pd


def rv_20(df: pd.DataFrame):
    """Realized volatility over 20 day rolling window"""
    df = df.copy()
    df['RV_20'] = df['squared_return'].rolling(20).mean()
    return df


def ewma(df: pd.DataFrame, gamma: float = .94):
    """Exponential weighted moving average"""
    df = df.copy()
    df["EWMA"] = (df["squared_return"]
                  .ewm(alpha=1 - gamma, adjust=False)
                  .mean()
                  )
    return df
