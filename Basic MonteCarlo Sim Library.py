import random
import math


class MonteCarloSimBase(object):
	"""docstring for MonteCarloBase"""
	def __init__(self):
		super(MonteCarloSimBase, self).__init__()
		self.simulation = []
		self.state = {}
		
	def GetState(self):
		"""docstring for CurrentState"""
		return( self.state )
		
	def NextValue(self):
		"""docstring for NextValue"""
		abstract
		
	def Simulate(self):
		"""docstring for Simulate"""
		for i in range( self.N ):
			self.NextValue()
			
		return( self.simulation )

class CIRMonteCarloSim(MonteCarloSimBase):
	"""docstring for CIRMonteCarlo"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		
	def NextValue(self):
		"""docstring for NextValue"""
		pass
	
	def Simulate(self):
		"""docstring for Simulate"""
		pass
		
class GaussianMonteCarloSim(MonteCarloSimBase):
	"""docstring for GaussianMonteCarlo"""
	def __init__(self, S0, mu, sigma, dt, N):
		super(GaussianMonteCarloSim, self).__init__()
		self.S0 = S0
		self.mu = mu
		self.sigma = sigma
		self.dt = dt
		self.N = N
		self.t = 0
		self.state["S"] = S0
		self.simulation.append( S0 )
		
	def CurrentState(self):
		"""docstring for CurrentState"""
		return( self.simulation )
		
	def NextValue(self):
		"""docstring for NextValue"""
		# print self.state
		factor = ( self.mu - self.sigma ** 2 / 2 ) * self.dt + \
						math.sqrt( self.dt ) * self.sigma * random.normalvariate(0,1)
		St = self.state[ "S" ] * math.exp( factor )
		self.t += self.dt
		self.state[ "S" ] = St
		self.simulation.append( { "S" : St, "t": self.t } )
		
	
				
x = GaussianMonteCarloSim( S0 = 100, mu = 0.06, sigma = 0.2, dt = 0.01, N = 100 )

# x.CurrentState()

print x.Simulate()



		