import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import yfinance as yf

# -------------------------------
# PARAMETERS
S0 = 100          # Starting price for simulation
r = 0.05          # Risk-free rate
T = 1.0           # 1 year
sigma = 0.3       # Estimated volatility
M = 50            # Number of Monte Carlo paths
N = 252           # Number of time steps (daily)

# -------------------------------
# FETCH HISTORICAL STOCK DATA (Tesla example)
ticker = "TSLA"
data = yf.download(ticker, period="1y", interval="1d")
hist_prices = data['Close'].values
hist_prices = hist_prices / hist_prices[0] * S0  # normalize to S0

# -------------------------------
# MONTE CARLO SIMULATION
dt = T / N
np.random.seed(42)
S = np.zeros((M, N))
S[:, 0] = S0

for t in range(1, N):
    Z = np.random.standard_normal(M)
    S[:, t] = S[:, t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)

# -------------------------------
# ENHANCED ANIMATION
fig, ax = plt.subplots(figsize=(12,6))

# Monte Carlo paths (blue)
mc_lines = [ax.plot([], [], color='blue', alpha=0.3)[0] for _ in range(M)]
# Historical stock line (red)
hist_line, = ax.plot(range(len(hist_prices)), hist_prices, color='red', linewidth=2, label=f'{ticker} Historical')

# Set axis limits
ax.set_xlim(0, N)
ax.set_ylim(0.9 * min(S.min(), hist_prices.min()), 1.1 * max(S.max(), hist_prices.max()))
ax.set_xlabel('Time Steps (Days)')
ax.set_ylabel('Stock Price')
ax.set_title(f'Monte Carlo Simulation vs {ticker} Historical Price')
ax.legend(loc='upper left')

# Initialize function
def init():
    for line in mc_lines:
        line.set_data([], [])
    hist_line.set_data(range(len(hist_prices)), hist_prices)
    return mc_lines + [hist_line]

# Update function for animation
def update(frame):
    for i, line in enumerate(mc_lines):
        # Gradual fade-in effect
        alpha = 0.1 + 0.9*(frame/N)
        line.set_alpha(alpha)
        line.set_data(range(frame), S[i,:frame])
    return mc_lines + [hist_line]

# Create animation
anim = FuncAnimation(fig, update, frames=N, init_func=init, blit=True)

# Save animation as GIF
anim.save('Phase5_MC_Animation_Enhanced.gif', writer=PillowWriter(fps=30))
plt.close()
