'''
Created on 4 May 2017

@author: Yukun
'''

from abc import ABCMeta, abstractmethod

class Environment(object, metaclass=ABCMeta):
    '''
    Environment for agent to observe and execute actions, then receive next state and reward
    '''
    
    @property
    @abstractmethod
    def state_dim(self):
        pass
        
    @property
    @abstractmethod
    def action_dim(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def render(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def step(self, action):
        pass