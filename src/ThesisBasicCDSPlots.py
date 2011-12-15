
import pylab
from pylab import arange,pi,sin,cos,sqrt
import numpy as np
import random
from scipy import vectorize, stats
import sys
from pylab import exp as vec_exp
import csv
import datetime
import matplotlib as mpl
from pylab import exp as vec_exp
import string
import re

#------------------------------------------------------------------------------
sys.path.append("../")
from CDS import *
from MarketData import *
from Calibration import *
from CopulaSimulation import *
from Payoff import *

#------------------------------------------------------------------------------
AUTOCOLOR = 1
AUTOCOLOR_COLORS = ("#348ABD", "#7A68A6", "#A60628", "#467821", "#CF4457", "#188487", "#E24A33")

pg_width = 469.7549
fig_width_pt = 0.8*pg_width  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width, fig_height]
params = {'backend': 'pdf',
          'axes.labelsize':  10,
          'text.fontsize':   10,
		  'suptitle.fontsize': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
		  'title.fontsize' : 10,
          'text.usetex'		: True,
          'figure.figsize': fig_size,
		  # 'axes.color_cycle'    : ("#348ABD", "#7A68A6", "A60628", "467821", "CF4457", "188487", "E24A33"),
		  'figure.subplot.bottom': 0.12,
		  'font.family' : 'serif',
          # 'font.serif' : ['Minion Pro']
			}

pylab.rcParams.update(params)

#------------------------------------------------------------------------------

def CDSCashflows( barcolour = "grey"):
	"""Creates the chart"""

				
	
	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})

	
	# pylab.rc("axes", linewidth=2.0)
	months = range(3, 24, 3)
	payments = [-2]*6 + [60]
	# print [(i,j) for i,j in zip(payments, months)]
	
	pylab.figure(1)
	pylab.clf()
	if AUTOCOLOR:
		pylab.bar(months, payments, align = "center", width=2, color = AUTOCOLOR_COLORS[0]) 
		# pylab.axhline(color="#bcbcbc")
		pylab.axhline(color="black")
		
		
	else:
		pylab.bar(months, payments, align = "center", facecolor = barcolour, width=2)
		pylab.axhline(color="black")
		
	
	ticks = range(22)
	# pylab.show()
	# pylab.title("Average Ratings on the Training Set")
	# pylab.xlabel( r"\textrm{Quarterly payments on a CDS of a two year tenor.  The notional is \$10,000,000, and the spread is 200bps (2.00\%).We assume default occurs at 21 months, with a recovery rate of 40\%}" )
	pylab.gca().set_xticks(months)
	pylab.gca().set_yticks([-10, 0, 10, 20, 30, 40, 50, 60, 70] )
	pylab.ylabel('Payments (\$mm)' )
	pylab.xlabel('Months' )
	pylab.savefig('../../Diagrams/CDSPaymentBarChart.pdf')
	print "CDS Payment Schedule Completed"

#------------------------------------------------------------------------------

def CDSIssuance( barcolour = "grey" ):
	"""docstring for CDSIssuance"""

	
	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
	
	CDO_Issuance = "1278.979	2901.09	3476.247	6478.862	10770.985	18341.068	25757.449	23990.644	16142.753	11933.994	10775.637	11881.516"
	CDS_Issuance = "6395.744	10211.378	13908.285	20352.307	28650.265	42580.546	58243.721	57402.758	41882.684	36046.236	32692.694	30260.93"
	Times = "Dec.2004	Jun.2005	Dec.2005	Jun.2006	Dec.2006	Jun.2007	Dec.2007	Jun.2008	Dec.2008	Jun.2009	Dec.2009	Jun.2010"
	Time_list = Times.split()
    # labels = []
	labels = [t[4:] for i, t in enumerate(Time_list) if i % 2 == 0]
    # for t in Time_list:
    #   if t[0:3] == "Dec":
    #       labels.append( "H2 " + t[6:])
    #   else:
    #       labels.append( "H1 " + t[6:])
	CDS_t = [ float(i)/1000 for i in CDS_Issuance.split()]
	CDO_t = [ float(i)/1000 for i in CDO_Issuance.split()]
	CDS = [CDS_t[i] + CDS_t[i+1] for i, v in enumerate(CDS_t) if i % 2 == 0]
	CDO = [CDO_t[i] + CDO_t[i+1] for i, v in enumerate(CDO_t) if i % 2 == 0]	
	
	N = len(CDS)
	ind = np.arange(N)
	width = 0.3
	
	# print labels
	
	pylab.figure(1)
	pylab.clf()
	if AUTOCOLOR:
		CDS = pylab.bar(ind, CDS, width, facecolor = "#348ABD", label = "CDS")
		CDO = pylab.bar(ind+width, CDO, width, facecolor = "#7A68A6", label = "CDO")
	else:		
		CDS = pylab.bar(ind, CDS, width, facecolor = barcolour, label = "CDS")
		CDO = pylab.bar(ind+width, CDO, width, facecolor = "black", label = "CDO")
		
		
	# pylab.legend( (CDS[0], CDO[0]), ('Credit Default Swaps', 'Collateralised Debt Obligations'), loc='upper left' )
	pylab.legend()
	pylab.ylabel('Amount outstanding (\$tn)' )
	pylab.xlabel('Year' )
	
	pylab.gca().set_xticks(ind+width)
	pylab.gca().set_xticklabels(labels )
	pylab.savefig('../../Diagrams/CDSIssuance.pdf')
	
	# pylab.show()
	print "CDS and CDO Issuance Completed"

