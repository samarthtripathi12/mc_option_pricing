import numpy as np

# ----- Parameters -----
K = 105       # Strike price
r = 0.05      # Risk-free rate
T = 1         # 1 year

# ----- Load stock data from Phase 1 -----
S = np.load("GBM_stock_data.npy")   # Load saved stock paths
S_T = S[-1]                         # Final stock prices at T=1

# ----- Monte Carlo Call Option Pricing -----
payoff = np.maximum(S_T - K, 0)     # European Call payoff
C0 = np.exp(-r*T) * np.mean(payoff) # Discounted expected value

print("European Call Option Price (Monte Carlo):", C0)
