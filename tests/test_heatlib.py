#!/usr/bin/env python

"""Tests for `heatlib` package."""

import pytest


from heatlib import *


@pytest.fixture
def domain_c():
    return Domain_Constant_1D(L=Length(35, 'km'), n=350, H=1e-6, plot_unit='km')


@pytest.fixture
def tbc():
    return Dirichlet_BC(0)


@pytest.fixture
def bbc():
    return Neumann_BC(-0.032)


@pytest.fixture
def model_c(domain_c, tbc, bbc):
    return Model_Constant_1D(domain_c, tbc, bbc, time_unit='y')


@pytest.fixture
def steady_c():
    return SteadyState_Constant_1D()


@pytest.fixture
def intrusion():
    return SetTemperature_1D(xmin=10000, xmax=15000, value=700)


@pytest.fixture
def single_step():
    return BTCS_Constant_1D(dt=Time('1000', 'y'))


@pytest.fixture
def repeated_step():
    return BTCS_Constant_1D(dt=Time('1000', 'y'), steps=20)


def test_steady_constant_solver(model_c, steady_c):
    model_c.solve(steady_c)
    assert model_c.T[-1] == pytest.approx(693)


def test_set_temperature_solver(model_c, steady_c, intrusion):
    model_c.solve(steady_c)
    model_c.solve(intrusion)
    assert model_c.get_T(12500) == 700


def test_btcs_constant_solver(model_c, steady_c, intrusion, repeated_step):
    model_c.solve(steady_c)
    model_c.solve(intrusion)
    model_c.solve(repeated_step)
    assert model_c.get_T(12500) == pytest.approx(688.48948)


def test_simulation(model_c, steady_c, intrusion, single_step):
    s = Simulation_1D(model_c, [steady_c, intrusion], [single_step], repeat=20)
    s.run()
    assert s.model.get_T(12500) == pytest.approx(688.48948)
