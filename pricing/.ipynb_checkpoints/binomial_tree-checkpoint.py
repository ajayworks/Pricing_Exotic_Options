# engines/binomial_tree.py

import numpy as np


class BinomialVanillaPricer:
    def __init__(self, S0, K, T, r, sigma, N=100, is_call=True):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.N = N
        self.is_call = is_call

        self.dt = T / N
        self.discount = np.exp(-r * self.dt)
        self.u = np.exp(sigma * np.sqrt(self.dt))
        self.d = 1 / self.u
        self.p = (np.exp(r * self.dt) - self.d) / (self.u - self.d)

    def price(self):
        # Step 1: Set up asset prices at maturity
        asset_prices = np.array(
            [self.S0 * self.u**j * self.d ** (self.N - j) for j in range(self.N + 1)]
        )

        # Step 2: Calculate payoff at maturity
        if self.is_call:
            option_values = np.maximum(asset_prices - self.K, 0)
        else:
            option_values = np.maximum(self.K - asset_prices, 0)

        # Step 3: Backward induction
        for i in range(self.N - 1, -1, -1):
            option_values = self.discount * (
                self.p * option_values[1:] + (1 - self.p) * option_values[:-1]
            )

        return option_values[0]
