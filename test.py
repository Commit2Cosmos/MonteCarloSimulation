import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

randints = np.random.randint(100, size=100)

fig, ax = plt.subplots()

vs = np.arange(0, 100, 25)

# Plot the histogram with hist() function
bar = ax.bar(vs, [0]*len(vs), width=0.9 * np.gradient(vs), align="edge", alpha=0.8)

# print(hist)

# Label axes and set title

ax.set_title("Title")
ax.set_xlabel("X_Label")
ax.set_ylabel("Y_Label")


def render(i):

    bar.set_offsets(np.random.randint(100, size=100), edgecolor = "black", bins = 5)
    return bar.patches


# anim = FuncAnimation(fig, render, interval=1000, frames=range(1200), blit = True, repeat = False)


plt.show()


















# # useful for drawing curve to show M-B distrib
# import scipy.stats as st

# plt.hist(x, density=True, bins=82, label="Data")
# mn, mx = plt.xlim()
# plt.xlim(mn, mx)
# kde_xs = np.linspace(mn, mx, 300)
# kde = st.gaussian_kde(x)
# plt.plot(kde_xs, kde.pdf(kde_xs), label="PDF")
# plt.legend(loc="upper left")
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Histogram");