==============
Heatlib module
==============

Basic functionality
-------------------

This module provides classess to solve steady-state or evolutionary heat
equation in 1D on grids with constant or variable properties.

Unit support
~~~~~~~~~~~~

-  ``Length`` - Class to manipulate with different length units
-  ``Time`` - Class to manipulate with different time units

Boundary conditions
~~~~~~~~~~~~~~~~~~~

-  ``Dirichlet_BC`` - Dirichlet boundary condition, i.e. prescribed
   temperature
-  ``Neumann_BC`` - Neumann boundary condition, i.e. prescribed heat
   flow density

Constant properties and grid size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``Domain_Constant_1D`` - Class for domain with constant physical
   properties
-  ``Model_Constant_1D`` - Model class to solve and visualize solution
   on ``Domain_Constant_1D``

Solvers
^^^^^^^

-  ``SteadyState_Constant_1D`` - Steady state heat equation solution on
   grid with constant properties
-  ``BTCS_Constant_1D`` - Evolutionary heat equation solution on grid
   with constant properties
-  ``Deform_Constant_1D`` - Instantaneous deformation of model domain
-  ``Shift_Constant_1D`` - Instantaneous shift of model domain. Could
   simulate erosion-sedimenatation

Variable properties and grid size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``Domain_Variable_1D`` - Class for domain with variable physical
   properties and geometry. Domain is composed from list of ``Element``
   instances.
-  ``Model_Variable_1D`` - Model class to solve and visualize solution
   on ``Domain_Variable_1D``

.. _solvers-1:

Solvers
^^^^^^^

-  ``SteadyState_Variable_1D`` - Steady state heat equation solution on
   grid with variable properties
-  ``BTCS_Variable_1D`` - Evolutionary heat equation solution on grid
   with variable properties
-  ``Deform_Variable_1D`` - Instantaneous deformation of model domain

Universal solvers
~~~~~~~~~~~~~~~~~

-  ``SetTemperature_1D`` - Instataneous change of temperature in given
   range

Simulations
~~~~~~~~~~~

-  ``Simulation_1D`` - Class to assembly model and solvers to run and
   post-process simulation
