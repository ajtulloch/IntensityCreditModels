import unittest

#------------------------------------------------------------------------------

import MarketData

#------------------------------------------------------------------------------

class CDSTests(unittest.TestCase):
	pass
	
#------------------------------------------------------------------------------

class CalibrationTests(unittest.TestCase):
	pass
	
#------------------------------------------------------------------------------
		
class CalibrationMaster(unittest.TestCase):
	pass
	
#------------------------------------------------------------------------------

class CreditDerivateCSVReaderTests(unittest.TestCase):
	pass
	
#------------------------------------------------------------------------------

class MarketDataTests(unittest.TestCase):
	def setUp(self):
		spreads = {'Date' : '17/5/10', '1' : '200', '2' : '250' }
		self.mkt_data = MarketData.MarketData(spreads)

	def tearDown(self):
		pass

	def testDate(self):
		date = self.mkt_data.Date()
		self.assertEqual(date, '17/5/10')
		
	def testTenors(self):
		tenors = self.mkt_data.Tenors()
		self.assertEqual(tenors, [1, 2])
		
	def testData(self):
		data = self.mkt_data.Data()
		self.assertEqual(data, [(1, 200), (2, 250)])
		
#------------------------------------------------------------------------------

if __name__ == "__main__":
	unittest.main()