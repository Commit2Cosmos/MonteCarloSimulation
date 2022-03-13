import sys
sys.dont_write_bytecode = True
import numpy as np
# Fixing random state for reproducibility
# resolve 3 particle collision!!!!!!!
np.random.seed(3)
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Particles import Particle


class Simulation():
    boxSize = [20,20]
    xLim = boxSize[0]/2
    yLim = boxSize[1]/2

    time = 0

    # CONSTANTS
    k = 1.38064852E-23
    nd = 2.5E25


    def __init__(self, dt = 0.5E-4, N = 20):
        self.dt, self.N = dt, N
        self.particles = [Particle(i) for i in range(self.N)]



    # runs the simulation 1 timestep

    def advance(self):
        self.incrementTime()
        self.wallCollision()
        self.particleCollisionClassical()
        self.eulerCromer()
        # self.saveInfo()





    # updates components of position and velocity using Euler-Cromer method

    def eulerCromer(self):
        for i in range(self.N):
            para = self.particles[i]
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
            # WHICH PARAMS TO WRITE????
            file.close()
            # self.particles.to_csv('data.csv',mode='a',header=False)



    def speedDistrib(self):
        speeds = []
        for i in range(self.N):
            para = self.particles[i]
            speed = np.sqrt(para.velocityX**2 + para.velocityY**2)
            speeds.append(speed)
        return speeds





    # collision management

    def wallCollision(self):
        for i in range(self.N):
            para = self.particles[i]
            if (((para.positionX > self.xLim - para.radius) and (para.velocityX > 0)) or ((para.positionX < -self.xLim + para.radius) and (para.velocityX < 0))):
                para.velocityX *= -1
            if (((para.positionY > self.yLim - para.radius) and (para.velocityY > 0)) or ((para.positionY < -self.yLim + para.radius) and (para.velocityY < 0))):
                para.velocityY *= -1


    # classical two particle collision (ignores > 2 particles collisions in one timestep)

    def particleCollisionClassical(self):
        collided = []
        for i in self.particles:
            for j in self.particles:

                # check so particle doesn't collide with itself & if particle already collided in current iteration
                if ((i == j) or (i.id in collided or j.id in collided)):
                    continue
                
                rx = i.positionX - j.positionX
                ry = i.positionY - j.positionY

                # Equations for angle-free representation of an elastic collision were taken from Wikipedia
                if np.dot((rx,ry),(rx,ry)) <= (i.radius + j.radius)**2:
                    vx = i.velocityX - j.velocityX
                    vy = i.velocityY - j.velocityY

                    self.velocityCalculation(vx,vy,rx,ry,i,j)

                    collided.append(i.id)
                    collided.append(j.id)



    def velocityCalculation(self,vx,vy,rx,ry,i,j):

        inner = np.dot((vx, vy),(rx,ry))
        mag = rx**2 + ry**2
        m = i.mass + j.mass
        mmag = (m * mag)


        i.velocityX -= 2*j.mass*inner*rx/mmag
        i.velocityY -= 2*j.mass*inner*ry/mmag
        j.velocityX += 2*i.mass*inner*rx/mmag
        j.velocityY += 2*i.mass*inner*ry/mmag




    # Monte-Carlo stuff ###########################

    # def maximumProb():


    # choosing collision pairs through acceptance/rejection procedure        

    def calculateFN(self):
        return self.N/(self.nd*4*self.xLim*self.yLim)

    def numberOfPairs(self):
        return (1/2 * self.N * (self.N - 1) * self.calculateFN() * self.maxProb * self.dt) / (4 * self.xLim * self.yLim)


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
            i, j = self.particles[first], self.particles[second]

            area = np.pi*(i.radius**2 + j.radius**2)/2

            vx = i.velocityX - j.velocityX
            vy = i.velocityY - j.velocityY
            relSpeed = np.sqrt(vx**2 + vy**2)

            prob = area * relSpeed

            # Random btw 0,1 if > -> pass
            if (prob/self.maxProb) > np.random.random(1)[0]:
                rx = i.positionX - j.positionX
                ry = i.positionY - j.positionY
                print('passed')

                self.velocityCalculation(vx,vy,rx,ry,i,j)




    # params of particles

    def getColor(self):
        colors = []
        for particle in self.particles:
            colors.append(particle.color)
        return np.array(colors)

    
    def getPositions(self):
        x, y = [], []
        for particle in self.particles:
            x.append(particle.positionX)
            y.append(particle.positionY)
        return x, y




    # macro params of a system

    def calculateRMSSquared(self):
        totalSpeedSquared = 0
        for particle in self.particles:
            speed = particle.velocityX**2 + particle.velocityY**2
            totalSpeedSquared += speed
        rmsSquared = totalSpeedSquared/self.N
        return rmsSquared


    def calculateTemp(self):
        rmsSquared = self.calculateRMSSquared()

        # average mass of all particles
        mass = self.particles[0].mass
        temp = rmsSquared * mass / (2 * self.k)
        return temp


    def avEnergy(self):
        E = 0
        for particle in self.particles:
            E += 0.5*particle.mass*(particle.velocityX**2+particle.velocityY**2)
        return E / self.N









# initialise the object
simulation = Simulation()

print(np.sqrt(simulation.calculateRMSSquared()))
print(simulation.calculateTemp())











# plot graphs


def particlesPositionAnimation():
    fig, (ax, ax2) = plt.subplots(1,2, gridspec_kw={'width_ratios': [7, 4]})
    # ax.set_aspect('auto')

    vs = np.linspace(0,3000,20)

    scatter = ax.scatter([],[])
    bar = ax2.bar(vs, [0]*len(vs), width=0.9 * np.gradient(vs), align="edge", alpha=0.8)

    def initial():
        ax.set_xlim(-simulation.xLim , simulation.xLim)
        ax.set_ylim(-simulation.yLim , simulation.yLim)
        
        ax2.set_xlim(vs[0],vs[-1])
        ax2.set_ylim(0, simulation.N)

        return (scatter, *bar.patches)


    def render(i):
        simulation.advance()

        freq, bins = np.histogram(simulation.speedDistrib(), bins=vs)

        for rect, height in zip(bar.patches,freq):
            rect.set_height(height)

        posX, posY = simulation.getPositions()
        scatter.set_offsets(np.c_[posX,posY])
        scatter.set_color(simulation.getColor())
        return (scatter, *bar.patches)

    anim = FuncAnimation(fig, render, init_func=initial, interval=1/30, frames=range(120), blit = True, repeat = True)
    plt.show()


particlesPositionAnimation()