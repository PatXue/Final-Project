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
            k (float): total spring constant of entire rope
            n (int): number of chains
            m (float): total mass of rope
            rest_len (float): rest length of rope
        '''
        
        self.k = n*k
        self.n = n
        self.m = m/n
        self.rest_len = rest_len/n

        self.time = 0.0

        self.pos_array = np.zeros((3,n))
        self.pos_array[0,:] = self.rest_len * (np.arange(n) + 1)
        self.mom_array = np.zeros((3,n))
        self.force_array = np.zeros((3,n))

        # Array used for calculating position difference to determine
        # spring force
        # For the ith particle, used to calculate
        # r_i - r_{i-1}
        self.CALC_DIFF = np.diagflat(self.n * [1])
        self.CALC_DIFF += np.diagflat((self.n-1) * [-1], 1)  
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
        # Equilibrium position of each particle pair
        equil_array = pos_diff * self.rest_len / np.linalg.norm(pos_diff, axis=0)

        spring_force = -self.k * (pos_diff - equil_array)
        # Use Newton's third law to get force on other particle in each pair
        spring_force[:,:-1] -= spring_force[:,1:]

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
        self.force_array = self.calc_force(torque)
        self.mom_array += self.force_array * dt
        self.pos_array += (self.mom_array / self.m) * dt
        
        self.time += dt