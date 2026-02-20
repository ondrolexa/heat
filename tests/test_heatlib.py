#!/usr/bin/env python

"""Tests for `heatlib` package."""

import pytest

from heatlib import (
    BTCS_1D,
    Dirichlet_BC,
    Domain_1D,
    Element,
    Model_1D,
    Neumann_BC,
    SetTemperature_1D,
    Simulation_1D,
    SteadyState_1D,
    Time,
)


@pytest.fixture
def domain():
    el = Element("A", dx=100, k=2.5, rho=2700, c=900, H=1e-6)
    return Domain_1D(350 * el, plot_unit="km")


@pytest.fixture
def tbc():
    return Dirichlet_BC(0)


@pytest.fixture
def bbc():
    return Neumann_BC(-0.032)


@pytest.fixture
def model(domain, tbc, bbc):
    return Model_1D(domain, tbc, bbc, time_unit="year")


@pytest.fixture
def steady():
    return SteadyState_1D()


@pytest.fixture
def intrusion():
    return SetTemperature_1D(xmin=10000, xmax=15000, value=700)


@pytest.fixture
def single_step():
    return BTCS_1D(dt=Time("1000", "year"))


@pytest.fixture
def repeated_step():
    return BTCS_1D(dt=Time("1000", "year"), steps=20)


def test_steady_state_solver(model, steady):
    model.solve(steady)
    assert model.T[-1] == pytest.approx(693)


def test_set_temperature_solver(model, steady, intrusion):
    model.solve(steady)
    model.solve(intrusion)
    assert model.get_T(12500) == 700


def test_btcs_solver(model, steady, intrusion, repeated_step):
    model.solve(steady)
    model.solve(intrusion)
    model.solve(repeated_step)
    assert model.get_T(12500) == pytest.approx(689.50185908)


def test_simulation(model, steady, intrusion, single_step):
    s = Simulation_1D(model, [steady, intrusion], [single_step], repeat=20)
    s.run()
    assert s.model.get_T(12500) == pytest.approx(689.50185908)
