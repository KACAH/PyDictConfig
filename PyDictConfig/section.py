class SectionChangeError(Exception):
    def __init__(self):
        super(SectionChangeError, self).__init__(
            "Can't set value of section elements"
        )

def is_subclass(cls, what_name):
    """Check all parent classes to find if what_name is subclass of cls"""

    if not isinstance(cls, type):
        return False

    if cls.__name__ == what_name:
        return True

    for _base in cls.__bases__:
        if _base.__name__ == what_name or is_subclass(_base, what_name):
            return True
    return False


class SectionMeta(type):
    """Meta class for section to find and validate section items"""

    def __new__(cls, name, bases, attrs):
        if not "SEC_DEFINITIONS" in attrs:
            attrs["SEC_DEFINITIONS"] = {}
        if not "OPT_DEFINITIONS" in attrs:
            attrs["OPT_DEFINITIONS"] = {}

        #find items in this class
        for _attr_name, _attr_value in attrs.iteritems():
            if is_subclass(_attr_value, "Section"):
                if not hasattr(_attr_value, "config_name"):
                    _attr_value.config_name = _attr_value.__name__
                attrs["SEC_DEFINITIONS"][_attr_name] = _attr_value
            elif is_subclass(_attr_value, "Option"):
                attrs["OPT_DEFINITIONS"][_attr_name] = _attr_value(_attr_name)

        return super(SectionMeta, cls).__new__(cls, name, bases, attrs)


class Section(object):
    """Config section"""

    __metaclass__ = SectionMeta

    def __init__(self, value_dict={}):
        self.value_dict = value_dict

        self.options = {}
        self.sections = {}

        self.init_options()
        self.init_sections()

    def __repr__(self):
        return str(self.value_dict)

    def __getattribute__(self, name):
        _ga = super(Section, self).__getattribute__
        _sections = _ga("sections")
        _options = _ga("options")
        if name in _sections:
            return _sections[name]
        if name in _options:
            return _options[name].value
        return _ga(name)

    def __setattr__(self, name, val):
        _sa = super(Section, self).__setattr__
        if hasattr(self, "sections") and name in self.sections:
            raise SectionChangeError()
        if hasattr(self, "options") and name in self.options:
            self.options[name].value = val
        _sa(name, val)

    def init_sections(self):
        """Init section values from definitions dict"""

        for _sec_name, _sec_cls in self.SEC_DEFINITIONS.iteritems():
            self.sections[_sec_name] = _sec_cls(
                self.value_dict.get(_sec_cls.config_name, {})
            )

    def init_options(self):
        """Init option values from definitions dict"""

        for _opt_name, _opt_cls in self.OPT_DEFINITIONS.iteritems():
            self.options[_opt_name] = _opt_cls(self.value_dict)
