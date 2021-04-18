#####
Usage
#####

To use this library you have to import it.

.. code-block:: python

    from heatlib import *

***************
Simple examples
***************

Example for domain with constant physical properties
====================================================

Lets create model for crustal (35 km) geotherm with 100m resolution,
1e-6 heat production and default other crustal properties… ``plot_unit``
argument allows change plotting spatial units.

.. code-block:: python

    d_c = Domain_Constant_1D(L=Length(35, 'km'), n=350, H=1e-6, plot_unit='km')

Now we need to define boundary conditions. We will use ``Dirichlet_BC``
at top and ``Neumann_BC`` with 32mW/m2 at bottom.

.. code-block:: python

    tbc = Dirichlet_BC(0)
    bbc = Neumann_BC(-0.032)

Now we can create ``Model_Constant_1D`` instance to assemble domain and
BCs… ``time_unit`` argument allows change plotting time units.

.. code-block:: python

    m_c = Model_Constant_1D(d_c, tbc, bbc, time_unit='y')

Now, we can setup solvers we will use for modelling

.. code-block:: python

    init_c = SteadyState_Constant_1D()
    intrusion_c = SetTemperature_1D(xmin=10000, xmax=15000, value=700)
    small_step_c = BTCS_Constant_1D(dt=Time(5000, 'y'))
    big_step_c = BTCS_Constant_1D(dt=Time(5000, 'y'), steps=50)

We will use two solvers to calculate initial state…

.. code-block:: python

    m_c.solve(init_c)
    m_c.solve(intrusion_c)
    m_c.plot()



.. image:: images/output_12_0.png


.. code-block:: python

    m_c.info()


.. parsed-literal::

    Dirichlet BC: 0
    Domain size: 35000.0 with 350 nodes.
    k=2.5 H=1e-06 rho=2700 c=900
    Neumann BC: -0.032


Once initial state is ready, we can use evolutionary solver to solve
evolutionary equation… Note, that time step is defined in solver.

.. code-block:: python

    m_c.solve(small_step_c)
    m_c.plot()



.. image:: images/output_15_0.png


.. code-block:: python

    m_c.get_T(Length(12.5, 'km'))




.. parsed-literal::

    699.2665798968195



To calculate evolutionary solution for more time steps, we can use
solver instantiated with ``steps`` argument.

.. code-block:: python

    m_c.solve(big_step_c)
    m_c.plot()



.. image:: images/output_18_0.png


.. code-block:: python

    m_c.get_T(Length(12.5, 'km'))

.. parsed-literal::

    488.2480815751985



Example for domain with variable physical properties and grid size
==================================================================

Lets create model for crustal geotherm with several layers…

.. code-block:: python

    uc_sed = Element('UCS', dx=25, k=3.2, H=1e-6, rho=2350, c=1000)
    uc_base = Element('UCB', dx=50, k=2.5, H=3e-6, rho=2700, c=900)
    mc = Element('MC', dx=100, k=2.3, H=1e-6, rho=2800, c=800)
    lc_felsic = Element('LCF', dx=100, k=2, rho=2900, c=750)
    lc_mafic = Element('LCM', dx=100, k=2, rho=3200, c=700)

To create domain, we need to provide list of elements to define domain
geometry… We can use multilication and addition of elements to assemble
it

.. code-block:: python

    geom = 100*uc_sed + 50*uc_base + 100*mc + 100*lc_felsic + 100*lc_mafic
    d_v = Domain_Variable_1D(geom, plot_unit='km')
    d_v




.. parsed-literal::

    Domain_Variable_1D: (450 elements)



``show`` method of could be used to visualize domain and property

.. code-block:: python

    d_v.show('H')



.. image:: images/output_25_0.png


Now we can create ``Model_Variable_1D`` instance to assemble domain and
BCs…

.. code-block:: python

    m_v = Model_Variable_1D(d_v, tbc, bbc, time_unit='y')

Now, we can setup solvers we will use for modelling

.. code-block:: python

    init_v = SteadyState_Variable_1D()
    intrusion_v = SetTemperature_1D(xmin=10000, xmax=15000, value=700)
    small_step_v = BTCS_Variable_1D(dt=Time(5000, 'y'))
    big_step_v = BTCS_Variable_1D(dt=Time(5000, 'y'), steps=50)

We will use two solvers to calculate initial state…

.. code-block:: python

    m_v.solve(init_v)
    m_v.solve(intrusion_v)
    m_v.plot()



.. image:: images/output_31_0.png


.. code-block:: python

    m_v.info()


