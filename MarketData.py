from CreditDerivativeCSVReader import *

#------------------------------------------------------------------------------

class MarketData(object):
	"""Provides an interface to credit spread data.  
	
	Provides various methods to obtain views on the underlying spreads.
	
	Initialised by passing a dictionary containing Date and Tenor fields, for 
	example: 
	
	>>> spreads = {'Date' : '17/5/10', '1' : '200', '2' : '250' }
	>>> data = MarketData(spreads)
	"""
	def __init__(self, data):
		super(MarketData, self).__init__()
		self.data = data
		
	def __repr__(self):
		"""Used when the print() method is called on a MarketData object."""
		string = "#" * 20
		string += "\nDate:\t%s\n" % self.Date()
		for tenor, value in sorted(self.Data()):
			string += "Tenor:\t%.1f\tSpread: %.0f \n" %(tenor, value)
		string += "#" * 20
		
		return string
			
	def Tenors(self):
		"""Returns a list of tenors."""
		
		tenors = [float(key) for key in self.data.iterkeys() \
					if len(key) is not 4]
		return tenors
		
	def Date(self):
		"""Returns the associated date for the MarketData"""
		return self.data[ "Date" ]
		
	def Data(self):
		"""Returns a list of tuples, representing the (tenor, spread) pairs 
		contained in the market data."""
		
		return [ (float(k),float(v) ) for k,v in self.data.iteritems() \
		 			if len(k) is not 4]
		
#------------------------------------------------------------------------------

if __name__ == '__main__':
	spreads = {'Date' : '17/5/10', '1' : '200', '2' : '250' }
	data = MarketData(spreads)
	print data
