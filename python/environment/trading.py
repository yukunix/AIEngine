'''
Created on 20 May 2017

@author: Yukun
'''

from tensorforce.environments import Environment
from oms.oms import OMS
from oms.execution import SingleStockExecutionSimulator
from portfolio.portfolio import Portfolio
from portfolio.valuer import MarketValuer
from marketdata.provider import MarketDataProvider
from portfolio.order import Side

class TradingEnvironment(Environment):
    '''
    A simple environment of financial trading
    
    State: float list (last 5 close prices, SMA10, position value, cash value)
    
    Action: (1, 0, -1) as BUY, HOLD, SELL
    
    Reward: return of total value (position value + cash value)
    '''

    def __init__(self, **kwargs):
        '''
        kwargs: {
                execution: {single_stock, multi_stocks},
                portfolio: {sharpe, dsharpe, ... ...} 
                valuer: {MarketValuer, SharpeValuer, ...  ... }
                }
        '''
        
        ### common variables
        self.__sym = kwargs['sym']
        self.__start = kwargs['start']
        self.__end = kwargs['end']
        
        ### market data providers
        self.__provider = MarketDataProvider('quandl', self.__sym, self.__start, self.__end)
        self.__OHLCV = self.__provider.getMarketData('OHLCV')
        self.__sma10 = self.__provider.getMarketData('close_sma', period=1)
        
        if (kwargs['execution'] == 'single_stock'):
            self.__executionservice = SingleStockExecutionSimulator(self.__sym, self.__start, self.__end, self.__OHLCV)

        self.__initial_value = 100000
        self.__current_value = self.__initial_value            
        if (kwargs['portfolio'] == 'basic'):
            self.__portfolio = Portfolio(self.__current_value)
            
        if (kwargs['valuer'] == 'market'):
            self.__portfolio_valuer = MarketValuer()
            
        self.__oms = OMS(self.__executionservice, self.__portfolio, self.__portfolio_valuer)
        
        
        
    @property
    def states(self):
        """
        Return the state space. Might include subdicts if multiple states are available simultaneously.
        Returns: dict of state properties (shape and type). 
        """
        return {'type': 'float', 'shape': (8, )}

    @property
    def actions(self):
        """
        Return the action space. Might include subdicts if multiple actions are available simultaneously.

        Returns: dict of action properties (continuous, number of actions)

        """
        return {'num_actions': 3, 'continuous': False}
    
    def execute(self, action):
        """
        Executes action, observes next state and reward.

        Args:
            action: Action to execute.
            1 - BUY, 0 - HOLD, -1 - SELL

        Returns: tuple of state (tuple), reward (float), and terminal_state (bool).
        """
        
        if (action[0] > 0):
            self.__oms.placeMarket(self.sym, 1, self.__portfolio.cash_value())
        elif (action[0] < 0):
            self.__oms.placeMarket(self.sym, -1, self.__portfolio.position_value(self.sym))
        else:
            self.__oms.no_operation(self.sym)

        ### time rolls to next period, e.g. next day, then place order
        self.__OHLCV.next()
        self.__sma10.next()
        
        _, _, _, self.current_price, _ = self.__OHLCV.current()
        
        self.position_value = self.__portfolio.position(self.__sym) * self.current_price
        self.market_value = self.position_value + self.__portfolio.cash
        self.reward = (self.market_value - self.__current_value) / self.__current_value
        self.__current_value = self.market_value
        
        self.terminate = False
        if (self.market_value < self.__initial_value * 0.8):
            self.terminate = True
            
        return (self.current_price, self.__sma10.current, self.position_value, self.__portfolio.cash, 
                self.reward, self.terminate) 
    
    def reset(self):
        """
        Reset environment and setup for new episode.

        Returns: initial state of resetted environment.
        """
        pass

    def close(self):
        """
        Close environment. No other method calls possible afterwards.
        """
        pass

    def __str__(self):
        return 'TradingEnvironment'
    