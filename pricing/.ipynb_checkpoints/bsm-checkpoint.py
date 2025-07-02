"""
bsm.py

Black–Scholes–Merton analytic pricing for European vanilla options.
"""

import numpy as np
from scipy.stats import norm


def bsm_price(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    is_call: bool = True
) -> float:
    """
    Compute the Black–Scholes–Merton price of a European option.

    Parameters
    ----------
    S0 : float
        Current spot price of the underlying.
    K : float
        Strike price of the option.
    r : float
        Risk-free interest rate (annual, continuously compounded).
    sigma : float
        Volatility of the underlying (annual).
    T : float
        Time to maturity (in years).
    is_call : bool, optional
        If True (default), price a call; if False, price a put.

    Returns
    -------
    price : float
        The option price.

    Formula
    -------
    d1 = [ln(S0/K) + (r + 0.5*sigma^2)*T] / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)

    Call price: S0*N(d1) - K*exp(-r*T)*N(d2)
    Put  price: K*exp(-r*T)*N(-d2) - S0*N(-d1)
    """
    if T <= 0:
        # At expiry the option is worth its intrinsic value
        return max(0.0, (S0 - K) if is_call else (K - S0))

    # Avoid division by zero if sigma=0
    if sigma <= 0:
        forward = S0 * np.exp(r * T)
        intrinsic = (forward - K) if is_call else (K - forward)
        return np.exp(-r * T) * max(intrinsic, 0.0)

    sqrtT = np.sqrt(T)
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    if is_call:
        price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    return float(price)


if __name__ == "__main__":
    # Smoke test
    S0_test, K_test, r_test, sigma_test, T_test = 100, 100, 0.05, 0.2, 1.0
    for option_type in (True, False):
        name = "Call" if option_type else "Put"
        price = bsm_price(
            S0_test, K_test, r_test, sigma_test, T_test, is_call=option_type
        )
        print(f"{name:4s}  BSM price = {price:.4f}")