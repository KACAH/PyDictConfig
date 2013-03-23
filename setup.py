from setuptools import setup, find_packages
import os


version = "0.1a"
author = "Den Paltov <kacah222@gmail.com>"


setup(
    name = "PyDictConfig",
    version = version,
    author = author,
    url = "https://github.com/KACAH/PyDictConfig",
    description = "Python config based on dict representation",
    packages = find_packages(),
)
