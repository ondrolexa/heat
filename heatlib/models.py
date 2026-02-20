import matplotlib.pyplot as plt
import numpy as np

from heatlib.boundary_conditions import Boundary_Condition
from heatlib.domains import Domain_1D
from heatlib.solvers import Solver_1D
from heatlib.units import Time

#################################################
#            Models                             #
#################################################


class Model_1D:
    def __init__(self, domain, bc0, bc1, **kwargs):
        assert isinstance(
            domain, Domain_1D
        ), "You have to use Domain_1D instance as argument."
        assert isinstance(
            bc0, Boundary_Condition
        ), "Second argument must be Boundary_Condition."
        assert isinstance(
            bc1, Boundary_Condition
        ), "Third argument must be Boundary_Condition."
        self.domain = domain
        self.bc0 = bc0
        self.bc1 = bc1
        self.time_unit = kwargs.get("time_unit", "s")  # default plotting time units
        self.orientation = kwargs.get(
            "orientation", "vertical"
        )  # default plotting orientation
        self.figsize = kwargs.get("figsize", (9, 6))  # default figure size
        self.T = None
        self._time_abs = 0.0

    @property
    def time(self):
        return (self._time_abs * Time(1).unit).to(self.time_unit).magnitude

    def get_T(self, x):
        if self.T is not None:
            return np.interp(abs(x), self.domain.x, self.T)
        else:
            print("Model has not yet solution.")
            return None

    def __repr__(self):
        if self.T is None:
            return "No solutions. Ready for initial one."
        elif self._time_abs == 0.0:
            return "Model with initial solution"
        else:
            return f"Model with evolutionary solution for time {self.time:g}{self.time_unit}"

    def info(self):
        print(self.bc0)
        print(self.domain.info())
        print(self.bc1)

    def solve(self, solver, **kwargs):
        assert isinstance(
            solver, Solver_1D
        ), "You have to use Solver_1D instance as argument."
        solver.solve(self, **kwargs)

    def plot(self):
        if self.T is not None:
            fig, ax = plt.subplots(figsize=self.figsize)
            if self.orientation == "vertical":
                ax.plot(
                    self.T,
                    self.domain.x_units,
                    label=f"t={self.time:g}{self.time_unit}",
                )
                ax.yaxis.set_inverted(True)
                ax.set_xlabel("Temperature [°C]")
                ax.set_ylabel(f"Depth [{self.domain.plot_unit}]")
            else:
                ax.plot(
                    self.domain.x_units,
                    self.T,
                    label=f"t={self.time:g}{self.time_unit}",
                )
                ax.set_xlabel(f"Distance [{self.domain.plot_unit}]")
                ax.set_ylabel("Temperature [°C]")
            ax.legend(loc="best")
            plt.show()
        else:
            print("Model has not yet any solution.")
