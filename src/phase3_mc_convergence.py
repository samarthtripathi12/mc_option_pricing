import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# -------------------------------
# Load GBM stock paths
# -------------------------------
S0 = 100
K = 100
r = 0.05
T = 1.0
sigma = 0.2

# -------------------------------
# Black-Scholes price
# -------------------------------
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
bs_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# -------------------------------
# Simulation sizes
# -------------------------------
simulation_sizes = [1000, 5000, 10000, 50000, 100000]
mc_prices = []

for M in simulation_sizes:
    np.random.seed(42)
    dt = 1/252
    N = int(T/dt)
    S = np.zeros((M, N))
    S[:, 0] = S0
    
    for t in range(1, N):
        Z = np.random.standard_normal(M)
        S[:, t] = S[:, t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)
    
    # Monte Carlo call price
    S_T = S[:, -1]
    payoff = np.maximum(S_T - K, 0)
    mc_price = np.exp(-r*T) * np.mean(payoff)
    mc_prices.append(mc_price)

# -------------------------------
# Plot convergence
# -------------------------------
plt.figure(figsize=(8,5))
plt.plot(simulation_sizes, mc_prices, marker='o', label='Monte Carlo Price')
plt.axhline(bs_price, color='r', linestyle='--', label='Black-Scholes Price')
plt.xlabel("Number of Simulations")
plt.ylabel("Option Price")
plt.title("Monte Carlo Convergence to Black-Scholes")
plt.legend()
plt.grid(True)
plt.savefig("Phase3_MC_Convergence.png")
plt.show()
