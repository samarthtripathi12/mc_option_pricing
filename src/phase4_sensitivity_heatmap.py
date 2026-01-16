import numpy as np
import matplotlib.pyplot as plt

# Parameters
S0 = 100
r = 0.05
T = 1.0
sigma_values = np.linspace(0.1, 0.5, 20)
K_values = np.linspace(90, 110, 20)
M = 5000  # number of Monte Carlo paths

prices = np.zeros((len(sigma_values), len(K_values)))

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
        payoff = np.maximum(S[:, -1] - K, 0)
        prices[i, j] = np.exp(-r*T) * np.mean(payoff)

# Plot heatmap
plt.figure(figsize=(8,6))
plt.imshow(prices, origin='lower', aspect='auto',
           extent=[K_values[0], K_values[-1], sigma_values[0], sigma_values[-1]],
           cmap='viridis')
plt.colorbar(label='Option Price')
plt.xlabel("Strike Price (K)")
plt.ylabel("Volatility (σ)")
plt.title("Sensitivity Analysis: Option Price vs σ & K")
plt.savefig("Phase4_Sensitivity.png")
plt.show()
