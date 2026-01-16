import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# -------------------------------
# Load GBM data (Phase 1)
# -------------------------------
S = np.load("GBM_stock_data.npy")

# -------------------------------
# Parameters (LOCKED)
# -------------------------------
S0 = 100.0
K = 100.0
r = 0.05
T = 1.0
sigma = 0.2   # THEORETICAL volatility (critical)

# -------------------------------
# Monte Carlo price
# -------------------------------
S_T = S[:, -1]
payoff = np.maximum(S_T - K, 0)
mc_price = np.exp(-r * T) * np.mean(payoff)

# -------------------------------
# Black-Scholes price
# -------------------------------
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

bs_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# -------------------------------
# Output
# -------------------------------
print("Monte Carlo Call Price:", mc_price)
print("Black-Scholes Call Price:", bs_price)

# -------------------------------
# Plot comparison
# -------------------------------
plt.figure()
plt.bar(["Monte Carlo", "Black-Scholes"], [mc_price, bs_price])
plt.ylabel("Option Price")
plt.title("Phase 3: Monte Carlo vs Black-Scholes (Convergence)")
plt.ylim(0, 15)
plt.savefig("Phase3_MC_vs_BS.png")
plt.show()
