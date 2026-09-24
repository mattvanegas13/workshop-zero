"""
Bits and pieces we use to help us how well our models perform
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np


def train_test_folds(start_year, end_year, preprocessed_dataframe):
    """
    generator for splitting a pre-processed dataframe into the appropriate folds used for walk-forward validation
    """

    start_date = pd.Timestamp(f"{start_year}-01-01")
    for test_year in range(start_year+2, end_year+1):
        # when we shifted date by -1, the last trading date of 2021 has a row with a target date thats in 2022 but the row itself has a date
        # that is < test_year - to make sure that isnt included we explicitly define the test start boundary
        # and check against that date to make sure we dont include something like
        # Dec 31, 2021 -- Dec 31  -- Jan 3 return^2 --- Jan 3, 2022 (target date)
        test_start = pd.Timestamp(f"{test_year}-01-01")
        training = preprocessed_dataframe.loc[
            (preprocessed_dataframe["date"] >= start_date)
            & (preprocessed_dataframe["date"] < test_start)
            # protects fold boundary from look ahead contamination
            & (preprocessed_dataframe["target_date"] < test_start)
        ]
        test = preprocessed_dataframe.loc[preprocessed_dataframe["date"].dt.year == test_year]
        yield test_year, training, test


# then we run our model
def run_fold(training_data, test_data, test_year, feature_col):
    """ What it says on the tin"""
    # Need double brackets so we return a dataframe that specifies shape (n,1)
    # which is what sklearn is expecting
    # if we return a timeseries we get something line (n,) or [ n1,n2,3 ]
    # which is a problem because this introduces
    # an ambuiguity - is this one sample with three features or 3 samples of one feature
    training_realized_volatiliy, training_squared_returns = training_data[[
        feature_col]], training_data['r^2_{t+1}']
    test_realized_volatiliy, test_squared_returns = test_data[[
        feature_col]], test_data['r^2_{t+1}']
    model = LinearRegression()
    model.fit(training_realized_volatiliy, training_squared_returns)
    y_pred = model.predict(test_realized_volatiliy)
    baseline_mean = training_squared_returns.mean()
    baseline_pred = np.full(len(test_squared_returns), baseline_mean)
    mse_model = mean_squared_error(test_squared_returns, y_pred)
    mse_baseline = mean_squared_error(test_squared_returns, baseline_pred)
    return {
        "test_year": test_year,
        "model_mse": mse_model,
        "baseline_mse": mse_baseline,
        "coef": model.coef_[0],
        "intercept": model.intercept_,
    }
