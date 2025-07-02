# Theoretical Framework: Vanilla Option Pricing

## 1. Black-Scholes-Merton (BSM) Model

The Black-Scholes model assumes the underlying asset follows a **geometric Brownian motion (GBM)** under the risk-neutral measure:

\[
dS_t = r S_t \,dt + \sigma S_t \,dW_t
\]

Where:
- \( S_t \): asset price at time \( t \)
- \( r \): risk-free rate
- \( \sigma \): volatility
- \( W_t \): standard Brownian motion

---

## 2. Derivation of the Black-Scholes-Merton (BSM) PDE via Itô's Lemma

Assume the asset price \( S(t) \) follows a **geometric Brownian motion (GBM)**:

\[
dS = \mu S \, dt + \sigma S \, dW_t
\]

Let \( V(S,t) \) be the price of a derivative depending on \( S \) and \( t \). By **Itô’s Lemma**:

\[
dV = \left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S \frac{\partial V}{\partial S} dW_t
\]

To eliminate risk, construct a **delta-hedged portfolio**:

\[
\Pi = V - \Delta S
\]

Differentiating:

\[
d\Pi = dV - \Delta dS
\]

Substitute the expressions for \( dV \) and \( dS \), and choose \( \Delta = \frac{\partial V}{\partial S} \) to eliminate the stochastic term:

\[
d\Pi = \left( \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt
\]

Since the portfolio is risk-free, it must earn the risk-free rate \( r \):

\[
d\Pi = r \Pi \, dt = r \left( V - S \frac{\partial V}{\partial S} \right) dt
\]

Equating both expressions and rearranging, we get the **BSM PDE**:

\[
\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0
\]

---

## 3. Closed-Form BSM Formula

### European Call Option:

\[
C(S, t) = S N(d_1) - K e^{-r(T - t)} N(d_2)
\]

\[
d_1 = \frac{\ln\left(\frac{S}{K}\right) + (r + \frac{1}{2} \sigma^2)(T - t)}{\sigma \sqrt{T - t}}, \quad
d_2 = d_1 - \sigma \sqrt{T - t}
\]

### European Put Option:

\[
P(S, t) = K e^{-r(T - t)} N(-d_2) - S N(-d_1)
\]

---

## 4. Greeks – Sensitivity Analysis

| Greek | Formula (Call) | Interpretation |
|-------|----------------|----------------|
| **Delta** | \( \frac{\partial C}{\partial S} = N(d_1) \) | Sensitivity to underlying asset |
| **Gamma** | \( \frac{\partial^2 C}{\partial S^2} = \frac{N'(d_1)}{S\sigma\sqrt{T - t}} \) | Rate of change of Delta |
| **Vega** | \( \frac{\partial C}{\partial \sigma} = S \sqrt{T - t} N'(d_1) \) | Sensitivity to volatility |
| **Theta** | \( \frac{\partial C}{\partial t} \) | Time decay |
| **Rho** | \( \frac{\partial C}{\partial r} = K (T - t) e^{-r(T - t)} N(d_2) \) | Sensitivity to interest rate |

---

## 5. Monte Carlo Derivation

We simulate asset paths under the risk-neutral GBM:

\[
S_T = S_0 \exp\left( \left(r - \frac{1}{2} \sigma^2\right) T + \sigma \sqrt{T} Z \right), \quad Z \sim \mathcal{N}(0,1)
\]

The price of a European call:

\[
C = e^{-rT} \mathbb{E}[\max(S_T - K, 0)]
\]

Use:
- \( N \) simulated paths
- Estimate via sample average

---

## 6. PDE Derivation from BSM

We solve the BSM PDE backward in time with terminal condition:

\[
V(S, T) = \max(S - K, 0) \quad \text{(for call)}
\]

Boundary conditions:
- \( V(0, t) = 0 \)
- \( V(S \to \infty, t) \sim S - K e^{-r(T - t)} \)

Numerical methods like **Crank-Nicolson**, **Explicit**, or **Implicit** schemes are used.

---

## 7. Implied Volatility: Newton-Raphson Method

Given market price \( C_{\text{mkt}} \), we solve for implied volatility \( \sigma^* \) such that:

\[
C_{\text{BSM}}(\sigma^*) = C_{\text{mkt}}
\]

Using Newton-Raphson:

\[
\sigma_{n+1} = \sigma_n - \frac{C_{\text{BSM}}(\sigma_n) - C_{\text{mkt}}}{\text{Vega}(\sigma_n)}
\]

---

## ✅ Summary

This document captures:
- Analytical BSM framework
- Derivation of Greeks
- PDE and MC formulation from first principles
- Implied volatility calibration

Used throughout the pricing engine for benchmarking and validation.