class CalcGameError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NotDivisibleError(CalcGameError):
    """NotDivisibleError"""

class CurNumTooBigError(CalcGameError):
    """CurNumTooBigError"""

class StoreNegativeError(CalcGameError):
    """StoreNegativeError"""

class OutOfRangeError(CalcGameError):
    """OutOfRangeError"""

class NotOptionError(CalcGameError):
    """NotOptionError"""

class NotHasError(CalcGameError):
    """NotHasError"""