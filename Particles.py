import numpy as np
# Fixing random state for reproducibility
np.random.seed(6)


# all particles will be instances of the Particle class with default properties

class Particle():

    def __init__(self, id, positionX = 0. , positionY = 0. , velocityX = 0. , velocityY = 0. , mass = 4.65E-26, radius = 1.85E-10, color = 'black'):

        self.id = id
        self.positionX, self.positionY = positionX, positionY
        self.velocityX, self.velocityY = velocityX, velocityY
        self.mass = mass
        self.radius = radius
        self.color = color