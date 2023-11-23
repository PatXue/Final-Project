import numpy as np

class Simulation:
    def __init__(self, k: float, n: int, m: float, rest_len: float) -> None:
        '''Create instance of Simulation class
        
        Args:
            k (float): spring constant of each chain
            n (int): number of chains
            m (float): mass of each chain
            rest_len (float): rest length of each chain
        '''
        
        self.k = k
        self.n = n
        self.m = m
        self.rest_len = rest_len

        self.time = 0.0

        self.pos_array = np.ndarray((3,n))
        self.mom_array = np.ndarray((3,n))

    def calc_force(self) -> np.ndarray:
        '''Returns the force on each particle based on the current particles'
        position as an ndarray of floats'''
        return np.zeros((3,self.n))
        

    def step(self, dt: float) -> None:
        '''Does physics calculations for one timestep.
        Called by visualization.ipynb'''

        self.mom_array += self.calc_force() * dt
        self.pos_array += (self.mom_array / self.m) * dt
        
        self.time += dt