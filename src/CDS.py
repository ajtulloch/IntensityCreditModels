from numpy import arange, arctanh
from scipy import derivative
from scipy.integrate import quad
from math import exp, sqrt, cosh, sinh, log, tanh
 
# from __future__ import division

from CreditDerivativeCSVReader import *
from DiscountCurve import *

#------------------------------------------------------------------------------

def coth(x):
    """docstring for coth"""
    return 1 / tanh(x)

#------------------------------------------------------------------------------

class CreditDefaultSwap(object):
    """Abstract base class for CDS object.  Implements the PaymentDates(),
    ParSpread(), and ContinuousParSpead() methods.
    
    To use this, subclass and implement the SurivivalProbability() method."""
    def __init__(self, maturity = None, DiscountCurve = None, spread = None):
        super(CreditDefaultSwap, self).__init__()
        self.maturity = maturity
        self.spread = 0.1
        self.DiscountCurve = DiscountCurve
        self.R = 0.4
                    
    def PaymentDates(self):
        """Returns array containing quarterly payment dates."""
        dates = arange( 0, self.maturity, 0.25)
        return dates
        
    def ParSpread(self, parameters):
        """Returns the CDS par spreads"""
        dates = self.PaymentDates()
        
        prot_leg = 0
        loss_leg = 0
        # Calculate par spread using formula provided in thesis.
        for date in dates:
            t_start = date
            t_end = date + 0.25
            prot_leg =  self.DiscountCurve.DF(0, t_end) * \
                        ( self.SurvivalProbability(parameters, t_start) - \
                        self.SurvivalProbability(parameters, t_end))
            loss_leg = self.DiscountCurve.DF(0, t_end) * \
                        self.SurvivalProbability( parameters, t_end) * 0.25

        par_spread = (1 - self.R) * prot_leg / loss_leg
        # Par spread is expressed in basis points (bps)
        ps = par_spread * 10000
        
        return ps
    
    def SurvivalProbability(self):
        """Returns P(tau > t) - the probability that the entity survives past
        time t"""
        abstract
        
    def ContinuousParSpread(self, parameters):
        surv_prob   = lambda t: self.SurvivalProbability(parameters, t)
        numerator   = lambda t: self.DiscountCurve.DF(0, t) * \
                        derivative( surv_prob, t, dx = 0.0001)
        denominator = lambda t: self.DiscountCurve.DF(0, t) * \
                        self.SurvivalProbability(parameters, t) 
        
        cts_ps = (1 - self.R) * -quad(numerator, 0, self.maturity)[0] \
                    / quad(denominator, 0, self.maturity)[0] * 10000
        
        return cts_ps
        
#------------------------------------------------------------------------------

class HPCreditDefaultSwap(CreditDefaultSwap):
    """Intensity is a constant gamma > 0."""
    def __init__(self, maturity = None, DiscountCurve = None, spread = 0.100):
        super(HPCreditDefaultSwap, self).__init__(  maturity, 
                                                    DiscountCurve, 
                                                    spread,
                                                    )
    
    def SurvivalProbability(self, gamma, t):
        return exp( - gamma * t)
                
    def ParSpread(self, gamma):
        """Returns the par spread for a CDS
        where the intensity of default is a Poisson process
        with parameter gamma"""
        
        par_spread = (1-self.R) * gamma
        return par_spread * 10000

#------------------------------------------------------------------------------     

class IHPCreditDefaultSwap(CreditDefaultSwap):
    """Itensity is piecewise constant between maturities"""
    def __init__(self,  tenors = None, maturity = None, \
                    DiscountCurve = None, spread = 0.100):
        super(IHPCreditDefaultSwap, self).__init__( maturity, 
                                                    DiscountCurve, 
                                                    spread,)
        self.tenors = tenors
        
    def SurvivalProbability(self, gammas, t):
        def Gamma(gammas, tenors, t):
            """Calculates hazard process \int_0^t gamma_u \, du.
            
                >>>Gamma([1,1,1], [1,2,3], 3)
                3
            """ 
            assert (len(gammas) == len(tenors))
            sum = 0
            i = 0
            for i in range(len(tenors)):
                tenor_t = tenors[i]
                gamma_t = gammas[i]
                if t >= tenors[i]:
                    if i == 0:
                        sum += gammas[i] * tenors[i]
                    else:
                        sum += gammas[i] * (tenors[i] - tenors[i-1])
                else:
                    if i == 0:
                        sum += gammas[i] * t
                    else:
                        sum += gammas[i] * (t - tenors[i-1])
                    break
                    # sum += gammas[i] * (t - tenors[i-1])
                # if t < tenors[i]:
                #   sum += gammas[i] * (t - tenors[i-1])
                #   break
            # print "Gammas: %s, Tenors: %s, t: %s" %(gammas, tenors, t)
            # print "Cululated gamma: ", sum
            return sum
    
        cumulated_intensity = -Gamma(gammas, self.tenors, t)
        return exp(cumulated_intensity)
        
#------------------------------------------------------------------------------

