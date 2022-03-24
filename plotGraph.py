import sys
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Simulation import Simulation



simulation = Simulation()



fig, (ax, ax2) = plt.subplots(1,2, gridspec_kw={'width_ratios': [7, 4]})

vs = np.linspace(0,simulation.maxRS/2 + 100,20)

scatter = ax.scatter([],[], s=4)
bar = ax2.bar(vs, [0]*len(vs), width=0.9 * np.gradient(vs), align="edge")


def initial():
    ax.set_xlim(-simulation.meanFP , simulation.meanFP)
    ax.set_ylim(-simulation.meanFP , simulation.meanFP)
    
    ax2.set_xlim(vs[0],vs[-1])
    ax2.set_ylim(0, simulation.N)

    return (scatter, *bar.patches)


def render(i):
    simulation.advance()

    freq, bins = np.histogram(simulation.getSpeeds(), bins=vs)

    for rect, height in zip(bar.patches,freq):
        rect.set_height(height)

    posX, posY = simulation.getPositions()
    scatter.set_offsets(np.c_[posX,posY])
    scatter.set_color(simulation.getColor())
    return (scatter, *bar.patches)

anim = FuncAnimation(fig, render, init_func=initial, interval=500, frames=range(120), blit = True, repeat = True)
plt.show()