class DiscountCurveBase(object):
	"""Defines the interface for a DiscountCurve.  The key method is DF(), 
	which returns the discount factor from t_1 to t_2.  Also defines helper 
	methods Initialise() and ReadFile()."""
	def __init__(self):
		super(DiscountCurveBase, self).__init__()
		
	def DF(self, t1, t2):
		"""docstring for DiscountFactor"""
		abstract
		
	def Initialise(self, t):
		"""docstring for Initialise"""
		pass
	
	def ReadFile(self):
		"""docstring for ReadFile"""
		abstract
		
#------------------------------------------------------------------------------
						
class FlatDiscountCurve(DiscountCurveBase):
	"""Implements a DiscountCurve where the yield curve is constant r."""
	def __init__(self, r):
		super(FlatDiscountCurve, self).__init__()
		self.r = r
		
	def DF(self, t1, t2):
		return (1 + self.r) ** -(t2 - t1) 		

#------------------------------------------------------------------------------

if __name__ == '__main__':
	x = FlatDiscountCurve( r=0.06)				
	print x.DF( 0, 10)