.. parsed-literal::

    Dirichlet BC: 0
    2500.0 100 UCS: k=3.2  H=1e-06  rho=2350  c=1000
    2500.0 50 UCB: k=2.5  H=3e-06  rho=2700  c=900
    10000.0 100 MC: k=2.3  H=1e-06  rho=2800  c=800
    10000.0 100 LCF: k=2  H=0  rho=2900  c=750
    10000.0 100 LCM: k=2  H=0  rho=3200  c=700
    Neumann BC: -0.032


Once initial state is ready, we can use evolutionary solver to solve
evolutionary equation… Remember that time step is defined in solver and
units of time step are defined by ``t_units`` property of model.

.. code-block:: python

    m_v.solve(small_step_v)
    m_v.plot()



.. image:: images/output_34_0.png


To calculate evolutionary solution for more time steps, we can use
solver instantiated with ``step`` argument.

.. code-block:: python

    m_v.solve(big_step_v)
    m_v.plot()



.. image:: images/output_36_0.png


******************
Additional solvers
******************


Deformation
===========

``Deform_Constant_1D`` solver allows to strech computational domain
instantaneosly by given ``factor``.

.. code-block:: python

    d_c = Domain_Constant_1D(L=35000, n=350, H=1e-6, plot_unit='km')
    m_c = Model_Constant_1D(d_c, tbc, bbc, time_unit='Ma')
    calc_dt = Time(5000, 'y')
    edot = 3e-15
    stretch = np.exp(edot * calc_dt.to('s'))
    deform_c = Deform_Constant_1D(factor=stretch)
    btcs_c = BTCS_Constant_1D(dt=calc_dt)

.. code-block:: python

    s = Simulation_1D(m_c, init_c, 50*[deform_c, btcs_c], repeat=10)

.. code-block:: python

    s.run()


.. parsed-literal::

    Done.


.. code-block:: python

    s.plot(figsize=(14, 8))



.. image:: images/output_49_0.png


Erosion
=======

``Shift_Constant_1D`` solver allows to extend/trim domain by given
``amount``.

.. code-block:: python

    d_c = Domain_Constant_1D(L=35000, n=350, H=1e-6, plot_unit='km')
    m_c = Model_Constant_1D(d_c, tbc, bbc, time_unit='Ma')
    calc_dt = Time(5000, 'y')
    erosion_vel = Length(0.5, 'cm').to('m') / Time(1, 'y')
    erode = erosion_vel * calc_dt
    erosion_c = Shift_Constant_1D(amount=-erode)
    btcs_c = BTCS_Constant_1D(dt=calc_dt)

.. code-block:: python

    s = Simulation_1D(m_c, [init_c, intrusion_c], 20*[erosion_c, btcs_c], repeat=10)

.. code-block:: python

    s.run()


.. parsed-literal::

    Done.


.. code-block:: python

    s.plot(figsize=(14, 8))



.. image:: images/output_54_0.png


***********
Simulations
***********

Assembly simulation
===================

``Simulation_1D`` class allows you to automatize the model calculation,
store model results and could be used for model post-processing.

We will use model used in previous example and we will define solvers…

.. code-block:: python

    init_v = SteadyState_Variable_1D()
    intrusion_v = SetTemperature_1D(xmin=Length(21, 'km'),
                                    xmax=Length(24, 'km'),
                                    value=700)
    diffuse_v = BTCS_Variable_1D(dt=Time(5000, 'y'), steps=50)

To define simulation, we will provide the model, solvers or lists of
solvers used to calculate initial state and evolutionary solution. The
number of simulation cycles to be calculated could be specified by
keyword argument ``repeat``.

.. code-block:: python

    init_solvers = [init_v]
    simulation_solvers = [intrusion_v, diffuse_v]
    s = Simulation_1D(m_v, init_solvers, simulation_solvers, repeat=10)

Once the simulation is created we can run model…

.. code-block:: python

    s.run()


.. parsed-literal::

    Done.


Now we can plot results

.. code-block:: python

    m_v.time_unit = 'Ma'
    s.plot(figsize=(14, 8))


.. image:: images/output_44_0.png


********************
User-defined solvers
********************

Tracking P-T-t evolution with tracer
====================================

Create program that will track time, temperature and depth evolution of
sample **S** involved in *“Naive orogeny”* characterized by convergence
with constant strain rate :math:`\dot{\epsilon}`, erosion with rate
:math:`\dot{r}` dependent on actual topography (which is calculated from
Airy isostasy of thickenned crust) and transient heat conduction for
total time 20 Ma.

We want to trace the depth-temperature evolution of particle initially
located in depth 25km within thermally equilibrated (steady-state geotherm)
crust with initial thickness 35km and plot results.

.. image:: images/naiveorogen.png

Convergence strain rate:

.. math:: \dot{\epsilon} = 3\cdot 10^{-15}~m\cdot s^{-1}

Erosion rate:

