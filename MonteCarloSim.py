class MonteCarloBase(object):
    """docstring for MonteCarloSim"""
    def __init__(self, parameters, N, T):
        super(MonteCarloSim, self).__init__()
        self.parameters = parameters
        self.N = N
        self.T = T
    
    
class HPSim(object):
    """docstring for HPSim"""
    def __init__(self, parameters, N, T):
        super(HPSim, self).__init__(parameters, N, T)
        

    def DefaultSimulation(self):
        """docstring for DefaultSimulation"""
        