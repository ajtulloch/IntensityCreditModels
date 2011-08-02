

import math
import scipy.integrate as integrate
import scipy.optimize as optimize
import numpy
import doctest




# -------------------------------------------------------------------

class CDSCalibration(object):
	"""docstring for CDSCalibration"""
	def __init__(self, yield_curve, market):
		super(CDSCalibration, self).__init__()
		self.yield_curve = yield_curve
		self.R = 0.4
		self.LGD = 1 - self.R
		self.T = numpy.arange(0, 10.25, 0.25)
		self.market = market
		self.model = {}
		
		
		
	def DF(self, t):
		"""docstring for DiscountFactor"""
		# DF = self.yield_curve[t]
		# return DF
		return 0.99
		
	def Gamma(self):
		"""docstring for Gamma"""
		pass
	
	def Calibrate(self):
		"""docstring for Calibrate"""
		pass
		
	def LGD(self):
		"""docstring for LGD"""
		return self.LGD

# -------------------------------------------------------------------

class HomogenousPoissonCalibration(CDSCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, yield_curve, market):
		super(HomogenousPoissonCalibration, self).__init__(yield_curve, market)
		self.gamma = 0.03
		self.Calibrate()
		
	def Gamma(self, gamma, t):
		"""docstring for Gamma"""
		return gamma * t

	def CDSValue(self, gamma, T):
		"""docstring for fname"""
	
		def RecoveryIntegral(t_old, t_new):
			"""docstring for Recovery Integral"""
			def f(x):
				return math.exp( -self.Gamma(gamma, t_old) - gamma * (x - t_old) ) * self.DF(x) * (x - t_old)
		
			i = gamma * integrate.quad( f, t_old, t_new )[0]
			return i
			
		def LossIntegral(t_old, t_new):
			"""docstring for Loss Integral"""
			def f(x):
				return math.exp( -self.Gamma(gamma, t_old) - gamma * (x - t_old) ) * self.DF(x)
			
			i = gamma * integrate.quad( f, t_old, t_new)[0]
			return i
		
		def RecoveryPV(t_old, t_new):
			"""docstring for RecoveryPV"""
			v = self.DF(t_new) * (t_new - t_old) * math.exp( self.Gamma(gamma, t_new) )
			return v
		
		def Value():
			"""docstring for Value"""
			v = 0
			for i in range( len(T) - 1 ):
				t_old = self.T[i]
				t_new = self.T[i+1]
				v += self.R * RecoveryIntegral(t_old, t_new)
				v += self.R * RecoveryPV(t_old, t_new)	
				v += self.LGD * LossIntegral(t_old, t_new)		
	
			return v
	
		v = Value()
		
		# print "CDS Value: %(cds)s \t\tGamma: %(gamma)s" % { "cds": v,  "gamma": gamma}
		return v
		
	def Calibrate(self):
		"""docstring for Calibrate"""	
		def CalibError(tenor, gamma):
			"""docstring for CalibError"""
			market_v = self.market[ tenor ]
			expiry = int( tenor * 4 + 1)
			model_v = self.CDSValue(gamma, self.T[:expiry])
			
			self.model[ tenor ] = model_v
			return model_v - market_v
			
		def ObjectiveFunction(gamma):
			"""docstring for ObjectiveFunction"""
			gamma = gamma[0]
			errors = 0
			for t in self.market:
				errors += CalibError(t, gamma) ** 2
				
			return math.sqrt( errors/len(self.market) )

		print "Optimizing..."
		g = optimize.fmin( ObjectiveFunction, [ self.gamma ] )[0]
		print g
		self.calib_gamma = g
		return g
	
	
# -------------------------------------------------------------------

