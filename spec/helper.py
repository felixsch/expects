import sys

from pytest import raises, fixture, set_trace
from hypothesis import given, settings

if sys.version_info >= (3, 3):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock

debug = set_trace

__all__ = ['raises', 'fixture', 'MagicMock', 'debug', 'given', 'settings']
