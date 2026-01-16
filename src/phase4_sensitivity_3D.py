import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------------------
# PHASE 4.2 – 3D Sensitivity Analysis
# Define the parameters (same as Phase 4.1)
S0 = 100
r = 0.05
T = 1.0
sigma_values = np.linspace(0.1, 0.5, 20)  # Volatility values
K_values = np.linspace(90, 110, 20)       # Strike price values
M = 5000  # Number of Monte Carlo paths

# Initialize price matrix
prices = np.zeros((len(sigma_values), len(K_values)))

# Compute Monte Carlo option prices for each combination of sigma and K
for i, sigma in enumerate(sigma_values):
    for j, K in enumerate(K_values):
        np.random.seed(42)
        dt = 1/252
        N = int(T/dt)
        S = np.zeros((M, N))
        S[:, 0] = S0
        for t in range(1, N):
            Z = np.random.standard_normal(M)
            S[:, t] = S[:, t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)
        payoff = np.maximum(S[:, -1] - K, 0)  # European Call Option
        prices[i, j] = np.exp(-r*T) * np.mean(payoff)

# -------------------------------
# Create 3D surface plot
K_grid, sigma_grid = np.meshgrid(K_values, sigma_values)

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(K_grid, sigma_grid, prices, cmap='viridis', edgecolor='k', alpha=0.9)

ax.set_xlabel("Strike Price (K)")
ax.set_ylabel("Volatility (σ)")
ax.set_zlabel("Option Price")
ax.set_title("3D Sensitivity Analysis: Option Price vs K & σ")

# Add colorbar
fig.colorbar(surf, shrink=0.5, aspect=10, label="Option Price")

# Save figure
plt.savefig("Phase4_Sensitivity3D.png")

# Show plot
plt.show()
