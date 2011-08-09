from CalibrationMaster import *
import csv


#------------------------------------------------------------------------------

def GenerateCSV(write_csv = False, debug = 1, NSims = 500):
	"""docstring for main"""
	HP = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
						CDS				= HPCreditDefaultSwap,
						Process			= "HP",
						Guess			= [0.01],
						)

	CIR = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
						CDS 			= CIRCreditDefaultSwap,
						Process			= "CIR",
						Guess			= [0.1, 0.3, 0.2, 0.02],
						)


	IHP = InhomogenousCalibration(	
						DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
						)

	GOU = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
						CDS				= GammaOUCreditDefaultSwap,
						Process			= "GOU",
						Guess			= [0.2, 189, 10000, 0.002],
						)

	IGOU = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
						CDS 			= IGOUCreditDefaultSwap,
						Process			= "IGOU",
						Guess			= [0.3, 0.8, 5, 0.02],
						)

	for Calib in [GOU, IGOU]:

		x = CalibrationMaster( \
						CreditDerivativeCSVReader(file = "../Data/CDX.csv"),
						Calib,
						)
		
		print Calib.Process
		results =  x.Calibrate(debug = debug, N = NSims, dynamic = False)
		output =  x.FormatResults(results)
		# print output 
		zipped = zip(*output)

		if write_csv:
			filename = "Calibration Results/CDX/Static/" + Calib.Process + ".csv"
			with open(filename, 'wb') as f:
			    writer = csv.writer(f)
			    writer.writerows(zipped)

		results =  x.Calibrate(debug = debug, N = NSims, dynamic = True)
		output =  x.FormatResults(results)
		# print output 
		zipped = zip(*output)

		if write_csv:
			filename = "Calibration Results/CDX/Dynamic/" + Calib.Process + ".csv"
			with open(filename, 'wb') as f:
			    writer = csv.writer(f)
			    writer.writerows(zipped)

#------------------------------------------------------------------------------

if __name__ == '__main__':
	GenerateCSV(write_csv = False, debug = 1, NSims = 2)
	


