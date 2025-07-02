"""
monte_carlo.py

Monte Carlo pricing for European and Asian options, with confidence intervals.
"""

import numpy as np


def mc_european_price(S0, K, r, sigma, T, N_paths=100_000, N_steps=252, 
                      is_call=True, seed=None):
    """
    Price a European call/put via Monte Carlo simulation of GBM.

    Returns
    -------
    price : float
        Discounted expectation E[e^{-rT} payoff].
    ci_95 : float
        Half-width of the 95% confidence interval.
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / N_steps
    # simulate log returns
    Z = np.random.randn(N_paths, N_steps)
    increments = (r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z
    logS = np.cumsum(increments, axis=1)
    ST = S0 * np.exp(logS[:,-1])

    # payoff
    if is_call:
        payoff = np.maximum(ST - K, 0.0)
    else:
        payoff = np.maximum(K - ST, 0.0)

    discounted = np.exp(-r*T) * payoff
    price = discounted.mean()
    stderr = discounted.std(ddof=1) / np.sqrt(N_paths)
    ci_95 = 1.96 * stderr
    return price, ci_95


def mc_arithmetic_asian_price(S0, K, r, sigma, T, N_paths=100_000, N_steps=252, 
                              is_call=True, seed=None):
    """
    Price an Arithmetic Asian call/put via Monte Carlo simulation (discrete averaging).
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / N_steps
    Z = np.random.randn(N_paths, N_steps)
    increments = (r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z
    logS   = np.cumsum(increments, axis=1)
    S_paths = S0 * np.exp(logS)
    S_avg   = S_paths.mean(axis=1)

    if is_call:
        payoff = np.maximum(S_avg - K, 0.0)
    else:
        payoff = np.maximum(K - S_avg, 0.0)

    discounted = np.exp(-r*T) * payoff
    price = discounted.mean()
    stderr = discounted.std(ddof=1) / np.sqrt(N_paths)
    ci_95 = 1.96 * stderr
    return price, ci_95


if __name__ == "__main__":
    # Quick smoke tests
    print("European call", mc_european_price(100, 100, 0.05, 0.2, 1, seed=42))
    print("Asian call   ", mc_arithmetic_asian_price(100, 100, 0.05, 0.2, 1, seed=42))