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





###################################################################################################################################

"""Demo generating random velocity vectors
"""


# Seed our random number generator for reproducibility in test.

# =============================================================================
#
# Firstly let's just look at a MB gas without any bulk speed in a particular
# direction
#
# =============================================================================

# Generate 100000 random velocity vectors for an O_2 gas at 300 K - will
# give us a 100000x3 array.  Note you could do this with a for loop (commented
# out below) - here I'm using a "list comprehension" which is a very "Pythonic"
# way to do it.
gas_temp = 300.0
particle_mass = 16.0*const.m_p
v = np.array([random(gas_temp, particle_mass) for i in range(100000)])
# v = np.zeros((100000,3))
# for i in range(100000):
# 	v[i,:] = random(300.0, 16.0*const.m_p)

# Now work out the speeds by taking the norm across the second axis (the
# components).
speed = np.linalg.norm(v, axis=1)

# Now make a histogram of the vx, vy, vz components and speeds and overplot
# the theoretical results.  The x and xp variables are just used to overplot
# the theory.
x = np.linspace(-1000,1000,50)
xp = np.linspace(0,2000,50)

# Vx histogram - the multiplication by np.max(h[0]) just means that the peak
# of the theoreitcal curve is scaled to the peak of the data for comparison.
plt.subplot(2,2,1)
h=plt.hist(v[:,0], bins=np.linspace(-1000,1000,100))
plt.plot(x, dist_component(x, gas_temp, particle_mass)*np.max(h[0]))
plt.xlabel(r'$v_x$ [m/s]')
plt.ylabel('Number')


# v histogram
plt.subplot(2,2,2)
h=plt.hist(speed, bins=np.linspace(0,2000,100))
plt.plot(xp, dist_speed(xp, gas_temp, particle_mass)*np.max(h[0]))
plt.xlabel(r'$v$ [m/s]')
plt.ylabel('Number')

# Here we save the figure to a PNG file with a resolution of 300 pixels/inch
plt.savefig('demo.png', dpi=300)
plt.show()


# =============================================================================
#
# Now let's assume that the gas is moving at 500 m/s in the z direction with
# the thermal motion superimposed.
#
# =============================================================================
gas_temp = 300.0
particle_mass = 16.0*const.m_p
v = np.array([random(gas_temp, particle_mass, vb=[0.0,0.0,500.0]) for i in range(100000)])

# Note here, the Maxwell-Boltzmann distribution of speeds that you know about
# is about the random thermal speed, the superimposed bulk velocity (500 m/s in
# z) is not part of that speed distribution, so I need to subtract it first before
# working out the speed for each vector.
speed = np.linalg.norm(v-[0,0,500], axis=1)

# Now make a histogram of the vx, vy, vz components and speeds and overplot
# the theoretical results.
x = np.linspace(-2000,2000,50)
xp = np.linspace(0,2000,50)

plt.subplot(2,2,1)
h=plt.hist(v[:,0], bins=np.linspace(-1000,1000,100))
plt.plot(x, dist_component(x, gas_temp, particle_mass)*np.max(h[0]))
plt.xlabel(r'$v_x$ [m/s]')
plt.ylabel('Number')

plt.subplot(2,2,2)
h=plt.hist(v[:,1], bins=np.linspace(-1000,1000,100))
plt.plot(x, dist_component(x, gas_temp, particle_mass)*np.max(h[0]))
plt.xlabel(r'$v_y$ [m/s]')
plt.ylabel('Number')

# Note here that I need to subtract 500 m/s from the distribution component
# as I haven't put a bulk speed in as a parameter to that function - I've sort
# of hacked it to shift it to visually check.
plt.subplot(2,2,3)
h=plt.hist(v[:,2], bins=np.linspace(-500,1500,100))
plt.plot(x, dist_component(x-500.0, gas_temp, particle_mass)*np.max(h[0]))
plt.xlabel(r'$v_z$ [m/s]')
plt.ylabel('Number')

plt.subplot(2,2,4)
h=plt.hist(speed, bins=np.linspace(0,2000,100))
plt.plot(xp, dist_speed(xp, gas_temp, particle_mass)*np.max(h[0]))
plt.xlabel(r'$v$ [m/s]')
plt.ylabel('Number')

# Here we save the figure to a PNG file with a resolution of 300 pixels/inch
plt.savefig('demo2.png', dpi=300)
plt.show()