from CalibrationMaster import *
import csv




def main():
	"""docstring for main"""
	HP = PoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS				= HPCreditDefaultSwap,
								Process			= "HP",
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
								Process			= "GOU",
								Guess			= [0.2, 189, 10000, 0.002],
								)

	IGOU = PoissonCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
								CDS 			= IGOUCreditDefaultSwap,
								Process			= "IGOU",
								Guess			= [0.3, 0.8, 5, 0.02],
								)

	for Calib in [HP, IHP, CIR, GOU, IGOU]:
		x = PoissonCalibrationMaster( 	CreditDerivativeCSVReader(file = "../Data/CDX.csv"),
										Calib,
										)
		print Calib.Process
		results =  x.Calibrate(debug = 0, N = 100, dynamic = False)
		output =  x.FormatResults(results)
		print output 
		zipped = zip(*output)

		filename = "Calibration Results/Static/" + Calib.Process + ".csv"
		with open(filename, 'wb') as f:
		    writer = csv.writer(f)
		    writer.writerows(zipped)

			results =  x.Calibrate(debug = 0, N = 100, dynamic = False)
			output =  x.FormatResults(results)
			print output 
			zipped = zip(*output)

		filename = "Calibration Results/Static/" + Calib.Process + ".csv"
		with open(filename, 'wb') as f:
		    writer = csv.writer(f)
		    writer.writerows(zipped)

			results =  x.Calibrate(debug = 0, N = 100, dynamic = False)
			output =  x.FormatResults(results)
			print output 
			zipped = zip(*output)
	
	
if __name__ == '__main__':
	main()
	


