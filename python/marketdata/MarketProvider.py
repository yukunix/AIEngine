
from abc import ABCMeta, abstractmethod

class MarketProvider(object, , metaclass=ABCMeta):

	@abstractmethod
    def next(self):
        pass
		
	def getSeries(self, size):
		pass
		
		