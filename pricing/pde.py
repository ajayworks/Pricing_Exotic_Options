import numpy as np


class CrankNicolsonSolver:
    def __init__(self, S_max, K, T, r, sigma, M, N, is_call=True):
        self.S_max = S_max
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.M = M  # time steps
        self.N = N  # price steps
        self.is_call = is_call

        self.dt = T / M
        self.dS = S_max / N
        self.grid = np.linspace(0, S_max, N + 1)

    def payoff(self):
        if self.is_call:
            return np.maximum(self.grid - self.K, 0)
        else:
            return np.maximum(self.K - self.grid, 0)

    def solve(self):
        dt, dS = self.dt, self.dS
        M, N = self.M, self.N
        r, sigma, K = self.r, self.sigma, self.K
        grid = self.grid

        V = self.payoff()
        alpha = (
            0.25 * dt * ((sigma**2) * (np.arange(N + 1) ** 2) - r * np.arange(N + 1))
        )
        beta = -dt * 0.5 * ((sigma**2) * (np.arange(N + 1) ** 2) + r)
        gamma = (
            0.25 * dt * ((sigma**2) * (np.arange(N + 1) ** 2) + r * np.arange(N + 1))
        )

        A = np.zeros((N - 1, N - 1))
        B = np.zeros((N - 1, N - 1))

        for i in range(1, N):
            if i > 1:
                A[i - 1, i - 2] = -alpha[i]
                B[i - 1, i - 2] = alpha[i]
            A[i - 1, i - 1] = 1 - beta[i]
            B[i - 1, i - 1] = 1 + beta[i]
            if i < N - 1:
                A[i - 1, i] = -gamma[i]
                B[i - 1, i] = gamma[i]

        for t in range(M):
            V_inner = V[1:-1]
            rhs = B @ V_inner

            # Boundary conditions
            rhs[0] += alpha[1] * V[0] + gamma[1] * V[0]
            rhs[-1] += alpha[N - 1] * V[N] + gamma[N - 1] * V[N]

            V[1:-1] = np.linalg.solve(A, rhs)

            # Enforce boundary values (Dirichlet)
            V[0] = 0
            V[N] = (
                self.S_max - K * np.exp(-r * (self.T - (t + 1) * dt))
                if self.is_call
                else K * np.exp(-r * (self.T - (t + 1) * dt))
            )

        return V, grid


{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