#------------------------------------------------------------------------------

def CDSTermStructure():
	"""docstring for CDSTermStructure"""

	
	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
	
	CDS_Term = [29.24999969, 44.25000028, 55.2500018, 89.25000016, 107.2499996, 121.2499997]
	AU_CDS = CDS_Term
	Maturity = [ 1, 2, 3, 5, 7, 10]
	# pylab.figure()
	pylab.subplot(1,2,1)
	# pylab.clf()
	if AUTOCOLOR:
		GR_CDS = pylab.scatter( Maturity, AU_CDS, label = "CDX (17/03/11)", c = AUTOCOLOR_COLORS[0], )
	else:
		GR_CDS = pylab.scatter( Maturity, AU_CDS, c = "grey", label = "CDX (17/03/11)" )
	
	# pylab.gca().set_xticks(Maturity)
	pylab.legend( scatterpoints = 1 )
	pylab.ylabel('Spread (bps)' )
	pylab.xlabel('Maturity (years)' )
	
	pylab.subplot(1,2,2)
	CDS_Term = [ 325.0000008, 311.0000001, 303.0000001, 283.0000001, 264, 251.0000001 ]
	GR_CDS = CDS_Term
	if AUTOCOLOR:
		GRCDS = pylab.scatter( Maturity, GR_CDS, label = "CDX (20/11/08)", c = AUTOCOLOR_COLORS[1], )
	else:
		GRCDS = pylab.scatter( Maturity, GR_CDS, c = "black", label = "CDX (20/11/08)" )
	
	pylab.legend( scatterpoints = 1 )
	pylab.ylabel('Spread (bps)' )
	pylab.xlabel('Maturity (years)' )
	
	# pylab.subplots_adjust(bottom=0.12)
	pylab.subplots_adjust(wspace=0.4)
	
	pylab.savefig('../../Diagrams/CDSTermStructure.pdf')
	print "CDS Term Structure Diagram Completed"
	# pylab.show()

#------------------------------------------------------------------------------

def IntensityStructure():
	"""docstring for fname"""
	xs = pylab.arange(0.0, 10.0, 0.001)
	HOMON_DEFAULT = 0.01240234375
	def inhom(t):
		"""docstring for f"""
		gamma = [ 0.00487255,  0.00736839,  0.00919817,  0.01484686,  0.01783495,  0.02015673 ]
		tenors = [ 1, 2, 3, 5, 7, 10]
		for i in range( len(tenors) ):
			if t <= tenors[0]:
				return gamma[0]
			if t < tenors[i] and t >= tenors[i-1]:
				return gamma[i]
	
	def homon(t):
		return HOMON_DEFAULT
	
	
	CDS = IHPCreditDefaultSwap(tenors = [1,2,3,5,7,10],
							DiscountCurve = FlatDiscountCurve(r = 0.00),
							maturity = 10,
							)
	
	def prob(t):
		"""docstring for prob"""
		gamma = [ 0.00487255,  0.00736839,  0.00919817,  0.01484686,  0.01783495,  0.02015673 ]
		return CDS.SurvivalProbability(gamma, t)
		
	# calculate x and y series for default probability plot
	ihp = vectorize(prob)
	ihp_ys = ihp(xs)
	hp_ys = vec_exp(-HOMON_DEFAULT * xs)
	
	# Calculate x and y series for the default intensity plot
	fvec = vectorize(inhom)
	inhomon = fvec(xs)
	gvec = vectorize(homon)
	homonss = gvec(xs)
	
	
	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
	
	pylab.clf()
	pylab.subplot(1,2,1)
	
	if AUTOCOLOR:
		homon = pylab.plot(xs, homonss, label = "HP")
		inhomon = pylab.plot(xs, inhomon, label = "IHP")
	else:
		homon = pylab.plot(xs, homonss, color = "black", label = "HP")
		inhomon = pylab.plot(xs, inhomon, color = "grey", linestyle="-", label = "IHP")
	
	pylab.xlabel('Maturity (years)' )
	pylab.ylabel('Default Intensity' )
	pylab.legend(loc = "upper left")
	
	
	pylab.subplot(1,2,2)
	# pylab.clf()
	if AUTOCOLOR:
		homon_prob = pylab.plot(xs, hp_ys, label = "HP")
		inhomon_prob = pylab.plot(xs, ihp_ys, label = "IHP")
	else:
		homon_prob = pylab.plot(xs, hp_ys, color = "black", label = "HP")
		inhomon_prob = pylab.plot(xs, ihp_ys, color = "grey", linestyle="-", label = "IHP")

	pylab.legend()
	pylab.xlabel('Maturity (years)' )
	pylab.ylabel('Survival Probability' )
	
	# pylab.subplots_adjust(bottom=0.15)
	pylab.subplots_adjust(wspace=0.4)
	pylab.savefig('../../Diagrams/InhomogenousDefaultIntensity.pdf')
	# pylab.show()
	
	# pylab.show()
	print "Poisson Default Intensity Term Structure Completed"

#------------------------------------------------------------------------------

