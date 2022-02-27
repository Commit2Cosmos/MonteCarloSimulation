from functools import partial
from tkinter import E
import numpy as np


# Creating a Particle class; all particles will be instances of this class with default properties


class Particle():

    # constructor
    # acceleration = np.zeros(2),
    def __init__(self, position = np.zeros(2), velocity = np.ones(2), mass = 1):
        
        self.position = position
        self.velocity = velocity
        # self.acceleration = acceleration
        self.mass = mass

# add children to create particles of different mass