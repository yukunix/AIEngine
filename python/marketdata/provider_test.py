from marketdata.provider import MarketDataProvider

provider = MarketDataProvider('quandl', 'AAPL', '2017-01-01', '2017-01-30')

### test iterating close price SMA
close_price_sma = provider.getMarketData('close_sma', period=5)
print('close_price_sma.next()')
for _ in range(len(provider.data)):
    print(close_price_sma.next())

close_price_sma2 = provider.getMarketData('close_sma', period=5)
print('for loop close_price_sma2')
for price in close_price_sma2:
    print(price)

# test OHLCV generator
OHLCV = provider.getMarketData('OHLCV', period=5)
print('iterate OHLCV')
for prices in OHLCV:
    print(prices)