def ParSpreadAndSurvivalProbabilities():
	"""docstring for ParSpreadAndSurvivalProbabilities"""
	pass
	y = CreditDerivativeCSVReader( file = "../../Data/CDX.csv")
	
	date = y.Dates()[-1]
	# print y.Dates()
	# if a is wrong
	data = y.TimeSlice(date)
	z = MarketData(data)
	# print z.Data()
	# print z.Dates()
	print z
	market_x = [k for k,v in z.Data()]
	market_y = [v for k,v in z.Data()]

	HP = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.03), 
								MarketData 		= z,
								CDS				= HPCreditDefaultSwap,
								Process			= "HP",
								Guess			= [0.01],
								)


	IHP = InhomogenousCalibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.03), 
											MarketData 		= z,
											# Process			= "IHP"
											)

	CIR = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.03), 
								MarketData 		= z,
								CDS 			= CIRCreditDefaultSwap,
								Process			= "CIR",
								Guess			= [0.1, 0.3, 0.2, 0.02],
								)

	GOU = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.03), 
								MarketData 		= z,
								CDS				= GammaOUCreditDefaultSwap,
								Process			= "G-OU",
								Guess			= [0.2, 189, 10000, 0.002],
								)

	IGOU = Calibration(	DiscountCurve 	= FlatDiscountCurve(r = 0.03), 
								MarketData 		= z,
								CDS 			= IGOUCreditDefaultSwap,
								Process			= "IG-OU",
								Guess			= [0.3, 0.8, 5, 0.02],
								)


	xs = arange(0.001,10,0.01)						


	CDSList = [HP, IHP, GOU, IGOU, CIR]

	# CDSList = [CIR]
	for Credit in CDSList:
		Credit.Calibrate()
		spreads = []
		probs	= []
		print Credit.Process
		print Credit.PrintParameters()
		for x in xs:
			# CDS = Credit.CDS
			CDS = Credit.CDS( 	DiscountCurve 	= FlatDiscountCurve(r = 0.00), 
					# MarketData 		= MarketData,
								maturity		= x,
								)

			if Credit.Process == "IHP":
				CDS.tenors = sorted(z.Tenors())
			spread 	= CDS.ParSpread(Credit.calibrated_gamma)
			prob 	= CDS.SurvivalProbability(Credit.calibrated_gamma, x)
			spreads.append(spread)
			probs.append(prob)
		# print spreads
		# if Credit.Process == "CIR":

			# print spreads, probs
		Credit.pars = spreads
		Credit.probs = probs
		Credit.defprob = 1 - np.array(probs)
	# 
	# print "########"
	# print "Tenors\t&\t1y\t&\t2y\t&\t3y\t&\t5y\t&\t7y\t&\t10y\t\\\\"
	# string = "Market"
	# for v in market_y:
	# 	string += "\t&\t%.0f" % v
	# string += "\\\\"
	# print string
		
	# dashes = ['--', #    : dashed line
	#           '-', #     : solid line
	#           '-.', #   : dash-dot line
	#           ':', #    : dotted line
	#            '-']


	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
	# pylab.rc('axes.color_cycle', **[["348ABD", "7A68A6", "A60628", "467821", "CF4457", "188487", "E24A33"]] )

	pylab.figure(1)
	pylab.clf()

	
	
	pylab.xlabel('Maturity (years)' )
	pylab.ylabel('Probability' )
	for i, CDS in enumerate(CDSList):
		y = pylab.plot(xs, CDS.probs, label = CDS.Process) #c= 'k', color = dashes[mod(i, len(dashes))])
		# print y

		# pylab.plot(xs, CDS.defprob, label = "", c= y[0].get_color() )
		# pylab.plot(xs, CDS.probs, label = CDS.Process, alpha = 0.5)
		# pylab.plot(xs, CDS.defprob, label = CDS.Process, alpha = 0.5)#, xs, CDS.defprob, label = CDS.Process + )

	pylab.legend( loc = "upper right")
	# pylab.subplots_adjust(bottom=0.15)
	pylab.savefig('../../Diagrams/ProcessDefaultProbs.pdf')


	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})

	pylab.figure(1)
	pylab.clf()
	# pylab.gray()

	pylab.xlabel('Maturity (years)' )
	pylab.ylabel('Par Spread (bps)' )
	for i, CDS in enumerate(CDSList):
		pylab.plot(xs, CDS.pars, label = CDS.Process)  #c= 'k', linestyle = dashes[mod(i, len(dashes))])
	if AUTOCOLOR:	
		pylab.scatter(market_x, market_y, label = "Market", c = AUTOCOLOR_COLORS[5])
	else:
		pylab.scatter(market_x, market_y, label = "Market", c = 'grey')
		
	pylab.xlim([0,10])
	pylab.legend( loc = "lower right", scatterpoints = 1 )

	# 
	# pylab.subplots_adjust(bottom=0.15)
	# pylab.subplots_adjust(wspace=0.4)
	pylab.gray()
	pylab.savefig('../../Diagrams/ProcessParSpreads.pdf')
	print "Par Spread and Probabilities Completed"

#------------------------------------------------------------------------------