class InhomogenousPoissonCalibration(CDSCalibration):
	"""docstring for HomogenousPoissonCalibration"""
	def __init__(self, yield_curve, market):
		super(InhomogenousPoissonCalibration, self).__init__(yield_curve, market)
		self.gamma_list = [ 0.03 ] * len(market)
		self.Calibrate()
		
	def Gamma(self, gamma, t):
		"""docstring for Gamma"""
		val = 0
		t_old = 0
		for k, v in gamma.iteritems():
			t_new = k
			if t_new < t:
				val += v * (t_new - t_old)
			else: 
				val += v * ( t - t_old )
				break
		
		return val
	
	def gamma(self, gamma, t):
		"""	>>> market1 = { 1 : 1.925, 	3 : 2.15, 	5 : 2.25, 	7 : 2.35, 	10 : 2.35	}
			>>> X = InhomogenousPoissonCalibration( market = market1, yield_curve = "a" )
			>>> g = { 1 : 0.5, 3 : 0.9, 5 : 1.3 }
			>>> X.gamma( g, 0.9 )
			0.5
			>>> X.gamma( g, 4 )
			1.3
		"""
		val = 0
		for k, v in gamma.iteritems():
			if t > k:
				pass
			else:
				val = v
				break
		return val 		

	def CDSValue(self, gamma, T):
		"""docstring for fname"""
	
		def RecoveryIntegral(t_old, t_new):
			"""docstring for Recovery Integral"""
			def f(x):
				return math.exp( -self.Gamma(gamma, t_old) - self.gamma(gamma, t_new) * (x - t_old) ) * self.DF(x) * (x - t_old)
		
			i = self.gamma(gamma, t_new) * integrate.quad( f, t_old, t_new )[0]
			return i
			
		def LossIntegral(t_old, t_new):
			"""docstring for Loss Integral"""
			def f(x):
				return math.exp( -self.Gamma(gamma, t_old) - self.gamma(gamma, t_new) * (x - t_old) ) * self.DF(x)
			
			i = self.gamma(gamma, t_new) * integrate.quad( f, t_old, t_new)[0]
			return i
		
		def RecoveryPV(t_old, t_new):
			"""docstring for RecoveryPV"""
			v = self.DF(t_new) * (t_new - t_old) * math.exp( self.Gamma(gamma, t_new) )
			return v
		
		def Value():
			"""docstring for Value"""
			v = 0
			for i in range( len(T) - 1 ):
				t_old = self.T[i]
				t_new = self.T[i+1]
				v += self.R * RecoveryIntegral(t_old, t_new)
				v += self.R * RecoveryPV(t_old, t_new)	
				v += self.LGD * LossIntegral(t_old, t_new)		
	
			return v
	
		v = Value()
		
		# print "CDS Value: %(cds)s \t\tGamma: %(gamma)s" % { "cds": v,  "gamma": gamma}
		return v
		
	def Calibrate(self):
		"""docstring for Calibrate"""	
		def CalibError(tenor, gamma):
			"""docstring for CalibError"""
			market_v = self.market[ tenor ]
			expiry = int( tenor * 4 + 1)
			model_v = self.CDSValue(gamma, self.T[:expiry])
			
			self.model[ tenor ] = model_v
			return model_v - market_v
			
		def ObjectiveFunction(gamma_list):
			"""docstring for ObjectiveFunction"""
			gamma_dict = {}
			i = 0
			for k, v in self.market.iteritems():
				gamma_dict[k] = gamma_list[i]
				i += 1
			print gamma_list
			errors = 0
			for t in self.market:
				errors += CalibError(t, gamma_dict) ** 2
				
			return math.sqrt( errors/len(self.market) )

		print "Optimizing..."
		g = optimize.fmin( ObjectiveFunction, self.gamma_list ) #lower = [0]*len(self.gamma_list), upper  = [1]*len(self.gamma_list) )
		print g
		self.calib_gamma = g
		return g

# -------------------------------------------------------------------

# -------------------------------------------------------------------

market1 = { 1 : 1.925, 	3 : 2.15, 	5 : 2.25, 	7 : 2.35, 	10 : 2.35 	}
market2 = { 1 : 1, 		3 : 2, 		5 : 3, 		7 : 4, 		10 : 5 		}

# x = HomogenousPoissonCalibration( market = market1, yield_curve = "a" )
# x = HomogenousPoissonCalibration( market = market2, yield_curve = "a" )

X = InhomogenousPoissonCalibration( market = market2, yield_curve = "a" )
# doctest.testmod( verbose = True)


