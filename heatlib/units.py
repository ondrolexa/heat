from pint import UndefinedUnitError, UnitRegistry

#################################################
#            Unit helpers                       #
#################################################

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


class Model_Unit(float):
    def __new__(cls, val, unit="m"):
        return float.__new__(cls, val)

    def __init__(self, val, unit, unit_str):
        self.unit_str = unit_str
        self.unit = check_unit(unit, self.unit_str)

    def __str__(self):
        return str(float(self) * self.unit)

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return (float(self) * self.unit).to(self.unit_str).magnitude


class Length(Model_Unit):
    def __init__(self, val, unit="m"):
        super().__init__(val, unit, "m")


class Thermal_Conductivity(Model_Unit):
    def __init__(self, val, unit="W/(m.K)"):
        super().__init__(val, unit, "W/(m.K)")


class Heat_Production(Model_Unit):
    def __init__(self, val, unit="W/m^3"):
        super().__init__(val, unit, "W/m^3")


class Density(Model_Unit):
    def __init__(self, val, unit="kg/m^3"):
        super().__init__(val, unit, "kg/m^3")


class Specific_Heat_Capacity(Model_Unit):
    def __init__(self, val, unit="J/(kg.K)"):
        super().__init__(val, unit, "J/(kg.K)")


class Time(Model_Unit):
    def __init__(self, val, unit="s"):
        super().__init__(val, unit, "s")