def TimeSeriesPlot():
	"""docstring for TimeSeriesPlot"""
	def GetData(CreditDerivativeCSV, maturity):
		"""docstring for GetData"""
		TS = CreditDerivativeCSV.PlotSeries(maturity)
		xs = [data[0] for data in TS]
		ys = [data[1] for data in TS]
		return (xs, ys)
	
	

	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
	# pylab.rc('axes.color_cycle', **[["348ABD", "7A68A6", "A60628", "467821", "CF4457", "188487", "E24A33 

	# pylab.gray()

	pylab.figure(1)
	pylab.clf()

	pylab.xlabel('Year' )
	pylab.ylabel('Spread (bps)' )
	Y = CreditDerivativeCSVReader( file = "../../Data/CDX.csv")
	# xs, ys = GetData(Y, "3")
	# plot = pylab.plot(xs, ys, label = "CDX 3y", )#color = "black" )

	xs, ys = GetData(Y, "5")
	plot = pylab.plot(xs, ys, label = "CDX 5y", )#color = "grey" ) 

	xs, ys = GetData(Y, "10")
	plot = pylab.plot(xs, ys, label = "CDX 10y", )# color = "grey" ) 
	# plot = pylab.plot(xs, ys, label = "CDX 10y") 
	pylab.legend()
	dateFmt = mpl.dates.DateFormatter('%b %y')
	pylab.gca().xaxis.set_major_formatter(dateFmt)	


	pylab.savefig('../../Diagrams/CDXIndexTS.pdf')
	print "CDX Time Series Completed"
	# pylab.show()

def LevyProcessPlots():
	"""docstring for LevyProcessPlots"""

	np.random.seed(50)
	N = 50
	dt = 10.0/N
	xs = arange(0, 10, dt)
	
	
	def ProcessGen(draws):
		res = [0.0] * N
		for i in range(len(draws)):
			res[i] = res[i-1] + draws[i]
		return res	
		
	def InverseGauss(a,b, N):
		"""docstring for InverseGauss"""
		res = []
		for i in range(N):
			nu = stats.norm.rvs()
			# print nu
			y = nu ** 2
			x = a / b + y / (2 * b ** 2) - sqrt(4 * a * b * y + y ** 2)/ (2 * b ** 2)
			u = stats.uniform.rvs()
			# print "nu:\t%.2f \tu:\t%.2f" %(nu, u)
			if u > a/ (a + x * b):
				res.append(a ** 2 / ( x * b ** 2 )) 
			else:
				res.append(x)
		return res
	
	def InverseGaussOU(gamma, a, b, y_0, N):
		"""docstring for InverseGaussOU"""
	
		# PRV process
		PRV = stats.poisson.rvs(a * b * dt / 2, size = N)
		Poisson = ProcessGen(PRV)
		POI = [int(i) for i in Poisson]
		# IG Process
		IVG = InverseGauss(a / 2 * dt, b, N)
		z_1 = ProcessGen(IVG)
		
		# Sum of normals
		norm_array = [];
		z_2	= [0.0] * len(POI);
		for i, n_i in enumerate(POI):
			if len(norm_array) != n_i:
				normal = (stats.norm.rvs() ** 2) / b
				norm_array.append(normal) 
			z_2[i] = sum(norm_array)
		
		# BDLP for IG-OU
		Z = [sum(a) for a in zip(*(z_1, z_2))]
		
		res = [y_0] * N
		for i in range(len(Z)):
			res[i] = -gamma * res[i-1] * dt + Z[i]
		return res
		
	def GammaOU(gamma, a, b, y_0, N):
		"""docstring for GammaOU"""
		PRV = stats.poisson.rvs(a * gamma * dt, size = N)
		Poisson = ProcessGen(PRV)
		POI = [int(i) for i in Poisson]
		
		norm_array = [];
		z	= [0.0] * len(POI);
		for i, n_i in enumerate(POI):
			if len(norm_array) != n_i:
				normal = stats.expon.rvs(b)
				norm_array.append(normal) 
			z[i] = sum(norm_array)
		
		res = [y_0] * N
		for i in range(len(z)):
			res[i] = -gamma * res[i-1] * dt + z[i]
		return res
	
		
	PRV = stats.poisson.rvs(1.5*dt, size = N)
	Poisson = ProcessGen(PRV)

	GRV = stats.gengamma.rvs(0.5*dt, 0.2, size = N)
	Gamma = ProcessGen(GRV)
	
	IVG = InverseGauss(0.2 * dt, 0.1, N)
	IG = ProcessGen(IVG)

	IGOU = InverseGaussOU(4, 0.20, 5, 0.08, N)
	
	GOU = GammaOU(2, 0.20, 18, 0.08, N)
	
	pylab.rcParams.update(params)
	# pylab.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
	
	pylab.figure(1)
	pylab.clf()

	# for process in [(Poisson, "Poisson"), (Gamma, "Gamma"), (IG, "IG"), (IGOU, "IG-OU"), (GOU, "G-OU") ]:
	for process in [ (GOU, "G-OU"), (IGOU, "IG-OU") ]:
		pylab.figure(1)
		pylab.clf()
		pylab.xlabel('Year' )
		pylab.ylabel('Default intensity ($\lambda_t$)' )
		if AUTOCOLOR:
			plot = pylab.plot(xs, process[0])
		else:
			plot = pylab.plot(xs, process[0], color = "black")
		pylab.savefig('../../Diagrams/Sim' + process[1] + '.pdf')

	for process in [ (Poisson, "Poisson") ]:
		pylab.figure(1)
		pylab.clf()
		pylab.xlabel('Year' )
		pylab.ylabel('Count ($N_t$)' )
		if AUTOCOLOR:
			plot = pylab.plot(xs, process[0])
		else:
			plot = pylab.plot(xs, process[0], color = "black")
		pylab.savefig('../../Diagrams/Sim' + process[1] + '.pdf')


	print "Process Simulations Completed"
	# pylab.show()

