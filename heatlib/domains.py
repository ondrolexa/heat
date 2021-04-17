from abc import ABC, abstractmethod
from itertools import groupby
import numpy as np
import matplotlib.pyplot as plt

from heatlib.units import Length

#################################################
#            Domains                            #
#################################################


class Domain_1D(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @property
    def x_units(self):
        return self.x / abs(Length(1, self.plot_unit))


class Domain_Constant_1D(Domain_1D):
    def __init__(self, **kwargs):
        self.k = kwargs.get('k', 2.5)  # conductivity
        self.H = kwargs.get('H', 0)  # heat production
        self.L = abs(kwargs.get('L', 35000))  # model length
        self.n = kwargs.get('n', 100)  # number of nodes
        self.rho = kwargs.get('rho', 2700)  # density
        self.c = kwargs.get('c', 900)  # specific heat
        self.plot_unit = kwargs.get('plot_unit', 'm')  # plotting spatial unit

    def __repr__(self):
        return f'Domain_Constant_1D: ({self.n} nodes)'

    def info(self):
        return '\n'.join(
            [
                f'Domain size: {self.L} with {self.n} nodes.',
                f'k={self.k:g} H={self.H:g} rho={self.rho:g} c={self.c:g}',
            ]
        )

    @property
    def dx(self):
        return self.L / (self.n - 1)

    @property
    def x(self):
        return np.linspace(0, self.L, self.n)

    def show(self):
        plt.plot(np.ones_like(self.x_units), -self.x_units, 'k.-')
        plt.ylabel(f'Depth [{self.plot_unit}]')
        plt.xlabel(f'k={self.k:g} H={self.H:g} rho={self.rho:g} c={self.c:g}')
        plt.title(self)
        plt.show()


class Domain_Variable_1D(Domain_1D):
    def __init__(self, elements, **kwargs):
        self.elements = elements
        self.plot_unit = kwargs.get('plot_unit', 'm')  # plotting spatial unit

    def __repr__(self):
        return f'Domain_Variable_1D: ({len(self.elements)} elements)'

    def info(self):
        res = []
        for e, blk in groupby(self.elements):
            n = len(list(blk))
            res.append(f'{e.dx * n} {n} {e.info()}')
        return '\n'.join(res)

    @property
    def n(self):
        return len(self.elements) + 1

    @property
    def x(self):
        return np.hstack((0, np.cumsum([e.dx for e in self.elements])))

    @property
    def xm(self):
        return np.cumsum([e.dx for e in self.elements]) - np.array(
            [e.dx / 2 for e in self.elements]
        )

    @property
    def dx(self):
        return np.array([e.dx for e in self.elements])

    @property
    def k(self):
        return np.array([e.k for e in self.elements])

    @property
    def H(self):
        return np.array([e.H for e in self.elements])

    @property
    def rho(self):
        return np.array([e.rho for e in self.elements])

    @property
    def c(self):
        return np.array([e.c for e in self.elements])

    def show(self, prop='k'):
        x = [np.zeros_like(self.x), np.ones_like(self.x)]
        y = [-self.x_units, -self.x_units]
        plt.pcolor(x, y, np.atleast_2d(getattr(self, prop)), shading='flat')
        plt.colorbar()
        plt.ylabel(f'Depth [{self.plot_unit}]')
        plt.title(prop)
        plt.show()
