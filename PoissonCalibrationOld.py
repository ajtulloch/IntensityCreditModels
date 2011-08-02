from scipy.optimize import fmin as optimise
from CreditDerivativeCSVReader import *
from CDS import *
from DiscountCurve import *
from MarketData import *
from math import sqrt
# from scipy import memoize


class PoissonCalibration(object):
	"""docstring for PoissonCalibration"""
	def __init__(self, DiscountCurve, MarketData):
		super(PoissonCalibration, self).__init__()
		self.DiscountCurve = DiscountCurve
		self.MarketData = MarketData
		self.R = 0.4
		if MarketData is not None:
			self.t0 = MarketData.Date() 
			self.DiscountCurve.Initialise(self.t0)
	
	def Calibrate(self):
		"""docstring for Calibrate"""
		abstract
		
	def CalibrationResults(self):
		"""docstring for CalibrationResults"""
		pass
		
#------------------------------------------------------------------------------

class HomogenousPoissonCalibration(PoissonCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, DiscountCurve = FlatDiscountCurve( r = 0 ), MarketData = None):
		super(HomogenousPoissonCalibration, self).__init__(DiscountCurve, MarketData)
		self.Guess = [ 0.01 ]
		
	def ObjectiveFunction(self, gamma):
		"""docstring for Calibration"""
	
		sum = 0
		for t, market_spread in self.MarketData.Data():
			CDS = HPCreditDefaultSwap(	DiscountCurve = self.DiscountCurve,
			 							maturity = t)
			model_spread = CDS.ParSpread(gamma)		
			# print "t: %s\t Market Spread: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2
		return sum
	
	def Calibrate(self):
		"""docstring for Calibrate"""
		output = optimise(	self.ObjectiveFunction, 
							self.Guess, 
							disp=0
							)
		self.calibrated_gamma = output
		return output
		
	def CalibrationResults(self):
		"""docstring for CalibrationError"""	
		print "-" * 80
		print "Calibration results for Homogenous Poisson on %s" %(self.MarketData.Date())
		print ""
		N = len(self.MarketData.Tenors())
		sum = 0
		for t, market_spread in self.MarketData.Data():
			CDS = HPCreditDefaultSwap(	DiscountCurve = self.DiscountCurve, 
										maturity = t
										)
			model_spread = CDS.ParSpread(self.calibrated_gamma)		
			print "Tenor: %s\t Market: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2
		
		RMSE = sqrt(sum/N)
		print "RMSE: ", RMSE
		return None

#------------------------------------------------------------------------------

class InhomogenousPoissonCalibration(PoissonCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, DiscountCurve = FlatDiscountCurve( r = 0 ), MarketData = None):
		super(InhomogenousPoissonCalibration, self).__init__(DiscountCurve, MarketData)
		if MarketData is not None:
			self.tenors = MarketData.Tenors()
			self.N = len(MarketData.Tenors())
			self.Guess = [ 0.01 ] * self.N
		
	def ObjectiveFunction(self, gamma):
		"""docstring for Calibration"""
		sum = 0
		for t, market_spread in self.MarketData.Data():
			CDS = IHPCreditDefaultSwap(	tenors = sorted(self.MarketData.Tenors()), 
										DiscountCurve = self.DiscountCurve,
			 							maturity = t)
			model_spread = CDS.ParSpread(gamma)		
			# print "t: %s\t Market Spread: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2
		return sum
	
	def Calibrate(self):
		"""docstring for Calibrate"""
		N = len(self.MarketData.Tenors())
		self.Guess = [0.01] * N
		output = optimise(	self.ObjectiveFunction, 
							self.Guess, 
							disp=0
							)
		self.calibrated_gamma = output
		return output
		
	def CalibrationResults(self):
		"""docstring for CalibrationError"""
		print "-" * 80
		print "Calibration results for Inhomogenous Poisson on %s" %(self.MarketData.Date())
		print ""
		N = len(self.MarketData.Tenors())
		sum = 0
		for t, market_spread in sorted(self.MarketData.Data()):
			CDS = IHPCreditDefaultSwap(	tenors = sorted(self.MarketData.Tenors()), 
										DiscountCurve = self.DiscountCurve, 
										maturity = t
										)
			model_spread = CDS.ParSpread(self.calibrated_gamma)	
			index = sorted(self.MarketData.Tenors()).index(t)
			gamma = self.calibrated_gamma[index]
			probability = CDS.SurvivalProbability( self.calibrated_gamma, t)*100
			print "Tenor: %s\t Market: %.0f\t Model Spread: %.0f\t Gamma: %.5f\t Survival Probability: %.1f" %(t, market_spread, model_spread, gamma, probability)
			# print "%.0f\t& %.0f\t & %.0f\t & %.5f\t & %.1f " %(t, market_spread, model_spread, gamma, probability)	
			# print "\hline"	
			sum += (model_spread - market_spread) ** 2
		
		RMSE = sqrt(sum/N)
		print "RMSE: ", RMSE
		return None

#------------------------------------------------------------------------------

