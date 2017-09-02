'''
Created on 16 May 2017

@author: Yukun
'''
from oms.execution import ExecutionService
from portfolio.portfolio import Portfolio
from portfolio.valuer import PortfolioValuer
from portfolio.order import Side

class OMS(object):
    '''
    Order Management System, managing both positions and execution
    '''
    
    def __init__(self, ExecutionService, Portfolio, PortfolioValuer):
        self.execution = ExecutionService
        self.portfolio = Portfolio
        self.portfolioValuer = PortfolioValuer
    
    def no_operation(self, sym):
        self.execution.no_operation(sym)
    
    def place(self, sym, side, quantity, price):
        '''
        place an order to execute, and update portfolio
        '''
        if (Side.Hold == side):
            return
        
        executed_price, executed_quantity = self.execution.place(sym, side, quantity, price)
        self.portfolio.update(sym, side, executed_quantity, executed_price, executed_price*executed_quantity)


        