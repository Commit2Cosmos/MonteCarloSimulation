from Simulation import Simulation
# import numpy as np
# import pytest

sim = Simulation(2,0.5)
sim.meanFP = 1

p1 = sim.particles[0]
p2 = sim.particles[1]


# tests two particle collision head on
def headOnCollisionTest():
        """
	"""
        p1.positionX, p1.positionY = -2, 1
        p1.velocityX, p1.velocityY = 1, 0
        p1.mass = 1
        p1.radius = 1

        p2.positionX, p2.positionY = 2, 1
        p2.velocityX, p2.velocityY = -1, 0
        p2.mass = 1
        p2.radius = 1

        for i in range(4):
                sim.eulerCromer()
                sim.particleCollisionClassical()
                print(p1.positionX, p1.velocityX, p2.positionX, p2.velocityX)

        return p1.positionX, p1.velocityX, p2.positionX, p2.velocityX


def newWallCollisionTest():

        p1.positionX, p1.positionY, p1.velocityX, p1.velocityY = 0.7, -0.6, 1, -1
        p2.positionX, p2.positionY, p2.velocityX, p2.velocityY = 0, 0, 0.1, 0.1
        sim.dt = 0.5
        sim.newWallCollision()
        return p1.positionX, p1.positionY, p1.velocityX, p1.velocityY


def test_all():
        assert headOnCollisionTest() == (-2, -1, 2, 1)
        assert newWallCollisionTest() == (0.8, -0.9, -1, 1)