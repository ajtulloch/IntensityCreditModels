from CreditDerivativeCSVReader import *

class MarketData(object):
	"""docstring for MarketData"""
	def __init__(self, data):
		super(MarketData, self).__init__()
		self.data = data
		
	def __repr__(self):
		string = "#" * 20
		string += "\nDate: \t %s\n" % self.Date()
		for tenor, value in sorted(self.Data()):
			string += "Tenor: %.1f\tSpread: %.0f \n" %(tenor, value)
		string += "#" * 20
		
		return string	
	def Tenors(self):
		"""docstring for Tenors"""
		
		tenors = [float(key) for key in self.data.iterkeys() if len(key) is not 4]
		return tenors
		
	def Date(self):
		"""docstring for Data"""
		return self.data[ "Date" ]
		
	def Data(self):
		"""docstring for Data"""
		
		return [ (float(k),float(v) ) for k,v in self.data.iteritems() if len(k) is not 4]
		
	
