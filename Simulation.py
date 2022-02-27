import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from Particles import Particle


class Simulation():

    box_size = [20,20]

    def __init__(self, dt = 1E-2, N = 10):
        self.dt, self.N = dt, N
        self.particles = pd.DataFrame(np.array([np.zeros(5)]*N), columns=['positionX', 'positionY', 'velocityX', 'velocityY', 'mass'], dtype = float)
        # name property is a unique id of a particle


    # RANDOMNESS
    def randomiseInitial(self):
        for i in range(self.N):
            self.particles.iloc[i].positionX, self.particles.iloc[i].positionY = self.box_size[0] * (np.random.rand(1,2)[0] - 0.5)
            self.particles.iloc[i].velocityX, self.particles.iloc[i].velocityY = 1/2*self.box_size[0] * (np.random.rand(1,2)[0] - 0.5)


    # updates components of position and velocity using Euler method
    # def euler(self, dt):
    #     self.position = self.position + self.velocity * dt
    #     self.velocity = self.velocity + self.acceleration * dt

    # updates components of position and velocity using Euler-Cromer method

    def eulerCromer(self):

        for i in range(self.N):
            self.particles.iloc[i].positionX += self.particles.iloc[i].velocityX * self.dt
            self.particles.iloc[i].positionY += self.particles.iloc[i].velocityY * self.dt
    

    # updates components of position and velocity of a body using Verlet method
    
    # acceleration issue, can use???????????
    # def verlet(self):
    #     for i in range(self.N):
    #         self.particles.iloc[i].positionX += self.particles.iloc[i].velocityX * self.dt + 1/2 * accelerationInitial * (self.dt)**2


    # -/-/-/-/-
    # def rungeKutta(self, dt):
        
    #     k_1 = 

    #     self.velocity = self.velocity + 1/6 * dt * (k_1 + 2 * k_2 + 2* k_3 + k_4)


    # getters
    # def get_positions(self):
    #     return [particle.position for particle in self.particles]
    
    # def get_velocity(self):
    #     return [particle.velocity for particle in self.particles]



    # regulates which method was selected
    def advance(self, n):
        if n == 1:
            self.eulerCromer()
        # if n == 2:
        #     self.rungeKutta()




# initialise the object
simulation = Simulation()
simulation.randomiseInitial()
# particles properties
print(simulation.particles)



# plot graph

fig = plt.figure()

plt.xlim(-simulation.box_size[0]/2 , simulation.box_size[0]/2)
plt.ylim(-simulation.box_size[1]/2 , simulation.box_size[1]/2)

graph, = plt.plot([], [], 'o')


def initial():
    graph.set_data([], [])
    return graph,


def render(i):
    # change number for different methods
    simulation.advance(1)
    posX = list(simulation.particles['positionX'])
    posY = list(simulation.particles['positionY'])
    graph.set_data(posX, posY)
    return graph,


anim = FuncAnimation(fig, render, init_func=initial, interval=1/10, frames=range(1200), blit = True, repeat = False)

plt.show()