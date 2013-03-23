__all__ = ["TestStrOption"]

import unittest

from PyDictConfig import *


class DefaultOptionSchema(Section):
    test_opt = StrOption(default="Val")

class SetOptionSchema(Section):
    test_opt = StrOption(default="Val")

class PassedOptionSchema(Section):
    test_opt = StrOption()

class NoValueOptionSchema(Section):
    test_opt = StrOption()

class ConfigNameOptionSchema(Section):
    test_opt = StrOption(config_name="Option")

class InvalidTypeOptionSchema(Section):
    test_opt = StrOption(default=1)

class ValidatorOptionSchema(Section):

    def test_validator(option, value):
        if value == "value":
            raise ValueError("Invalid value")

    test_opt = StrOption(validator=test_validator)

class TestStrOption(unittest.TestCase):
    """Test types of the options"""

    def test_default(self):
        _config = DictConfig(DefaultOptionSchema)
        _config.load({})
        self.assertEqual(
            _config.test_opt, "Val", "Default value doesn't work"
        )

    def test_set(self):
        _config = DictConfig(SetOptionSchema)
        _config.load({})
        _config.test_opt = "Changed_val"
        self.assertEqual(
            _config.test_opt, "Changed_val", "Value changing doesn't work"
        )

    def test_passed(self):
        _config = DictConfig(PassedOptionSchema)
        _config.load({"test_opt": "Val"})
        self.assertEqual(
            _config.test_opt, "Val", "Passed value doesn't work"
        )

    def test_novalue(self):
        _config = DictConfig(NoValueOptionSchema)
        self.assertRaises(ValueError, _config.load, {})

    def test_configname(self):
        _config = DictConfig(ConfigNameOptionSchema)
        _config.load({"Option": "Val"})
        self.assertEqual(
            _config.test_opt, "Val", "Passed value doesn't work"
        )

    def test_validator(self):
        _config = DictConfig(ValidatorOptionSchema)
        self.assertRaises(ValueError, _config.load, {"test_opt": "value"})

    def test_invalidtype(self):
        _config = DictConfig(InvalidTypeOptionSchema)
        self.assertRaises(TypeError, _config.load, {})
