require(PortfolioAnalytics)
symbol_list = c(
  "MSFT","AAPL","GOOG","XOM","FB","JNJ","AMZN","GE","WFC","JPM","BAC","T","WMT","PG","CHL","BUD","V")
getSymbols(symbol_list, from = '2014-01-01')
getSymbols("SPY", from = '2014-01-01')
securities_matrix = NULL
for (sym in symbol_list) {
  securities_matrix = merge.xts(securities_matrix,
                                Return.calculate(Ad(get(paste(
                                  sym
                                ))),
                                method = 'discrete'))
}
securities_matrix = securities_matrix[complete.cases(securities_matrix)]
SPYReturn = Return.calculate(Ad(SPY), method = 'discrete')
View(securities_matrix)
chart.CumReturns(securities_matrix, main = "Matrix")
#An Example of PortfolioAnalytics - Minimum Variance
MinimumVariancePortfolio = portfolio.spec(assets = colnames(securities_matrix))

MinimumVariancePortfolio = add.objective(portfolio = MinimumVariancePortfolio,
                                         type = 'risk',
                                         name = 'StdDev')
#An Example of PortfolioAnalytics - Setting up Constraints
MinimumVariancePortfolio = add.constraint(portfolio = MinimumVariancePortfolio,
                                          type = "full_investment")

MinimumVariancePortfolio = add.constraint(portfolio = MinimumVariancePortfolio,
                                          type = "long_only")

MinimumVariancePortfolio = add.constraint(
  portfolio = MinimumVariancePortfolio,
  type = "box",
  min = 0,
  max = 0.3
)
#Optimization with PortfolioAnalytics
.storage <- new.env()
OptimizedPortfolioMinVariance = optimize.portfolio(R = securities_matrix,
                                                   
                                                   portfolio = MinimumVariancePortfolio,
                                                   trace = TRUE)
chart.Weights(OptimizedPortfolioMinVariance)

#Mean Variance Optimization
MeanVariancePortfolio = add.objective(portfolio = MinimumVariancePortfolio,
                                      type = 'return',
                                      name = 'mean')
OptimizedPortfolioMeanVariance = optimize.portfolio(R = securities_matrix,
                                                    portfolio = MeanVariancePortfolio,
                                                    trace = TRUE)
chart.Weights(OptimizedPortfolioMeanVariance)
#Risk to Return Analysis
chart.RiskReward(
  OptimizedPortfolioMeanVariance,
  return.col = 'mean',
  risk.col = 'StdDev',
  main = 'Risk to Return Plot of various Portfolio Combinations'
)
#Backtesting with PortfolioAnalytics

MinimumVarianceBT = optimize.portfolio.rebalancing(
  R = securities_matrix,
  MinimumVariancePortfolio,
  rebalance_on = 'years',
  training_period = 252,
  rolling_window = 252
)

MeanVarianceBT = optimize.portfolio.rebalancing(
  R = securities_matrix,
  MeanVariancePortfolio,
  rebalance_on = 'years',
  training_period = 252,
  rolling_window = 252
)

#Using PerformanceAnalytics to compute portfolio returns

MinVariancePortfReturns = Return.rebalancing(R = securities_matrix,
                                             weights = extractWeights(MinimumVarianceBT))
colnames(MinVariancePortfReturns) = c('MinVariancePortfReturns')
MeanVariancePortfReturns = Return.rebalancing(R = securities_matrix,
                                              weights = extractWeights(MeanVarianceBT))
colnames(MeanVariancePortfReturns) = c('MeanVariancePortfReturns')
EqualWeightPortfReturns = Return.rebalancing(R = securities_matrix)
colnames(EqualWeightPortfReturns) = c('EqualWeightPortfReturns')

#Analysing our portfolios

PortfolioComparisonData = merge.xts(
  MinVariancePortfReturns,
  MeanVariancePortfReturns,
  EqualWeightPortfReturns,
  SPYReturn
)['2014-01-01/2017-07-27']
chart.CumReturns(PortfolioComparisonData,
                 main = 'Performance of Various Strategies',
                 legend.loc = 'topleft')

#Analysing our portfolios - Functions

table.AnnualizedReturns(PortfolioComparisonData)
maxDrawdown(PortfolioComparisonData)
table.CAPM(PortfolioComparisonData[, 1:3],
           PortfolioComparisonData[, 4])[c(2, 6, 9, 10, 11, 12), ]