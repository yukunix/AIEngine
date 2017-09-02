'''
Created on 17 May 2017

@author: Yukun
'''

import random
from marketdata.MarketData import MarketData
from marketdata.provider import MarketDataProvider

class ExecutionService(object):
    '''
    Base class for execution service. 
    Subclasses may be various types of simulator or live execution service.
    '''

    def no_operation(self, sym):
        raise NotImplemented
    
    def place(self, sym, side, quantity, price):
        '''
        place an order to execute.
        return (executed_price, executed_quantity)
        '''
        raise NotImplemented
    
    def amend(self, order):
        raise NotImplemented
    
    def cancel(self, order):
        raise NotImplemented
    
class SingleStockExecutionSimulator(ExecutionService):
    '''
    A simple execution simulator for trading a stock
    '''
        
    def __init__(self, sym, start, end, OHLCV):
        self.marketdata = OHLCV
        
    def no_operation(self, sym):
        pass
        
    def place(self, sym, side, quantity, price):
        ohlcv = self.marketdata.next() ### change to call current() !!!!!
        executed_price = (ohlcv[1] + ohlcv[2]) / 2 ## executed at the mid price of the day
        if (random.random() <= 0.9):
            executed_quantity = quantity
        else:
            executed_quantity = random.randint(round(quantity*0.8), quantity)
        return (executed_price, executed_quantity)
        
        