import numpy as np
from numpy import ndarray as nd
from config import Config
import sys
from copy import copy
from datetime import datetime as dt
class DataUtil:
    def __init__(self, config):
        self.config = config

    def preprocess_state(self, data, portfolio):
        featured_data = copy(data)
        stock_value = portfolio['stock_value']
        total = portfolio['total']
        featured_data += self.time_to_vec()
        featured_data += self.stock_portion(stock_value, total)

        # featured_data += [self.trade_confidence(buy_quantity, stock_amount)]
        '''TODO'''
        return featured_data

    @staticmethod
    def stock_portion(stock_value, total):
        portion = 1.0 * stock_value / total
        if portion < 0.2:
            return [portion]+[1,0,0,0,0]
        elif portion < 0.4:
            return [portion]+[0,1,0,0,0]
        elif portion < 0.6:
            return [portion]+[0,0,1,0,0]
        elif portion < 0.8:
            return [portion]+[0,0,0,1,0]
        elif portion <= 1:
            return [portion]+[0,0,0,0,1]
        else:
            print "sth wrong with stock portion", portion, stock_value, total
            sys.exit(0)

    @staticmethod
    def trade_confidence(buy_quantity, stock_amount):
        return buy_quantity / stock_amount

    @staticmethod
    def time_to_vec():
        #aus time...
        now = dt.now().hour - 3
        if now == 9:
            return [1,0,0,0,0]
        if now == 10:
            return [0,1,0,0,0]
        if now == 11:
            return [0,0,1,0,0]
        if now == 13:
            return [0,0,0,1,0]
        if now == 14:
            return [0,0,0,0,1]
        else:
            return [0,0,0,0,0]
