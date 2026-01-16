# ==============================
# Interactive Monte Carlo Finance Simulator
# Phases 2 + 4 + 5 Combined
# ==============================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf
from IPython.display import display, clear_output
import ipywidgets as widgets
from scipy.stats import norm

# -------------------------------
# DEFAULT PARAMETERS
S0 = 100          # initial stock price
r = 0.05          # risk-free rate
T = 1.0           # maturity in years
sigma = 0.3       # volatility
mu = 0.07         # drift / expected return
K = 100           # strike price
M = 50            # Monte Carlo paths
N = 252           # time steps (daily)
ticker = "TSLA"   # default stock for historical data

# -------------------------------
# FUNCTION: Black-Scholes Price
def black_scholes_call(S0, K, T, r, sigma):
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

# -------------------------------
# FUNCTION: Monte Carlo Simulation
def monte_carlo_sim(S0, r, sigma, mu, T, M, N):
    dt = T/N
    S = np.zeros((M, N))
    S[:,0] = S0
    for t in range(1, N):
        Z = np.random.standard_normal(M)
        S[:,t] = S[:,t-1]*np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)
    return S

# -------------------------------
# FUNCTION: European Call Price via Monte Carlo
def monte_carlo_call_price(S, K, r, T):
    payoff = np.maximum(S[:,-1] - K, 0)
    price = np.exp(-r*T)*np.mean(payoff)
    return price

# -------------------------------
# FETCH HISTORICAL DATA
data = yf.download(ticker, period="1y", interval="1d")
hist_prices = data['Close'].values
hist_prices = hist_prices / hist_prices[0] * S0  # normalize to S0

# -------------------------------
# INTERACTIVE WIDGETS
sigma_slider = widgets.FloatSlider(value=sigma, min=0.05, max=0.6, step=0.01, description='Volatility')
mu_slider = widgets.FloatSlider(value=mu, min=-0.1, max=0.2, step=0.01, description='Drift')
K_slider = widgets.IntSlider(value=K, min=int(0.8*S0), max=int(1.2*S0), step=1, description='Strike Price')
T_slider = widgets.FloatSlider(value=T, min=0.25, max=2.0, step=0.05, description='Maturity (yrs)')
M_slider = widgets.IntSlider(value=M, min=10, max=200, step=5, description='Paths')

# -------------------------------
# PLOTTING FUNCTION
def update_plot(sigma, mu, K, T, M):
    S = monte_carlo_sim(S0, r, sigma, mu, T, M, N)
    mc_price = monte_carlo_call_price(S, K, r, T)
    bs_price = black_scholes_call(S0, K, T, r, sigma)
    
    plt.figure(figsize=(12,6))
    # Monte Carlo paths
    for i in range(M):
        plt.plot(S[i,:], color='blue', alpha=0.3)
    # Historical stock line
    plt.plot(hist_prices, color='red', linewidth=2, label=f'{ticker} Historical')
    plt.xlabel('Time Steps (Days)')
    plt.ylabel('Stock Price')
    plt.title(f'Monte Carlo Paths vs {ticker} Historical')
    plt.legend()
    plt.show()
    
    # Display Option Prices
    print(f"Monte Carlo Call Price: {mc_price:.4f}")
    print(f"Black-Scholes Call Price: {bs_price:.4f}")

# -------------------------------
# CREATE INTERACTIVE DISPLAY
widgets.interactive(update_plot, sigma=sigma_slider, mu=mu_slider, K=K_slider, T=T_slider, M=M_slider)
