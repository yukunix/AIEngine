'''
Created on 17 May 2017

@author: Yukun
'''

class Exchange(object):
    '''
    An Exchange Emulator
    '''


    def __init__(self, params):
        pass
    
    def place(self, order):
        '''
        place an order to execute.
        order: {side:buy/sell, quantity:10000, limitPrice:23.56}
        return (executed_price, executed_quantity)
        '''
        pass
    
    def amend(self, order):
        raise NotImplemented
    
    def cancel(self, order):
        raise NotImplemented
    
    
    
        