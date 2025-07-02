# 📘 Exotic Option Theory – Asian and Barrier Options

## Objectives

- Understand the mathematical formulation of Asian and barrier options
- Explore path integral formulation for Asian options
- Discuss sources of bias, variance, and discretization errors in exotic option pricing

## Asian Option Theory

Asian options depend on the **average price** of the underlying over time, making them path-dependent.

There are two types:
- **Average Price**: payoff based on average of prices.
- **Average Strike**: strike is the average.

### Payoff (Average Price Asian Call):

\[
C_{\text{Asian}} = \max\left( \frac{1}{n} \sum_{i=1}^n S_{t_i} - K, 0 \right)
\]

Due to the averaging, Asian options exhibit **lower volatility** than vanilla options.

### Limitation of Black-Scholes:

The arithmetic average of lognormal prices is **not lognormal** ⇒ no closed-form like vanilla options.

### PDE Formulation:

Let:

- \( A_t = \frac{1}{t} \int_0^t S_u \, du \) (running average)

Then the PDE becomes:

\[
\frac{\partial V}{\partial t} + rS \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + \left( \frac{A - A_t}{t} \right) \frac{\partial V}{\partial A} = rV
\]

## Barrier Option Theory

Barrier options activate or deactivate depending on whether the underlying crosses a set **barrier level**.

### Types:
- **Knock-in**: Only becomes active if barrier is touched.
- **Knock-out**: Expires worthless if barrier is touched.

Example: Down-and-Out Call → becomes worthless if asset falls below barrier \( B \) anytime.

### Boundary Conditions:

These are critical in PDE formulations.

- For Down-and-Out Call:
  \[
  V(S = B, t) = 0 \quad \text{(absorbing barrier)}
  \]
- For Knock-In options:
  More complex — requires tracking two regimes (activated/inactivated).

These are solved using **finite difference methods** or **Monte Carlo with path tracking**.

## Path Integrals for Asian Options

Asian option payoff depends on **integral over path**:

\[
A_T = \frac{1}{T} \int_0^T S_t \, dt
\]

This makes it a **functional** of the stochastic process \( S_t \).

We can express the expectation:

\[
C_{\text{Asian}} = e^{-rT} \mathbb{E} \left[ \max\left( A_T - K, 0 \right) \right]
\]

### 🔍 Challenges:
- Arithmetic average of lognormal distribution has no closed-form.
- **Geometric average** allows analytical solution via lognormality.

## Bias, Variance & Discretization Pitfalls

### Discretization Bias:

Sampling at discrete time steps introduces bias in estimating the integral:

\[
\hat{A}_T = \frac{1}{n} \sum_{i=1}^n S_{t_i} \neq \frac{1}{T} \int_0^T S_t \, dt
\]

This becomes negligible as \( n \to \infty \), but increases runtime.

---

### Variance & Monte Carlo:

Monte Carlo estimation has high variance. We reduce it using:
- **Antithetic Variates**
- **Control Variates** (e.g., using vanilla option)
- **Quasi-random sequences** (Sobol, Halton)

---

### Error Trade-off:

| Method           | Bias      | Variance   | Speed     |
|------------------|-----------|------------|-----------|
| PDE (FDM)        | Low       | None       | Fast      |
| Monte Carlo      | Low-ish   | High       | Slower    |
| Analytical (Geo) | None      | None       | Instant   |

## Summary

- Exotic options require more advanced techniques due to path dependence.
- Asian options involve time-averaging, while barrier options involve state-triggered conditions.
- Closed-form solutions are rare; we rely on **Monte Carlo** and **PDE solvers**.
- Numerical methods must balance accuracy, runtime, and stability.