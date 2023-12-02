from vpython import *
import numpy as np
from calculations import Simulation

arr_to_vector = lambda A: vector(A[0],A[1],A[2])

n = 10
m = 1
rest_len = 1
sim = Simulation(500, n, m, rest_len)
dt = 1e-3

scene = canvas(center=vector(rest_len/2,0,0))
pivot = box(pos=vector(0,0,0),size=vector(0.05,.1,.1),color=color.blue)

spheres = [sphere(pos=arr_to_vector(sim.pos_array[:,i]),radius=0.025,color=color.red) for i in range(n)]

# springs = [helix(radius=0.01,thickness=.004,coils=10,color=color.green)] * n

lastPosition = spheres[n-1].pos

spheres[n-1].trail = curve(color=color.red)

t = 0

while (t < 10):
    rate(100)
    sim.step(dt, 1)
    
    for i in range(n):
       
        spheres[i].pos = arr_to_vector(sim.pos_array[:,i])
        
    spheres[n-1].trail.append(pos=spheres[n-1].pos)
  
    velocityOfTail = (spheres[n-1].pos - lastPosition) / dt
    lastPosition = spheres[n-1].pos
    print(velocityOfTail,mag(velocityOfTail))
            
        #if i>1:
            #springs[i].pos = arr_to_vector(sim.pos_array[:,i]) - arr_to_vector(sim.pos_array[:,i-1]) 

        #elif i==1:
            #springs[i].pos = arr_to_vector(sim.pos_array[:,i]) - pivot.pos

    t += dt