import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import yfinance as yf

# -------------------------------
# PARAMETERS
S0 = 100
r = 0.05
T = 1.0
sigma = 0.3
M = 50
N = 252

# -------------------------------
# FETCH HISTORICAL STOCK DATA
ticker = "TSLA"
data = yf.download(ticker, period="1y", interval="1d")
hist_prices = data['Close'].values
hist_prices = hist_prices / hist_prices[0] * S0  # normalize

# -------------------------------
# MONTE CARLO SIMULATION
dt = T/N
np.random.seed(42)
S = np.zeros((M, N))
S[:,0] = S0

for t in range(1, N):
    Z = np.random.standard_normal(M)
    S[:,t] = S[:,t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)

# -------------------------------
# ENHANCED ANIMATION
fig, ax = plt.subplots(figsize=(12,6))

# Lines for Monte Carlo paths
mc_lines = [ax.plot([], [], color='blue', alpha=0.3)[0] for _ in range(M)]
# Line for historical stock
hist_line, = ax.plot([], [], color='red', linewidth=2, label=f'{ticker} Historical')

# Axes setup
ax.set_xlim(0, N)
ax.set_ylim(0.9 * min(S.min(), hist_prices.min()), 1.1 * max(S.max(), hist_prices.max()))
ax.set_xlabel('Time Steps (Days)')
ax.set_ylabel('Stock Price')
ax.set_title(f'Monte Carlo Simulation vs {ticker} Historical Price')
ax.legend(loc='upper left')

def init():
    for line in mc_lines:
        line.set_data([], [])
    hist_line.set_data(range(len(hist_prices)), hist_prices)
    return mc_lines + [hist_line]

def update(frame):
    for i, line in enumerate(mc_lines):
        # Animate with growing opacity for standout effect
        alpha = 0.1 + 0.9*(frame/N)
        line.set_alpha(alpha)
        line.set_data(range(frame), S[i,:frame])
    return mc_lines + [hist_line]

# Run animation
anim = FuncAnimation(fig, update, frames=N, init_func=init, blit=True)

# Save animation as GIF
anim.save('Phase5_MC_Animation_Enhanced.gif', writer=PillowWriter(fps=30))
plt.close()