#------------------------------------------------------------------------------

def ParameterStabilityRMSE():
	"""docstring for ParameterStability"""
	pylab.rcParams.update(params)
	
	def GetRMSE(process, dynamic):
		"""docstring for GetRMSE"""
		if dynamic == True:
			filename = "../Calibration Results/CDX/Dynamic/" + process + ".csv" 
		else:
			filename = "../Calibration Results/CDX/Static/" + process + ".csv"
		
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			RMSE = [float(row[-1]) for row in reader]
		# print RMSE
		return RMSE
	
	def PlotRMSEs(process):
		pretty_mapping = {
			'IGOU': 'Inverse Gaussian-OU',
			'GOU' : 'Gamma-OU',
			'CIR' : 'CIR',
			'HP'  : 'HP',
			'IHP' : 'IHP',
		}
		
		
		"""docstring for PlotRMSE"""
		dynamic_rmse = GetRMSE(process, True)
		static_rmse = GetRMSE(process, False)
		lower = np.concatenate((dynamic_rmse,static_rmse)).min()	
		upper = np.concatenate((dynamic_rmse,static_rmse)).max()	
		bounds = (lower, upper)
		
		pylab.figure(1)
		pylab.clf()
		
		pylab.subplot(1,2,1)

		if AUTOCOLOR:
			homon = pylab.hist(dynamic_rmse, range = bounds, color = AUTOCOLOR_COLORS[0])
		else:
			homon = pylab.hist(dynamic_rmse, range = bounds, color = "black")
		# pylab.title('Dynamic')
		pylab.xlabel('RMSE')
		pylab.ylabel('Frequency')

		pylab.subplot(1,2,2)
		# pylab.clf()
		if AUTOCOLOR:
			homon = pylab.hist(static_rmse, range = bounds, color = AUTOCOLOR_COLORS[1])
		else:
			homon = pylab.hist(static_rmse, range = bounds, color = "grey")
		
		# pylab.title('Static')
		pylab.xlabel('RMSE')
		pylab.ylabel('Frequency')

		# pylab.subplots_adjust(bottom=0.15)
		pylab.subplots_adjust(wspace=0.4)
		pylab.suptitle(pretty_mapping[process], fontsize=10)
		
		pdf_file = "../../Diagrams/ParameterStability/" + process + ".pdf"

		pylab.savefig(pdf_file)

		# pylab.show()
	
	for process in ['IHP', 'CIR', 'GOU', 'IGOU', 'HP']:
		PlotRMSEs(process)
		
	print "Parameter Stability RMSE Completed"

#------------------------------------------------------------------------------

def RMSEDensity():
	"""docstring for RMSEDensity"""
	pylab.rcParams.update(params)
	
	def GetRMSE(process, dynamic):
		"""docstring for GetRMSE"""
		if dynamic == True:
			filename = "../Calibration Results/CDX/Dynamic/" + process + ".csv" 
		else:
			filename = "../Calibration Results/CDX/Static/" + process + ".csv"
		
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			RMSE = [float(row[-1]) for row in reader]
		# print RMSE
		return RMSE
	
	def PlotRMSEs(process):
		pretty_mapping = {
			'IGOU': 'Inverse Gaussian-OU',
			'GOU' : 'Gamma-OU',
			'CIR' : 'CIR',
			'HP'  : 'HP',
			'IHP' : 'IHP',
		}
		
		
		"""docstring for PlotRMSE"""
		dynamic_rmse = GetRMSE(process, True)
		static_rmse = GetRMSE(process, False)
		lower = np.concatenate((dynamic_rmse,static_rmse)).min()	
		upper = np.concatenate((dynamic_rmse,static_rmse)).max()	

		xs = np.linspace(lower, upper, 200)
		dynamic_kde = stats.gaussian_kde(dynamic_rmse)
		static_kde = stats.gaussian_kde(static_rmse)
		
		pylab.figure(1)
		pylab.clf()
		
		if AUTOCOLOR:
			dynamic = pylab.plot(xs, dynamic_kde(xs), color = AUTOCOLOR_COLORS[0], label = "Dynamic")
			static = pylab.plot(xs, static_kde(xs), color = AUTOCOLOR_COLORS[1], label = "Static")
		else:
			pass
		
		pylab.legend()
		pylab.title(pretty_mapping[process], fontsize = 10)
		pylab.xlabel('RMSE')
		pylab.ylabel('Frequency')

		
		pdf_file = "../../Diagrams/ParameterStability/" + process + "Density.pdf"

		pylab.savefig(pdf_file)

		# pylab.show()
	
	for process in ['CIR', 'GOU', 'IGOU']:
		PlotRMSEs(process)
		
	print "Density RMSE Completed"
	
#------------------------------------------------------------------------------

