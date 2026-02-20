from itertools import groupby

import matplotlib.pyplot as plt
import numpy as np

from heatlib.units import Length

#################################################
#            Domains                            #
#################################################


class Domain_1D:
    def __init__(self, elements, **kwargs):
        self.elements = elements
        self.figsize = kwargs.get("figsize", (9, 6))  # default figure size
        self.plot_unit = kwargs.get("plot_unit", "m")  # plotting spatial unit

    def __repr__(self):
        return f"Domain_1D: ({len(self.elements)} elements)"

    def info(self):
        res = []
        for e, blk in groupby(self.elements):
            n = len(list(blk))
            res.append(f"{e.dx * n} {n} {e.info()}")
        return "\n".join(res)

    @property
    def n(self):
        return len(self.elements) + 1

    @property
    def x(self):
        return np.hstack((0, np.cumsum([e.dx for e in self.elements])))

    @property
    def x_units(self):
        return (self.x * Length(1).unit).to(self.plot_unit).magnitude

    @property
    def xm(self):
        return np.cumsum([e.dx for e in self.elements]) - np.array(
            [e.dx / 2 for e in self.elements]
        )

    @property
    def xm_units(self):
        return (self.xm * Length(1).unit).to(self.plot_unit).magnitude

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

    def show(self, prop="k"):
        fig, ax = plt.subplots(figsize=self.figsize)
        x = [np.zeros_like(self.x), np.ones_like(self.x)]
        y = [self.x_units, self.x_units]
        h = ax.pcolor(x, y, np.atleast_2d(getattr(self, prop)), shading="flat")
        ax.yaxis.set_inverted(True)
        cbar = fig.colorbar(h, ax=ax)
        cbar.minorticks_on()
        plt.ylabel(f"Depth [{self.plot_unit}]")
        plt.title(prop)
        plt.show()
