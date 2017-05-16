'''
Created on 16 May 2017

@author: Yukun
'''

class OMS(object):
    '''
    Order Management System, managing both positions and execution
    '''

    def __init__(self, params):
        pass
       
    def place(self, order):
        '''
        place an order to execute.
        order: {side:buy/sell, quantity:10000, limitPrice:23.56}
        '''
        pass
    
    def position(self, sym):
        '''
        get current position of a stock
        
        return position: {(price1, quantity1), (price2, quantity2), ...}
        '''
        pass 