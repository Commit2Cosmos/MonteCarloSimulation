import sys
sys.dont_write_bytecode = True
import numpy as np
import scipy.constants as const
from Particles import Particle



class Simulation():
    # check maxRS value 1347
    def __init__(self, N = 1000, dt = 1E-10, p = 1E5, maxRS = 1800, time = 0., T=293, factor=2):

        self.N, self.dt, self.p, self.maxRS, self.time, self.T, self.factor = N, dt, p, maxRS, time, T, factor

        self.particles = [Particle(i) for i in range(self.N)]

        self.nd = self.p / (const.k * self.T)
        print('nd: ' + str(self.nd))
        self.sigma = const.pi * (2 * self.particles[0].radius)**2
        print('sigma: ' + str(self.sigma))
        self.meanFP = 1/(np.sqrt(2) * self.sigma * self.nd)
        print('meanFP: ' + str(self.meanFP))
        self.volume = (self.factor * self.meanFP) ** 2

        self.FN = self.nd * self.volume / self.N
        print('FN: ' + str(self.FN))
        self.pairs = self.numberOfPairs()

        self.uniformPosition()
        self.normalVelocity()

        self.collisions = []



    def uniformPosition(self):
        for i in self.particles:
            i.positionX, i.positionY = self.factor * self.meanFP * (np.random.rand(1,2)[0]-0.5)

    def uniformVelocity(self):
        for i in self.particles:
            i.velocityX, i.velocityY = self.maxRS * (np.random.rand(1,2)[0]-0.5)

    def normalVelocity(self):
        for i in self.particles:
            i.velocityX, i.velocityY = np.random.normal(0 , np.sqrt(const.k*self.T/i.mass) , size=(1,2))[0]



    def advance(self):
        # run either wallCollision + Cromer or newWallCollision // particleCollisionClassical or particleCollisionMC
        """Calls the necessary functions to run the simulation for one timestep
    	"""
        # if self.time == 0:
        #     self.saveInfo()
        # self.wallCollision()
        # self.eulerCromer()
        self.newWallCollision()
        # self.particleCollisionClassical()
        self.particleCollisionMC()
        # self.saveInfo()



    def eulerCromer(self):
        """Update position and velocity components using Euler-Cromer method
	    """
        for i in self.particles:
            i.positionX += i.velocityX * self.dt
            i.positionY += i.velocityY * self.dt



    def saveInfo(self, tPeriod=1E-10):
        """Increment the time every timestep & save information about system's parameters to the csv file

        Args:

            :param float tPeriod: Time period after which the data is saved [s]
	    """
        self.time = round(self.time + self.dt, 10)

        if (round(self.time % tPeriod, 1) == 0):
            time = self.time
            file = open('data.csv','a')
            file.write('\n\nTime: ' + str(time) + '\n')
            T = self.calculateTemperature()
            E = self.calculateTotalEnergy()
            file.write('T: ' + str(T))
            file.write('\nE: ' + str(E))
            file.close()



