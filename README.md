# Pricing Exotic Options using Stochastic Calculus, PDEs, and Monte Carlo Simulations

This project presents a rigorous numerical study on pricing exotic options using mathematical finance tools, including stochastic calculus, finite difference methods for partial differential equations (PDEs), and Monte Carlo simulations. Emphasis is placed on the comparative accuracy, stability, and efficiency of different numerical methods applied to exotic derivatives.

## 🔍 Objectives

- Implement the Black-Scholes-Merton model for vanilla European options
- Extend models to exotic payoffs: Asian, Barrier, and Lookback options
- Apply stochastic calculus and Ito’s Lemma to derive pricing PDEs
- Develop finite difference solvers (Explicit, Implicit, Crank-Nicolson)
- Build Monte Carlo engines with variance reduction techniques
- Use quasi-random methods (Sobol sequences) for high-dimensional simulation
- Analyze convergence, bias, and computational performance

## 📁 Project Structure

PricingExoticOptions/
├── notebooks/       ← Jupyter notebooks for development and experiments
├── pricing/         ← Modular pricing libraries (Monte Carlo, PDE solvers, BSM)
├── report/          ← Formal write-up with equations, plots, and conclusions
├── data/            ← Intermediate results, sample paths, market data
├── plots/           ← Saved figures for report and analysis
└── README.md        ← Project overview and guide

## ⚙️ Technologies Used

- **Python**: NumPy, SciPy, SymPy, Pandas
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Jupyter Notebooks** for prototyping and experiments
- **LaTeX** for final report with mathematical rigor
- **Git** for version control

## 📈 Methodological Highlights

- Closed-form pricing via Black-Scholes-Merton
- Numerical solution of parabolic PDEs using FDM
- Monte Carlo methods with antithetic and control variate techniques
- Convergence analysis with theoretical vs. empirical comparison
- Evaluation of Sobol sequences for low-discrepancy sampling

## 📚 Mathematical Tools

- Stochastic Differential Equations (SDEs)
- Ito’s Lemma and Feynman-Kac Theorem
- Partial Differential Equations in finance
- Brownian motion and martingales

## 🧪 Benchmarking and Validation

The models are tested against known analytic solutions where applicable and benchmarked on:
- Accuracy (vs. closed-form or high-resolution results)
- Speed (simulation vs. PDE)
- Stability and bias (for path-dependent options)

---

> This project is designed as a high-precision, modular, and mathematically grounded quantitative research tool for exotic derivatives pricing.