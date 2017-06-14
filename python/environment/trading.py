'''
Created on 20 May 2017

@author: Yukun
'''

from tensorforce.environments import Environment
from oms.oms import OMS
from oms.execution import SingleStockExecutionSimulator
from portfolio.portfolio import Portfolio
from portfolio.valuer import MarketValuer

class TradingEnvironment(Environment):
    '''
    An Environment of financial trading
    
    State:
    
    Action:
    
    Reward:
    
    '''


    def __init__(self, **kwargs):
        '''
        kwargs: {
                execution: {single_stock, multi_stocks},
                portfolio: {sharpe, dsharpe, ... ...} 
                valuer: {MarketValuer, SharpeValuer, ...  ... }
                }
        '''
        if (kwargs['execution'] == 'single_stock'):
            self.__executionservice = SingleStockExecutionSimulator(kwargs['sym'], kwargs['start'], kwargs['end'], kwargs['interval'])
            
        if (kwargs['portfolio'] == 'basic'):
            self.__portfolio = Portfolio()
            
        if (kwargs['valuer'] == 'market'):
            self.__portfolio_valuer = MarketValuer()
            
        self.__oms = OMS(self.__executionservice, self.__portfolio)
        
        
    def __str__(self):
        return 'TradingEnvironment'

    def close(self):
        """
        Close environment. No other method calls possible afterwards.
        """
        raise NotImplementedError

    def reset(self):
        """
        Reset environment and setup for new episode.

        :return: initial state
        """
        raise NotImplementedError

    def execute(self, action):
        """
        Executes action, observes next state and reward.

        :param action: Action to execute

        :return: dict containing at least next_state, reward, and terminal_state
        """
        raise NotImplementedError

    @property
    def states(self):
        raise NotImplementedError

    @property
    def actions(self):
        raise NotImplementedError