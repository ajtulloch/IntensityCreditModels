import csv
from datetime import date as pydate

class CreditDerivativeCSVReader(object):
	"""docstring for CreditDerivativeCSVReader"""
	def __init__(self, file):
		super(CreditDerivativeCSVReader, self).__init__()
		self.file = file
				
	def DictData(self):
		"""docstring for dict"""
		reader = csv.DictReader( open( self.file, "rU" ), dialect = "excel" )
		return reader
		
	def Dates(self):
		"""docstring for dates"""
		data = self.DictData()
		dates = [ row[ "Date"] for row in data ]
		return dates
	
	def PlotSeries(self, header):
		"""Need to fix this function."""
		
		data = self.DictData()
		
		def convert_date(string):
			# print string
			ddmmyy = string.split( "/" )
			# print ddmmyy
			ddmmyy.reverse()
			
			yymmdd = [int(i) for i in ddmmyy]
			# print yymmdd
			return pydate(2000 + yymmdd[0], yymmdd[1], yymmdd[2])
			
		time_series = [ (convert_date(row[ "Date" ]), float(row[ header ]))for row in data ]
		return time_series
	
	
	def TimeSeries(self, header):
		"""Returns an array of (date, value) tuples"""
		data = self.DictData()
		time_series = [ (row[ "Date" ], float(row[ header ]) )for row in data ]
		return time_series

	def TimeSlice(self, date = None):
		if date == None:
			date = self.Dates()[0]
		"""Returns a dictionary corresponding to the term structure at a given time"""
		data = self.DictData()
	 	for	i in data:
			if i[ "Date" ] == date:
				return i
		
		raise Exception( "Date not found in data")
		
		
		
if __name__ == '__main__':
	Y = CreditDerivativeCSVReader( "../Data/CDX.csv" )
	# print Y.TimeSeries("5")
	print Y.PlotSeries("3")