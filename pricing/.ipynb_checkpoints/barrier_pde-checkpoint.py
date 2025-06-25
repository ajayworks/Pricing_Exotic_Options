import numpy as np


class CrankNicolsonBarrierSolver:
    def __init__(
        self,
        S_max,
        K,
        B,
        T,
        r,
        sigma,
        M=100,
        N=100,
        is_call=True,
        barrier_type="down-and-out",
        rebate=0.0,
    ):
        self.S_max = S_max
        self.K = K
        self.B = B
        self.T = T
        self.r = r
        self.sigma = sigma
        self.M = M  # time steps
        self.N = N  # price steps
        self.is_call = is_call
        self.barrier_type = barrier_type
        self.rebate = rebate

        self.dS = S_max / N
        self.dt = T / M

        self.grid = np.zeros((M + 1, N + 1))
        self.S = np.linspace(0, S_max, N + 1)
        self.boundary_condition()
        self.setup_coefficients()

    def payoff(self):
        if self.is_call:
            return np.maximum(self.S - self.K, 0)
        else:
            return np.maximum(self.K - self.S, 0)

    def boundary_condition(self):
        if self.barrier_type == "down-and-out":
            self.barrier_index = int(self.B / self.dS)
            self.grid[:, : self.barrier_index + 1] = self.rebate
        elif self.barrier_type == "up-and-out":
            self.barrier_index = int(self.B / self.dS)
            self.grid[:, self.barrier_index :] = self.rebate

    def setup_coefficients(self):
        self.alpha = (
            0.25
            * self.dt
            * (
                (self.sigma**2) * (np.arange(1, self.N)) ** 2
                - self.r * np.arange(1, self.N)
            )
        )
        self.beta = (
            -0.5 * self.dt * ((self.sigma**2) * (np.arange(1, self.N)) ** 2 + self.r)
        )
        self.gamma = (
            0.25
            * self.dt
            * (
                (self.sigma**2) * (np.arange(1, self.N)) ** 2
                + self.r * np.arange(1, self.N)
            )
        )

        self.A = (
            np.diag(1 - self.beta)
            + np.diag(-self.alpha[1:], k=-1)
            + np.diag(-self.gamma[:-1], k=1)
        )
        self.B_mat = (
            np.diag(1 + self.beta)
            + np.diag(self.alpha[1:], k=-1)
            + np.diag(self.gamma[:-1], k=1)
        )

    def solve(self):
        self.grid[-1, :] = self.payoff()

        for m in reversed(range(self.M)):
            rhs = self.B_mat @ self.grid[m + 1, 1 : self.N]
            # Solve tridiagonal system
            self.grid[m, 1 : self.N] = np.linalg.solve(self.A, rhs)

            # Apply rebate/barrier boundary again to maintain knockout condition
            if self.barrier_type == "down-and-out":
                self.grid[m, : self.barrier_index + 1] = self.rebate
            elif self.barrier_type == "up-and-out":
                self.grid[m, self.barrier_index :] = self.rebate

        return np.interp(self.K, self.S, self.grid[0, :])
