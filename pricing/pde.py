"""
pde.py

Crank–Nicolson finite-difference solvers for European vanilla and barrier options,
plus the Reiner–Rubinstein analytic formula for down-and-out calls.
"""

import numpy as np
from scipy.linalg import solve_banded
from scipy.stats import norm


def crank_nicolson(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    Smax: float = None,
    N_S: int = 400,
    N_t: int = 800,
    is_call: bool = True,
) -> float:
    """
    Solve the Black–Scholes PDE via Crank–Nicolson and return the European
    call/put price at S0.

    Parameters
    ----------
    S0, K, r, sigma, T : floats
        Model parameters.
    Smax : float, optional
        Domain upper bound; default = 4*K if None.
    N_S  : int
        Number of spatial grid points.
    N_t  : int
        Number of time steps.
    is_call : bool
        True for call, False for put.

    Returns
    -------
    price : float
        Option price at S0.
    """
    if Smax is None:
        Smax = 4 * K

    dS = Smax / N_S
    dt = T / N_t
    S = np.linspace(0, Smax, N_S + 1)

    # Terminal payoff
    if is_call:
        V = np.maximum(S - K, 0.0)
    else:
        V = np.maximum(K - S, 0.0)

    # Precompute tridiagonal coefficients
    i = np.arange(1, N_S)
    alpha = 0.25 * dt * (sigma**2 * i**2 - r * i)
    beta = -0.5 * dt * (sigma**2 * i**2 + r)
    gamma = 0.25 * dt * (sigma**2 * i**2 + r * i)

    # Build banded matrix A and matrix Bm
    # A x_new = Bm x_old + bc terms
    A = np.zeros((3, N_S - 1))
    Bm = np.zeros((3, N_S - 1))

    A[0, 1:] = -gamma[:-1]
    A[1, :] = 1 - beta
    A[2, :-1] = -alpha[1:]

    Bm[0, 1:] = gamma[:-1]
    Bm[1, :] = 1 + beta
    Bm[2, :-1] = alpha[1:]

    # Time-stepping backward
    for n in range(N_t):
        t = T - n * dt
        rhs = Bm[0] * V[2:] + Bm[1] * V[1:-1] + Bm[2] * V[:-2]
        # boundary conditions: V(0) = 0 (for calls), V(Smax) = intrinsic at top
        # left BC contributes nothing, right BC:
        bc = (
            (Smax - K * np.exp(-r * (t - dt)))
            if is_call
            else (K * np.exp(-r * (t - dt)))
        )
        rhs[-1] -= gamma[-1] * bc

        # solve tridiagonal system
        V[1:-1] = solve_banded((1, 1), A, rhs)

        # enforce boundaries
        V[0] = 0 if is_call else K * np.exp(-r * (t - dt))
        V[-1] = bc

    # interpolate to S0
    return float(np.interp(S0, S, V))


def crank_nicolson_barrier(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    B: float,
    Smax: float = None,
    N_S: int = 400,
    N_t: int = 800,
) -> float:
    """
    Crank–Nicolson solver for a down-and-out European call.
    Barrier B knocks the option out if S <= B at any grid node.
    """
    if Smax is None:
        Smax = 4 * K

    dS = Smax / N_S
    dt = T / N_t
    S = np.linspace(0, Smax, N_S + 1)

    # Terminal payoff with barrier
    V = np.maximum(S - K, 0.0)
    V[S <= B] = 0.0

    # Interior indices
    i = np.arange(1, N_S)
    alpha = 0.25 * dt * (sigma**2 * i**2 - r * i)
    beta = -0.5 * dt * (sigma**2 * i**2 + r)
    gamma = 0.25 * dt * (sigma**2 * i**2 + r * i)

    A = np.zeros((3, N_S - 1))
    Bm = np.zeros((3, N_S - 1))
    A[0, 1:] = -gamma[:-1]
    A[1] = 1 - beta
    A[2, :-1] = -alpha[1:]
    Bm[0, 1:] = gamma[:-1]
    Bm[1] = 1 + beta
    Bm[2, :-1] = alpha[1:]

    for n in range(N_t):
        t = T - n * dt
        rhs = Bm[0] * V[2:] + Bm[1] * V[1:-1] + Bm[2] * V[:-2]

        # enforce top boundary
        bc = Smax - K * np.exp(-r * (t - dt))
        rhs[-1] -= gamma[-1] * bc

        V[1:-1] = solve_banded((1, 1), A, rhs)

        # enforce barrier at each time slice
        V[S <= B] = 0.0
        V[0] = 0.0
        V[-1] = bc

    return float(np.interp(S0, S, V))


def rr_down_out_call(
    S0: float, K: float, B: float, r: float, T: float, sigma: float
) -> float:
    """
    Reiner–Rubinstein closed-form for a down-and-out European call (no rebate).
    """
    if not (0 < B < S0):
        raise ValueError("Barrier B must satisfy 0 < B < S0")

    mu = (r + 0.5 * sigma**2) / sigma**2
    sigmaT = sigma * np.sqrt(T)

    x1 = np.log(S0 / B) / sigmaT + mu * sigmaT
    x2 = x1 - sigmaT
    y1 = np.log(B**2 / (S0 * K)) / sigmaT + mu * sigmaT
    y2 = y1 - sigmaT

    A = S0 * norm.cdf(x1) - K * np.exp(-r * T) * norm.cdf(x2)
    Bterm = S0 * (B / S0) ** (2 * mu) * norm.cdf(y1) - K * np.exp(-r * T) * (
        B / S0
    ) ** (2 * mu - 2) * norm.cdf(y2)
    return float(A - Bterm)
