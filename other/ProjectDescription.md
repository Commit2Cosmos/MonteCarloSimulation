Project Title: Monte Carlo simulation of particles in a box.



The system I will attempt to simulate involves particles in a hard box with arbitrary parameters (such as position, velocity and mass). The particles would be assigned a random position and velocity at the start. As the simulation runs the macroscopic parameters of the system will be recorded and plotted. The box will be split into sections within which particles can interact (I will start with 1 and see how increasing it changes the 'accuracy' of the simulation). To detect collisions Monte Carlo method will be used. Once detected, the collision will be resolved classically.

Some outcomes the simulation aims to reproduce: dependence of macroscopic parameters (such as temperature) on microscopic (such as kinetic energy), distributions (i.e. Maxwell-Boltzmann) for various temperatures, thermal equilibration of particles with each other and with the box walls after long enough time.

At the end, the simulation validity will be assessed by comparing results to those predicted theoretically and the limitations of methods used will be discussed.


The python packages I will be using are matplotlib, numpy and pandas (if found that tabulating data is preferred).

The equations necessary for the simulation are equations associated with implementing time step methods (Euler-Cromer, Verlet, Runge-Kutta), thermal properties of matter (e.g. root mean square speed [v_rms = sqrt(3kT/m)], kinetic energy of an ideal gas [K = 3/2*NkT]).

The programming techniques I am planning to use are inheritance (to make particles of different mass/size), random number generation, encapsulation (to define variables and functions that should not be accessed directly) and abstraction (to hide internal functionality of functions from users)