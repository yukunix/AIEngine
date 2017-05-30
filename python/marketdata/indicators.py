'''

Market indicators, including technical indicators like SMA, EMA, MACD, etc.

'''
import pandas as pd
from marketdata.MarketData import MarketData

class CloseSMAProvider(MarketData):
    
    def __init__(self, data, period):
        if (len(data) < period):
            raise ValueError('length of data is smaller than period')
        
        self.closes = data['Close']
        self.ma = pd.Series.rolling(self.closes, period).mean()
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.ma[self.current_position - 1]
        else:
            raise StopIteration()
    
class SMA(MarketData):
    def __init__(self):
        pass

    def next(self):
        pass


class EMA(MarketData):
    def __init__(self):
        pass

    def next(self):
        pass


class MACD(MarketData):
    def __init__(self):
        pass

    def next(self):
        pass