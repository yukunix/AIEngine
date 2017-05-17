import quandl as qd
import pandas as pd
import numpy as np
import MarketProvider
import os


class MassData:
    path_cwd = os.getcwd()

    def __init__(self, source, symbol, start, end, interval='1d'):
        """initialize source data, start downloading data for the time range
        interval: e.g. 1d, 1w, 1m
        if not in localstore, download from source, then persist to localstore
        with key: source_symbol_start_end_interval, otherwise load local file."""
        self.symbol = symbol
        self.source = source
        self.start = start
        self.end = end
        self.interval = interval
        self.path = (MassData.path_cwd + '/dataWarehouse' + '/' + self.source + '_' + self.symbol + '_'
                     + self.start + '_' + self.end + '_' + self.interval + '.csv')

        if self.is_existing_df():
            self.df = pd.read_csv(self.path)  # if there is a same df downloaded before, use it
        else:  # if there is no same df, then download and store it
            if source == 'quandl':  # to '/dataWarehouse'
                qd.ApiConfig.api_key = 'Uk8aW7H-x7bvsqD2wH98'
                self.df = qd.get('WIKI/' + symbol, start_date=start, end_date=end)
                self.df.to_csv(self.path, index=False)  # store new data to '/dataWarehouse'
            elif source == 'google':
                pass
            elif source == 'yahoo':
                pass
            else:
                raise ValueError('unknown source: ' + source)
        print('loading done.')

    def is_existing_df(self):
        """1. check the existence of local '/dataWarehouse' directory to store data, if no then create one.
        2. check if the data file already exists, return True if file already exists, return False otherwise"""
        path_dataWarehouse = MassData.path_cwd + '/dataWarehouse'
        if not os.path.exists(path_dataWarehouse):
            print('Creating new directory \'~/dataWarehouse\'...')
            os.makedirs(path_dataWarehouse)
        if os.path.isfile(self.path):
            print('There exists a same file in the data warehouse, loading data from local disk.')
            return True
        else:
            print('There is NO same file, now retrieving from {0} ...'.format(self.source.upper()))
            return False

    # def getMarketProvider(type, **kwargs):
    #     # type cloase_price: **kwargs: {period:5d}
    #     # type MA: {period: 15d}
    #     # type MACD: {period1:5d, period2:10d}
    #     if (type == 'close_price_ma'):
    #         return ClosePriceProvider(self.data, kwargs['period'])
    #     else:
    #         raise ValueError('unknown type: ' + type)

    def is_existing_df(self):
        """1. check the existence of local '/dataWarehouse' directory to store data, if no then create one.
        2. check if the data file already exists, return True if file already exists, return False otherwise"""
        path_dataWarehouse = MassData.path_cwd + '/dataWarehouse'
        if not os.path.exists(path_dataWarehouse):
            print('Creating new directory \'~/dataWarehouse\'... at current working directory.')
            os.makedirs(path_dataWarehouse)
        if os.path.isfile(self.path):
            print('There exists a same file in the data warehouse, loading data from local disk.')
            return True
        else:
            print('There is NO same file, now retrieving from {0} ...'.format(self.source.upper()))
            return False
