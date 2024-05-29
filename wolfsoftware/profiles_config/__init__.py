"""
A simple Python package to manage profile based configuration files.

Attributes:
- __version__: The version of the package, retrieved from the package metadata.
- __all__: A list of all public symbols that the module exports.
"""

import importlib.metadata

from .parser import ConfigHandler

try:
    __version__: str = importlib.metadata.version('wolfsoftware.profiles_config')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'

__all__: list[str] = [
    'ConfigHandler'
]
