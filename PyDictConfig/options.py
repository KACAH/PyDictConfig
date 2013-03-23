__all__ = [
    "StrOption",
    "BoolOption",
    "IntOption",
    "FloatOption",
]

from option_base import Option


class StrOption(Option):
    """Option that represents string value"""

    def convert_type(self, val):
        if not isinstance(val, basestring):
            raise ValueError("%s is not a string" % val)
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

        raise ValueError("%s is not a bool" % val)


class IntOption(Option):
    """Option that represents int value"""

    def convert_type(self, val):
        return int(val)


class FloatOption(Option):
    """Option that represents float value"""

    def convert_type(self, val):
        return float(val)
