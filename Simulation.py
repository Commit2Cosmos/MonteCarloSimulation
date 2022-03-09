import sys
sys.dont_write_bytecode = True
import numpy as np
# import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from Particles import Particle



class Simulation():

    box_size = [20,20]

    xLim = box_size[0]/2
    yLim = box_size[1]/2

    time = 0
    
    # CONSTANTS
    R = 1


    def __init__(self, dt = 1E-2, N = 20):
        self.dt, self.N = dt, N
        self.particles = pd.DataFrame(np.array([np.zeros(6)]*N), columns=['positionX', 'positionY', 'velocityX', 'velocityY', 'mass', 'radius'], dtype = float)
        # name property is a unique id of a particle


    # RANDOMNESS
    def randomiseInitial(self):
        for i in range(self.N):
            para = self.particles.iloc[i]
            para.positionX, para.positionY = 2 * self.xLim * (np.random.rand(1,2)[0] - 0.5)
            para.velocityX, para.velocityY = self.yLim * (np.random.rand(1,2)[0] - 0.5) * 3
            para.mass = 1
            para.radius = 0.25


    # updates components of position and velocity using Euler-Cromer method

    def eulerCromer(self):
        self.wallCollision()
        for i in range(self.N):
            para = self.particles.iloc[i]
            para.positionX += para.velocityX * self.dt
            para.positionY += para.velocityY * self.dt
    

    

    def wallCollision(self):
        for i in range(self.N):
            para = self.particles.iloc[i]
            if (((para.positionX > self.xLim - para.radius) and (para.velocityX > 0)) or ((para.positionX < -self.xLim + para.radius) and (para.velocityX < 0))):
                para.velocityX *= -1
            if (((para.positionY > self.yLim - para.radius) and (para.velocityY > 0)) or ((para.positionY < -self.yLim + para.radius) and (para.velocityY < 0))):
                para.velocityY *= -1


    # Classical two particle collision (ignores > 2 particles collisions in one timestep)


    # def particleCollision(self):
    #     collided = []
    #     for i in range(self.N):
    #         para1 = self.particles.iloc[i]

    #         for j in range(self.N):
    #             para2 = self.particles.iloc[j]
                
    #             # check so particle doesn't collide with itself
    #             if (i == j):
    #                 continue

    #             # checks if particle already collided in current iteration
    #             if para1.name in collided or para2.name in collided:
    #                 continue
                
                

    



    def calculateTotalSpeedSquared(self):
        totalSpeedSquared = 0
        for i in range(self.N):
            # calculate speed
            speed = self.particles.iloc[i].velocityX**2 + self.particles.iloc[i].velocityY**2
            totalSpeedSquared += speed
        rmsSquared = totalSpeedSquared/self.N
        return rmsSquared


    def calculateTemp(self):
        rmsSquared = self.calculateTotalSpeedSquared()

        totalMass = 0
        for i in range(self.N):
            totalMass += self.particles.iloc[i].mass
        temp = rmsSquared * totalMass / (2 * self.R)
        return temp








# initialise the object
simulation = Simulation()

# assign random starting positions & velocities
simulation.randomiseInitial()

# particles properties
print(simulation.particles)




# plot graph

fig = plt.figure()

plt.xlim(-simulation.xLim , simulation.xLim)
plt.ylim(-simulation.yLim , simulation.yLim)

posX = list(simulation.particles['positionX'])
posY = list(simulation.particles['positionY'])
graph, = plt.plot([],[], 'o', markersize=5)


def initial():
    graph.set_data([], [])
    return graph,


def render(i):
    # change number for different methods
    simulation.eulerCromer()
    posX = list(simulation.particles['positionX'])
    posY = list(simulation.particles['positionY'])
    graph.set_data(posX, posY)
    return graph,



anim = FuncAnimation(fig, render, init_func=initial, interval=1/10, frames=range(1200), blit = True, repeat = False)

plt.show()