class CIRCreditDefaultSwap(CreditDefaultSwap):
    """docstring for OUCreditDefaultSwap"""
    def __init__(self, maturity = None,  DiscountCurve = None, spread = 0.100):
        super(CIRCreditDefaultSwap, self).__init__(maturity, DiscountCurve, \
                                                    spread = 0.100)

    def SurvivalProbability(self, parameters, t):
        """Solves \phi_{CIR}(i, t; \kappa, \nu, \zeta, \gamma_0)
        Parameters: [ kappa, nu, zeta, gamma]"""
        assert( len(parameters) == 4)
        kappa, nu, vega, lamb = parameters
        
        if t == 0.0:
            probability = 1
        else:   
            gamma = sqrt( kappa** 2 + 2 * lamb ** 2)
            probability =  1 - ( exp( kappa ** 2 * nu * t / vega ** 2 ) * \
                        exp( -2 * lamb/(kappa + gamma * coth(gamma * t / 2)))) \
                         / ( coth( gamma * t / 2) \
                         + kappa * sinh( gamma * t / 2) / gamma) \
                         ** (2 * kappa * nu / vega ** 2) 
            
        
        return probability

#------------------------------------------------------------------------------
        
class GammaOUCreditDefaultSwap(CreditDefaultSwap):
    """Intensity follows a Gamma-OU process"""
    def __init__(self, maturity = None,  DiscountCurve = None, spread = 0.100):
        super(GammaOUCreditDefaultSwap, self).__init__(maturity, \
                                                DiscountCurve, spread = 0.100)
    
    def SurvivalProbability(self, parameters, t):
        """Parameters: [ vega, a, b, y ]"""
        assert( len(parameters) == 4)
        vega, a, b, y = parameters
        prob = exp( -y / vega * (1 - exp(-vega * t)) - \
            ((vega * a) / (1 + vega * b)) * \
            ( b * log( b / (b + 1/vega * (1 - exp(-vega * t)))) + t))
        
        return prob
        
        
#------------------------------------------------------------------------------

class IGOUCreditDefaultSwap(CreditDefaultSwap):
    """Intensity follows an Inverse Gaussian-OU process"""
    def __init__(self, maturity = None,  DiscountCurve = None, spread = 0.100):
        super(IGOUCreditDefaultSwap, self).__init__(maturity, 
                                                    DiscountCurve, 
                                                    spread = 0.100)
    
    def SurvivalProbability(self, parameters, t):
        """Parameters: [ vega, a, b, y ]"""
        assert( len(parameters) == 4)
        vega, a, b, y = parameters
        def function_A(vega, a, b, t):
            """Helper function A(t) defined in thesis."""
            kappa = 2 * b ** (-2) / vega
            val = (1 - sqrt( 1 + kappa * (1 - exp( -vega * t )))) \
                / kappa + 1 / sqrt( 1 + kappa) \
                * (arctanh( sqrt( 1 + kappa * ( 1 - exp( -vega * t)))/ \
                sqrt(1 + kappa)) - arctanh(1 / sqrt( 1 + kappa))) 
            return val
            
        x = function_A(vega, a, b, t)
            
        val = exp( -y / vega * (1 - exp( -vega * t)) - 2 * a / (b * vega) * x )
        return val
        
#------------------------------------------------------------------------------

if __name__ == '__main__':
    print "HP"
    y = HPCreditDefaultSwap(    DiscountCurve = FlatDiscountCurve(r = 0.00),
                                maturity = 2,
                                )
    print y.ParSpread(0.018)
    print y.ContinuousParSpread(0.018)
    
    print "IHP"
    z = IHPCreditDefaultSwap(   DiscountCurve = FlatDiscountCurve(r = 0.00),
                                maturity = 2,
                                tenors = [1,2,3,5,7,10],
                                )
    print z.ParSpread([0.018, 0.018, 0.018, 0.018, 0.1, 0.2])
    print z.ContinuousParSpread([ 0.018, 0.018, 0.018, 0.018, 0.1, 0.2])
    
    print "G-OU"
    y = GammaOUCreditDefaultSwap(   DiscountCurve = FlatDiscountCurve(r = 0.00),
                                    maturity = 2,
                                )
    
    print y.ParSpread([ 0.2, 189, 10000, 0.002])
    print y.ContinuousParSpread([0.2, 189, 10000, 0.002])
    
    print "IG-OU"
    y = IGOUCreditDefaultSwap(  DiscountCurve = FlatDiscountCurve(r = 0.00),
                                maturity = 2,
                                )
    
    print y.ParSpread([ 0.3, 0.8, 5, 0.02])
    print y.ContinuousParSpread([ 0.3, 0.8, 5, 0.02])
    
    print "CIR"
    y = CIRCreditDefaultSwap(   DiscountCurve = FlatDiscountCurve(r = 0.00),
                                maturity = 2,
                                )
    
    print y.ParSpread([ 0.1, 0.3, 0.2, 0.02])
    print y.ContinuousParSpread([ 0.1, 0.3, 0.2, 0.02])

        