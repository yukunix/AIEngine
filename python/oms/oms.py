'''
Created on 16 May 2017

@author: Yukun
'''
from oms.execution import ExecutionService
from portfolio.portfolio import Portfolio

class OMS(object):
    '''
    Order Management System, managing both positions and execution
    '''
    
    def __init__(self, ExecutionService, Portfolio):
        self.execution = ExecutionService
        self.portfolio = Portfolio
    
    def no_operation(self, sym):
        self.execution.no_operation(sym)
    
    def place(self, sym, side, quantity, price):
        '''
        place an order to execute, and update portfolio
        '''
        executed_price, executed_quantity = self.execution.place(sym, side, quantity, price)
        self.portfolio.update(sym, side, executed_quantity, executed_price)
    
    