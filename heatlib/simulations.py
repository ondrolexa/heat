import numpy as np
import matplotlib.pyplot as plt

from heatlib.units import Length, Time
from heatlib.tracers import Tracer_1D
from heatlib.solvers import Solver_1D

#################################################
#            Simulation                         #
#################################################


class Simulation_1D:
    def __init__(self, model, init_solvers, sim_solvers, **kwargs):
        # args
        self.model = model
        if isinstance(init_solvers, Solver_1D):
            self.init_solvers = [init_solvers]
        else:
            self.init_solvers = init_solvers
        if isinstance(sim_solvers, Solver_1D):
            self.sim_solvers = [sim_solvers]
        else:
            self.sim_solvers = sim_solvers
        tracers = kwargs.get('tracers', None)
        if isinstance(tracers, Tracer_1D):
            self.tracers = [tracers]
        else:
            self.tracers = tracers
        # kwargs
        self.repeat = kwargs.get('repeat', 1)
        # init
        self._sols = []

    def time_steps(self):
        return np.array(
            [sol['time_abs'] / abs(Time(1, self.model.time_unit)) for sol in self._sols]
        )

    def plot(self, **kwargs):
        solutions = kwargs.pop('solutions', range(len(self._sols)))
        fig, ax = plt.subplots(**kwargs)
        for sol in solutions:
            T = self._sols[sol]['T']
            x = self._sols[sol]['x'] / abs(Length(1, self.model.domain.plot_unit))
            tm = self._sols[sol]['time_abs'] / abs(Time(1, self.model.time_unit))
            lbl = f'{tm:g}'
            ax.plot(T, -x, label=lbl)
            ax.set_xlabel('Temperature [°C]')
            ax.set_ylabel(f'Depth [{self.model.domain.plot_unit}]')
            ax.legend(loc='best', title=f'Time [{self.model.time_unit}]')
        plt.show()

    def run(self):
        # Init solvers
        for s in self.init_solvers:
            s.solve(self.model, tracers=self.tracers)
        self._sols.append(
            dict(
                time_abs=self.model._time_abs,
                x=self.model.domain.x.copy(),
                T=self.model.T.copy(),
            )
        )
        if self.tracers is not None:
            for tracer in self.tracers:
                tracer.mark_current()
        # main simulation loop
        for i in range(self.repeat):
            for s in self.sim_solvers:
                s.solve(self.model, tracers=self.tracers)
            self._sols.append(
                dict(
                    time_abs=self.model._time_abs,
                    x=self.model.domain.x.copy(),
                    T=self.model.T.copy(),
                )
            )
            if self.tracers is not None:
                for tracer in self.tracers:
                    tracer.mark_current()
        print('Done.')
