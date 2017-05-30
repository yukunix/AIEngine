import quandl as qd
import pandas as pd
import os
from marketdata.indicators import CloseSMAProvider
from marketdata.MarketData import OHLCV


class MarketDataProvider:
    
    local_store_dir = os.getcwd() + '/marketstore/'

    def __init__(self, source, symbol, start, end, interval='1d'):
        """
        initialize source data, start downloading data for the time range
        interval: e.g. 1d, 1w, 1m
        if not in local data store, download from source, then persist to local store
        with key: source_symbol_start_end_interval, otherwise load local file.
        """
        
        self.symbol = symbol
        self.source = source
        self.start = start
        self.end = end
        self.interval = interval
        self.local_store_file = (MarketDataProvider.local_store_dir + self.source + '_' + self.symbol + '_'
                     + self.start + '_' + self.end + '_' + self.interval + '.csv')

        if self.is_existing_df():
            # if there is a same dataframe downloaded before, use it
            self.data = pd.read_csv(self.local_store_file)  
        else:  
            # if there is no same dataframe, then download and store it to local store
            if source == 'quandl':
                qd.ApiConfig.api_key = 'Uk8aW7H-x7bvsqD2wH98'
                self.data = qd.get('WIKI/' + symbol, start_date=start, end_date=end)
                self.data.to_csv(self.local_store_file, index=False)  # store new data to local store
            elif source == 'google':
                pass
            elif source == 'yahoo':
                pass
            else:
                raise ValueError('unknown source: ' + source)
            
        print('loading done.')

    def is_existing_df(self):
        """
        1. check the existence of local store, if no then create one.
        2. check if the data file already exists, return True if file already exists, return False otherwise
        """
        
        if not os.path.exists(MarketDataProvider.local_store_dir):
            print('local store does not exist, creating directory ' + MarketDataProvider.local_store_dir)
            os.makedirs(MarketDataProvider.local_store_dir)
            
        if os.path.isfile(self.local_store_file):
            print('There exists a same file in the local store, loading data from ' + self.local_store_file)
            return True
        else:
            print('There is NO same file in the local store, retrieving from {} ...'.format(self.source.upper()))
            return False

    def getMarketData(self, data_type, **kwargs):
        """
        data_type OHLCV: 
        data_type close_sma: {period:5d}
        data_type EMA: {period: 15d, ......}
        data_type MACD: {period1:5d, period2:10d}
        """
        
        if (data_type == 'close_sma'):
            return CloseSMAProvider(self.data, kwargs['period'])
        elif (data_type == 'OHLCV'):
            return OHLCV(self.data)
        else:
            raise ValueError('unknown type: ' + type)
