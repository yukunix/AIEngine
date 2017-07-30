'''
Created on 30 Jul 2017

@author: Yukun
'''

import unittest
from environment.trading import TradingEnvironment

class TestEnvironment(unittest.TestCase):

    def test_test(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def setUp(self):
        self.kwargs = {'execution':'single_stock',
                  'sym':'AAPL', 'start':'2015-01-01', 'end':'2017-06-30',
                  'portfolio':'basic', 
                  'valuer':'market'}
        self.simpleTradingEnvironment = TradingEnvironment(**self.kwargs)       
        
    def test_states(self):
        states = self.simpleTradingEnvironment.states
        self.assertDictEqual({'type': 'float', 'shape': (8, )}, states, "unexpected states") 

    def test_actions(self):
        actions = self.simpleTradingEnvironment.actions
        self.assertDictEqual({'num_actions': 3, 'continuous': False}, actions, "unexpected actions") 

    def test_execute(self):
        pass

    def test_reset(self):
        pass
        
    def test_close(self):
        pass
        
if __name__ == '__main__':
    unittest.main()