def ParameterStabilityParameters(acorr = False):
	"""docstring for ParameterStability"""
	
	pylab.rcParams.update(params)
	def GetParameters(process, dynamic):
		"""docstring for GetRMSE"""
		if dynamic == True:
			filename = "../Calibration Results/CDX/Dynamic/" + process + ".csv" 
		else:
			filename = "../Calibration Results/CDX/Static/" + process + ".csv"
		
		def DateFromString(string):
			"""docstring for DateFromString"""
			lists = string.split('/')
			return datetime.date(2000 + int(lists[2]), int(lists[1]), int(lists[0]))
		
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			str_parameters = [row[0:-1] for row in reader]
			parameters = []
			for i in range(len(str_parameters[0])):
				if i == 0:
					str_dates = [row[0] for row in str_parameters]
					dates = [DateFromString(string) for string in str_dates]
					# print dates
				else:
					values = [float(row[i]) for row in str_parameters]
					parameters.append(values)
			
		return dates, parameters

	def PlotParameters(process, acorr = False):
		"""docstring for PlotRMSE"""
		
		mapping = {
			'IGOU': ['Inverse Gaussian-OU', ['\\gamma', 'a', 'b', '\\lambda_0'] ],
			'GOU' : [ 'Gamma-OU', ['\\gamma', 'a', 'b', '\\lambda_0'] ],
			'CIR' : ['CIR', ['\\kappa', '\\nu', '\\gamma', '\\lambda_0'] ], 	
}


		dates, dynamic_parameters = GetParameters(process, True)
		dates, static_parameters = GetParameters(process, False)
		
		# print dates
		# print dynamic_parameters
		
		
		parameter_names = mapping[process][1]
		process_name = mapping[process][0]
		

		pylab.clf()
		
		pylab.figure(1)
		
		for i, param in enumerate(parameter_names):
			dynamic_values = dynamic_parameters[i]
			static_values = static_parameters[i]

			pylab.subplot(2,2,i)
			lag = 5
			usevlines = False
			from matplotlib.patches import Rectangle
			
			if acorr:
				if AUTOCOLOR:
					dyn = pylab.acorr(dynamic_values, label = "Dynamic", color = AUTOCOLOR_COLORS[0], maxlags = lag, usevlines = usevlines)
					stat = pylab.acorr(static_values, label = "Static", color = AUTOCOLOR_COLORS[1], maxlags = lag, usevlines = usevlines)
			
					p = Rectangle((0, 0), 1, 1, fc=AUTOCOLOR_COLORS[0])
					q = Rectangle((0, 0), 1, 1, fc=AUTOCOLOR_COLORS[1])
					pylab.ylim([0,1])
				
					pylab.legend((p, q), ("Dynamic", "Static"))
				else:
					dyn = pylab.acorr(dates, dynamic_values, label = "Dynamic", color = AUTOCOLOR_COLORS[0])
					stat = pylab.acorr(dates, static_values, label = "Static", color = AUTOCOLOR_COLORS[1])
			
			else:		
				if AUTOCOLOR:
					dyn = pylab.plot(dynamic_values, label = "Dynamic", color = AUTOCOLOR_COLORS[0])
					stat = pylab.plot(static_values, label = "Static", color = AUTOCOLOR_COLORS[1])
					pylab.legend()
					
				else:
					dyn = pylab.plot(dates, dynamic_values, label = "Dynamic", color = AUTOCOLOR_COLORS[0])
					stat = pylab.plot(dates, static_values, label = "Static", color = AUTOCOLOR_COLORS[1])
					pylab.legend()
					
			# pylab.title('Stability of $' + param + '$')
			# pylab .xlabel('Year')
			pylab.ylabel('$' + param + '$')
			# loc = mpl.dates.MonthLocator(1)
			# 		dateFmt = mpl.dates.DateFormatter('%b %y')
			# 		pylab.gca().xaxis.set_major_formatter(dateFmt)	
			# 		# 
			# 		pylab.gca().xaxis.set_major_locator(loc)
			# 	
			
				
			
			
		# pylab.subplots_adjust(bottom=0.15)
		
		pylab.subplots_adjust(wspace=0.4)
		pylab.suptitle(process_name, fontsize = 10)

		pdf_file = "../../Diagrams/ParameterStability/" + process + "Parameters.pdf"
	
		if acorr:
			pdf_file = "../../Diagrams/ParameterStability/" + process + "ParametersAutoCorr.pdf"
			
		pylab.savefig(pdf_file)
		# pylab.show()

		# pylab.show()
	

	for process in ['CIR', 'GOU', 'IGOU']:
		PlotParameters(process, acorr)

	print "Parameter Stability Parameters Completed"

