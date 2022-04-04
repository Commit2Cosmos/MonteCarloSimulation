import sys
sys.dont_write_bytecode = True
import scipy.constants as const
import numpy as np
from Simulation import Simulation

sim = Simulation()

dt = sim.dt
N = sim.N
T = sim.T
m = sim.particles[0].mass
FP = sim.meanFP
nd = sim.nd
r = sim.particles[0].radius
FN = sim.FN

 
def rmsSpeed():
    """Calculate the root-mean-square speed of particles

    Args:

        :return: Root-mean-square particle speed (m/s)
    """
    rmsSpeed = np.sqrt((2 * const.k * T)/(m))
    return rmsSpeed


def mostProbableSpeed():
    """Calculate the most probable particle speed

    Args:

        :return: Most probable particle speed (m/s)
    """
    speed = np.sqrt((const.k * T)/m)
    return speed


def meanSpeed():
    """Calculate the mean particle speed

    Args:

        :return: Mean particle speed (m/s)
    """
    speed = np.sqrt((const.k * T * const.pi)/(2 * m))
    # print('meanSpeed: ' + str(speed))
    return speed


def averageCollisionFrequency():
    """Calculate the average collision frequency of 1 particle

    Args:

        :return: The average number of collisions in a system per second per unit volume
    """
    Z = meanSpeed()/FP
    # print('collision frequency: ' + str(Z))
    return Z


def totalCollisionNumber():
    """Calculate the average total number of collisions per unit volume and time

    Args:

        :return: The average number of collisions in a system per second per meter squared
    """
    colNum = averageCollisionFrequency() * 1/2 * nd
    # print('Total coll: ' + str(colNum))
    return colNum


# print('totalCollisionNumber: ' + str(totalCollisionNumber() * dt * (2 * FP)**2 / FN))
print(meanSpeed())


# # to choose initial maxRS
# print(meanSpeed() * np.sqrt(2) * 2)


# for i in range(1000):
#     sim.advance()

# tot = 0
# for i in sim.collisions:
#     tot += i
# print(tot/len(sim.collisions))

sim.advance()


















# CHECK FOR VALIDITY
# def averageCollisionFrequency():
#     """Calculate the average total collision frequency per unit volume

#     Args:

#         :return: The average number of collisions in a system per second per unit volume
#     """
#     avRelSpeed = meanSpeed() * np.sqrt(2)
#     fre = avRelSpeed * nd**2 * const.pi * 2 * (2*r)**2 * dt
#     # N**2 * relSpeed * dt * (sigma * FN) / V
#     print('collision frequency: ' + str(fre))
#     return fre