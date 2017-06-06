'''
Created on 7 Jun 2017

@author: Yukun
'''
from portfolio import sharpe
from portfolio.portfolio import Portfolio

class PortfolioValuer(object):
    '''
    portfolio valuer
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def value(self, portfolio):
        pass
    
class MarketValuer(PortfolioValuer):
    
    def value(self, portfolio):
        return portfolio.market_value
        
        