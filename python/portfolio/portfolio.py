'''
Created on 17 May 2017

@author: Yukun
'''

from portfolio.order import Side

class Portfolio(object):
    '''
    a portfolio of stock(s)
    
    valued by cash + marked market positions value
    '''

    def __init__(self, cash):
        '''
        cash: total available cash for the portfolio
        '''
        self.cash = cash
        self.positions = dict()
    
    def update(self, sym, side, quantity, price, consideration):
        '''
        sym: traded stock
        side: long/short
        quantity: traded quantity
        price: traded price
        consideration: total benefit/cost of the transaction
        '''
        
        if Side.Buy == side:
            self.positions[sym] = self.positions.get(sym, 0) + quantity
            self.cash -= consideration
        else:
            self.positions[sym] = self.positions.get(sym, 0) - quantity
            self.cash += consideration
        
        
    
    def market_value(self):
        '''
        get marked to market value of the portfolio, including both positions and cash
        return $
        '''
        pass
    
    def cash_value(self):
        '''
        get current available cash of the portoflio
        return $
        '''
        pass
    
    def position_value(self, sym):
        '''
        get marked to market value of a stock in the portfolio
        return $
        '''
        pass
    
    def portfolio_value(self):
        '''
        use valuer instead
        
        A value to measure the portfolio, for example, 
        Sharpe ratio(return to volatility), Sortino ratio(return to downside deviation), 
        Jensen's alpha(risk-adjusted), Treynor(reward-to-volatility) ratio, 
        or simply market value. 
        '''
        pass
    

class SharpePortfolio(Portfolio):
    
    def portfolio_value(self):
        '''
        use valuer instead
        
        return Sharpe ratio of the portfolio
        '''
        pass
            