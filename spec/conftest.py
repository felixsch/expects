import pytest
from contextlib import contextmanager


class Double():
    def double_method():
        return 42


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("Raised expection {0} where it shouldn't raise"
                          .format(exception))
