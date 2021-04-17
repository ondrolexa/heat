import copy

#################################################
#            Elements                           #
#################################################


class Element:
    def __init__(self, name, **kwargs):
        self.name = name
        self.dx = float(abs(kwargs.get('dx', 1)))
        self.k = float(kwargs.get('k', 1))
        self.H = float(kwargs.get('H', 0))
        self.rho = float(kwargs.get('rho', 1))
        self.c = float(kwargs.get('c', 1))

    def __mul__(self, other):
        return [copy.copy(self) for i in range(other)]

    def __add__(self, other):
        return [self] + other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return other + [self]

    def __repr__(self):
        return f'|{self.name}|'

    def info(self):
        return (
            f'{self.name}: k={self.k:g}  H={self.H:g}  rho={self.rho:g}  c={self.c:g}'
        )

    def __eq__(self, othr):
        cmp = (self.name, self.k, self.H, self.rho, self.c) == (
            othr.name,
            othr.k,
            othr.H,
            othr.rho,
            othr.c,
        )
        return isinstance(othr, type(self)) and cmp

    def __hash__(self):
        return hash((self.name, self.k, self.H, self.rho, self.c))
