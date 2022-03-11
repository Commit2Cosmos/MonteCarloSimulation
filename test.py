import pandas as pd
import numpy as np

np.random.seed(5)
# from Particles import Particle

# N = 3

# data=[Particle(i) for i in range(N)]

# particlesData = pd.DataFrame()

# print(data[0].positionX)



x, y = np.random.rand(1,2)[0]

















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