##### WALL COLLISION MANAGEMENT ###############################################

    def wallCollision(self):
        """Reverse particle's velocity component if collision with the wall is detected
	    """
        for i in self.particles:
            diff = (1/2 * self.factor * self.meanFP) - i.radius
            if (((i.positionX > diff) and (i.velocityX > 0)) or ((i.positionX < -diff) and (i.velocityX < 0))):
                i.velocityX *= -1
            if (((i.positionY > diff) and (i.velocityY > 0)) or ((i.positionY < -diff) and (i.velocityY < 0))):
                i.velocityY *= -1


    def newWallCollision(self):
        """Detect and resolve a particle/wall collision; does not allow the particle to cross the border of the box
        """
        wallsVectors = [[0,1],[-1,0],[0,-1],[1,0]]
        midWall = [1, 1, -1, -1]
        toWall = 1/2 * self.factor * self.meanFP - self.particles[0].radius

        # walls mid points, selected as 'some point on the wall' from geometrical definition are -1 * the corresponding wall vector
        # 1 collision with each wall for 1 particle at a timestep only

        for i in self.particles:

            tcList = []

            for index in range(len(wallsVectors)):
                # include radius of particle
                # include double wall collisions

                # always 2 positive & 2 negative values for tc
                tc = (midWall[index]*np.dot((toWall,toWall),wallsVectors[index]) - np.dot((i.positionX,i.positionY),wallsVectors[index]))/np.dot((i.velocityX,i.velocityY),wallsVectors[index])
                if (tc > 0) and (tc <= self.dt):
                    tcList.append([index,tc])

            if len(tcList) == 0:
                i.positionX += i.velocityX * self.dt
                i.positionY += i.velocityY * self.dt


            if len(tcList) == 1:
                i.positionX += i.velocityX * tcList[0][1]
                i.positionY += i.velocityY * tcList[0][1]

                if tcList[0][0] == 0 or tcList[0][0] == 2:
                    i.velocityY *= -1
                if tcList[0][0] == 1 or tcList[0][0] == 3:
                    i.velocityX *= -1

                t = self.dt - tcList[0][1]

                i.positionY += i.velocityY * t
                i.positionX += i.velocityX * t


            if len(tcList) == 2:
                sortedTc = sorted(tcList)
                i.positionX += i.velocityX * sortedTc[0][1]
                i.positionY += i.velocityY * sortedTc[0][1]

                if sortedTc[0][0] == 0 or sortedTc[0][0] == 2:
                    i.velocityY *= -1
                if sortedTc[0][0] == 1 or sortedTc[0][0] == 3:
                    i.velocityX *= -1

                t = self.dt - sortedTc[0][1]

                newTc = sortedTc[1][1] - sortedTc[0][1]

                i.positionX += i.velocityX * newTc
                i.positionY += i.velocityY * newTc

                if sortedTc[1][0] == 0 or sortedTc[1][0] == 2:
                    i.velocityY *= -1
                if sortedTc[1][0] == 1 or sortedTc[1][0] == 3:
                    i.velocityX *= -1

                # same as self.dt - tcList[1][1]
                t -= newTc

                i.positionY += i.velocityY * t
                i.positionX += i.velocityX * t

##### PARTICLE COLLISION MANAGEMANT ##############################################

    def particleCollisionClassical(self):
        """Check for and resolve a classical two particle collision (ignores > 2 particles collisions in one timestep)
	    """
        collided = []
        for i in self.particles:
            for j in self.particles:

                # check so particle doesn't collide with itself & if particle already collided in current iteration
                if ((i == j) or (i.id in collided or j.id in collided)):
                    continue

                rx = i.positionX - j.positionX
                ry = i.positionY - j.positionY

                if np.dot((rx,ry),(rx,ry)) <= (i.radius + j.radius)**2:
                    vx = i.velocityX - j.velocityX
                    vy = i.velocityY - j.velocityY

                    self.velocityCalculation(vx,vy,rx,ry,i,j)

                    collided.append(i.id)
                    collided.append(j.id)


    def velocityCalculation(self,vx,vy,rx,ry,i,j):
        """Utilise equations for angle-free representation of an elastic collision to resolve velocities of particles after the collision

	    Args:

            :param float vx: Difference between velocity x-component of the two particles [m/s]
            :param float vy: Difference between velocity y-component of the two particles [m/s]
            :param float rx: Difference between position x-component of the two particles [m]
            :param float ry: Difference between position y-component of the two particles [m]
            :param i Particle class instance: First colliding particle
            :param j Particle class instance: Second colliding particle
	    """
        inner = np.dot((vx, vy),(rx,ry))
        mag = rx**2 + ry**2
        m = i.mass + j.mass
        mmag = (m * mag)

        i.velocityX -= 2*j.mass*inner*rx/mmag
        i.velocityY -= 2*j.mass*inner*ry/mmag
        j.velocityX += 2*i.mass*inner*rx/mmag
        j.velocityY += 2*i.mass*inner*ry/mmag







