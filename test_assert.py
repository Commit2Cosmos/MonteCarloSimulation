from Simulation import Simulation
import numpy as np

sim = Simulation(2,0.1)
sim.meanFP = 1

p1 = sim.particles[0]
p2 = sim.particles[1]


# tests two particle collision head on
def test_headOn():

        p1.positionX, p1.positionY = -1, 0
        p1.velocityX, p1.velocityY = 1, 0
        p1.mass = 1
        p1.radius = 0

        p2.positionX, p2.positionY = 1, 0
        p2.velocityX, p2.velocityY = -1, 0
        p2.mass = 1
        p2.radius = 0


def test_wallCollision():
        
        p1.positionX, p1.positionY = -0.81, 0
        p1.velocityX, p1.velocityY = -1, 0
        p1.mass = 1
        p1.radius = 0

        wallsVectors = [[-1,0],[1,0]]
        midWall = [1,-1]

        for j in range(6):
                tc = round((midWall[1]*np.dot((sim.meanFP,sim.meanFP),wallsVectors[1]) - np.dot((p1.positionX,p1.positionY),wallsVectors[1]))/np.dot((p1.velocityX,p1.velocityY),wallsVectors[1]),3)
                # (1) - (p1.positionX)/(p1.velocityX)
                
                if (tc < sim.dt) and (tc > 0):
                        print('yes')
                        p1.positionX += p1.velocityX * tc
                        p1.velocityX *= -1
                        p1.positionX += p1.velocityX * (sim.dt - tc)

                
                sim.eulerCromer()
                print('position: ' + str(p1.positionX))


test_wallCollision()