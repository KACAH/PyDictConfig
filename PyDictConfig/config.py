class ConfigBase(object):
    """Base class for all PyDictConfig configs"""

    def __init__(self, schema_cls):
        self.schema_cls = schema_cls
        self.data = {}

    def __repr__(self):
        return str(self.schema)

    def __getattribute__(self, name):
        _ga = super(ConfigBase, self).__getattribute__
        try:
            return getattr(self.schema, name)
        except:
            return _ga(name)

    def load(self):
        """Load config from source"""
        raise NotImplementedError(
            "Config %s can't load data from source" % ConfigBase
        )

    def save(self):
        """Save config to destination"""
        raise NotImplementedError(
            "Config %s can't save data to destination" % ConfigBase
        )


class DictConfig(ConfigBase):
    """Simple config loaded for Python dict object"""

    def load(self, dicts):
        """Can take single dict or list of dicts"""

        if isinstance(dicts, dict):
            dicts = [dicts]
        self.data = {}
        for _dict in dicts:
            self.data.update(_dict)

        self.schema = self.schema_cls(self.data)


class YamlConfig(ConfigBase):
    """Config based on yaml syntax file"""

    def load(self, files):
        """Can take single file or list of files"""

        import yaml

        if isinstance(files, basestring):
            files = [files]
        self.data = {}
        for _file in files:
            _dict = yaml.load(file(_file))
            self.data.update(_dict)

        self.schema = self.schema_cls(self.data)