.. math:: \dot{r}(h) = \dot{\epsilon}\cdot\exp\left(K_e\cdot\left[\frac{E_t(h)}{E_t(h_{max})}-1\right]\right)

Topography:

.. math:: E_t(h) = \frac{(h - h_0)(\rho_m-\rho_c)}{\rho_m}

========================= =============== ============
property                  symbol          value
========================= =============== ============
Crust density             :math:`\rho_c`  2800 kg/m3
Mantle density            :math:`\rho_m`  3200 kg/m3
Thermal conductivity      :math:`\lambda` 2.5 W/(m⋅K)
Specific heat capacity    :math:`c`       900 J/(kg.K)
Heat production           :math:`H`       1e-6 W/m3
Surface temperature       :math:`T_0`     0°C
MOHO heat flow            :math:`q_m`     0.025 W/m2
Erosion coefficient       :math:`K_e`     3
Maximum crustal thickness :math:`h_{max}` 70 km
========================= =============== ============

Hints
^^^^^

For each time step :math:`dt` deformation increase thickness, so:

.. math:: h_{def} = h\cdot\exp(\dot \epsilon dt)

and erosion decrease thickness, so:

.. math:: h_{new} = h_{def}\cdot\exp(-\dot r(h_{def}) dt)

The amount of erosion for given tie step could be calculated as:

.. math:: dh = h_{def} - h_{new}

To implement new functionality, you can create user-defined solvers,
which could be plugged into simulation. Easiest way is to subclass existing
solvers. The first example is solver based on `Deform_Constant_1D` and
calculate deformation factor from time-step and strain-rate.

.. code-block:: python

    class MyDeformation_Constant_1D(Deform_Constant_1D):
    
        def __init__(self, edot, dt=0, **kwargs):
            # calculate factor based on strain-rate and time
            factor = np.exp(edot * abs(dt))
            super().__init__(factor=factor, **kwargs)

Second example shows, how to implement solver, which need to access model properties
during simulation...

.. code-block:: python
    
    class MyErosion_Constant_1D(Shift_Constant_1D):
    
        def __init__(self, edot, dt=0,
                     Ke=3, rhoc=2800, rhom=3200,href=35000, hmax=70000, **kwargs):
            self.dt = abs(dt)
            # lambdas for Airy topography and erosion rate
            self.topo = lambda h: ((h - href) * (rhom - rhoc)) / rhom
            self.rdot = lambda h: edot * np.exp(Ke * (self.topo(h) / self.topo(hmax) - 1))
            super().__init__(**kwargs)
    
        def solve(self, model, tracers=None):
            # calculate amount and call parent solver
            self.amount = model.domain.L * (np.exp(-self.rdot(model.domain.L) * self.dt) - 1)
            super().solve(model, tracers=tracers)

.. code-block:: python

    d_c = Domain_Constant_1D(L=Length(35, 'km'), k=2.5,
                              n=350, H=1e-6, rho=2800, c=900, plot_unit='km')
    tbc = Dirichlet_BC(0)
    bbc = Neumann_BC(-0.025)
    m_c = Model_Constant_1D(d_c, tbc, bbc, time_unit='Ma')
    edot = 3e-15
    calc_dt = Time(5000, 'y')
    init_c = SteadyState_Constant_1D(log=True)  # store to tracers
    deform_c = MyDeformation_Constant_1D(edot=3e-15, dt=calc_dt)
    erosion_c = MyErosion_Constant_1D(edot=3e-15, dt=calc_dt, rhoc=d_c.rho)
    btcs_c = BTCS_Constant_1D(dt=calc_dt, log=True)  # store to tracers

.. code-block:: python

    p = Tracer_1D('A', Length(25, 'km'), plot_unit='km', time_unit='Ma')
    s = Simulation_1D(m_c, init_c, 400*[deform_c, erosion_c, btcs_c], repeat=10, tracers=p)

.. code-block:: python

    s.run()


.. parsed-literal::

    Done.


.. code-block:: python

    s.plot(figsize=(14, 8))



.. image:: images/output_60_0.png


.. code-block:: python

    plt.figure(figsize=(14, 8))
    plt.plot(p.T_all, p.x_all*2750*9.81/1e5)
    plt.xlabel('Temperature [°C]')
    plt.ylabel('Pressure [kbar]');



.. image:: images/output_61_0.png


.. code-block:: python

    fig, ax1 = plt.subplots(figsize=(14, 6))
    color1 = 'tab:red'
    ax1.plot(p.time_all, p.x_all*2750*9.81/1e5, color=color1)
    ax1.set_xlabel(f'Time [{p.time_unit}]')
    ax1.set_ylabel('Pressure [kbar]', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.plot(p.time_all, p.T_all, color=color2)
    ax2.set_ylabel('Temperature [°C]', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)



.. image:: images/output_62_0.png
