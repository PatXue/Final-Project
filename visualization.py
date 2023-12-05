from vpython import *
import numpy as np
from calculations import Simulation
from typing import Callable

arr_to_vector = lambda A: vector(A[0],A[1],A[2])

linear = lambda t: -1 * t + 1
def step(t: float):
    if t < 0.2:
        return 0.5
    elif t < 0.4:
        return -0.5
    else:
        return 0
torque_func: Callable[[float], float] = step

n: int = 20
m: float = 1
rest_len: float = 1
sim = Simulation(1000, 0.05, n, m, rest_len)
dt: float = 1e-4

scene = canvas(center=vector(rest_len/2,0,0))
pivot = box(pos=vector(0,0,0),size=vector(0.05,.1,.1),color=color.blue)

spheres = [sphere(pos=arr_to_vector(sim.pos_array[:,i]),radius=0.005,color=color.red) for i in range(n)]
# springs = [helix(radius=0.01,thickness=.004,coils=10,color=color.green)] * n

last_position = spheres[-1].pos

spheres[-1].trail = curve(color=color.green)

graph(title='Dynamic of Whips', xtitle='Time', ytitle='Velocity',xmax=5.50, ymax=15, ymin=0,
      x=0, y=500, width=500, height=300)

draw_velocity = gcurve(color=color.magenta,label='Velocity of Tail')

t: float = 0

step=0
print_vel = False

while (t < 5):
    rate(100)
    sim.step(dt, torque_func(t))

    step += 1

    for i in range(n):
        spheres[i].pos = arr_to_vector(sim.pos_array[:,i])

    spheres[-1].trail.append(pos=spheres[-1].pos)
    velocity_of_tail = sim.mom_array[:,-1] / sim.m
    draw_velocity.plot(pos=(t, np.linalg.norm(velocity_of_tail)))

    if print_vel and step % 10 == 0:
        print(np.linalg.norm(velocity_of_tail))
        #if i>1:
            #springs[i].pos = arr_to_vector(sim.pos_array[:,i]) - arr_to_vector(sim.pos_array[:,i-1]) 

        #elif i==1:
            #springs[i].pos = arr_to_vector(sim.pos_array[:,i]) - pivot.pos

    t += dt