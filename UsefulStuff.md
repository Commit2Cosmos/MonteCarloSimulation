Monte Carlo simulation methods do not always require truly random numbers to be useful


From papers:

Good Monte Carlo:

-the (pseudo-random) number generator has certain characteristics (e.g. a long "period" before the sequence repeats)
-the (pseudo-random) number generator produces values that pass tests for randomness
-there are enough samples to ensure accurate results
-the proper sampling technique is used
-the algorithm used is valid for what is being modeled
-it simulates the phenomenon in question.

Continuum description not accurate if Knudsen number (Kn) > 1/10


Estimate collision rate

How big is the box? IE cannot be greater than some limit, as not realistic for particles to interact at such distance => split to more squares?



Image.io for visualisation or matplotlib

E(t) graph constant CHECK macroscopic measurable parameters (such as Energy, temperature, pressure)

Ideal gas
Color represents speed


Method:

Populate 'box' with particles (Params: random ? one half filled, Temperature (i.e. average velocity), different mass)
Move each particle using some numerical method (v_i(t)*\delta t)
Split to squares
Find how many particles in each square
Using parameters like collision cross section and RNG check if there's a collision between each particle (i.e if its collision's 'magic value' is greater than the average for the whole square)
If yes => compute collision classically


Checks:

Total Energy (Temperature)
MB distribution
Pressure ?



Qs:

If non-point particles are 'touching'?
What does 'magic value' represent and how to calculate it?
How to implement Runge-Kutta & linear multistep methods (or any other advanced ones e.g. multiderivative, 2nd order ODEs)?
Verlet method?