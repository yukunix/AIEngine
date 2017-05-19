'''
Created on 20 May 2017

@author: Yukun
'''

from tensorforce.environments import Environment

class TradingEnvironment(Environment):
    '''
    An Environment of financial trading
    
    State:
    
    Action:
    
    Reward:
    
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
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