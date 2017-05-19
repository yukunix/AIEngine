'''
Created on 17 May 2017

@author: Yukun
'''

class Portfolio(object):
    '''
    a portfolio of stock(s)
    '''

    def __init__(self, cash):
        '''
        cash: total available cash for the portfolio
        '''
        self.cash = cash
    
    def update(self, sym, side, quantity, price):
        '''
        sym: traded stock
        side: long/short
        quantity: traded quantity
        price: traded price
        '''
        pass
    
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
    
        