class CIRCalibration(PoissonCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, DiscountCurve = FlatDiscountCurve( r = 0 ), MarketData = None):
		super(CIRCalibration, self).__init__(DiscountCurve, MarketData)
		self.Guess = [ 0.1, 0.3, 0.2, 0.02 ]
		
	def ObjectiveFunction(self, gamma):
		"""docstring for Calibration"""
		sum = 0
		for t, market_spread in self.MarketData.Data():
			CDS = CIRCreditDefaultSwap(	DiscountCurve = self.DiscountCurve,
			 							maturity = t)
			model_spread = CDS.ParSpread(gamma)		
			# print "t: %s\t Market Spread: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2
		return sum
	
	def Calibrate(self):
		"""docstring for Calibrate"""
		output = optimise(	self.ObjectiveFunction, 
							self.Guess, 
							disp=0
							)
		self.calibrated_gamma = output
		return output
		
	def CalibrationResults(self):
		"""docstring for CalibrationError"""
		print "-" * 80
		print "Calibration results for CIR on %s" %(self.MarketData.Date())
		print ""		
		N = len(self.MarketData.Tenors())
		sum = 0
		for t, market_spread in sorted(self.MarketData.Data()):
			CDS = CIRCreditDefaultSwap(	DiscountCurve = self.DiscountCurve, 
										maturity = t
										)
			model_spread = CDS.ParSpread(self.calibrated_gamma)	
			probability = CDS.SurvivalProbability(self.calibrated_gamma, t) * 100
			print "Tenor: %s\t Market: %.0f\t Model Spread: %.0f\t Survival Probability: %.1f" %(t, market_spread, model_spread, probability)
			sum += (model_spread - market_spread) ** 2
		
		RMSE = sqrt(sum/N)
		print "RMSE: ", RMSE
		return None

#------------------------------------------------------------------------------

class GammaOUCalibration(PoissonCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, DiscountCurve = FlatDiscountCurve( r = 0 ), MarketData = None):
		super(GammaOUCalibration, self).__init__(DiscountCurve, MarketData)
		self.Guess = [ 0.2, 189, 10000, 0.002 ]

	def ObjectiveFunction(self, gamma):
		"""docstring for Calibration"""
		sum = 0
		for t, market_spread in self.MarketData.Data():
			CDS = GammaOUCreditDefaultSwap(	DiscountCurve = self.DiscountCurve,
			 							maturity = t)
			model_spread = CDS.ParSpread(gamma)		
			# print "t: %s\t Market Spread: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2
		return sum

	def Calibrate(self):
		"""docstring for Calibrate"""
		output = optimise(	self.ObjectiveFunction, 
							self.Guess, 
							disp=0
							)
		self.calibrated_gamma = output
		# print output
		return output

	def CalibrationResults(self):
		"""docstring for CalibrationError"""
		print "-" * 80
		print "Calibration results for Gamma OU on %s" %(self.MarketData.Date())
		print ""
		
		N = len(self.MarketData.Tenors())
		sum = 0
		for t, market_spread in sorted(self.MarketData.Data()):
			CDS = GammaOUCreditDefaultSwap(	DiscountCurve = self.DiscountCurve, 
										maturity = t
										)
			model_spread = CDS.ParSpread(self.calibrated_gamma)		
			probability = CDS.SurvivalProbability(self.calibrated_gamma, t) * 100
			print "Tenor: %s\t Market: %.0f\t Model Spread: %.0f\t Survival Probability: %.1f" %(t, market_spread, model_spread, probability)
			sum += (model_spread - market_spread) ** 2

		RMSE = sqrt(sum/N)
		print "RMSE: ", RMSE
		return None

#------------------------------------------------------------------------------

class IGOUCalibration(PoissonCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, DiscountCurve = FlatDiscountCurve( r = 0 ), MarketData = None):
		super(IGOUCalibration, self).__init__(DiscountCurve, MarketData)
		self.Guess = [ 0.3, 0.8, 5, 0.02 ]

	def ObjectiveFunction(self, gamma):
		"""docstring for Calibration"""
		sum = 0
		for t, market_spread in self.MarketData.Data():
			CDS = IGOUCreditDefaultSwap(	DiscountCurve = self.DiscountCurve,
			 							maturity = t)
			model_spread = CDS.ParSpread(gamma)		
			# print "t: %s\t Market Spread: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2
		return sum

	def Calibrate(self):
		"""docstring for Calibrate"""
		output = optimise(	self.ObjectiveFunction, 
							self.Guess, 
							disp=0
							)
		self.calibrated_gamma = output
		# print output
		return output

	def CalibrationResults(self):
		"""docstring for CalibrationError"""
		print "-" * 80
		print "Calibration results for Inverse Gamma OU on %s" %(self.MarketData.Date())
		print ""
		N = len(self.MarketData.Tenors())
		sum = 0
		for t, market_spread in sorted(self.MarketData.Data()):
			CDS = IGOUCreditDefaultSwap(	DiscountCurve = self.DiscountCurve, 
										maturity = t
										)
			model_spread = CDS.ParSpread(self.calibrated_gamma)		
			probability = CDS.SurvivalProbability(self.calibrated_gamma, t) * 100
			print "Tenor: %s\t Market: %.0f\t Model Spread: %.0f\t Survival Probability: %.1f" %(t, market_spread, model_spread, probability)
			# print "Tenor: %s\t Market: %s\t Model Spread: %s\t" %(t, market_spread, model_spread)	
			sum += (model_spread - market_spread) ** 2

		RMSE = sqrt(sum/N)
		print "RMSE: ", RMSE
		return None

#------------------------------------------------------------------------------

if __name__ == '__main__':	
	y = CreditDerivativeCSVReader( file = "../Data/CDX.csv")
	date = y.Dates()[-1]
	data = y.TimeSlice(date)
	z = MarketData(data)
	# print z.Data()
	# print z.Date()
	
	HP = HomogenousPoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
										MarketData 		= z
										)

	CIR = CIRCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
							MarketData 		= z
							)
										
										
	IHP = InhomogenousPoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
											MarketData 		= z
											)

	GOU = GammaOUCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								MarketData 		= z
								)
						
	IGOU = IGOUCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
							MarketData 		= z
							)
	
	for CDS in [HP, IHP, GOU, IGOU, CIR]:
		CDS.Calibrate()
		CDS.CalibrationResults()
		
		