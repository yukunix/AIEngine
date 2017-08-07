import pandas as pd
import os
import marketdata.techIndicators as ind
import marketdata.indicators as myind
from marketdata.provider import MarketDataProvider


provider = MarketDataProvider('quandl', 'AAPL', '2017-01-01', '2017-01-30')

df = provider.data

df_ma = ind.EMA(df, 5)
print(df_ma)