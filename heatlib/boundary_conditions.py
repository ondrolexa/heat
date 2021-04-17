from abc import ABC, abstractmethod

#################################################
#            Boundary conditions                #
#################################################


class Boundary_Condition(ABC):
    @abstractmethod
    def __repr__(self):
        pass


class Dirichlet_BC(Boundary_Condition):
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return f'Dirichlet BC: {self.value}'


class Neumann_BC(Boundary_Condition):
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return f'Neumann BC: {self.value}'
