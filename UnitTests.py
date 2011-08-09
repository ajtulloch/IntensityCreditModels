import unittest

#------------------------------------------------------------------------------

import MarketData
import DiscountCurve
import CreditDerivativeCSVReader
import Calibration
import CDS
import CalibrationMaster

#------------------------------------------------------------------------------

class CDSTests(unittest.TestCase):
	def setUp(self):
		"""docstring for setUP"""
		self.HP = CDS.HPCreditDefaultSwap(
					DiscountCurve = DiscountCurve.FlatDiscountCurve(r = 0.00), 
					maturity = 2,
					)
		# print y.ParSpread(0.018)
					
		self.IHP = CDS.IHPCreditDefaultSwap(
					DiscountCurve = DiscountCurve.FlatDiscountCurve(r = 0.00),  
					maturity = 2,
					tenors = [1,2,3,5,7,10],  
					)		
		# print z.ParSpread([0.018, 0.018, 0.018, 0.018, 0.1, 0.2])
					
		self.GOU = CDS.GammaOUCreditDefaultSwap( 	
					DiscountCurve = DiscountCurve.FlatDiscountCurve(r = 0.00),  
					maturity = 2,
					)
		# print y.ParSpread([ 0.2, 189, 10000, 0.002])
			
		self.IGOU = CDS.IGOUCreditDefaultSwap(
					DiscountCurve = DiscountCurve.FlatDiscountCurve(r = 0.00),  
					maturity = 2,
					)
		# print y.ParSpread([ 0.3, 0.8, 5, 0.02])
				
		self.CIR = CDS.CIRCreditDefaultSwap(
					DiscountCurve = DiscountCurve.FlatDiscountCurve(r = 0.00),  
					maturity = 2,
					)

		# print y.ParSpread([ 0.1, 0.3, 0.2, 0.02])
		
	def testCDSSpread(self):
		HP = self.HP.ParSpread(0.018)
		IHP = self.IHP.ParSpread([0.018, 0.018, 0.018, 0.018, 0.1, 0.2])
		GOU = self.GOU.ParSpread([0.2, 189, 10000, 0.002])
		IGOU = self.IGOU.ParSpread([0.3, 0.8, 5, 0.02])
		CIR = self.CIR.ParSpread([0.1, 0.3, 0.2, 0.02])
		
		self.assertEqual(round(HP, 1), 108.0)
		self.assertEqual(round(IHP, 1), round(108.2433, 1))
		self.assertEqual(round(GOU, 1), round(43.735, 1))
		self.assertEqual(round(IGOU, 1), round(463.863956231, 1))
		self.assertEqual(round(CIR, 1), round(173.527, 1))
		
	
#------------------------------------------------------------------------------

class CalibrationTests(unittest.TestCase):
	def setUp(self):
		"""docstring for setUp"""
		CSV = CreditDerivativeCSVReader.CreditDerivativeCSVReader( file = "../Data/CDX.csv")
		date = CSV.Dates()[-1]
		data = CSV.TimeSlice(date)
		z = MarketData.MarketData(data)
		
		self.HP = Calibration.Calibration(	
				DiscountCurve 	= DiscountCurve.FlatDiscountCurve(r = 0.00), 
				MarketData 		= z,
				CDS				= CDS.HPCreditDefaultSwap,
				Process			= "HP",
				Guess			= [0.01],
				)
														
		self.IHP = Calibration.InhomogenousCalibration( \
				DiscountCurve 	= DiscountCurve.FlatDiscountCurve(r = 0.00), 
				MarketData 		= z,
				)
							
	def testCalibrate(self):
		"""docstring for fname"""
		HP_calib = self.HP.Calibrate()
		IHP_calib = self.IHP.Calibrate()
		
		self.assertEqual(round(HP_calib[0], 4), round(0.01240234, 4))
		self.assertEqual(round(IHP_calib[0], 4), round(0.00487254926212, 4))
		
		# self.assertEqual(self.IHP.Calibrate(), [ 0.01240234])
		
	
#------------------------------------------------------------------------------


class CalibrationMaster(unittest.TestCase):
	
	def setUp(self):
		"""docstring for setUP"""
		import CalibrationMaster
		import Calibration
		
		HP = Calibration.Calibration(	
					DiscountCurve 	= DiscountCurve.FlatDiscountCurve(r = 0.00), 
					CDS				= CDS.HPCreditDefaultSwap,
					Process			= "HP",
					Guess			= [0.01],
					)
		
		self.CalibrationMaster = CalibrationMaster.CalibrationMaster( 
				CreditDerivativeCSVReader.CreditDerivativeCSVReader(file = "../Data/CDX.csv"),
				HP,
				)
				
		# results =  x.Calibrate(debug = 1, N = 2)
		# print x.FormatResults(results)

	def testCalibrate(self):
		"""docstring for testCalibrate"""
		calibration_results = self.CalibrationMaster.Calibrate(N = 2, debug = 0)
				
		self.assertEqual(calibration_results[0][0], '16/03/11')
		self.assertEqual(calibration_results[1][0], '17/03/11')
		self.assertEqual(round(calibration_results[0][2], 4), \
							round(33.686874479088694, 4))
		self.assertEqual(calibration_results[1][0], '17/03/11')
		
		
		# self.assertEqual( self.CalibrationMaster,)
		

	
#------------------------------------------------------------------------------

class CreditDerivateCSVReaderTests(unittest.TestCase):
	def setUp(self):
		"""docstring for setUp"""
		self.CSVReader = CreditDerivativeCSVReader.CreditDerivativeCSVReader( \
		 					"../Data/CDX.csv" )
	
	def tearDown(self):
		"""docstring for tearDown"""
		self.CSVReader = None
	
	def testDates(self):
		"""docstring for testDates"""
		dates = self.CSVReader.Dates()
		self.assertTrue('17/03/11' in dates)
		self.assertTrue('17/3/11' not in dates)
		
	def testTimeSlice(self):
		"""docstring for test"""
		date = '17/03/11'
		time_slice = self.CSVReader.TimeSlice(date)
		
		self.assertTrue(type(time_slice) == type(dict()))
		self.assertTrue(time_slice['Date'] == date)
	
	def testBadTime(self):
		"""docstring for testBadTime"""
		bad_date = '17/3/11'
		
		self.assertRaises(Exception, self.CSVReader.TimeSlice, bad_date)
					
	
	
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