import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.animation import FuncAnimation

# -------------------------------
# Parameters
S0 = 100           # starting stock price for simulation
r = 0.05           # risk-free rate
T = 1.0            # 1 year
sigma = 0.3        # estimated volatility
M = 50             # number of Monte Carlo paths
N = 252            # number of time steps (daily)

# -------------------------------
# Fetch historical stock data (example: Tesla)
ticker = "TSLA"
data = yf.download(ticker, period="1y", interval="1d")
historical_prices = data['Close'].values
historical_prices = historical_prices / historical_prices[0] * S0  # normalize

# -------------------------------
# Monte Carlo simulation
dt = T/N
np.random.seed(42)
S = np.zeros((M, N))
S[:, 0] = S0

for t in range(1, N):
    Z = np.random.standard_normal(M)
    S[:, t] = S[:, t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)

# -------------------------------
# Plot Monte Carlo vs Historical
plt.figure(figsize=(10,6))
for i in range(M):
    plt.plot(S[i], color='blue', alpha=0.3)
plt.plot(historical_prices, color='red', linewidth=2, label=f'{ticker} Historical')
plt.title(f'Monte Carlo Simulations vs {ticker} Historical Price')
plt.xlabel('Time Steps (Days)')
plt.ylabel('Price')
plt.legend()
plt.savefig("Phase5_MC_vs_Real.png")
plt.show()

# -------------------------------
# Optional: Animation of Monte Carlo paths
fig, ax = plt.subplots(figsize=(10,6))
lines = [ax.plot([], [], color='blue', alpha=0.3)[0] for _ in range(M)]
hist_line, = ax.plot([], [], color='red', linewidth=2, label=f'{ticker} Historical')

ax.set_xlim(0, N)
ax.set_ylim(0.9*np.min(S), 1.1*np.max(S))
ax.set_xlabel('Time Steps (Days)')
ax.set_ylabel('Price')
ax.set_title(f'Monte Carlo Paths Animation vs {ticker} Historical')
ax.legend()

def init():
    for line in lines:
        line.set_data([], [])
    hist_line.set_data(range(len(historical_prices)), historical_prices)
    return lines + [hist_line]

def update(frame):
    for i, line in enumerate(lines):
        line.set_data(range(frame), S[i,:frame])
    return lines + [hist_line]

anim = FuncAnimation(fig, update, frames=N, init_func=init, blit=True)
anim.save('Phase5_MC_Animation.gif', writer='pillow', fps=30)
plt.close()
