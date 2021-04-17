"""Top-level package for Heatlib."""

from heatlib.units import Length, Time
from heatlib.tracers import Tracer_1D
from heatlib.boundary_conditions import Boundary_Condition, Dirichlet_BC, Neumann_BC
from heatlib.elements import Element
from heatlib.domains import Domain_Constant_1D, Domain_Variable_1D
from heatlib.models import Model_Constant_1D, Model_Variable_1D
from heatlib.solvers import (
    SetTemperature_1D,
    Deform_Constant_1D,
    Shift_Constant_1D,
    SteadyState_Constant_1D,
    BTCS_Constant_1D,
    Deform_Variable_1D,
    SteadyState_Variable_1D,
    BTCS_Variable_1D,
)
from heatlib.simulations import Simulation_1D

__all__ = [
    'Length',
    'Time',
    'Tracer_1D',
    'Boundary_Condition',
    'Dirichlet_BC',
    'Neumann_BC',
    'Element',
    'Domain_Constant_1D',
    'Domain_Variable_1D',
    'Model_Constant_1D',
    'Model_Variable_1D',
    'SetTemperature_1D',
    'Deform_Constant_1D',
    'Shift_Constant_1D',
    'SteadyState_Constant_1D',
    'BTCS_Constant_1D',
    'Deform_Variable_1D',
    'SteadyState_Variable_1D',
    'BTCS_Variable_1D',
    'Simulation_1D',
]

__author__ = """Ondrej Lexa"""
__email__ = 'lexa.ondrej@gmail.com'
__version__ = '0.1.0'
