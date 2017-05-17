import MassData as md
import MarketProvider as mp

mass_data = md.MassData('quandl', 'AAPL', '2017-01-01', '2017-01-30')
close_price = mp.OHLCVProvider(mass_data.df, 'Close')

# test of generator
generator = close_price.gen()
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))

print()

# test of series
print(close_price.series())
