from marketdata.provider import MarketDataProvider

provider = MarketDataProvider('quandl', 'AAPL', '2017-01-01', '2017-02-20')

### test iterating close price SMA
close_price_sma = provider.getMarketData('close_sma', period=5)
print('close_price_sma.next()')
for _ in range(len(provider.data)):
    print(close_price_sma.next())

close_price_sma2 = provider.getMarketData('close_sma', period=5)
print('for loop close_price_sma2')
for price in close_price_sma2:
    print(price)


### test OHLCV generator
OHLCV = provider.getMarketData('OHLCV', period=5)
print('iterate OHLCV')
for prices in OHLCV:
    print(prices)


### test iterating close price EMA
close_price_ema = provider.getMarketData('close_ema', period=5)
print('close_price_ema.next()')
for _ in range(len(provider.data)):
    print(close_price_ema.next())


### test iterating close price MACD, signal line and MACD difference
### test Signal Line
### test MACD difference
close_price_macd = provider.getMarketData('close_macd', period1=12, period2=26)
print('close_price_macd.next()')
for _ in range(len(provider.data)):
    print(close_price_macd.next())

signaline = provider.getMarketData('signal_line', period1=12, period2=26)
print('signaline.next()')
for _ in range(len(provider.data)):
    print(signaline.next())

macdiff = provider.getMarketData('macd_diff', period1=12, period2=26)
print('macdiff.next()')
for _ in range(len(provider.data)):
    print(macdiff.next())


### test Momentum
mom = provider.getMarketData('close_momentum', period=5)
print('momentum.next()')
for _ in range(len(provider.data)):
    print(mom.next())

### test ROC
roc = provider.getMarketData('close_roc', period=5)
print('roc.next()')
for _ in range(len(provider.data)):
    print(roc.next())

###