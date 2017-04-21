import pandas as pd
import numpy as np


# simple moving average
# input: column data set (pd.Series) , num_periods (int)
# output: sma data set (pd.Series)
def sma(col_data, num_periods=None):
    temp = []
    sma_series = []
    if num_periods is None:
        num_periods = col_data.count()
    for i in range(num_periods):
        temp.append(col_data[i])
        temp_mean = np.mean(temp)
        sma_series.append(temp_mean)
    sma_series.reverse()
    sma_series = pd.Series(sma_series)
    return sma_series


# exponential moving average
# input: column data set (pd.Series) , num_periods (int)
# output: ema data set (pd.Series)
def ema(col_data, num_periods=None):
    if num_periods is None:
        num_periods = col_data.count()
    ema_0 = sma(col_data, num_periods).tolist()[-1]
    print('ema_0 is:', ema_0)
    alpha = 2 / (1 + num_periods)
    ema_series = [ema_0]
    for i in range(1, num_periods):
        current_price = col_data[i]
        ema_i = (current_price * alpha) + (ema_series[i - 1] * (1 - alpha))
        ema_series.append(ema_i)
    ema_series.reverse()
    ema_series = pd.Series(ema_series)
    return ema_series
