import csv
from datetime import date as pydate

#------------------------------------------------------------------------------

class CreditDerivativeCSVReader(object):
    """Implements an interface for reading a CSV file containing term
    structures of credit spreads."""
    def __init__(self, file):
        super(CreditDerivativeCSVReader, self).__init__()
        self.file = file
                
    def DictData(self):
        """Returns a dictionary object containing the CSV file data"""
        reader = csv.DictReader( open( self.file, "rU" ), dialect = "excel" )
        return reader
        
    def Dates(self):
        """Returns list of dates in the CSV file"""
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
            
        time_series = [ (convert_date(row[ "Date" ]), float(row[ header ])) \
            for row in data ]
        return time_series
    
    def TimeSeries(self, header):
        """Returns an array of (date, value) tuples"""
        data = self.DictData()
        time_series = [ (row[ "Date" ], float(row[ header ]) )for row in data ]
        return time_series

    def TimeSlice(self, date = None):
        if date == None:
            date = self.Dates()[0]
        """Returns a dictionary corresponding to the term structure at a given 
        time.  Raises exception if otherwise"""
        data = self.DictData()
        
        for i in data:
            if i[ "Date" ] == date:
                return i
        
        raise Exception
        
#------------------------------------------------------------------------------
                
if __name__ == '__main__':
    Y = CreditDerivativeCSVReader( "../Data/CDX.csv" )
    print Y.TimeSlice()
    Y = CreditDerivativeCSVReader( "../Data/GE.csv" )
    print Y.TimeSlice()
