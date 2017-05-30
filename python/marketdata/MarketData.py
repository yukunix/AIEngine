from abc import ABCMeta, abstractmethod


class MarketData(object, metaclass=ABCMeta):
    
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

    def next(self):
        if self.row_index < len(self.data):
            self.row_index += 1
            row = self.data.ix[self.row_index - 1]
            return row['Adj. Open'], row['Adj. High'], row['Adj. Low'], row['Adj. Close'], row['Adj. Volume']
        else:
            raise StopIteration()

    def series(self):
        return self.data


