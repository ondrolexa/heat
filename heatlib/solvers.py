from abc import ABC, abstractmethod

import numpy as np
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve

from heatlib.boundary_conditions import Dirichlet_BC

#################################################
#            Solvers                            #
#################################################


class Solver_1D(ABC):
    def __init__(self, **kwargs):
        self.log = kwargs.get("log", False)

    @abstractmethod
    def solve(self, model, tracers=None):
        pass

    def tracers(self, model, tracers, init=False):
        if tracers is not None and self.log:
            for tracer in tracers:
                tracer.record(model, type(self).__name__, init)


class SetTemperature_1D(Solver_1D):
    def __init__(self, **kwargs):
        self.xmin = abs(kwargs.get("xmin", 0))
        self.xmax = abs(kwargs.get("xmax", np.inf))
        self.value = kwargs.get("value", 0)
        super().__init__(**kwargs)

    def solve(self, model, tracers=None):
        idx = (model.domain.x >= self.xmin) & (model.domain.x <= self.xmax)
        model.T[idx] = self.value
        super().tracers(model, tracers)


class Deform_1D(Solver_1D):
    def __init__(self, **kwargs):
        self.factors = kwargs.get("factors", 1)
        self.steps = kwargs.get("steps", 1)
        super().__init__(**kwargs)

    def solve(self, model, tracers=None):
        factors = np.atleast_1d(self.factors)
        if len(factors) == 1:
            factors = factors * np.ones_like(model.domain.elements)
        for i in range(self.steps):
            x_old = model.domain.x
            for e, factor in zip(model.domain.elements, factors):
                e.dx *= factor
            if tracers is not None:
                x_new = model.domain.x
                for tracer in tracers:
                    tracer._x = np.interp(tracer._x, x_old, x_new)
        super().tracers(model, tracers)


class SteadyState_1D(Solver_1D):
    def solve(self, model, tracers=None):
        if model.bc0 is not None and model.bc1 is not None:
            kl, kr = model.domain.k[:-1], model.domain.k[1:]
            Hl, Hr = model.domain.H[:-1], model.domain.H[1:]
            dxl, dxr = model.domain.dx[:-1], model.domain.dx[1:]
            alfa, beta = kl / dxl, kr / dxr
            dl = np.hstack((alfa, 1, 0))
            dm = np.hstack((1, -(alfa + beta), 1))
            dr = np.hstack((0, 1, beta))
            # Sparse coefficient matrix
            A = spdiags([dl, dm, dr], [-1, 0, 1], model.domain.n, model.domain.n, "csr")
            # Column vector of constant terms and BC
            b = np.hstack((0, -(dxr * Hl + dxl * Hr) / 2, 0))
            # Boundary conditions
            if isinstance(model.bc0, Dirichlet_BC):
                A[0, :2] = [1, 0]
                b[0] = model.bc0.value
            else:  # Neumann
                A[0, :2] = [-2 * model.domain.k[0], 2 * model.domain.k[0]]
                b[0] = (
                    -2 * model.bc0.value * model.domain.dx[0]
                    - model.domain.H[0] * model.domain.dx[0] ** 2
                )

            if isinstance(model.bc1, Dirichlet_BC):
                A[-1, -2:] = [0, 1]
                b[-1] = model.bc1.value
            else:  # Neumann
                A[-1, -2:] = [2 * model.domain.k[-1], -2 * model.domain.k[-1]]
                b[-1] = (
                    2 * model.bc1.value * model.domain.dx[-1]
                    - model.domain.H[-1] * model.domain.dx[-1] ** 2
                )
            # solution
            model.T = spsolve(A, b)
            model._time_abs = 0.0
            super().tracers(model, tracers, init=True)


class BTCS_1D(Solver_1D):
    def __init__(self, **kwargs):
        self.dt = abs(kwargs.get("dt", 1))
        self.steps = kwargs.get("steps", 1)
        super().__init__(**kwargs)

    def solve(self, model, tracers=None):
        if model.T is not None:
            kl, kr = model.domain.k[:-1], model.domain.k[1:]
            Hl, Hr = model.domain.H[:-1], model.domain.H[1:]
            dxl, dxr = model.domain.dx[:-1], model.domain.dx[1:]
            rl, rr = model.domain.rho[:-1], model.domain.rho[1:]
            cl, cr = model.domain.c[:-1], model.domain.c[1:]
            alfa = kl * (1 + dxr / dxl)
            beta = kr * (1 + dxl / dxr)
            gama = (
                cl * rl * dxr**2 + dxl * dxr * (cl * rr + cr * rl) + cr * rr * dxl**2
            ) / (2 * self.dt)
            delta = (Hl * dxr**2 + dxl * dxr * (Hl + Hr) + Hr * dxl**2) / 2
            # Sparse coefficient matrix and column vector
            dl = np.hstack((-alfa, 1, 0))
            dm = np.hstack((1, alfa + beta + gama, 1))
            dr = np.hstack((0, 1, -beta))
            # Sparse coefficient matrix A
            A = spdiags([dl, dm, dr], [-1, 0, 1], model.domain.n, model.domain.n, "csr")
            # Column vector of constant terms
            b = np.hstack((0, delta, 0))
            # Boundary conditions
            if isinstance(model.bc0, Dirichlet_BC):
                A[0, :2] = [1, 0]
                b[0] = model.bc0.value
                gamma_b0 = 0
            else:  # Neumann
                gamma_b0 = (
                    model.domain.c[0]
                    * model.domain.rho[0]
                    * model.domain.dx[0] ** 2
                    / self.dt
                )
                A[0, :2] = [gamma_b0 + 2 * model.domain.k[0], -2 * model.domain.k[0]]
                b[0] = (
                    -model.domain.H[0] * model.domain.dx[0] ** 2
                    + 2 * model.domain.dx[0] * model.bc0.value
                )
            if isinstance(model.bc1, Dirichlet_BC):
                A[-1, -2:] = [0, 1]
                b[-1] = model.bc1.value
                gamma_b1 = 0
            else:  # Neumann
                gamma_b1 = (
                    model.domain.c[-1]
                    * model.domain.rho[-1]
                    * model.domain.dx[-1] ** 2
                    / self.dt
                )
                A[-1, -2:] = [
                    -2 * model.domain.k[-1],
                    gamma_b1 + 2 * model.domain.k[-1],
                ]
                b[-1] = (
                    -model.domain.H[-1] * model.domain.dx[-1] ** 2
                    - 2 * model.domain.dx[-1] * model.bc1.value
                )
            # Calculate solution of next time step(s)
            m = np.hstack((gamma_b0, gama, gamma_b1))
            for i in range(self.steps):
                model.T = spsolve(A, b + m * model.T)
                model._time_abs += self.dt
            super().tracers(model, tracers)
