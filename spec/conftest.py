import pytest
import sys
from contextlib import contextmanager

from receives.context import Context


# A simple test class to test the implementation
class TestClass():
    def valid():
        pass

    def invalid():
        pass


# Generate a context on the fly
def make_context(self, instance, attribute):
    frame = sys._getframe(1)
    return Context(instance, attribute, frame)


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("Raised expection {0} where it shouldn't raise"
                          .format(exception))
