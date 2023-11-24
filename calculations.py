import numpy as np

class Simulation:
    ROT90 = np.array(
        [[0,-1, 0],
        [1, 0, 0],
        [0, 0, 1]]
    )

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

        self.pos_array = np.zeros((3,n))
        self.mom_array = np.zeros((3,n))

        # Array used for calculating position difference to determine
        # spring force
        # For the ith particle, used to calculate
        # r_i - r_{i-1} + r_i - r_{i+1}
        self.CALC_DIFF = np.diagflat(self.n * [2])
        self.CALC_DIFF += np.diagflat((self.n-1) * [-1], -1)  
        self.CALC_DIFF += np.diagflat((self.n-1) * [-1], 1)  
        self.CALC_DIFF[-1,-1] = 1 # Final particle is linked only on 1 side
        self.CALC_DIFF = self.CALC_DIFF.reshape((1,self.n,self.n))

    def calc_force(self, torque: float) -> np.ndarray:
        '''Calculates the force on each particle based on the current particles'
        position

        -------
        ### Args:
            torque (float): torque to apply to first chain in segment (Nm)

        -------
        ### Returns:
            np.ndarray: 3xn array of floats holding the calculated net force
            vector on each particle
        '''
        pos_diff = np.einsum("ij,ijk->ik", self.pos_array, self.CALC_DIFF)
        spring_force = -self.k * pos_diff

        first_pos = self.pos_array[:,0] # Position of first chain
        radius = np.linalg.norm(first_pos)
        transverse = self.ROT90 @ (first_pos / radius)

        torque_force = np.zeros((3,self.n))
        torque_force[:,0] = torque/radius * transverse

        return spring_force + torque_force

    def step(self, dt: float, torque: float=0.0) -> None:
        '''Does physics calculations for one timestep.
        Called by visualization.ipynb

        -------
        ### Args:
            dt (float): size of timestep (seconds)
            torque (float): torque to apply to first chain in segment (Nm)
        '''
        self.mom_array += self.calc_force(torque) * dt
        self.pos_array += (self.mom_array / self.m) * dt
        
        self.time += dt