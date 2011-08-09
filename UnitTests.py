import unittest

#------------------------------------------------------------------------------

import MarketData
import DiscountCurve

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
		self.mkt_data = None

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

class FlatDiscountCurveTests(unittest.TestCase):
	def setUp(self):
		self.r = 0.05
		self.DiscountCurve = DiscountCurve.FlatDiscountCurve(r = self.r)

	def tearDown(self):
		self.mkt_data = None

	def testDF(self):
		t1, t2 = 3.0, 5.0
		df_value = self.DiscountCurve.DF(t1, t2)
		df_test = (1 / (1 + self.r)) ** (t2 - t1)
		self.assertEqual(df_value, df_test)
		
		
#------------------------------------------------------------------------------

if __name__ == "__main__":
	unittest.main()