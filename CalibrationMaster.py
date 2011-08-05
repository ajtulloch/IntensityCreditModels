from CreditDerivativeCSVReader import *
from CDS import *
from DiscountCurve import *
from MarketData import *
from Calibration import *

#------------------------------------------------------------------------------
		
class CalibrationMaster(object):
	"""docstring for CalibrationMaster"""
	def __init__(self, CreditDerivativesCSVReader, Calibration):
		super(CalibrationMaster, self).__init__()
		self.CSVData = CreditDerivativesCSVReader
		self.Calibration = Calibration

	def Calibrate(self, debug = 1, N = False, dynamic = True):
		"""docstring for Calibrate"""
		dates = self.CSVData.Dates()
		
		if N != False:
			# Get the last N dates
			dates = dates[-N:]
		
		
		results = []
		for date in dates:
			Data = MarketData(self.CSVData.TimeSlice(date))
			self.Calibration.MarketData = Data
			try:
				intensity = self.Calibration.Calibrate()
				RMSE = self.Calibration.RMSE()
				if debug == 1:
					print "Date: %s \tParameters: %s" %(date, intensity)
				results.append((date, intensity, RMSE) ) 
				if dynamic == True:
					self.Calibration.Guess = intensity
			except:
				pass
		if debug == 1:
			self.Calibration.CalibrationResults()
		self.results = results
		return results
	
	def FormatResults(self, results):
		"""docstring for FormatResults"""
		parameter_length = len(results[0][1]) 
		# Number of parameters in output
		output = []
		dates = [row[0] for row in results]
		output.append(dates)
		for parameter in range(parameter_length):
			parameter_values = [row[1][parameter] for row in results] 
			output.append(parameter_values)
		RMSEs = [row[2] for row in results]
		output.append(RMSEs)
		return output

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------

if __name__ == '__main__':
	# y = HomogenousCalibrationMaster( 
	# 			CreditDerivativeCSVReader(file = "../Data/CDX.csv"),
	# 			HomogenousCalibration(),)
	# y.Calibrate()

	# y = CalibrationMaster( 
	# 			CreditDerivativeCSVReader(file = "../Data/iTraxx.csv"),
	# 			InhomogenousCalibration())
				
	HP = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS				= HPCreditDefaultSwap,
								Process			= "Homogenous Poisson",
								Guess			= [0.01],
								)

	CIR = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS 			= CIRCreditDefaultSwap,
								Process			= "CIR",
								Guess			= [0.1, 0.3, 0.2, 0.02],
								)


	IHP = InhomogenousCalibration( \
								DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								)

	GOU = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS				= GammaOUCreditDefaultSwap,
								Process			= "Gamma OU",
								Guess			= [0.2, 189, 10000, 0.002],
								)

	IGOU = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS 			= IGOUCreditDefaultSwap,
								Process			= "Inverse Gamma OU",
								Guess			= [0.3, 0.8, 5, 0.02],
								)
								
	for Calib in [HP, IHP, CIR, GOU, IGOU]:
		x = CalibrationMaster( 
							CreditDerivativeCSVReader(file = "../Data/CDX.csv"),
							Calib,
							)
		print Calib.Process
		results =  x.Calibrate(debug = 1, N = 2)
		print x.FormatResults(results)
		print 
		