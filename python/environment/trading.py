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

        Returns: initial state of resetted environment.
        """
        raise NotImplementedError

    def execute(self, action):
        """
        Executes action, observes next state and reward.

        Args:
            action: Action to execute.

        Returns: tuple of state (tuple), reward (float), and terminal_state (bool).
        """
        raise NotImplementedError

    @property
    def states(self):
        """
        Return the state space. Might include subdicts if multiple states are available simultaneously.

        Returns: dict of state properties (shape and type).

        """
        raise NotImplementedError

    @property
    def actions(self):
        """
        Return the action space. Might include subdicts if multiple actions are available simultaneously.

        Returns: dict of action properties (continuous, number of actions)

        """
        raise NotImplementedError