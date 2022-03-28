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

Using parameters like collision cross section check if there's a collision between each particle (i.e if its collision's probability is greater than the average for the whole square)
If yes => compute collision classically



Checks:

Total Energy (Temperature)
MB distribution
Pressure ?



Switch units to mean free path!!!!!!! (check dimensions as a test)
Provide diagnostics at the start of the simulation
Separate file for testing (pytest/unit test)




Introduce seeds for reproducibility
Use config files to use specific funcs


\sigma * c_r is P(collision per time per number density)
* number density * time => P(collision)

F_N = statistical weight (# of real per simulated) (collection/blob)

n (number density) = (N / A) * F_N


Qs:

total kinetic E at different T
-Flow time vs next output time


ToDo:

-Knudsen number
-Wall collision
-Tests
-Collision frequency comparison: theory vs mine discrepancy !!!!!!!!!!!!
-Change mean free path



I talked with a few people over the last week or so about collision detection and thought I would pass some broad thoughts on. I see a difference between collision detection and collision resolution.  You can detect that a collision has happened and respond to it, but that doesn't necessarily mean that you've accurately resolved the collision itself.  If we have a particle that is approaching a wall, it might be physically important to resolve where on the wall the collision took place.  To do that you can check, before you step the particle forward in time, whether the particle will intersect the wall.  If it does intersect the wall then you step the particle forward in time to the point of intersection, do any collision physics (e.g., reversing the component of the perpendicular velocity so the particle 'reflects' from the wall), and then step the particle forward in time by the amount of time remaining in the time step.  The way I do this is as follows:
 
We can represent the wall by a normal vector, n, and a point, a, on the wall (this is just a geometrical definition of a plane).  With that, some other point on the wall, let's say s, satisfies: (s-a) dot n=0.  The point s will be our intersection point where the particle meets the wall.
 
With a particle located at a point p at the beginning of the time step, moving with velocity v, if it intersects the wall at point s after time t_c then: s = p + vt_c.  This is just Forward Euler.
 
Substitute and rearrange for t (the time when the intersection happens):  t_c = (a dot n - p dot n)/(v dot n).  If t_c is smaller than the time-step (dt) then you know that the collision has happened part-way through a time step.  If t_c is greater than the time-step then the collision isn't going to happen in this time step.  If t_c is negative then this tells you that the collision isn't going to happen because it is in the "past".
 

If <t_c < dt> then you can update your particle position with position + velocity*t_c, do the collision physics (which will affect velocity), then do position + velocity*(dt-t_c) to make up the remaining part of the time step.  Of course it may collide with another wall, but you can check for that too.

 

Hope that helps anyone who is considering this sort of thing.