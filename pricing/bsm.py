import numpy as np
from scipy.stats import norm


def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    """
    Computes the Black-Scholes price of a European call or put option.

    Parameters
    ----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate
    sigma : float
        Volatility of the underlying asset
    option_type : str
        "call" or "put"

    Returns
    -------
    float
        Option price
    """
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return 0.0  # Handle degenerate input gracefully

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")


{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
