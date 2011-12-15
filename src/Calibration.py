import scipy.optimize as optimize
from math import sqrt

#------------------------------------------------------------------------------

from CreditDerivativeCSVReader import *
from CDS import *
from DiscountCurve import *
from MarketData import *

#------------------------------------------------------------------------------

class Calibration(object):
    """Defines a class for the calibration of CDS objects.
    
    Input a CDS class, a DiscountCurve object, and a MarketData object, 
    along with an initial guess for parameters, and the Calibration object
    can then be used to calibrate the CDS intensity process to market data.
    """
    def __init__(self, DiscountCurve = FlatDiscountCurve(r = 0.0), \
            MarketData = None, Method = "nm", CDS = None, Process = None, \
            Guess = None):
        super(Calibration, self).__init__()
        self.DiscountCurve = DiscountCurve
        self.R = 0.4
        self.CDS = CDS
        self.Process = Process
        self.Guess = Guess
        self.Method = Method
        if MarketData is not None:
            self.SetMarketData(MarketData)
    
    def SetMarketData(self, MarketData):
        """docstring for SetMarketData"""
        self.MarketData = MarketData
    
    def ObjectiveFunction(self, gamma):
        """Calculates the error in estimation for use in our calibration
        routines.  
        
        Currently we use the L^2 norm."""

        sum = 0
        for t, market_spread in self.MarketData.Data():
            CDS = self.CDS( DiscountCurve = self.DiscountCurve,
                            maturity = t)
            model_spread = CDS.ParSpread(gamma)     
            sum += (model_spread - market_spread) ** 2
        return sum

    def Calibrate(self, method = 'nm'):
        """Performs the calibration and returns the optimal parameters.  
        
        The built in Optimise method in SciPy uses Nelder-Mead optimisation."""
        methods = { 'nm'        : optimize.fmin, 
                    'powell'    : optimize.fmin_powell,
                    'cg'        : optimize.fmin_cg,
                    'bfgs'      : optimize.fmin_bfgs
                    }
        
        if method == None:
            optimise = methods[self.Method]
        else:
            optimise = methods[method]
        
        output = optimise(  self.ObjectiveFunction, 
                            self.Guess, 
                            disp = 0
                            )
        self.calibrated_gamma = output
        return output
    
    def RMSE(self):
        """Returns the RMSE for the calibrated parameters."""
        N = len(self.MarketData.Tenors())
        return sqrt(self.ObjectiveFunction(self.calibrated_gamma) / N)

    def CalibrationResults(self):
        """Outputs our calibration results."""  
        print "-" * 80
        print "Calibration results for %s on %s" \
                % (self.Process, self.MarketData.Date())
        print ""
        N = len(self.MarketData.Tenors())
        string = self.Process
        sum = 0
        for t, market_spread in sorted(self.MarketData.Data()):
            CDS = self.CDS( DiscountCurve = self.DiscountCurve, 
                            maturity = t
                            )
            model_spread = CDS.ParSpread(self.calibrated_gamma)     
            if type(model_spread).__name__ == 'ndarray':
                model_spread = model_spread[0]
                                
            survival_probability = \
                CDS.SurvivalProbability(self.calibrated_gamma, t) * 100
            print   "Tenor: %.1f\t Market: %.0f\t Model Spread: %.0f\t Survival Probability: %.1f" \
                    %(t, market_spread, model_spread, survival_probability) 
            # string += "\t&\t%.0f" % model_spread
            sum += (model_spread - market_spread) ** 2

        RMSE = sqrt(sum/N)
        print "RMSE: ", RMSE
        # string += "\t&\t%.2f\t&\t\\\\" % RMSE
        # print string
        return None 
        
    def PrintParameters(self):
        """Prints parameters for formatting in a LaTeX table."""
        string = ""
        for i, param in enumerate(self.calibrated_gamma):
            string += "\t&\t$\lambda_%s = %.4f$\t" %(i, param)
        string += "\t\\\\"
        return string
#------------------------------------------------------------------------------

