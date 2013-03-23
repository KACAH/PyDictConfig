__all__ = ["TestBoolOption"]

import unittest

from PyDictConfig import *


class DefaultOptionSchema(Section):
    test_opt = BoolOption(default=False)

class SetOptionSchema(Section):
    test_opt = BoolOption(default=False)

class PassedOptionSchema(Section):
    test_opt = BoolOption()

class NoValueOptionSchema(Section):
    test_opt = BoolOption()

class ConfigNameOptionSchema(Section):
    test_opt = BoolOption(config_name="Option")

class InvalidTypeOptionSchema(Section):
    test_opt = BoolOption(default="invalid")

class ValidatorOptionSchema(Section):

    def test_validator(option, value):
        if value:
            raise ValueError("Invalid value")

    test_opt = BoolOption(validator=test_validator)

class TestBoolOption(unittest.TestCase):
    """Test types of the options"""

    def test_default(self):
        _config = DictConfig(DefaultOptionSchema)
        _config.load({})
        self.assertEqual(
            _config.test_opt, False, "Default value doesn't work"
        )

    def test_set(self):
        _config = DictConfig(SetOptionSchema)
        _config.load({})
        _config.test_opt = True
        self.assertEqual(
            _config.test_opt, True, "Value changing doesn't work"
        )

    def test_passed(self):
        _config = DictConfig(PassedOptionSchema)
        _config.load({"test_opt": False})
        self.assertEqual(
            _config.test_opt, False, "Passed value doesn't work"
        )

    def test_novalue(self):
        _config = DictConfig(NoValueOptionSchema)
        self.assertRaises(ValueError, _config.load, {})

    def test_configname(self):
        _config = DictConfig(ConfigNameOptionSchema)
        _config.load({"Option": False})
        self.assertEqual(
            _config.test_opt, False, "Passed value doesn't work"
        )

    def test_validator(self):
        _config = DictConfig(ValidatorOptionSchema)
        self.assertRaises(ValueError, _config.load, {"test_opt": True})

    def test_invalidtype(self):
        _config = DictConfig(InvalidTypeOptionSchema)
        self.assertRaises(ValueError, _config.load, {})
