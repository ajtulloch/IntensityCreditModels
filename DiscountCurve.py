		
#------------------------------------------------------------------------------
						
class DiscountCurveBase(object):
	"""docstring for DiscountCurve"""
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
	"""docstring for FlatDiscountCurve"""
	def __init__(self, r):
		super(FlatDiscountCurve, self).__init__()
		self.r = r
		
	def DF(self, t1, t2):
		"""docstring for DiscountFactor"""
		return (1 + self.r) ** -(t2 - t1) 		

#------------------------------------------------------------------------------

if __name__ == '__main__':
	x = FlatDiscountCurve( r=0.06)				
	print x.DF( 0, 10)
