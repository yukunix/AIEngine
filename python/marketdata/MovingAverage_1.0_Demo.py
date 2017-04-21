import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import MovingAverage as ma

df = pd.read_csv('SP500_Data.csv', parse_dates=['Date'])

# recent 50 days moving average
num_days = 50

# real stock price
Adj_Close_50 = df['Adj Close'][:num_days]
reversed_Adj_Close = Adj_Close_50.tolist()[::-1]   # reverse the list
reversed_Adj_Close = pd.Series(reversed_Adj_Close)  # redefine reverse list as a pd.Series
plt.plot(reversed_Adj_Close)

# sma & ema
SMA = ma.sma(Adj_Close_50, num_days)
EMA = ma.ema(Adj_Close_50, num_days)

plt.plot(reversed_Adj_Close, 'ko-')
plt.plot(SMA, 'r--')
plt.plot(EMA, 'b-')
plt.legend()
plt.show()

