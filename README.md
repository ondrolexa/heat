Heatlib
=======


[![GitHub version](https://badge.fury.io/gh/ondrolexa%2Fheatlib.svg)](https://badge.fury.io/gh/ondrolexa%2Fheatlib)

Python module for heat transfer modelling for students


* Free software: MIT license
* Documentation: https://ondrolexa.github.io/heat


This module provides classess to solve steady-state or evolutionary heat equation in 1D.

## Provided functionality

### Element, Domain and Model

  * ``Element`` - Class to define element with given physical properties and geometry
  * ``Domain_1D`` - Class for domain composed from list of ``Element`` instances.
  * ``Model_1D`` - Model class to solve and visualize solution on ``Domain_1D``

### Boundary conditions

  * ``Dirichlet_BC`` - Dirichlet boundary condition, i.e. prescribed temperature
  * ``Neumann_BC`` - Neumann boundary condition, i.e. prescribed heat flux

#### Solvers

  * ``SteadyState_1D`` - Steady state heat equation solution
  * ``BTCS_1D`` - Evolutionary heat equation solution
  * ``Deform_1D`` - Instantaneous deformation of model domain
  * ``SetTemperature_1D`` - Instantaneous change of temperature in given range

### Simulations

  * ``Simulation_1D`` - Class to assembly model and solvers to run and post-process simulation

## Simulation example

```python
from heatlib import *

uc_sed = Element('UCS', dx=25, k=3.2, H=1e-6, rho=2350, c=1000)
uc_base = Element('UCB', dx=50, k=2.5, H=3e-6, rho=2700, c=900)
mc = Element('MC', dx=100, k=2.3, H=1e-6, rho=2800, c=800)
lc_felsic = Element('LCF', dx=100, k=2, rho=2900, c=750)
lc_mafic = Element('LCM', dx=100, k=2, rho=3200, c=700)

geom = 100*uc_sed + 50*uc_base + 100*mc + 100*lc_felsic + 100*lc_mafic
dom = Domain_1D(geom, plot_unit="km")

tbc = Dirichlet_BC(0)
bbc = Neumann_BC(-0.032)

m = Model_1D(dom, tbc, bbc, time_unit='year')

init_solvers = [
    SteadyState_1D(),
    SetTemperature_1D(xmin=10000, xmax=15000, value=700)
]
simulation_solvers = [
    BTCS_1D(dt=Time(5000, 'year'), steps=10)
]
s = Simulation_1D(m, init_solvers, simulation_solvers, repeat=10)

s.run()

s.plot()
```
