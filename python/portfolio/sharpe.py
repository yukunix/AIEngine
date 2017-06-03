'''
Created on 29 May 2017

@author: Yukun
'''

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

def annualised_sharpe(data, periods, weights):
    '''
    data: pandas dataframe (pandas.core.frame.DataFrame) with time and numbers(trade prices)
    periods: number of periods in a year, e.g. 252 for daily data, 252*6.5 for hourly data
    weights: portfolio weights in numpy array, e.g. np.asarray([0.5,0.2,0.2,0.1])
    '''
    #convert daily stock prices into daily returns
    returns = data.pct_change()

    #calculate mean daily return and covariance of daily returns
    mean_daily_returns = returns.mean()
    cov_matrix = returns.cov()

    #calculate annualised portfolio return
    portfolio_return = np.sum(mean_daily_returns * weights) * periods
    
    #calculate annualised portfolio volatility
    portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(periods)
    
    # Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    sharpe_ratio = portfolio_return/portfolio_std_dev
    return sharpe_ratio, portfolio_return, portfolio_std_dev


def tangent_portfolio(data, periods, num_portfolios=25000, ret_results=False):
    '''
    data: pandas dataframe (pandas.core.frame.DataFrame) with time and numbers(trade prices)
    periods: number of periods in a year, e.g. 252 for daily data, 252*6.5 for hourly data
    num_portfolios: number of runs of random portfolio weights, default 25000
    ret_results: True - return all randomly generated weights along with std_dev, sharpe and period returns 
    '''
    
    stocks = list(data)
    
    #set up array to hold results
    #We have increased the size of the array to hold the weight values for each stock
    results = np.zeros((len(stocks)+3, num_portfolios))
    
    for i in range(num_portfolios):
        #select random weights for portfolio holdings
        weights = np.array(np.random.random(len(stocks)))
        #rebalance weights to sum to 1
        weights /= np.sum(weights)
        
        (results[2,i], results[0,i], results[1,i]) = annualised_sharpe(data, periods, weights)
        
        #iterate through the weight vector and add data to results array
        for j in range(len(weights)):
            results[j+3,i] = weights[j]

    #convert results array to Pandas DataFrame
    results_frame = pd.DataFrame(results.T, columns=['ret','stdev','sharpe']+stocks)
    
    #locate position of portfolio with highest Sharpe Ratio
    max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
    #locate positon of portfolio with minimum standard deviation
    min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]
    
    if ret_results:
        return (max_sharpe_port, min_vol_port, results_frame)
    else:
        return (max_sharpe_port, min_vol_port)


def plot_annualised_sharpe(results_frame, max_sharpe_port, min_vol_port):
    '''
    plot all weights with x axis return and y axis volatility, maximum sharpe ratio point and minimum volatility point 
    '''
    
    #create scatter plot coloured by Sharpe Ratio
    plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
    plt.xlabel('Volatility')
    plt.ylabel('Returns')
    plt.colorbar()
    #plot red star to highlight position of portfolio with highest Sharpe Ratio
    plt.scatter(max_sharpe_port['stdev'],max_sharpe_port['ret'],marker=(5,1,0),color='r',s=1000)
    #plot green star to highlight position of minimum variance portfolio
    plt.scatter(min_vol_port['stdev'],min_vol_port['ret'],marker=(5,1,0),color='g',s=1000)
    plt.show()
    

if __name__ == "__main__":
    #list of stocks in portfolio
    stocks = ['AAPL','MSFT','AMZN','YHOO']

    #download daily price data for each of the stocks in the portfolio
    data = web.DataReader(stocks,data_source='google',start='01/01/2010')['Close']
    
    #set array holding portfolio weights of each stock
    weights = np.asarray([0.5,0.2,0.2,0.1])
    
    periods = 252
    
    (sharpe, annualised_return, volatility) = annualised_sharpe(data, periods, weights)
    
    print('Portfolio expected annualised sharpe is {}, annualised return is {} and volatility is {}'.format(round(sharpe,2), round(annualised_return,2), round(volatility,2)))
    
    
    (max_sharpe_port, min_vol_port, results_frame) = tangent_portfolio(data, periods, 25000, True)
    
    print('max sharpe portfolio')
    print(max_sharpe_port.to_string())
    print('min volatility portfolio')
    print(min_vol_port.to_string())
    
    plot_annualised_sharpe(results_frame, max_sharpe_port, min_vol_port)
    
    