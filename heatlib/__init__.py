"""Top-level package for Heatlib."""

import importlib.metadata

from heatlib.boundary_conditions import Boundary_Condition, Dirichlet_BC, Neumann_BC
from heatlib.domains import Domain_1D
from heatlib.elements import Element
from heatlib.models import Model_1D
from heatlib.simulations import Simulation_1D
from heatlib.solvers import (
    BTCS_1D,
    Deform_1D,
    SetTemperature_1D,
    SteadyState_1D,
)
from heatlib.tracers import Tracer_1D
from heatlib.units import (
    Density,
    Heat_Production,
    Length,
    Specific_Heat_Capacity,
    Thermal_Conductivity,
    Time,
)

__all__ = [
    "Length",
    "Thermal_Conductivity",
    "Heat_Production",
    "Density",
    "Specific_Heat_Capacity",
    "Time",
    "Tracer_1D",
    "Boundary_Condition",
    "Dirichlet_BC",
    "Neumann_BC",
    "Element",
    "Domain_1D",
    "Model_1D",
    "SetTemperature_1D",
    "SteadyState_1D",
    "BTCS_1D",
    "Deform_1D",
    "Simulation_1D",
]

__author__ = """Ondrej Lexa"""
__email__ = "lexa.ondrej@gmail.com"
try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode
