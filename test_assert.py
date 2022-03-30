from Simulation import Simulation
import numpy as np

sim = Simulation(1,0.1)
sim.meanFP = 1

p1 = sim.particles[0]
# p2 = sim.particles[1]


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
        
        p1.positionX, p1.positionY = 0.7 , -0.6
        p1.velocityX, p1.velocityY = 1, -1
        sim.dt = 0.5
        sim.newWallCollision()
        print(p1.positionX, p1.positionY, p1.velocityX, p1.velocityY)


test_wallCollision()