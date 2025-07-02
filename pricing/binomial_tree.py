"""
binomial_tree.py

Cox–Ross–Rubinstein (CRR) binomial‐tree pricing for European vanilla options.
"""

import numpy as np


def binomial_crr_price(
    S0: float, K: float, r: float, sigma: float, T: float, N: int, is_call: bool = True
) -> float:
    """
    Price a European vanilla call or put using the Cox–Ross–Rubinstein binomial tree.

    Parameters
    ----------
    S0 : float
        Initial stock price.
    K : float
        Option strike price.
    r : float
        Risk-free interest rate (annual, continuously compounded).
    sigma : float
        Volatility of the underlying (annual).
    T : float
        Time to maturity (in years).
    N : int
        Number of time steps in the binomial tree.
    is_call : bool, optional
        If True (default), prices a call; if False, prices a put.

    Returns
    -------
    float
        The discounted option price at time zero.
    """
    # Step size
    dt = T / N
    # Up/down factors
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    # Risk-neutral probability
    p = (np.exp(r * dt) - d) / (u - d)
    # Discount factor per step
    disc = np.exp(-r * dt)

    # 1) Compute terminal asset prices S_T at all nodes
    j = np.arange(N + 1)
    ST = S0 * (u ** (N - j)) * (d**j)

    # 2) Compute terminal payoffs
    if is_call:
        payoff = np.maximum(ST - K, 0.0)
    else:
        payoff = np.maximum(K - ST, 0.0)

    # 3) Backward induction with overflow-suppression
    price = payoff.copy()
    for step in range(N, 0, -1):
        with np.errstate(over="ignore"):
            price = disc * (p * price[:step] + (1 - p) * price[1 : step + 1])
        # sanitize infinities/nans
        price = np.nan_to_num(price, posinf=0.0, neginf=0.0, nan=0.0)

    return float(price[0])


if __name__ == "__main__":
    # Simple smoke test: compare small N vs known values
    S0_test, K_test, r_test, vol_test, T_test = 100, 100, 0.05, 0.2, 1.0
    for N_test in (10, 50, 100, 500):
        c = binomial_crr_price(
            S0_test, K_test, r_test, vol_test, T_test, N_test, is_call=True
        )
        p = binomial_crr_price(
            S0_test, K_test, r_test, vol_test, T_test, N_test, is_call=False
        )
        print(f"N={N_test:3d}  Call={c:.4f}  Put={p:.4f}")
