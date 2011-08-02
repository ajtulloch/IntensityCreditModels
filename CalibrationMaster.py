from CreditDerivativeCSVReader import *
from CDS import *
from DiscountCurve import *
from MarketData import *
from PoissonCalibration import *

#------------------------------------------------------------------------------

class CalibrationMaster(object):
	"""docstring for CalibrationMaster"""
	def __init__(self):
		super(CalibrationMaster, self).__init__()

		
class PoissonCalibrationMaster(CalibrationMaster):
	"""docstring for CalibrationMaster"""
	def __init__(self, CreditDerivativesCSVReader, PoissonCalibration):
		super(CalibrationMaster, self).__init__()
		self.CSVData = CreditDerivativesCSVReader
		self.PoissonCalibration = PoissonCalibration

	def Calibrate(self):
		"""docstring for Calibrate"""
		dates = self.CSVData.Dates()
		results = []
		for date in dates:
			Data = MarketData(self.CSVData.TimeSlice(date))
			self.PoissonCalibration.MarketData = Data
			intensity = self.PoissonCalibration.Calibrate()
			print "Date: %s \tParameters: %s" %(date, intensity)
			results.append((date, intensity) ) 
			
		self.PoissonCalibration.CalibrationResults()
		self.results = results
		return results
		


#------------------------------------------------------------------------------



#------------------------------------------------------------------------------

if __name__ == '__main__':
	# y = HomogenousPoissonCalibrationMaster( 
	# 			CreditDerivativeCSVReader(file = "../Data/CDX.csv"),
	# 			HomogenousPoissonCalibration(),)
	# y.Calibrate()

	# y = PoissonCalibrationMaster( 
	# 			CreditDerivativeCSVReader(file = "../Data/iTraxx.csv"),
	# 			InhomogenousPoissonCalibration())
				
	HP = PoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS				= HPCreditDefaultSwap,
								Process			= "Homogenous Poisson",
								Guess			= [0.01],
								)

	CIR = PoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS 			= CIRCreditDefaultSwap,
								Process			= "CIR",
								Guess			= [0.1, 0.3, 0.2, 0.02],
								)


	IHP = InhomogenousPoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
											)

	GOU = PoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS				= GammaOUCreditDefaultSwap,
								Process			= "Gamma OU",
								Guess			= [0.2, 189, 10000, 0.002],
								)

	IGOU = PoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS 			= IGOUCreditDefaultSwap,
								Process			= "Inverse Gamma OU",
								Guess			= [0.3, 0.8, 5, 0.02],
								)
								
	for Calib in [HP, CIR, IHP, GOU, IGOU]:
		x = PoissonCalibrationMaster( 
							CreditDerivativeCSVReader(file = "../Data/iTraxxAU.csv"),
							Calib,
							)
		x.Calibrate()