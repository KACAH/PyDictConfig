from schema import TestSchema
from PyDictConfig import DictConfig, YamlConfig


TEST_CONFIG = {
    "test2": 2,
    "InSec": {
        "test3": "1.1",
    }
}


if __name__ == "__main__":
    print "Runnning PyDictConfig tests"
    _config_d = DictConfig(TestSchema)
    _config_y = YamlConfig(TestSchema)

    _config_d.load(TEST_CONFIG)
    _config_y.load("test_conf.yaml")
