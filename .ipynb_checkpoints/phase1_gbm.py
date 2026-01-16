# Phase 1: Simulate Stock Prices with Geometric Brownian Motion
import numpy as np
import matplotlib.pyplot as plt

# Parameters
np.random.seed(42)  # for reproducibility
S0 = 100            # initial stock price
mu = 0.08           # expected return
sigma = 0.2         # volatility
T = 1               # 1 year
dt = 1/252          # daily steps (252 trading days)
N = 1000            # number of paths
steps = int(T/dt)   # total steps

# Initialize stock price array
S = np.zeros((steps, N))
S[0] = S0

# Simulate GBM paths
for t in range(1, steps):
    Z = np.random.standard_normal(N)
    S[t] = S[t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)

# Plot the first 50 paths
plt.figure(figsize=(10,6))
plt.plot(S[:, :50])
plt.title("Sample GBM Stock Price Paths")
plt.xlabel("Days")
plt.ylabel("Stock Price")
plt.show()
