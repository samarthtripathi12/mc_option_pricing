import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters -----
S0 = 100       # starting stock price
mu = 0.08      # expected return
sigma = 0.2    # volatility
T = 1          # 1 year
dt = 1/252     # daily step
N = 50         # number of simulated paths

# ----- Prepare array -----
steps = int(T/dt)
S = np.zeros((steps, N))
S[0] = S0

# ----- Simulate stock price paths -----
for t in range(1, steps):
    S[t] = S[t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.randn(N))

# ----- Plot -----
plt.figure(figsize=(10,6))
plt.plot(S)
plt.title("GBM Stock Price Paths")
plt.xlabel("Days")
plt.ylabel("Stock Price")
plt.savefig("GBM_stock_paths.png")   # Save plot BEFORE show
plt.show()                            # Display plot in notebook

# ----- Save stock price data -----
np.save("GBM_stock_data.npy", S)     # Save the stock paths
print("Phase 1 complete: Plot and data saved as 'GBM_stock_paths.png' and 'GBM_stock_data.npy'.")
