import numpy as np
import scipy.constants as const
import scipy.special
import matplotlib.pyplot as plt
np.random.seed(1524)


def dist_speed(v, T, m, n=3):
	"""Return the Maxwell Boltzmann distribution of speeds

	Args:

		:param v np.array: Array of speeds to calculate the distribution at.
		:param float T: Temperature of the gas [K]
		:param float m: Mass of the species in the gas [kg]
		:param int n: Number of degrees of freedom (default=3)
		:return: Unnormalised distribution
	"""
	z = np.exp(-m*v*v/(2.0*const.k*T))*v**(n-1)
	return z/np.max(z)


def dist_component(v, T, m):
	"""Return the Maxwell Boltzmann distribution for a component

	Args:
		:param v np.array: Array of velocities to calculate the distribution at.
		:param float T: Temperature of the gas [K]
		:param float m: Mass of the species in the gas [kg]
		:return: Unnormalised distribution
	"""
	return np.exp(-m*v*v/(2.0*const.k*T))


def mean_speed(T, m, n=3):
    # Calculate the mean speed for a particle.

    # Args:

    # 	:param float T: Temperature of the gas [K]
    # 	:param float m: Mass of the species in the gas [kg]
    # 	:param int n: Number of degrees of freedom (default=3)
    # 	:return: Speed [m/s]
	
	return np.sqrt(2.0*const.k*T/m)*scipy.special.gamma(0.5*(n+1))/scipy.special.gamma(n/2)


def most_probable_speed(T, m, n=3):
	"""Calculate the most probable speed for a particle

	Args:

		:param float T: Temperature of the gas [K]
		:param float m: Mass of the species in the gas [kg]
		:param int n: Number of degrees of freedom (default=3)
		:return: Speed [m/s]
	"""
	return np.sqrt((n-1)*const.k*T/m)


def random(T, m, vb=np.array([0.0,0.0,0.0])):
	"""Return a three-vector drawn from a Maxwell-Boltzmann distribution

	Args:

		:param float T: Temperature of the gas [K]
		:param float m: Mass of the species in the gas [kg]
		:param np.array vb: Bulk velocity of the gas [m/s]
		:return: Velocity vector as np.array with three components
		:raises ValueError: if the bulk velocity array doesn't have three components.
		:raises ValueError: if the temperature or mass is zero or negative.
	"""

	# Check inputs
	if ((T<=0) or (m<=0)):
		raise ValueError
	if len(vb)!=3:
		raise ValueError

	# Calculate random thermal velocity vector in the frame of
	# reference moving with the gas, then we add the bulk velocity when we
	# return the vector to the caller.
	v = np.random.normal(0.0, np.sqrt(const.k*T/m), 3)
	return v+np.array(vb)


# print(mean_speed(300, 1.6735575E-27, 2))