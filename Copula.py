from scipy.stats import norm, chi2
from scipy.optimize import brentq
from numpy.random import multivariate_normal
from numpy import ones, eye
import math

#------------------------------------------------------------------------------

from CDS import *
from MarketData import *
from Calibration import *

#------------------------------------------------------------------------------

class CopulaBase(object):
    """docstring for Copula"""
    def __init__(self):
        abstract
    
    def Invert(self, y):
        """docstring for invert"""
        pass
        # print y

        # Hacky way to get around HP only accepting double for its survival probability
        if len(self.cds_parameter) == 1:
            cds_parameter = self.cds_parameter[0]
        else:
            cds_parameter = self.cds_parameter

        p_default = lambda x: 1 - self.CDS.SurvivalProbability(cds_parameter, x)
        f = lambda x: p_default(x) - y

        tau = brentq(f, 0, 200)
        return tau

      
#------------------------------------------------------------------------------


class GaussianCopula(CopulaBase):
    """docstring for GaussianCopula"""
    def __init__(self, CDS, cds_parameter, copula_parameter, size):
        # super(GaussianCopula, self).__init__()
        self.CDS = CDS
        self.copula_parameter = copula_parameter
        self.cds_parameter = cds_parameter
        self.size = size
        assert size == len(copula_parameter)
    
    
    def Simulate(self):
        """docstring for Simulate"""
        mean = [0.0] * self.size
        cov = self.copula_parameter
        Z = multivariate_normal(mean, cov)
        Y = map(norm.cdf, Z)
        T = map(self.Invert, Y)

        return T
        
        
class StudentTCopula(CopulaBase):
    """docstring for StudentTCopula"""
    def __init__(self, CDS, cds_parameter, copula_covariance, size, copula_degree_freedom = 5):
        # super(GaussianCopula, self).__init__()
        self.CDS = CDS
        self.copula_covariance = copula_covariance
        self.cds_parameter = cds_parameter
        self.dof = copula_degree_freedom
        self.size = size
        assert size == len(copula_covariance)

    def Simulate(self):
        """docstring for Simulate"""
        mean = [0.0] * self.size
        cov = self.copula_covariance
        
        s = chi2.rvs(self.dof)
        Z = multivariate_normal(mean, cov)
        Y = map(norm.cdf, Z)
        X = [math.sqrt(self.dof)/math.sqrt(s) * y for y in Y]
        T = map(self.Invert, Y)

        return T
    



#------------------------------------------------------------------------------

if __name__ == '__main__':

    spreads = {'Date' : '17/5/10', '1' : '350', '2' : '350', '5' : '400', '7' : '450', '10' : '600' }
    z = MarketData(spreads)
    
    
    IGOU = Calibration(   DiscountCurve   = FlatDiscountCurve(r = 0.03), 
                      MarketData      = z,
                      CDS             = IGOUCreditDefaultSwap,
                      Process         = "IG-OU",
                      Guess           = [0.3, 0.8, 5, 0.02],
                      )
    
    IGOU.Calibrate()

    calibrated_gamma = IGOU.calibrated_gamma 
    # calibrated_gamma = [  0.134919923,  0.217639626,  7.21669773,   0.00127923735]
    # 
    # calibrated_gamma = [0.1]


    # CDS = HPCreditDefaultSwap()
    CDS = IGOUCreditDefaultSwap()

    copula = GaussianCopula(CDS, calibrated_gamma, [[1, 0.88], [0.88, 1]], 2)
    copula.Simulate()
    copula = StudentTCopula(CDS, calibrated_gamma, [[1, 0.88], [0.88, 1]], 5, 2)
    copula.Simulate()


    

        