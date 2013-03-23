import unittest

from PyDictConfig import *


class SingleSectionSchema(Section):
    pass

class NestedSectionSchema(Section):
    class InSection(Section):
        pass

class ConfigNameSectionSchema(Section):
    class InSection(Section):
        config_name = "nested_conf"

        opt = StrOption()

class MultipleSectionSchema(Section):
    class InSection1(Section):
        class InSection11(Section):
            pass
        class InSection12(Section):
            pass
    class InSection2(Section):
        pass


class TestSections(unittest.TestCase):
    """Test sections structure"""

    def test_single(self):
        _config = DictConfig(SingleSectionSchema)
        _config.load({})

    def test_nested(self):
        _config = DictConfig(NestedSectionSchema)
        _config.load({})
        _config.InSection

    def test_configname(self):
        _config = DictConfig(ConfigNameSectionSchema)
        _config.load({"nested_conf": {"opt": "test"}})
        self.assertEqual(_config.InSection.opt, "test")

    def test_multiple(self):
        _config = DictConfig(MultipleSectionSchema)
        _config.load({})
        _config.InSection1
        _config.InSection1.InSection11
        _config.InSection1.InSection12
        _config.InSection2
