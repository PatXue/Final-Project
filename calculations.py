import numpy as np

class Simulation:
    def __init__(self, k: float, n: int, m: float, rest_len: float) -> None:
        '''
        Create instance of Simulation class

        -------
        ### Args:
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

        # Array used for calculating position difference to determine
        # spring force
        # For the ith particle, used to calculate
        # r_i - r_{i-1} + r_i - r_{i+1}
        self.CALC_DIFF = np.diagflat(self.n * [2])
        self.CALC_DIFF += np.diagflat((self.n-1) * [-1], -1)  
        self.CALC_DIFF += np.diagflat((self.n-1) * [-1], 1)  
        self.CALC_DIFF[-1,-1] = 1 # Final particle is linked only on 1 side
        self.CALC_DIFF = self.CALC_DIFF.reshape((1,self.n,self.n))

    def calc_force(self) -> np.ndarray:
        '''Calculates the force on each particle based on the current particles'
        position

        -------
        ### Returns:
            np.ndarray: 3xn array of floats holding the calculated net force
            vector on each particle
        '''
        pos_diff = np.einsum("ij,ijk->ik", self.pos_array, self.CALC_DIFF)
        spring_force = -self.k * pos_diff
        return spring_force

    def step(self, dt: float) -> None:
        '''Does physics calculations for one timestep.
        Called by visualization.ipynb

        -------
        ### Args:
            dt (float): size of timestep (seconds)
        '''
        self.mom_array += self.calc_force() * dt
        self.pos_array += (self.mom_array / self.m) * dt
        
        self.time += dt