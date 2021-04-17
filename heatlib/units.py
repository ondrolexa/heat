#################################################
#            Unit helpers                       #
#################################################


class Length(float):
    unit2m = dict(mm=0.001, cm=0.01, dm=0.1, m=1, km=1000)

    def __new__(cls, val, unit):
        return float.__new__(cls, val)

    def __init__(self, val, unit):
        assert unit in Length.unit2m, 'Unknown units'
        self.unit = unit

    def __str__(self):
        return f'{float(self)} {self.unit}'

    def __repr__(self):
        return self.__str__()

    def to(self, name):
        if name in Length.unit2m:
            return Length.unit2m[self.unit] * float(self) / Length.unit2m[name]

    def __abs__(self):
        return Length.unit2m[self.unit] * float(self)


class Time(float):
    unit2s = dict(
        s=1,
        min=60,
        h=3600,
        d=24 * 3600,
        y=365.25 * 24 * 3600,
        ky=1e3 * 365.25 * 24 * 3600,
        Ma=1e6 * 365.25 * 24 * 3600,
    )

    def __new__(cls, val, unit):
        return float.__new__(cls, val)

    def __init__(self, val, unit):
        assert unit in Time.unit2s, 'Unknown units'
        self.unit = unit

    def __str__(self):
        return f'{float(self)} {self.unit}'

    def __repr__(self):
        return self.__str__()

    def to(self, name):
        if name in Time.unit2s:
            return Time.unit2s[self.unit] * float(self) / Time.unit2s[name]

    def __abs__(self):
        return Time.unit2s[self.unit] * float(self)
