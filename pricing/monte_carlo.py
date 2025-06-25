import numpy as np


class MonteCarloPricer:
    def __init__(
        self,
        S0,
        K,
        T,
        r,
        sigma,
        n_paths=10000,
        n_steps=100,
        option_type="call",
        seed=None,
    ):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.n_paths = n_paths
        self.n_steps = n_steps
        self.option_type = option_type.lower()
        self.dt = T / n_steps
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)

    def generate_paths(self):
        """Simulate GBM paths"""
        S = np.zeros((self.n_paths, self.n_steps + 1))
        S[:, 0] = self.S0
        for t in range(1, self.n_steps + 1):
            Z = np.random.randn(self.n_paths)
            S[:, t] = S[:, t - 1] * np.exp(
                (self.r - 0.5 * self.sigma**2) * self.dt
                + self.sigma * np.sqrt(self.dt) * Z
            )
        return S

    def price_european_option(self):
        """Price European Call/Put using MC"""
        S = self.generate_paths()
        S_T = S[:, -1]
        if self.option_type == "call":
            payoff = np.maximum(S_T - self.K, 0)
        elif self.option_type == "put":
            payoff = np.maximum(self.K - S_T, 0)
        else:
            raise ValueError("Invalid option_type. Choose 'call' or 'put'.")
        return np.exp(-self.r * self.T) * np.mean(payoff)

    def price_asian_option(self):
        """Price Arithmetic Asian Option using MC"""
        S = self.generate_paths()
        S_avg = S.mean(axis=1)
        if self.option_type == "call":
            payoff = np.maximum(S_avg - self.K, 0)
        elif self.option_type == "put":
            payoff = np.maximum(self.K - S_avg, 0)
        else:
            raise ValueError("Invalid option_type. Choose 'call' or 'put'.")
        return np.exp(-self.r * self.T) * np.mean(payoff)

    def price_with_confidence_interval(self):
        """Returns option price and 95% confidence interval"""
        S = self.generate_paths()
        S_T = S[:, -1]
        if self.option_type == "call":
            payoff = np.maximum(S_T - self.K, 0)
        elif self.option_type == "put":
            payoff = np.maximum(self.K - S_T, 0)
        else:
            raise ValueError("Invalid option_type. Choose 'call' or 'put'.")

        discounted = np.exp(-self.r * self.T) * payoff
        price = np.mean(discounted)
        stderr = np.std(discounted) / np.sqrt(self.n_paths)
        ci_95 = 1.96 * stderr
        return price, (price - ci_95, price + ci_95)

    def simulate_payoffs(self):
        S = self.generate_paths()
        S_T = S[:, -1]

        if self.option_type == "call":
            payoff = np.maximum(S_T - self.K, 0)
        elif self.option_type == "put":
            payoff = np.maximum(self.K - S_T, 0)
        else:
            raise ValueError("Invalid option_type. Choose 'call' or 'put'.")

        discounted = np.exp(-self.r * self.T) * payoff
        return discounted


{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
