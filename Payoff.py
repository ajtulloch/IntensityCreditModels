import numpy as np
from scipy.stats import scoreatpercentile

#------------------------------------------------------------------------------

from DiscountCurve import *
from Copula import *
from CDS import *
from MarketData import *
from Calibration import *
from CopulaSimulation import *

#------------------------------------------------------------------------------

class Payoff(object):
    """docstring for Payoff"""
    def __init__(self, DiscountCurve):
        """docstring for __init__"""
        self.DiscountCurve = DiscountCurve
    
    def Payoff(self, taus):
        """docstring for Payoff"""
        pass
    
#------------------------------------------------------------------------------
        
class KthToDefault(Payoff):
    """Pays of a sum of 1 at time t is the k-th default in the basket occurs at
    time t < T.  Pays off nothing otherwise"""
    def __init__(self, k, T, DiscountCurve = FlatDiscountCurve(r=0.00)):
        super(KthToDefault, self).__init__(DiscountCurve)
        self.T = T
        self.k = k
     
    def __str__(self):
        """docstring for __str__"""
        if self.k == 1:
            return "1st to Default"
        elif self.k == 2:
            return "2nd to Default"
        else:
            return str(self.k) + "th to Default"   
        
    def Payoff(self, taus):
        """docstring for Payoff"""
        sorted_taus = np.sort(taus)
        k = self.k
        if len(sorted_taus) < k:
            value = 0     
        elif sorted_taus[k-1] < self.T:
            t = sorted_taus[k-1]
            value = self.DiscountCurve.DF(0, t)            
        else:
            value = 0   
        return value
   
class KthToLthTranche(Payoff):
    """Pays off 0 if less than k defaults occur, pays l-k if more than l defaults
    occur, and pays (x-k) if k <= x < l defaults occur"""
    def __init__(self, k, l, n, T, DiscountCurve = FlatDiscountCurve(r=0.00)):
        super(KthToLthTranche, self).__init__(DiscountCurve)
        self.T = T
        self.k = k
        self.l = l
        self.n = n
        assert k < l

    def __str__(self):
        """docstring for __str__"""
        lower_percent = int(float(self.k) / self.n * 100)
        upper_percent = int(float(self.l) / self.n * 100)
        return str(lower_percent) + "\%-" + str(upper_percent) + "\%"

    def Payoff(self, taus):
        """docstring for Payoff"""
        defaults_before_t = sum(map(lambda x: x < self.T, taus))
        if defaults_before_t > self.l:
            value = self.l - self.k
        elif defaults_before_t < self.k:
            value = 0
        else:
            value = defaults_before_t - self.k
        return float(value) / (self.l - self.k)
     
#------------------------------------------------------------------------------

class MonteCarloPricingSim(object):
    """docstring for MonteCarloPricingSim"""
    def __init__(self, payoff, copula_simulation):
        self.payoff = payoff
        self.copula_simulation = copula_simulation
        
    def Price(self, n_sim):
        """docstring for fname"""
        # Simulate default times $tau_i$
        taus = self.copula_simulation.Simulation(n_sim)
        # print taus
        payoffs = map(lambda x: self.payoff.Payoff(x), taus)
        # print payoffs
        price = float(sum(payoffs)) / n_sim
        return price
        
    def VaR(self, n_sim, percentile = 0.95):
        """docstring for VaR"""
        taus = self.copula_simulation.Simulation(n_sim)
        payoffs = map(lambda x: self.payoff.Payoff(x), taus)
        price = float(sum(payoffs)) / n_sim
        var = scoreatpercentile(payoffs, percentile)
        return (price, var)
        
        
    def AdjustCorrelation(self, new_rho):
        """docstring for AdjustCorrelation"""
        size = self.copula_simulation.copula.size
        cov = FlatCorrelationMatrix(new_rho, size)
        self.copula_simulation.copula.copula_parameter = cov
        # print self.copula_simulation.copula.copula_parameter
        return True
        
        
#------------------------------------------------------------------------------
if __name__ == '__main__':
    rho = 0.5
    guess = [0.3, 0.8, 5, 0.02]
    size = 2
    copula_class = GaussianCopula

    spreads = { 'Date' : '17/5/10', 
                '1' : '350', 
                '2' : '350', 
                '5' : '400', 
                '7' : '450', 
                '10' : '600' 
                }
    data = MarketData(spreads)

    calib = Calibration(    DiscountCurve   = FlatDiscountCurve(r = 0.02), 
                            MarketData      = data,
                            CDS             = IGOUCreditDefaultSwap,
                            Guess           = guess,
                            )
    calib.Calibrate()
    calibrated_gamma = calib.calibrated_gamma 
    CDS = IGOUCreditDefaultSwap()
    cov = FlatCorrelationMatrix(rho, size)

    copula = copula_class(CDS, calibrated_gamma, cov, size)
    CopSim = CopulaSimulation(copula)

    C = KthToDefault(k = 1, T = 10)
    D = KthToLthTranche(k=4, l = 6, T = 10)

    # Y = MonteCarloPricingSim(C, CopSim)
    print Y.Price(10000)
    Y.AdjustCorrelation(0.8)
    print Y.Price(10000)
    Defaults = [1, 2, 5, 7, 9, 15]
    print C.Payoff(Defaults)
    print D.Payoff(Defaults)
