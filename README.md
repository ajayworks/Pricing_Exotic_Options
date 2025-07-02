# Pricing Exotic Options

[![GitHub last commit](https://img.shields.io/github/last-commit/ajayworks/Pricing_Exotic_Options)](https://github.com/ajayworks/Pricing_Exotic_Options)
[![GitHub repo size](https://img.shields.io/github/repo-size/ajayworks/Pricing_Exotic_Options)](https://github.com/ajayworks/Pricing_Exotic_Options)
[![GitHub stars](https://img.shields.io/github/stars/ajayworks/Pricing_Exotic_Options?style=social)](https://github.com/ajayworks/Pricing_Exotic_Options/stargazers)

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Pricing Exotic Options using Stochastic Calculus, PDEs, and Monte Carlo Simulations

This project presents a rigorous numerical study on pricing exotic options using mathematical finance tools, including stochastic calculus, finite difference methods for partial differential equations (PDEs), and Monte Carlo simulations. Emphasis is placed on the comparative accuracy, stability, and efficiency of different numerical methods applied to exotic derivatives.

## 🔍 Objectives

- Implement the Black-Scholes-Merton model for vanilla European options
- Extend models to exotic payoffs: Asian and Barrier
- Apply stochastic calculus and Ito’s Lemma to derive pricing PDEs
- Develop finite difference solvers (Explicit, Implicit, Crank-Nicolson)
- Build Monte Carlo engines with variance reduction techniques
- Use quasi-random methods (Sobol sequences) for high-dimensional simulation
- Analyze convergence, bias, and computational performance

## 📁 Project Structure

PricingExoticOptions/
├── notebooks/       ← Jupyter notebooks for development and experiments
├── pricing/         ← Modular pricing libraries (Monte Carlo, PDE solvers, BSM, Binomial Tree)
├── report/          ← Formal write-up with equations, plots, and conclusions
├── plots/           ← Saved figures for report and analysis
└── README.md        ← Project overview and guide

## ⚙️ Technologies Used

- **Python**: NumPy, SciPy, SymPy, Pandas
- **Visualization**: Matplotlib, Seaborn
- **Jupyter Notebooks** for prototyping and experiments
- **LaTeX** for final report with mathematical rigor
- **Git** for version control

## Quickstart

1. **Install dependencies (conda recommended):**
    ```bash
    conda env create -f environment.yml
    conda activate exotic-options
    ```
    _or, for pip:_
    ```bash
    pip install -r requirements.txt
    ```

2. **Run notebooks**  
    Open the `notebooks/` directory and run any Jupyter notebook for interactive experiments and theory.

3. **Core modules usage**
    You can import classes/functions from the `pricing/` directory in your own scripts.


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

> This project is designed as a high-precision, modular, and mathematically grounded quantitative research tool for exotic options pricing.