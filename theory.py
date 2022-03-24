import scipy.constants as const
import scipy.special as spec
import numpy as np

T = 300
m = 4.65E-26
FP = 4.9071E-7
nd = 2.7E25
r = 1.55E-10

# av rel speed = sqrt(2) * av speed


def averageRelativeSpeed():
    
    avRelSpeed = (16*const.k*T/(const.pi*m))**0.5
    print(avRelSpeed)

    return avRelSpeed



def averageCollisionFrequency():
    """Calculate the average total collision frequency per unit volume

    Args:

        :return: The average number of collisions in a system per second
    """
    
    avRelSpeed = averageRelativeSpeed()
    fre = avRelSpeed * nd**2 * const.pi * (2*r)**2/2
    # print('collision frequency: ' + str(fre))

    print(fre * FP)

    return fre



def meanSpeed():
    """Calculate the mean particle speed

    Args:

        :return: Mean particle speed
    """

    return np.sqrt(2.0*const.k*T/m)*spec.gamma(1.5)

averageCollisionFrequency()