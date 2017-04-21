# Wrote by Michael Li
# April 21

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import MovingAverage as ma

df = pd.read_csv('SP500_Data.csv', index_col='Date', parse_dates=['Date'])

# recent 50 days moving average
# 5 day sma and ema
recent_days = 50
num_periods = 5

# real stock price
adj_close = df['Adj Close'][:recent_days]
reversed_Adj_Close = adj_close.tolist()[::-1]   # reverse the list
reversed_Adj_Close = pd.Series(reversed_Adj_Close)  # redefine reverse list as a pd.Series


# sma & ema
SMA = ma.sma(adj_close, num_periods)
EMA = ma.ema(adj_close, num_periods)
MACD = ma.macd(adj_close)
SIGLINE = ma.sigline(adj_close)

time_series = np.linspace(5, 50, num=45)

plt.title('5 day sma & ema for the most recent 50 days')
plt.xlabel('Days')
plt.ylabel('Price $')

plt.plot(time_series, reversed_Adj_Close[:45], color='black', label='real-price')
plt.plot(time_series, SMA, color='red', label='sma')
plt.plot(time_series, EMA, color='blue', label='ema')
plt.legend()
plt.show()

print(MACD)
print(SIGLINE)
