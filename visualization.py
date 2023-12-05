from vpython import *
import numpy as np
import pandas as pd
from calculations import Simulation
from typing import Callable


def linear(t: float) -> float:
    if t > 0.4: return 0
    else: return -1/0.4 * t + 1

def step(t: float) -> float:
    '''A square step down function'''
    if t < 0.2: return 0.5
    elif t < 0.4: return -0.5
    else: return 0

def impulse_gen(t_spacing: float) -> Callable[[float], float]:
    '''Returns a function that returns 2 instantaneous impulses
    
    --------
    ### Args:
        t_spacing (float): spacing between the two impulses
    '''
    global dt
    def impulse(t: float):
        if isclose(t, 0, abs_tol=dt/2): return 0.1/dt
        elif isclose(t, 0 + t_spacing, abs_tol=dt/2): return -0.1/dt
        else: return 0
    
    return impulse

def cosine(t: float):
    if t > 0.4: return 0
    else: return 0.5 * np.pi/2*np.cos(np.pi/0.4 * t)

func_table = {
    "step": step,
    "linear": linear,
    "cosine": cosine,
    "impulse (0.05s)": impulse_gen(0.05),
    "impulse (0.1s)": impulse_gen(0.1)
}

arr_to_vector = lambda A: vector(A[0],A[1],A[2])


n: int = 20
m: float = 1
rest_len: float = 1
dt: float = 1e-4
record_vel = False

if record_vel:
    data_table = pd.DataFrame(
        columns=["t"] + list(func_table.keys()),
        index=pd.RangeIndex(stop= np.ceil(1/dt)+1)
    )

    for func_name in data_table.columns[1:]:
        sim = Simulation(1000, 0.05, n, m, rest_len)
        torque_func = func_table[func_name]

        t: float = 0
        step: int = 0
        while (t < 1):
            velocity_of_tail = sim.mom_array[:,-1] / sim.m
            data_table.loc[step, func_name] = np.linalg.norm(velocity_of_tail)

            sim.step(dt, torque_func(t))

            t += dt
            step += 1
    
    data_table["t"] = data_table.index.to_series() * dt
    print(data_table)
    data_table.to_csv("output.csv", index=False)

else:
    sim = Simulation(1000, 0.05, n, m, rest_len)
    torque_func: Callable[[float], float] = step

    scene = canvas()
    pivot = sphere(pos=vector(0,0,0),radius=0.025,color=color.blue)

    spheres = [sphere(pos=arr_to_vector(sim.pos_array[:,i]),radius=0.005,color=color.red) for i in range(n)]

    last_position = spheres[-1].pos
    spheres[-1].trail = curve(color=color.green)

    graph(title='Dynamic of Whips', xtitle='Time', ytitle='Velocity',xmax=1, ymax=15, ymin=0,
        x=0, y=500, width=500, height=300)
    draw_velocity = gcurve(color=color.magenta,label='Velocity of Tail')

    t = 0
    while (t < 1):
        rate(500)
        sim.step(dt, torque_func(t))

        for i in range(n):
            spheres[i].pos = arr_to_vector(sim.pos_array[:,i])

        spheres[-1].trail.append(pos=spheres[-1].pos)
        velocity_of_tail = sim.mom_array[:,-1] / sim.m
        draw_velocity.plot(pos=(t, np.linalg.norm(velocity_of_tail)))

        if record_vel:
            pass

        t += dt