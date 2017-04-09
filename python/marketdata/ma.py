'''
Created on 6 Apr 2017

@author: Yukun
'''

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

tickers = ['AAPL', 'MSFT', '^GSPC']

data_source = 'yahoo'

start_date = '2000-01-01'
end_date = '2016-12-31'

panel_data = data.DataReader(tickers, data_source, start_date, end_date)

adj_close = panel_data.ix['Adj Close']

all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

adj_close = adj_close.reindex(all_weekdays)

adj_close = adj_close.fillna(method='ffill')

adj_close.head(7)
adj_close.describe()

msft = adj_close.ix[:, 'MSFT']

short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(msft.index, msft, label='MSFT')
ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()

plt.show()






