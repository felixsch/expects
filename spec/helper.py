import sys

from contextlib import contextmanager
from pytest import raises
from mamba import description, describe, before, it, context
from unittest.mock import MagicMock

from receives.context import Context


__all__ = ['raises', 'not_raises',
           'TestClass', 'test_function',
           'make_context',
           'description', 'describe', 'before', 'it', 'context',
           'MagicMock']


def test_function(string):
    return string


# A simple test class to test the implementation
class TestClass():
    prop2_value = 42

    def valid(self, string):
        return string

    def invalid(self, string, optional=None):
        return string

    @property
    def prop(self):
        return 42

    @property
    def prop2(self):
        return self.prop2_value

    @prop2.setter
    def prop2(self, value):
        self.prop2_value = value


# Generate a context on the fly
def make_context(instance, attribute):
    frame = sys._getframe(1)
    return Context(instance, attribute, frame)


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise AssertionError("Raised expection {0} where it shouldn't raise"
                             .format(exception))
