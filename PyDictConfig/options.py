__all__ = [
    "StrOption",
    "BoolOption",
    "IntOption",
    "FloatOption",
    "ListOption",
]

from option_base import Option


class StrOption(Option):
    """Option that represents string value"""

    def convert_type(self, val):
        if not isinstance(val, basestring):
            raise TypeError("%s is not a string" % val)
        return val


class BoolOption(Option):
    """Option that represents bool value"""

    CONVERT_MAP = {
        "true": True,
        "True": True,
        1: True,
        "false": False,
        "False": False,
        0: False,
    }

    def convert_type(self, val):
        if isinstance(val, bool):
            return val

        if val in self.CONVERT_MAP:
            return self.CONVERT_MAP[val]

        raise TypeError("%s is not a bool" % val)


class IntOption(Option):
    """Option that represents int value"""

    def convert_type(self, val):
        try:
            val = int(val)
        except ValueError, _ex:
            raise TypeError(_ex.message)
        return val


class FloatOption(Option):
    """Option that represents float value"""

    def convert_type(self, val):
        try:
            val = float(val)
        except ValueError, _ex:
            raise TypeError(_ex.message)
        return val


class ListOption(Option):
    """Option that represents value list"""

    def convert_type(self, val):
        #check if value is iterable
        return list(val)
