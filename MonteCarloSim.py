import scipy.stats as stats

class MonteCarloBase(object):
    """docstring for MonteCarloSim"""
    def __init__(self, parameters, N, T):
        super(MonteCarloBase, self).__init__()
        self.parameters = parameters
        self.N = N
        self.T = T
        self.dt = float(T)/N

    def DefaultSimulation(self):
        """docstring for DefaultSimulation"""
        cumulated_intensity = 0 
        t = 0
        threshold = stats.expon.rvs()
        print threshold
        while t < self.T:
            # print t
            cumulated_intensity += self.dLambda(cumulated_intensity)
            if cumulated_intensity > threshold:
                return t
            t += self.dt
        return self.T
    
class HPSim(MonteCarloBase):
    """docstring for HPSim"""
    def __init__(self, parameters, N, T):
        super(HPSim, self).__init__(parameters, N, T)
        

    def dLambda(self, cumulated_intensity):
        """docstring for DefaultSimulation"""
        gamma = self.parameters[0]
        increment = gamma * self.dt
        return increment
        
# class IGOUSim(MonteCarloBase):
#     """docstring for HPSim"""
#     def __init__(self, parameters, N, T):
#         super(IGOUSim, self).__init__(parameters, N, T)
#         
#     def dLambda(self, cumulated_intensity):
#         gamma, a, b, y_0 = self.parameters
#         increment = self.
    
#------------------------------------------------------------------------------

y = HPSim([0.1], 1000, 10)
print y.DefaultSimulation()
    
        