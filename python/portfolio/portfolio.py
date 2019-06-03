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
    
    def cash(self):
        '''
        get current available cash of the portoflio
        return $
        '''
        return self.cash
    
    def position(self, sym):
        '''
        get the quantity of a stock in the portfolio
        return $
        '''
        return self.positions.get(sym, 0)
    
    def portfolio_value(self):
        '''
        Deprecated!!! Use valuer instead
        
        A value to measure the portfolio, for example, 
        Sharpe ratio(return to volatility), Sortino ratio(return to downside deviation), 
        Jensen's alpha(risk-adjusted), Treynor(reward-to-volatility) ratio, 
        or simply market value. 
        '''
        pass
    