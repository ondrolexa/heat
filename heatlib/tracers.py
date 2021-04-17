import numpy as np

from heatlib.units import Length, Time

#################################################
#            Tracer                             #
#################################################


class Tracer_1D:
    def __init__(self, name, x, **kwargs):
        self.name = name
        self._x = abs(x)
        self._T = None
        self.store = {}
        self.log = None
        self._store_ix = []
        self.plot_unit = kwargs.get('plot_unit', 'm')  # plotting spatial unit
        self.time_unit = kwargs.get('time_unit', 's')  # default plotting time units

    def __repr__(self):
        return f'Tracer {self.name}: x={self._x} T={self._T}'

    def record(self, model, log, init=False):
        if self._x >= 0:
            if init:
                self._T = model.get_T(self._x)
                self.store['T'] = [self._T]
                self.store['x'] = [self._x]
                self.store['time_abs'] = [0]
                self.log = [log]
            else:
                self._T = model.get_T(self._x)
                self.store['T'].append(self._T)
                self.store['x'].append(self._x)
                self.store['time_abs'].append(model._time_abs)
                self.log.append(log)

    @property
    def x_all(self):
        f = abs(Length(1, self.plot_unit))
        return np.array([x / f for x in self.store['x']])

    @property
    def x(self):
        return self.x_all[self._store_ix]

    @property
    def T_all(self):
        return np.array(self.store['T'])

    @property
    def T(self):
        return self.T_all[self._store_ix]

    @property
    def time_all(self):
        f = abs(Time(1, self.time_unit))
        return np.array([t / f for t in self.store['time_abs']])

    @property
    def time(self):
        return self.time_all[self._store_ix]
