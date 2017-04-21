# Wrote by Michael Li
# April 21

import pandas as pd
import numpy as np


# simple moving average
# input: column data set (pd.Series) , num_periods (int)
# output: sma data set (pd.Series)
def sma(col_data, num_periods):
    col_data = col_data.tolist()[::-1]
    col_data = pd.Series(col_data)
    length = col_data.count() - num_periods
    sma_series = []
    for i in range(length):
        start = i
        end = i + num_periods
        temp_mean = np.mean(col_data[start:end])
        sma_series.append(temp_mean)
    return pd.Series(sma_series)


# exponential moving average
# input: column data set (pd.Series) , num_periods (int)
# output: ema data set (pd.Series)
def ema(col_data, num_periods):
    ema_0 = sma(col_data, num_periods)[0]   # have to put this in first to avoid reverse tricks
    col_data = col_data.tolist()[::-1]
    col_data = pd.Series(col_data)
    alpha = 2 / (num_periods + 1)
    ema_series = [ema_0]
    for i in range(0, col_data.count() - num_periods - 1):
        current_price = col_data.tolist()[num_periods + i]
        ema_i = current_price * alpha + (ema_series[i] * (1 - alpha))
        ema_series.append(ema_i)
    return pd.Series(ema_series)


# moving average convergence divergence
# input: column data set (pd.Series)
# output: macd (pd.Series)
def macd(col_data):
    ema_26 = ema(col_data, 26)
    ema_12 = ema(col_data, 12)[:ema_26.count()]     # make sure the length are the same to do subtraction
    macd_result = [x - y for x, y in zip(ema_12, ema_26)]
    return pd.Series(macd_result)


# signal line
def sigline(col_data):
    return ema(macd(col_data), 9)
