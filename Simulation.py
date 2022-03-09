import sys
sys.dont_write_bytecode = True
import numpy as np
# Fixing random state for reproducibility
np.random.seed(3)
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from Particles import Particle


class Simulation():
    boxSize = [20,20]

    xLim = boxSize[0]/2
    yLim = boxSize[1]/2

    time = 0
    
    # CONSTANTS
    R = 1


    def __init__(self, dt = 0.5E-2, N = 20):
        self.dt, self.N = dt, N
        # move particle creation to Particle class
        arr = [np.zeros(7)]
        self.particles = pd.DataFrame(np.array(arr*N), columns=['positionX', 'positionY', 'velocityX', 'velocityY', 'mass', 'radius', 'color'])
        # name property is a unique id of a particle


    # RANDOMNESS
    def randomiseInitial(self):
        for i in range(self.N):
            para = self.particles.iloc[i]
            para.positionX, para.positionY = 2 * self.xLim * (np.random.rand(1,2)[0] - 0.5)
            para.velocityX, para.velocityY = self.yLim * (np.random.rand(1,2)[0] - 0.5) * 10
            para.mass = 1
            para.radius = 0.25
            para.color = 100


    # collision detection TEST (head on)
    def setConditions(self):
        para1 = self.particles.iloc[0]
        para2 = self.particles.iloc[1]

        para1.positionX, para1.positionY = -2, 0
        para1.velocityX, para1.velocityY = 1, 0
        para1.mass = 1
        para1.radius = 0.25

        para2.positionX, para2.positionY = 2, 0
        para2.velocityX, para2.velocityY = -1, 0
        para2.mass = 1
        para2.radius = 0.25



    # runs the simulation 1 timestep

    def advance(self):
        self.incrementTime()
        self.wallCollision()
        self.particleCollisionClassical()
        self.eulerCromer()
        self.saveInfo()





    # updates components of position and velocity using Euler-Cromer method

    def eulerCromer(self):
        for i in range(self.N):
            para = self.particles.iloc[i]
            para.positionX += para.velocityX * self.dt
            para.positionY += para.velocityY * self.dt




    # increment time

    def incrementTime(self):
        self.time = round(self.time + self.dt, 3)



    # save info

    def saveInfo(self):
        if (self.time % 0.05 == 0):
            time = self.time
            file = open('data.csv','a')
            file.write('\n\nTime: ' + str(time) + '\n')

            file.close()
            # self.particles.to_csv('data.csv',mode='a',header=False)



    def speedDistrib(self):
        speeds = []
        for i in range(self.N):
            para = self.particles.iloc[i]
            speed = np.sqrt(para.velocityX**2 + para.velocityY**2)
            speeds.append(speed)
        return speeds





    # collision management

    def wallCollision(self):
        for i in range(self.N):
            para = self.particles.iloc[i]
            if (((para.positionX > self.xLim - para.radius) and (para.velocityX > 0)) or ((para.positionX < -self.xLim + para.radius) and (para.velocityX < 0))):
                para.velocityX *= -1
            if (((para.positionY > self.yLim - para.radius) and (para.velocityY > 0)) or ((para.positionY < -self.yLim + para.radius) and (para.velocityY < 0))):
                para.velocityY *= -1


    # classical two particle collision (ignores > 2 particles collisions in one timestep)

    def particleCollisionClassical(self):
        collided = []
        for i in range(self.N):
            para1 = self.particles.iloc[i]

            for j in range(self.N):
                para2 = self.particles.iloc[j]

                # check so particle doesn't collide with itself & if particle already collided in current iteration
                if ((i == j) or (para1.name in collided or para2.name in collided)):
                    continue
                
                rx = para1.positionX - para2.positionX
                ry = para1.positionY - para2.positionY

                # Equations for angle-free representation of an elastic collision were taken from Wikipedia
                if np.dot((rx,ry),(rx,ry)) <= (para1.radius + para2.radius)**2:
                    vx = para1.velocityX - para2.velocityX
                    vy = para1.velocityY - para2.velocityY

                    inner = np.dot((vx, vy),(rx,ry))
                    mag = rx**2 + ry**2
                    m = para1.mass + para2.mass
                    mmag = (m * mag)

                    
                    para1.velocityX -= 2*para2.mass*inner*rx/mmag
                    para1.velocityY -= 2*para2.mass*inner*ry/mmag
                    para2.velocityX += 2*para1.mass*inner*rx/mmag
                    para2.velocityY += 2*para1.mass*inner*ry/mmag

                    collided.append(para1.name)
                    collided.append(para2.name)





    # Monte-Carlo stuff ###########################

    maxProb = 0.8

    # choosing collision pairs through acceptance/rejection procedure        


    def numberOfPairs(self):
        fN = 1000
        return (1/2 * self.N * (self.N - 1) * fN * self.maxProb * self.dt) / (4 * self.xLim * self.yLim)


    def chooseRandomParticles(self):
        first = np.random.randint(0, self.N)
        second = np.random.randint(0, self.N)
        while second == first:
            second = np.random.randint(0, self.N)
        return first, second


    def particleCollisionMC(self):
        count = 0
        while count < int(np.floor(self.numberOfPairs())):
            first, second = self.chooseRandomParticles()
            para1, para2 = self.particles.iloc[first], self.particles.iloc[second]

            area = np.pi*(para1.radius**2 + para2.radius**2)/2

            vx = para1.velocityX - para2.velocityX
            vy = para1.velocityY - para2.velocityY
            relSpeed = np.sqrt(vx**2 + vy**2)

            prob = area * relSpeed

            if prob > self.maxProb:
                rx = para1.positionX - para2.positionX
                ry = para1.positionY - para2.positionY

                inner = np.dot((vx, vy),(rx,ry))
                mag = rx**2 + ry**2
                m = para1.mass + para2.mass
                mmag = (m * mag)

                para1.velocityX -= 2*para2.mass*inner*rx/mmag
                para1.velocityY -= 2*para2.mass*inner*ry/mmag
                para2.velocityX += 2*para1.mass*inner*rx/mmag
                para2.velocityY += 2*para1.mass*inner*ry/mmag








    # Macro params of a system

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


    def getColor(self):
        colors = []
        for i in range(self.N):
            colors.append(self.particles.iloc[i].color)
        return np.array(colors)


        





