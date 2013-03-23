__all__ = ["TestIntOption"]

import unittest

from PyDictConfig import *


class DefaultOptionSchema(Section):
    test_opt = IntOption(default=0)

class SetOptionSchema(Section):
    test_opt = IntOption(default=0)

class PassedOptionSchema(Section):
    test_opt = IntOption()

class NoValueOptionSchema(Section):
    test_opt = IntOption()

class ConfigNameOptionSchema(Section):
    test_opt = IntOption(config_name="Option")

class InvalidTypeOptionSchema(Section):
    test_opt = IntOption(default="invalid")

class ValidatorOptionSchema(Section):

    def test_validator(option, value):
        if value == 10:
            raise ValueError("Invalid value")

    test_opt = IntOption(validator=test_validator)

class TestIntOption(unittest.TestCase):
    """Test types of the options"""

    def test_default(self):
        _config = DictConfig(DefaultOptionSchema)
        _config.load({})
        self.assertEqual(
            _config.test_opt, 0, "Default value doesn't work"
        )

    def test_set(self):
        _config = DictConfig(SetOptionSchema)
        _config.load({})
        _config.test_opt = 1
        self.assertEqual(
            _config.test_opt, 1, "Value changing doesn't work"
        )

    def test_passed(self):
        _config = DictConfig(PassedOptionSchema)
        _config.load({"test_opt": 0})
        self.assertEqual(
            _config.test_opt, 0, "Passed value doesn't work"
        )

    def test_novalue(self):
        _config = DictConfig(NoValueOptionSchema)
        self.assertRaises(ValueError, _config.load, {})

    def test_configname(self):
        _config = DictConfig(ConfigNameOptionSchema)
        _config.load({"Option": 0})
        self.assertEqual(
            _config.test_opt, 0, "Passed value doesn't work"
        )

    def test_validator(self):
        _config = DictConfig(ValidatorOptionSchema)
        self.assertRaises(ValueError, _config.load, {"test_opt": 10})

    def test_invalidtype(self):
        _config = DictConfig(InvalidTypeOptionSchema)
        self.assertRaises(ValueError, _config.load, {})
