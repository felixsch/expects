from functools import partial
from receives.error import assert_failed


class Expectation(object):
    def __init__(self, context, persistant=False):
        self._context = context
        self._kargs = None
        self._kwargs = None
        self._return_value = None

        self._persistant = persistant

    def evaluate(self, kargs, kwargs):
        message = "received unexpected arguments"
        failed = partial(assert_failed, self._context, message)

        if (self._kargs is not None and self._kargs != kargs):
            raise AssertionError(failed(self._kargs, kargs))

        if (self._kwargs is not None and self._kwargs != kwargs):
            raise AssertionError(failed(self._kwargs, kwargs))

    def is_persistant(self):
        return self._persistant

    def return_value(self):
        return self._return_value

    def set_args(self, kargs, kwargs):
        self._kargs = kargs
        self._kwargs = kwargs

    def set_return_value(self, value):
        self._return_value = value


def empty_expectation(context, is_persistant=False):
    return Expectation(context, persistant=is_persistant)
