from Particles import Particle
from Simulation import Simulation




# tests two particle collision head on
def test_headOn():
        sim = Simulation()
        particles = [Particle(i) for i in range(2)]

        p1 = particles[0]
        p2 = particles[1]

        p1.positionX, p1.positionY = -1, 0
        p1.velocityX, p1.velocityY = 1, 0
        p1.mass = 1
        p1.radius = 0

        p2.positionX, p2.positionY = 1, 0
        p2.velocityX, p2.velocityY = -1, 0
        p2.mass = 1
        p2.radius = 0

        