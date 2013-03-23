__all__ = ["TestListOption"]

import unittest

from PyDictConfig import *


class DefaultOptionSchema(Section):
    test_opt = ListOption(default=["item1"])

class SetOptionSchema(Section):
    test_opt = ListOption(default=["item1"])

class PassedOptionSchema(Section):
    test_opt = ListOption()

class NoValueOptionSchema(Section):
    test_opt = ListOption()

class ConfigNameOptionSchema(Section):
    test_opt = ListOption(config_name="Option")

class InvalidTypeOptionSchema(Section):
    test_opt = ListOption(default=12)

class ValidatorOptionSchema(Section):

    def test_validator(option, value):
        if value == ["item1"]:
            raise ValueError("Invalid value")

    test_opt = ListOption(validator=test_validator)

class TestListOption(unittest.TestCase):
    """Test types of the options"""

    def test_default(self):
        _config = DictConfig(DefaultOptionSchema)
        _config.load({})
        self.assertEqual(
            _config.test_opt, ["item1"], "Default value doesn't work"
        )

    def test_set(self):
        _config = DictConfig(SetOptionSchema)
        _config.load({})
        _config.test_opt = []
        self.assertEqual(
            _config.test_opt, [], "Value changing doesn't work"
        )

    def test_passed(self):
        _config = DictConfig(PassedOptionSchema)
        _config.load({"test_opt": ["item2"]})
        self.assertEqual(
            _config.test_opt, ["item2"], "Passed value doesn't work"
        )

    def test_novalue(self):
        _config = DictConfig(NoValueOptionSchema)
        self.assertRaises(ValueError, _config.load, {})

    def test_configname(self):
        _config = DictConfig(ConfigNameOptionSchema)
        _config.load({"Option": ["item2"]})
        self.assertEqual(
            _config.test_opt, ["item2"], "Passed value doesn't work"
        )

    def test_validator(self):
        _config = DictConfig(ValidatorOptionSchema)
        self.assertRaises(ValueError, _config.load, {"test_opt": ["item1"]})

    def test_invalidtype(self):
        _config = DictConfig(InvalidTypeOptionSchema)
        self.assertRaises(TypeError, _config.load, {})