##### MONTE CARLO METHOD #####################################################

    def numberOfPairs(self):
        """Calculate the number of collision pairs in 1 timestep (calculated once at the star of the simulation as the value stays constant throughout)

        Args:

            :return: Collision pairs number
	    """
        nP = (1/2 * self.N * (self.N - 1) * self.FN * (self.maxRS * self.sigma) * self.dt) / self.volume
        print('pairs: ' + str(nP))
        return nP


    def chooseRandomParticles(self):
        """Return two random non-equal integers in the range of the number of particles

	    Args:

		    :return: Two integers
	    """
        first = np.random.randint(0, self.N)
        second = np.random.randint(0, self.N)
        while second == first:
            second = np.random.randint(0, self.N)
        return first, second


    def particleCollisionMC(self):
        """Implementation of the Monte-Carlo method based on acceptance/rejection procedure
	    """
        count = 0
        for dummy in range(int(self.pairs)):
            first, second = self.chooseRandomParticles()
            i, j = self.particles[first], self.particles[second]

            vx = i.velocityX - j.velocityX
            vy = i.velocityY - j.velocityY
            relSpeed = np.sqrt(vx**2 + vy**2)
            ratio = relSpeed/self.maxRS
            # print(ratio)

            # resets the maximum probability value if a higher one was encountered
            if ratio > 1:
                self.maxRS = relSpeed
                print('!!new maxRS!!: ' + str(self.maxRS))
                self.pairs = self.numberOfPairs()

            # resolves the collision classically if the ratio of current and maximum collision probabilities is greater than a random number between 0 and 1
            if ratio > np.random.random(1)[0]:
                rx = i.positionX - j.positionX
                ry = i.positionY - j.positionY
                # print('!collision!')
                count += 1

                self.velocityCalculation(vx,vy,rx,ry,i,j)
        self.collisions.append(count)
        # print('collisions detected: ' + str(count))






##### PARTICLES' PARAMETERS GETTERS##################################


    def getColor(self):
        """Return colours of all particles

	    Args:

		    :return: np.array of particles' colours
	    """
        colors = []
        for particle in self.particles:
            colors.append(particle.color)
        return np.array(colors)


    def getPositions(self):
        """Return the position of each particle

	    Args:

    		:return: Two arrays with x- and y-components of each particle's position
	    """
        x, y = [], []
        for particle in self.particles:
            x.append(particle.positionX)
            y.append(particle.positionY)
        return x, y


    def getSpeeds(self):
        """Return the speed of each particle

	    Args:

		    :return: An array with each particle's speed
	    """
        speeds = []
        for particle in self.particles:
            speed = np.sqrt(particle.velocityX**2 + particle.velocityY**2)
            speeds.append(speed)
        return speeds







##### CALCULATE PROPERTIES OF SIMULATION #############################

    def calculateMeanSpeed(self):
        """Calculate actual mean speed value

	    Args:

		    :return: The mean speed of the particles [m/s]
	    """
        totalSpeed = 0
        for particle in self.particles:
            speed = np.sqrt(particle.velocityX**2 + particle.velocityY**2)
            totalSpeed += speed
        meanSpeed = totalSpeed/self.N
        print('meanSpeed: ' + str(meanSpeed))
        return meanSpeed


    def calculateRMSSquared(self):
        """Calculate actual rms speed squared value

	    Args:

		    :return: The rms speed of the particles [m/s]
	    """
        totalSpeedSquared = 0
        for particle in self.particles:
            speed = particle.velocityX**2 + particle.velocityY**2
            totalSpeedSquared += speed
        rmsSquared = totalSpeedSquared/self.N
        print('rmsSpeed: ' + str(np.sqrt(rmsSquared)))
        return rmsSquared


    def calculateTemperature(self):
        """Calculate actual temperature of the system from the rms speed value

	    Args:

		    :return: Temperature of the system [K]
	    """
        # average mass of all particles
        T = self.calculateRMSSquared() * self.particles[0].mass / (2 * const.k)
        print('T: ' + str(T))
        return T


    def calculateTotalEnergy(self):
        """Calculate actual total energy of the system from the rms speed value

	    Args:

		    :return: Total energy of the system [J]
	    """
        E = 1/2 * self.particles[0].mass * self.calculateMeanSpeed()**2
        # print('E: ' + str(E))
        return E


# initialise the object
simulation = Simulation()

simulation.calculateMeanSpeed()
# simulation.calculateRMSSquared()
simulation.calculateTemperature()