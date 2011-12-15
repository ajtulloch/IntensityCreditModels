import scipy.stats as stats
import numpy as np
import math

class MonteCarloBase(object):
    """docstring for MonteCarloSim"""
    def __init__(self, parameters, N, T):
        super(MonteCarloBase, self).__init__()
        self.parameters = parameters
        self.N = N
        self.T = T
        self.dt = float(T)/N

    def Simulation(self):
        """docstring for DefaultSimulation"""
        cumulated_intensity = 0
        process = []
        for i in range(self.N):
            increment = self.dLambda(cumulated_intensity)
            cumulated_intensity += increment
            process.append(cumulated_intensity)
        
        return process
        # threshold = stats.expon.rvs()
        # print threshold
        # while t < self.T:
        #     # print t
        #     cumulated_intensity += self.dLambda(cumulated_intensity)
        #     if cumulated_intensity > threshold:
        #         return t
        #     t += self.dt
        # return self.T
    
    def DefaultTime(self, threshold, simulation):
        """docstring for Default"""

        countdown = map(lambda x: math.exp(-x), simulation)
        # print countdown
        try:
            index = min(i for i, val in enumerate(countdown) if val < threshold)
            tau =  self.dt * index
        except:
            tau = 1000
            
        return tau 

class HPSim(MonteCarloBase):
    """docstring for HPSim"""
    def __init__(self, parameters, N, T):
        super(HPSim, self).__init__(parameters, N, T)
        

    def dLambda(self, cumulated_intensity):
        """docstring for DefaultSimulation"""
        gamma = self.parameters[0]
        increment = gamma * self.dt
        return increment
        
#------------------------------------------------------------------------------
   
class IGOUSim(MonteCarloBase):
    """docstring for HPSim"""
    def __init__(self, parameters, N, T):
        super(IGOUSim, self).__init__(parameters, N, T)
        
    def Simulation(self, cumulated_intensity):
        gamma, a, b, y_0 = self.parameters
    
        def ProcessGen(draws):
    
            res = [0.0] * N
    
            for i in range(len(draws)):
    
                res[i] = res[i-1] + draws[i]
    
            return res  
    
        def InverseGaussOU(gamma, a, b, y_0, N, T):
            """docstring for InverseGaussOU"""
            dt = float(T)/N
            # PRV process
            PRV = stats.poisson.rvs(a * b * dt / 2, size = N)
            Poisson = ProcessGen(PRV)
            POI = [int(i) for i in Poisson]
            # IG Process
            IVG = InverseGauss(a / 2 * dt, b, N)
            z_1 = ProcessGen(IVG)
            
            # Sum of normals
            norm_array = [];
            z_2 = [0.0] * len(POI);
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

        sim = InverseGaussOU(gamma, a, b, y_0, self.N, self.T)
        return sim
        
class GammaOUSim(MonteCarloBase):
    """docstring for GammaOUSim"""
    def __init__(self, parameters, N, T):
        super(GammaOUSim, self).__init__(parameters, N, T)
        
    def Simulation(self):
        gamma, a, b, y_0 = self.parameters
        def ProcessGen(draws):

            res = [0.0] * self.N

            for i in range(len(draws)):

                res[i] = res[i-1] + draws[i]

            return res
        def GammaOU(gamma, a, b, y_0, N, T):
            """docstring for GammaOU"""
            dt = float(T)/N
            PRV = stats.poisson.rvs(a * gamma * dt, size = N)
            print PRV
            Poisson = ProcessGen(PRV)
            POI = [int(i) for i in Poisson]
    
            norm_array = [];
            z   = [0.0] * len(POI);
            for i, n_i in enumerate(POI):
                if len(norm_array) != n_i:
                    normal = stats.expon.rvs(b)
                    norm_array.append(normal) 
                z[i] = sum(norm_array)
    
            res = [y_0] * N
            for i in range(len(z)):
                res[i] = -gamma * res[i-1] * dt + z[i]
            return res
        sim = GammaOU(gamma, a, b, y_0, self.N, self.T)
        return sim
    

#------------------------------------------------------------------------------

y = HPSim([0.1], 1000, 20)
sim = y.Simulation()
print y.DefaultTime(0.4, sim)

        