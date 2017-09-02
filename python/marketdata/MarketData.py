from abc import ABCMeta, abstractmethod


class MarketData(object, metaclass=ABCMeta):

    def current(self):
        pass
    
    @abstractmethod
    def next(self):
        pass

    def __iter__(self):
        return self
    
    # Python 3 compatibility
    def __next__(self):
        return self.next()
    
    def series(self, size):
        pass


class OHLCV(MarketData):

    def __init__(self, df):
        self.data = df
        self.row_index = 0

    def current(self):
        return self.open, self.high, self.low, self.close, self.volume
        
    def next(self):
        if self.row_index < len(self.data):
            self.row_index += 1
            row = self.data.ix[self.row_index - 1]
            
            self.open = row['Adj. Open']
            self.high = row['Adj. High']
            self.low = row['Adj. Low']
            self.close = row['Adj. Close']
            self.volume = row['Adj. Volume']
            return self.open, self.high, self.low, self.close, self.volume
        else:
            raise StopIteration()

    def series(self):
        return self.data


