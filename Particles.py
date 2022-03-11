import numpy as np
np.random.seed(5)


# Creating a Particle class; all particles will be instances of this class with default properties

N = 3

class Particle():

    # constructor

    def __init__(self, id = 0, positionX = 0. , positionY = 0. , velocityX = 1. , velocityY = 1. , mass = 1, radius = 0.25, color = 'blue'):

        self.id = id
        self.positionX, self.positionY = positionX, positionY
        self.velocityX, self.velocityY = velocityX, velocityY
        self.mass = mass
        self.radius = radius
        self.color = color
        self.randomiseInitial()


    def randomiseInitial(self):
        self.positionX, self.positionY = 20*(np.random.rand(1,2)[0]-0.5)
        self.velocityX, self.velocityY = 10*np.random.normal(0.,2, size=(1,2))[0]

        # 10*np.random.normal(0.,2, size=(1,2))[0]

        # return [self.positionX, self.positionY, self.velocityX, self.velocityY, self.mass, self.radius]


    # # collision detection 2 particles TEST (head on)
    # def setConditions(self):
    #     para1 = self.particles.iloc[0]
    #     para2 = self.particles.iloc[1]

    #     para1.positionX, para1.positionY = -2, 0
    #     para1.velocityX, para1.velocityY = 1, 0
    #     para1.mass = 1
    #     para1.radius = 0.25

    #     para2.positionX, para2.positionY = 2, 0
    #     para2.velocityX, para2.velocityY = -1, 0
    #     para2.mass = 1
    #     para2.radius = 0.25


# print(10*np.random.normal(0.,2, size=(2,1)))