# initialise the object
simulation = Simulation()

# assign random starting positions & velocities
simulation.randomiseInitial()
# simulation.setConditions()

# print(simulation.getColor())

# particles properties
# print(simulation.particles)




# plot graphs

# def maxwellDistrib(bins=5):
#     values = simulation.speedDistrib()
#     plt.hist(values, bins=bins)
#     plt.show()


vrange = np.arrange(1, 100, 10)


def particlesPositionAnimation():
    fig, (ax,ax2) = plt.subplots(nrows = 2, figsize=(5, 8))
    # fig, ax = plt.subplots()

    scatter = ax.scatter([],[])
    bar = ax2.bar(vrange, [0]*len(vrange), width = 0.9 * np.gradient(vrange), align="edge", alpha=0.8)

    def initial():
        ax.set_xlim(-simulation.xLim , simulation.xLim)
        ax.set_ylim(-simulation.yLim , simulation.yLim)
        # scatter.set_array(simulation.getColor())
        return scatter,


    def render(i):
        simulation.advance()

        # use to set bins limits when actual values of speed are known
        # bins = np.linspace() 
        # freq, bins = np.histogram(simulation.speedDistrib(), bins=5)

        posX = list(simulation.particles['positionX'])
        posY = list(simulation.particles['positionY'])
        scatter.set_offsets(np.c_[posX,posY])
        # scatter.set_array(simulation.getColor())
        return scatter,

    anim = FuncAnimation(fig, render, init_func=initial, interval=1, frames=range(1200), blit = True, repeat = False)
    plt.show()


# particlesPositionAnimation()
maxwellDistrib()