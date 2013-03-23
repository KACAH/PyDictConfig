class OptionArgumentError(Exception):
    """Invalid argument passed to Option"""

    def __init__(self, option_type, argument_name):
        super(OptionArgumentError, self).__init__(
            "Option type '%s' doesn't have argument with name '%s'" \
            % (option_type, argument_name)
        )


class NO_VALUE(object):
    """Dummy value for default values without default"""

def always_valid(option, value):
    """Dummy validator that is always valid"""


def define_name_new(cls, name):
    _name = "%s_%s" % (cls.__name__, name)
    if hasattr(cls, "config_name"):
        _config_name = cls.config_name
    else:
        _config_name = name
    return type(_name, (cls, ), {
        "__new__": object.__new__,
        "name": name,
        "config_name": _config_name,
    })

def define_base_new(cls, **kwargs):
    cls.check_arguments(kwargs)

    _class_fields = {
        "__new__": define_name_new,
    }
    _class_fields.update(kwargs)
    _name = "%s_%s" % (cls.__name__, cls.id)

    cls.id += 1
    return type(_name, (cls, ), _class_fields)

class Option(object):
    """Base config option

    @note: change cls.option_fields to add new arguments in subclasses

    """
    id = 0
    option_fields = ("config_name", "default", "validator", "doc")
    default = NO_VALUE
    validator = always_valid
    doc = ""

    __new__ = define_base_new

    @classmethod
    def check_arguments(cls, arg_dict):
        for _arg_name, _arg_value in arg_dict.iteritems():
            if not _arg_name in cls.option_fields:
                raise OptionArgumentError(cls.__name__, _arg_name)

    @property
    def value(self):
        return self.value_dict[self.config_name]

    @value.setter
    def value(self, val):
        val = self.validate(val)
        self.value_dict[self.config_name] = val

    def __init__(self, value_dict={}):
        self.value_dict = value_dict

        _val = value_dict.get(self.config_name, NO_VALUE)
        if _val == NO_VALUE and self.default == NO_VALUE:
            raise ValueError("Required value '%s' not found in config" \
                % self.config_name
            )
        if _val == NO_VALUE:
            _val = self.default
        self.value = _val

    def validate(self, val):
        """Validate this option value"""

        val = self.convert_type(val)
        self.validator(val)
        return val

    def convert_type(self, val):
        """Convert value into valid type"""

        raise NotImplementedError(
            "Unknown value type. Don't use Option directly."
            "Override validate_type method in final option class."
        )
