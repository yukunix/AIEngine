'''
Created on 20 May 2017

@author: Yukun
'''

from tensorforce.environments import Environment
from oms.oms import OMS
from oms.execution import ExecutionService, SingleStockExecutionSimulator
from portfolio.portfolio import Portfolio, SharpePortfolio

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
                }
        '''
        if (kwargs['execution'] == 'single_stock'):
            self.executionservice = SingleStockExecutionSimulator(kwargs['sym'], kwargs['start'], kwargs['end'], kwargs['interval'])
            
        if (kwargs['portfolio'] == 'sharpe'):
            self.portfolio = SharpePortfolio()
            
        self.oms = OMS(self.executionservice, self.portfolio)
        
        
    def __str__(self):
        return 'TradingEnvironment'

    def reset(self):
        """
        Reset environment and setup for new episode.

        :return: initial state
        """
        raise NotImplementedError

    def close(self):
        """
        Close environment. No other method calls possible afterwards.
        """
        raise NotImplementedError

    def execute_action(self, action):
        """
        Executes action, observes next state and reward.

        :param action: Action to execute

        :return: dict containing at least next_state, reward, and terminal_state
        """
        raise NotImplementedError   