from abc import ABCMeta, abstractmethod


class MarketProvider(object, metaclass=ABCMeta):

    def __init__(self, df):
        self.data = df
    @abstractmethod
    def gen(self):
        pass

    def series(self, size):
        pass


class OHLCVProvider(MarketProvider):

    def __init__(self, df, type_):
        self.data = df
        self.type_ = type_
        self.row_index = 0

    def gen(self):
        while self.row_index < len(self.data.index):
            yield self.data[self.row_index: self.row_index + 1][self.type_]
            self.row_index += 1

    def series(self):
        return self.data[self.type_]


class SMAProvider(MarketProvider):
    def __init__(self):
        pass

    def next(self):
        pass


class EMAProvider(MarketProvider):
    def __init__(self):
        pass

    def next(self):
        pass


class MACDProvider(MarketProvider):
    def __init__(self):
        pass

    def next(self):
        pass

# class ClosePriceMAProvider(MarketProvider):
#     def __init__(self, data, period):
#         self.ma = pd.Series.rolling(data['Close'], period).mean()
#         self.current_position = 0
#
#     def next(self):
#         self.current_position += 1
#         return self.ma[self.current_position - 1]
#
#
# class MACDProvider(MarketProvider):
#     def __init__(period1, period2):
#         pass
#
#     def next():
#         pass
