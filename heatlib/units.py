#################################################
#            Unit helpers                       #
#################################################

from pint import UnitRegistry, UndefinedUnitError

ureg = UnitRegistry()


def check_unit(unit_str, base):
    target_dimensionality = ureg.Unit(base).dimensionality
    try:
        unit = ureg.Unit(unit_str)
        if unit.dimensionality == target_dimensionality:
            return unit
        else:
            raise ValueError(f"Unit {unit_str} is not defined.")
    except UndefinedUnitError:
        raise ValueError(f"Unit {unit_str} is not defined.")


class Length(float):
    def __new__(cls, val, unit="metre"):
        return float.__new__(cls, val)

    def __init__(self, val, unit="metre"):
        self.unit = check_unit(unit, "metre")

    def __str__(self):
        return str(self * self.unit)

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return (self * self.unit).to("metre").magnitude


class Time(float):

    def __new__(cls, val, unit="seconds"):
        return float.__new__(cls, val)

    def __init__(self, val, unit="seconds"):
        self.unit = check_unit(unit, "seconds")

    def __str__(self):
        return str(self * self.unit)

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return (self * self.unit).to("seconds").magnitude
