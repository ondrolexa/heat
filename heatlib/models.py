from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

from heatlib.units import Time
from heatlib.boundary_conditions import Boundary_Condition
from heatlib.domains import Domain_Constant_1D, Domain_Variable_1D
from heatlib.solvers import Solver_1D

#################################################
#            Models                             #
#################################################


class Model_1D(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        assert isinstance(
            self.bc0, Boundary_Condition
        ), 'Second argument must be Boundary_Condition.'
        assert isinstance(
            self.bc1, Boundary_Condition
        ), 'Third argument must be Boundary_Condition.'
        self.time_unit = kwargs.get('time_unit', 's')  # default plotting time units
        self.T = None
        self._time_abs = 0.0

    @property
    def time(self):
        return self._time_abs / abs(Time(1, self.time_unit))

    def get_T(self, x):
        if self.T is not None:
            return np.interp(abs(x), self.domain.x, self.T)
        else:
            print('Model has not yet solution.')
            return None

    def __repr__(self):
        if self.T is None:
            return 'No solutions. Ready for initial one.'
        elif self._time_abs == 0.0:
            return 'Model with initial solution'
        else:
            return f'Model with evolutionary solution for time {self.time:g}{self.time_unit}'

    def info(self):
        print(self.bc0)
        print(self.domain.info())
        print(self.bc1)

    def solve(self, solver, **kwargs):
        assert isinstance(
            solver, Solver_1D
        ), 'You have to use Solver_1D instance as argument.'
        solver.solve(self, **kwargs)

    def plot(self):
        if self.T is not None:
            fig, ax = plt.subplots(figsize=(9, 6))
            ax.plot(
                self.T, -self.domain.x_units, label=f't={self.time:g}{self.time_unit}'
            )
            ax.set_xlabel('Temperature [°C]')
            ax.set_ylabel(f'Depth [{self.domain.plot_unit}]')
            ax.legend(loc='best')
            plt.show()
        else:
            print('Model has not yet any solution.')


class Model_Constant_1D(Model_1D):
    def __init__(self, domain, bc0, bc1, **kwargs):
        assert isinstance(
            domain, Domain_Constant_1D
        ), 'You have to use Domain_Constant_1D instance as argument.'
        self.domain = domain
        self.bc0 = bc0
        self.bc1 = bc1
        super().__init__(**kwargs)


class Model_Variable_1D(Model_1D):
    def __init__(self, domain, bc0, bc1, **kwargs):
        assert isinstance(
            domain, Domain_Variable_1D
        ), 'You have to use Domain_Variable_1D instance as argument.'
        self.domain = domain
        self.bc0 = bc0
        self.bc1 = bc1
        super().__init__(**kwargs)

    @property
    def Tm(self):
        if self.T is not None:
            return np.interp(self.domain.xm, self.domain.x, self.T)
        else:
            print('Model has not yet solution.')