class InhomogenousCalibration(Calibration):
    """As the IHP process requires us to specify the tenors for the calibration,
    we must modify the __init__(), ObjectiveFunction(), and Calibrate() methods 
    to correctly account for this."""
    def __init__(self, DiscountCurve = FlatDiscountCurve( r = 0 ), \
            MarketData = None, Method = "nm"):
        super(InhomogenousCalibration, self).__init__(DiscountCurve, MarketData, Method)
        self.Process = "IHP"
        self.CDS = IHPCreditDefaultSwap
        
    def SetMarketData(self, MarketData):
        """docstring for SetMarketData"""
        self.MarketData = MarketData
        self.tenors = MarketData.Tenors()
        self.N = len(MarketData.Tenors())
        self.Guess = [ 0.01 ] * self.N
    
    def ObjectiveFunction(self, gamma):
        """Calculates the error in estimation for use in our calibration
        routines.  
        
        Currently we use the L^2 norm."""
        sum = 0
        for t, market_spread in self.MarketData.Data():
            CDS = IHPCreditDefaultSwap( tenors = sorted(self.MarketData.Tenors()), 
                                        DiscountCurve = self.DiscountCurve,
                                        maturity = t)
            model_spread = CDS.ParSpread(gamma)     
            sum += (model_spread - market_spread) ** 2
        return sum
        
    def CalibrationResults(self):
        """Outputs our calibration results."""  
        print "-" * 80
        print "Calibration results for Inhomogenous Poisson on %s" %(self.MarketData.Date())
        print ""
        N = len(self.MarketData.Tenors())
        sum = 0
        for t, market_spread in sorted(self.MarketData.Data()):
            CDS = IHPCreditDefaultSwap( tenors = sorted(self.MarketData.Tenors()), 
                                        DiscountCurve = self.DiscountCurve, 
                                        maturity = t
                                        )
            model_spread = CDS.ParSpread(self.calibrated_gamma) 
            index = sorted(self.MarketData.Tenors()).index(t)
            gamma = self.calibrated_gamma[index]
            probability = CDS.SurvivalProbability( self.calibrated_gamma, t)*100
            print "Tenor: %s\t Market: %.0f\t Model Spread: %.0f\t Gamma: %.5f\t Survival Probability: %.1f" \
                    % (t, market_spread, model_spread, gamma, probability)
            sum += (model_spread - market_spread) ** 2
        
        RMSE = sqrt(sum/N)
        print "RMSE: ", RMSE
        return RMSE

#------------------------------------------------------------------------------

if __name__ == '__main__':  
    y = CreditDerivativeCSVReader( file = "../Data/CDX.csv")
    date = y.Dates()[-1]
    data = y.TimeSlice(date)
    z = MarketData(data)
    # print z.Data()
    # print z.Date()
    
    HP = Calibration(   DiscountCurve   = FlatDiscountCurve(r = 0.00), 
                        MarketData      = z,
                        CDS             = HPCreditDefaultSwap,
                        Process         = "HP",
                        Guess           = [0.01],
                        )

    CIR = Calibration(  DiscountCurve   = FlatDiscountCurve(r = 0.00), 
                        MarketData      = z,
                        CDS             = CIRCreditDefaultSwap,
                        Process         = "CIR",
                        Guess           = [0.1, 0.3, 0.2, 0.02],
                        )
                                        
                                        
    IHP = InhomogenousCalibration( \
                        DiscountCurve   = FlatDiscountCurve(r = 0.00), 
                        MarketData      = z,
                        )
    
    GOU = Calibration(  DiscountCurve   = FlatDiscountCurve(r = 0.00), 
                        MarketData      = z,
                        CDS             = GammaOUCreditDefaultSwap,
                        Process         = "G-OU",
                        Guess           = [0.2, 189, 10000, 0.002],
                        )
                        
    IGOU = Calibration( DiscountCurve   = FlatDiscountCurve(r = 0.00), 
                        MarketData      = z,
                        CDS             = IGOUCreditDefaultSwap,
                        Process         = "IG-OU",
                        Guess           = [0.3, 0.8, 5, 0.02],
                        )
    
    for Credit in [HP, IHP, GOU, IGOU, CIR]:
        Credit.Calibrate()
        Credit.CalibrationResults()
        
        