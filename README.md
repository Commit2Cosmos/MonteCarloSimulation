# Monte Carlo Simulation of Particles in a Box

This project simulates the dynamics of particles in a hard-walled box using Monte Carlo methods to model collisions and interactions. Particles are initialized with random positions, velocities, and masses, and the simulation tracks their motion while conserving energy and momentum. The goal is to investigate how macroscopic properties, such as temperature and pressure, depend on microscopic variables like kinetic energy and velocity distributions.

## Files of interest

- `Simulation.py` — simulation core (initialisation, time stepping, collision handling, observables)
- `Particles.py` — `Particle` class and defaults
- `plotGraph.py` — matplotlib animation that runs the simulation and plots the speed distribution
- `test_assert.py`, `stats.py`, `theory.py` — supporting scripts and tests

## Key Features

- Monte Carlo Collision Detection: The simulation detects collisions between particles and resolves them classically, ensuring conservation of momentum and energy.
- Macroscopic Observables: The program calculates and records properties like temperature, pressure, and kinetic energy, and plots these as a function of time or other variables.
- Statistical Distributions: The simulation reproduces distributions such as the Maxwell-Boltzmann distribution and explores how they evolve under different conditions (e.g., varying temperatures).
- Thermal Equilibration: It demonstrates the equilibration process of particles with each other and the walls over time, following the laws of thermodynamics.
- Sectional Box Division: The box can be divided into sections, allowing for a tunable accuracy of collision detection and interactions between particles.
- Validation: Results are compared to theoretical predictions to assess the accuracy of the simulation and the limitations of the chosen methods.

## Simulation Methods:

- Time-Stepping Algorithms: Implements time integration techniques like Euler-Cromer, Verlet, and Runge-Kutta to update particle positions and velocities.
- Conservation Laws: Ensures energy and momentum are conserved during particle interactions and collisions.


## Prerequisites

Packages:

- matplotlib >= 3.10.7
- numpy >= 2.3.3
- scipy >= 1.16.2
- sympy >= 1.14.0

## Installation (macOS / zsh)

```bash
# create and activate a venv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || python -m pip install matplotlib numpy scipy sympy

# run the simulation
python plotGraph.py
```