def PlotBivariateCopula(uniforms = False, n_sim = 500):
    """docstring for fname"""
    spreads = { 'Date' : '17/5/10', 
                '1' : '350', 
                '2' : '350', 
                '5' : '400', 
                '7' : '450', 
                '10' : '600' 
                }
    data = MarketData(spreads)
    
    print_mapping = {   GaussianCopula : "Gaussian Copula",
                        StudentTCopula : "Student's $t$ Copula"
                        }
    
    def CreateScatters(copula):
        """docstring for CreateScatters"""
        pretty_copula = print_mapping[copula]
        # 
        # gou = SimulatedDefaultTimes(GammaOUCreditDefaultSwap, 
        #                         data, 
        #                         copula, 
        #                         rho, 
        #                         100, 
        #                         2000)
        # # print res
        rhos = [0.2, 0.8]
        default_times = {'HP' : {}, 'IG-OU' : {}, 'Gamma-OU': {}}
        N = n_sim
        for rho in rhos:
            default_times['HP'][rho] = SimulatedDefaultTimes( HPCreditDefaultSwap, 
                                            data, 
                                            copula, 
                                            rho, 
                                            2, 
                                            N,
                                            uniforms = uniforms)
    
            default_times['IG-OU'][rho] = SimulatedDefaultTimes(IGOUCreditDefaultSwap, 
                                            data, 
                                            copula, 
                                            rho, 
                                            2, 
                                            N,
                                            uniforms = uniforms)

            default_times['Gamma-OU'][rho] = SimulatedDefaultTimes(GammaOUCreditDefaultSwap, 
                                            data, 
                                            copula, 
                                            rho, 
                                            2, 
                                            N,
                                            uniforms = uniforms)

            
        pylab.clf()
	
        pylab.figure(1)
	    
        for i, process in enumerate(default_times.keys()):
            pylab.clf()
    
            for j, rho in enumerate(rhos):
                pylab.subplot(1, 2, j+1)
                defaults = default_times[process][rho]
                x, y = zip(*defaults)
            
                if AUTOCOLOR:
                    pylab.scatter(x, y, s = 1, color = AUTOCOLOR_COLORS[j])
            
                pylab.title("$\\rho$ = " + str(rho), fontsize = 8)
                if uniforms:
                    label = ["u_1", "u_2" ]
                    title = pretty_copula
                    pylab.xlim([0,1])
                    pylab.ylim([0,1])
                else:
                    label = ["\\tau_1", "\\tau_2"]
                    title = pretty_copula + " with " + process + " marginals"
                    tmax = 60
                    pylab.xlim([0, tmax])
                    pylab.ylim([0, tmax])
                    
                pylab.xlabel('$' + label[0] + '$')
                pylab.ylabel('$' + label[1] + '$')
                # pylab.xlim([0,50])
                # pylab.ylim([0,50])
        	
                    		# loc = mpl.dates.MonthLocator(1)
        		# 		dateFmt = mpl.dates.DateFormatter('%b %y')
        		# 		pylab.gca().xaxis.set_major_formatter(dateFmt)
        		# 		#
        		# 		pylab.gca().xaxis.set_major_locator(loc)
        		#

                pylab.subplots_adjust(top=0.85)
                pylab.subplots_adjust(bottom=0.10)
                pylab.subplots_adjust(wspace=0.4)
            	
            pylab.suptitle(title, fontsize = 10)
            file_title = re.sub("[\s'$]", "", title)
            pdf_file = "../../Diagrams/Copulas/" + file_title + "Scatterplot.pdf"
    
            pylab.savefig(pdf_file)
	
    CreateScatters(GaussianCopula)
    CreateScatters(StudentTCopula)
    
def MonteCarloCorrelationSensitivities():
    """docstring for MonteCarloCorrelationSensitivities"""
    def PricePayoff(data, payoff, cds_class, calibrated_gamma, copula_class, rho, n_obligors, n_sims):
        """docstring for Pricing"""
        
        CDS = cds_class()
        cov = FlatCorrelationMatrix(rho, n_obligors)
        copula = copula_class(CDS, calibrated_gamma, cov, n_obligors)
        CopSim = CopulaSimulation(copula)


        MCSim = MonteCarloPricingSim(payoff, CopSim)
        return MCSim.Price(n_sims)
    
    def SetupPayoffCopula(payoff, cds_class, copula_class, rhos, n_sims, n_obligors):
        """docstring for fname"""
        
        spreads = { 'Date' : '17/5/10', 
                    '1' : '350', 
                    '2' : '350', 
                    '5' : '400', 
                    '7' : '450', 
                    '10' : '600' 
                    }
        data = MarketData(spreads)
        
        if cds_class == HPCreditDefaultSwap:
            guess = [0.01]
        else:
            guess = [0.3, 0.8, 5, 0.02]
        
        calib = Calibration(DiscountCurve   = FlatDiscountCurve(r = 0.02), 
                            MarketData      = data,
                            CDS             = cds_class,
                            Guess           = guess,
                            )
        calib.Calibrate()
        calibrated_gamma = calib.calibrated_gamma 
        prices = []
        for rho in rhos:
            price = PricePayoff(data, 
                                payoff,
                                IGOUCreditDefaultSwap,
                                calibrated_gamma,
                                GaussianCopula,
                                rho,
                                n_obligors,
                                n_sims)
            prices.append(price)
        return prices
    
    
    
    print_mapping = {   GaussianCopula : "Gaussian",
                        StudentTCopula : "Student's $t$"
                        }
    cds_mapping = {     HPCreditDefaultSwap : "HP", 
                        GammaOUCreditDefaultSwap : "Gamma-OU", 
                        IGOUCreditDefaultSwap: "Inverse Gaussian-OU"
                        }
    # Pairs of (payoff, n_obligors, n_sims)
    payoff_specification = [(KthToDefault(k=1, T=5), 5, 5000), 
                            (KthToDefault(k=2, T=5), 5, 5000),
                            (KthToDefault(k=5, T=5), 5, 5000),    
                            # (KthToLthTranche(k = 10, l = 100, T=5), 20, 100),
                            ]
    rhos = np.linspace(0,0.2,3)
    
    for cds_class in [GammaOUCreditDefaultSwap, IGOUCreditDefaultSwap]:
        price_array = []
        for copula_class in print_mapping.keys():
            for (payoff, n_obligors, n_sims) in payoff_specification:
                prices = SetupPayoffCopula(payoff, cds_class, copula_class, rhos, n_sims, n_obligors)
                name = str(payoff)[:3] + ", " + print_mapping[copula_class]
                price_array.append((prices, name))
                print name
                
        pylab.figure(1)
        pylab.clf()
        for (prices, name) in price_array:
            pylab.plot(rhos, prices, label = name)
        pylab.xlabel('$' + '\\rho' + '$')
        pylab.ylabel('Premium')
        title = cds_mapping[cds_class]
        pylab.xlim([0,1])
        pylab.ylim([0,1])  
        pylab.suptitle(title, fontsize = 10)
        
        pylab.legend()    
        file_title = re.sub("[\s'$-]", "",  cds_mapping[cds_class] + str(payoff) )
                  
        pdf_file = "../../Diagrams/Copulas/" + file_title + ".pdf"
        print pdf_file
        pylab.savefig(pdf_file)
        

