import quandl as qd
import numpy as np
import marketdata.MarketProvider as MarketProvider

class MarketProviderFactory:
	
	def __init__(self, source, sym, start, end, interval, localstore):
		## initialize quandl, start downloading file for the time range
		## interval: e.g. 1d
		## if not in localstore, download from source, then persist to localstore with key: sym-start-end-quandl-params, otherwise load local file.
		
		if (source == 'qundle'):				
			qd.ApiConfig.api_key = 'Uk8aW7H-x7bvsqD2wH98'
			self.data = qd.get('WIKI/'+sym, start_date=start, end_date=end)
			
		print(self.data.head(5))
	
	def getMarketProvider(type, **kwargs):
		# type cloase_price: **kwargs: {period:5d}
		# type MA: {period: 15d}
		# type MACD: {period1:5d, period2:10d}
		if (type == 'close_price_ma'):
			return ClosePriceProvider(self.data, kwargs['period'])
		else:
			raise ValueError('unknown type: ' + type)
		
class ClosePriceMAProvider(MarketProvider):

	def __init__(self, data, period):
		self.ma=pd.Series.rolling(data['Close'], period).mean()
		self.current_position = 0

	def next(self):
		self.current_position += 1
		return self.ma[self.current_position-1]


class MACDProvider(MarketProvider):

	def __init__(period1, period2):
		pass
		
	def next():
		# calculate MACD
		return maValue


# input: data file (format pandas)
#        interval options (1d, 1w, 1m)
# output: list (column data)
def provider(data_file, column, start, end, interval='1d'):
    global dt_len
    df = data_file
    df = df[column]
    df = df.loc[start:end]
    df = list(df)
    if interval == '1d':
        dt_len = len(df)
        return iter(df)
    elif interval == '1w':
        df_wk = []
        days = 5
        weeks = len(df) // days  # how many weeks
        for week in range(0, weeks):
            temp = df[week*5:(week+1)*5]
            df_wk.append(np.mean(temp))
        dt_len = len(df_wk)
        return iter(df_wk)
    elif interval == '1m':
        df_mth = []
        days = 30
        months = len(df) // days  # how many weeks
        for week in range(0, months):
            temp = df[week*30:(week+1)*30]
            df_mth.append(np.mean(temp))
        dt_len = len(df_mth)
        return iter(df_mth)
    else:
        print('Wrong interval')

my_dt = provider(my_data, 'Close', start='2008-01-05', end='2008-01-30', interval='1w')
for i in range(dt_len):
    print(next(my_dt))

"""有待优化的问题
1. 日期选择， 对于 week 和 month 的选择不是很准确， 现在只是选周期为5或者30 trading days"""
