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



Image.io for visualisation

E(t) graph constant CHECK macroscopic measurable parameters (such as Energy, temperature, pressure)

Ideal gas
Color represents speed


Method:

Populate 'box' with particles (Params: random ? one half filled, Temperature (i.e. average velocity), different mass)
Move each particle using some numerical method (v_i(t)*\delta t)
Split to squares
Find how many particles in each square

Using parameters like collision cross section check if there's a collision between each particle (i.e if its collision's probability is greater than the average for the whole square)
If yes => compute collision classically


Introduce seeds for reproducibility

F_N = statistical weight (# of real per simulated) (collection/blob)

n (number density) = (N / A) * F_N




ToDo:

-Knudsen number
-Split into Areas !


Global tests:

-Collision frequency matching
-Constant Energy
-Check theory vs actual: temperature, rms & average speed
-Evolution of speed distribution w temperature (with various initial conditions) (check for MB distribution) & whether speed distribution matches values of rms, mean and most probable speeds


Improve:
-How the number of areas alters accuracy [How big is the box? i.e. cannot be greater than some limit, as not realistic for particles to interact at such distance => split to more squares?]