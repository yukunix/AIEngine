library(PortfolioAnalytics)
library(quantmod)
library(PerformanceAnalytics)
library(zoo)
library(plotly)
if (!exists("prices.data")) {
  funds <- c("MSFT",  "AAPL", "GOOG", "XOM", "FB")
  getSymbols(funds, from = '2014-01-01')
  prices.data <-
    merge.zoo(MSFT[, 6],  AAPL[, 6], GOOG[, 6], XOM[, 6], FB[, 6])
  #prices.data <- merge.zoo(MSFT[,6],  AAPL[,6],GOOG[,6],XOM[,6],FB[,6],JNJ[,6],AMZN[,6],GE[,6],WFC[,6],JPM[,6],BAC[,6],T[,6],WMT[,6],PG[,6],CHL[,6],BUD[,6],V[,6])
  getSymbols("SPY", from = '2014-01-01')
  SPYReturn = Return.calculate(Ad(SPY), method = 'discrete')
 
}


# Calculate returns
returns.data <-
  Return.calculate(prices = prices.data, method =  c("discrete", "log"))
returns.data <- na.omit(returns.data)
# Set names


# Save mean return vector and sample covariance matrx
meanReturns <- colMeans(returns.data)
#returns <- edhec[, 1:6]
#funds <- colnames(returns)
init.portfolio <- portfolio.spec(assets = funds)
print.default(init.portfolio)
init.portfolio <-
  add.constraint(portfolio = init.portfolio, type = "full_investment")
init.portfolio <-
  add.constraint(portfolio = init.portfolio, type = "long_only")
# Add objective for portfolio to minimize portfolio standard deviation
minSD.portfolio <- add.objective(portfolio = init.portfolio,
                                 type = "risk",
                                 name = "StdDev")

# Add objectives for portfolio to maximize mean per unit ES
meanES.portfolio <- add.objective(portfolio = init.portfolio,
                                  type = "return",
                                  name = "mean")

meanES.portfolio <- add.objective(portfolio = meanES.portfolio,
                                  type = "risk",
                                  name = "ES")


# Run the optimization for the minimum standard deviation portfolio
minSD.opt <-
  optimize.portfolio(
    R = returns.data,
    portfolio = minSD.portfolio,
    optimize_method = "ROI",
    trace = TRUE
  )

print(minSD.opt)

# Run the optimization for the maximize mean per unit ES
meanES.opt <-
  optimize.portfolio(
    R = returns.data,
    portfolio = meanES.portfolio,
    optimize_method = "ROI",
    trace = TRUE
  )

print(meanES.opt)

plot(
  minSD.opt,
  risk.col = "StdDev",
  chart.assets = TRUE,
  main = "Min SD Optimization",
  ylim = c(0, 0.0083),
  xlim = c(0, 0.06)
)

plot(
  meanES.opt,
  chart.assets = TRUE,
  main = "Mean ES Optimization",
  ylim = c(0, 0.0083),
  xlim = c(0, 0.16)
)
EqualWeightPortfReturns = Return.rebalancing(R = returns.data)
colnames(EqualWeightPortfReturns) <- c("equalweight")
minSD.returns = Return.rebalancing(R = returns.data, weights = extractWeights(minSD.opt))
colnames(minSD.returns) <- c("minReturn")
meanES.returns = Return.rebalancing(R = returns.data, weights = extractWeights(meanES.opt))
#Analysing our portfolios
colnames(meanES.returns) <- c("meanESReturns")
PortfolioComparisonData = merge.xts(minSD.returns ,
                                    meanES.returns,
                                    EqualWeightPortfReturns,
                                    SPYReturn)['2014-01-02/2017-08-04']
chart.CumReturns(PortfolioComparisonData,
                 main = 'Performance of Various Strategies',
                 legend.loc = 'topleft')