def MonteCarloVaR():
    """Create CSV and VaR Charts for Various Securities Tranches"""
    def VarAndPricePayoff(data, payoff, cds_class, calibrated_gamma, copula_class, rho, n_obligors, n_sims):
        """docstring for Pricing"""
        
        CDS = cds_class()
        cov = FlatCorrelationMatrix(rho, n_obligors)
        copula = copula_class(CDS, calibrated_gamma, cov, n_obligors)
        CopSim = CopulaSimulation(copula)

        MCSim = MonteCarloPricingSim(payoff, CopSim)
        return MCSim.VaR(n_sims)
    
    def SetupPayoffCopula(payoff, cds_class, copula_class, rhos, n_sims, n_obligors):
        """docstring for fname"""
        
        spreads = { 'Date' : '17/5/10', 
                    '1' : '350', 
                    '2' : '350', 
                    '5' : '400', 
                    '7' : '450', 
                    '10' : '600' 
                    }
        data = MarketData(spreads)
        
        if cds_class == HPCreditDefaultSwap:
            guess = [0.01]
        else:
            guess = [0.3, 0.8, 5, 0.02]
        
        calib = Calibration(DiscountCurve   = FlatDiscountCurve(r = 0.02), 
                            MarketData      = data,
                            CDS             = cds_class,
                            Guess           = guess,
                            )
        calib.Calibrate()
        calibrated_gamma = calib.calibrated_gamma 
        prices = []
        value_at_risks = []
        for rho in rhos:
            price, var = VarAndPricePayoff(data, 
                                payoff,
                                IGOUCreditDefaultSwap,
                                calibrated_gamma,
                                GaussianCopula,
                                rho,
                                n_obligors,
                                n_sims)
            prices.append(price)
            value_at_risks.append(price)
            
        return (prices, value_at_risks) 

    print_mapping = {   GaussianCopula : "Gaussian",
                        StudentTCopula : "Student's $t$"
                        }
    cds_mapping = {     HPCreditDefaultSwap : "HP", 
                        GammaOUCreditDefaultSwap : "Gamma-OU", 
                        IGOUCreditDefaultSwap: "Inverse Gaussian-OU"
                        }
    # Pairs of (payoff, n_obligors, n_sims)
    n_obligs = 100
    n_simus = 500
    payoff_specification = [(KthToLthTranche(k=0, l=3, n = n_obligs, T=5), n_obligs, n_simus), 
                            (KthToLthTranche(k=10, l=15, n = n_obligs, T=5), n_obligs, n_simus),    
                            (KthToLthTranche(k=30, l=100, n = n_obligs, T=5), n_obligs, n_simus),
                            # (KthToLthTranche(k = 10, l = 100, T=5), 20, 100),
                            ]
    rhos = np.linspace(0,1,5)
    
    for cds_class in [GammaOUCreditDefaultSwap, IGOUCreditDefaultSwap]:
        var_array = []
        for copula_class in print_mapping.keys():
            for (payoff, n_obligors, n_sims) in payoff_specification:
                prices, value_at_risks = SetupPayoffCopula(payoff, cds_class, copula_class, rhos, n_sims, n_obligors)
                name = str(payoff) + ", " + print_mapping[copula_class]
                var_array.append((value_at_risks, name))
                print name
                print value_at_risks
        
        pylab.figure(1)
        pylab.clf()
        print "DOING CDS CLASS PLOTS"
        for (var, name) in var_array:
            pylab.plot(rhos, var, label = name)
        pylab.xlabel('$' + '\\rho' + '$')
        pylab.ylabel('VaR')
        title = cds_mapping[cds_class]
        pylab.xlim([0,1])
        pylab.ylim([0,1])  
        pylab.suptitle(title, fontsize = 10)
        
        pylab.legend()    
        file_title = re.sub("[\\%\s'$-]", "",  cds_mapping[cds_class] + str(payoff) )
                  
        pdf_file = "../../Diagrams/Copulas/" + file_title + ".pdf"
        print pdf_file
        pylab.savefig(pdf_file)


        		# loc = mpl.dates.MonthLocator(1)
	# 		dateFmt = mpl.dates.DateFormatter('%b %y')
	# 		pylab.gca().xaxis.set_major_formatter(dateFmt)
	# 		#
	# 		pylab.gca().xaxis.set_major_locator(loc)
	#

	
    # pylab.suptitle(pretty_copula + " copula with " + process + " marginals", fontsize = 10)
# PlotBivariateCopula(uniforms = False, n_sim = 1000)
# PlotBivariateCopula(uniforms = True, n_sim = 2000)
# MonteCarloVaR()
# MonteCarloCorrelationSensitivities()