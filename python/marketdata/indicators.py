'''

Market indicators, including technical indicators like SMA, EMA, MACD, etc.

'''
import pandas as pd
from marketdata.MarketData import MarketData


# SMA: adding up all the recent N close prices and divided by N
# Formula: N-period sum / N
# Parameters: {N: period}
class CloseSMAProvider(MarketData):
    
    def __init__(self, data, period):
        if (len(data) < period):
            raise ValueError('length of data is smaller than period')
        
        self.closes = data['Close']
        self.sma = pd.Series.rolling(self.closes, period).mean()
        self.length = len(data)
        self.current_position = 0

    def current(self):
        return self.current_sma
        
    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            self.current_sma = self.sma[self.current_position - 1]
            return self.current_sma
        else:
            raise StopIteration()


# EMA: similar to the SMA, but more weight is given to the latest date.
#      popular N choices: 12, 26 for short term and 50, 200 for long term.
# Formula: 1. Initial SMA: N-period sum / N
#          2. Multiplier: (2 / (N + 1) ) = (2 / (10 + 1) ) = 0.1818 (18.18%)
#          3. EMA: {Close - EMA(previous day)} x Multiplier + EMA(previous day)
# Parameters: {N: period}
class CloseEMAProvider(MarketData):

    def __init__(self, data, period):
        if (len(data) < period):
            raise ValueError('length of data is smaller than period')

        self.closes = data['Close']
        self.ema = pd.Series.ewm(self.closes, span = period, min_periods = period - 1).mean()
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.ema[self.current_position - 1]
        else:
            raise StopIteration


# MACD: (M-day-EMA) - (N-day-EMA)
#       normally M = 12, N =26
#
# Parameters: period 1: M, period 2: N
class CloseMACDProvider(MarketData):

    def __init__(self, data, period1, period2):
        if (len(data) < period1) or (len(data) < period2):
            raise ValueError('length of data is smaller than period')

        self.closes = data['Close']
        self.ema_1 = pd.Series.ewm(self.closes, span=period1, min_periods=period1 - 1).mean()
        self.ema_2 = pd.Series.ewm(self.closes, span=period2, min_periods=period2 - 1).mean()
        self.macd = self.ema_1 - self.ema_2
        # self.signaline = pd.Series.ewm(self.macd, span=9, min_periods =8).mean()
        # self.macdiff = self.macd - self.signaline
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.macd[self.current_position - 1]

        else:
            raise StopIteration



# Signal Line: 9 day EMA of MACD Line
# Parameters: period1, period2
class SignalLineProvider(MarketData):

    def __init__(self, data, period1, period2):
        if (len(data) < period1) or (len(data) < period2):
            raise ValueError('length of data is smaller than period')

        self.closes = data['Close']
        self.ema_1 = pd.Series.ewm(self.closes, span=period1, min_periods=period1 - 1).mean()
        self.ema_2 = pd.Series.ewm(self.closes, span=period2, min_periods=period2 - 1).mean()
        self.macd = self.ema_1 - self.ema_2
        self.signaline = pd.Series.ewm(self.macd, span=9, min_periods =8).mean()
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.signaline[self.current_position - 1]

        else:
            raise StopIteration

# MACDdiff: MACD - Singal Line
# Parameters: period1, period2

class MACDDifferenceProvider(MarketData):

    def __init__(self, data, period1, period2):
        if (len(data) < period1) or (len(data) < period2):
            raise ValueError('length of data is smaller than period')

        self.closes = data['Close']
        self.ema_1 = pd.Series.ewm(self.closes, span=period1, min_periods=period1 - 1).mean()
        self.ema_2 = pd.Series.ewm(self.closes, span=period2, min_periods=period2 - 1).mean()
        self.macd = self.ema_1 - self.ema_2
        self.signaline = pd.Series.ewm(self.macd, span=9, min_periods=8).mean()
        self.macdiff = self.macd - self.signaline
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.macdiff[self.current_position - 1]


# Momentum
class CloseMomentumProvider(MarketData):

    def __init__(self, data, period):
        if (len(data) < period):
            raise ValueError('length of data is smaller than period')

        self.closes = data['Close']
        self.mom = self.closes.diff(period)
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.mom[self.current_position - 1]


# Rate of Change
class CloseROCProvider(MarketData):

    def __init__(self, data, period):
        if (len(data) < period):
            raise ValueError('length of data is smaller than period')

        self.closes = data['Close']
        self.changes = self.closes.diff(period - 1)
        self.originals = self.closes.shift(period - 1)
        self.roc = self.changes / self.originals
        self.length = len(data)
        self.current_position = 0

    def next(self):
        self.current_position += 1
        if (self.current_position <= self.length):
            return self.roc[self.current_position - 1]
