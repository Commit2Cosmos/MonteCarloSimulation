import sys
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Simulation import Simulation



simulation = Simulation()

lim = 1/2 * simulation.factor * simulation.meanFP


fig, (ax, ax2) = plt.subplots(1,2, gridspec_kw={'width_ratios': [1, 7]})

vs = np.linspace(0, 870, 40)

scatter = ax.scatter([],[], s=4)
bar = ax2.bar(vs, [0]*len(vs), width=0.9 * np.gradient(vs), align="edge")


def initial():
    ax.set_xlim(-lim , lim)
    ax.set_ylim(-lim , lim)
    ax.axis('off')

    ax2.set_xlim(vs[0],vs[-1])
    ax2.set_ylim(0, simulation.N)

    ax2.set_title('Distribution of speeds for Nitrogen gas')

    ax2.set_xlabel("Speed (m/s)")
    ax2.set_ylabel("Probability density (s/m)")

    return (scatter, *bar.patches)


def render(i):

    freq, bins = np.histogram(simulation.getSpeeds(), bins=vs)

    for rect, height in zip(bar.patches,freq):
        rect.set_height(height)

    simulation.advance()

    # posX, posY = simulation.getPositions()
    # scatter.set_offsets(np.c_[posX,posY])
    # scatter.set_color(simulation.getColor())
    return (scatter, *bar.patches)


anim = FuncAnimation(fig, render, init_func=initial, interval=1000, frames=range(120), blit = True, repeat = True)
plt.show()