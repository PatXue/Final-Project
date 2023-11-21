import numpy as np

class Simulation:
    def __init__(self, k: float, n: int) -> None:
        '''Create instance of Simulation class
        
        Args:
            k (float): spring constant of each chain
            n (int): number of chains
        '''
        
        self.k = k
        self.n = n

    def step(self) -> None:
        '''Does physics calculations for one timestep.
        Called by visualization.ipynb'''