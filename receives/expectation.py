from functools import partial

from receives.error import assert_failed


class Expectation():
    def __init__(self, context):
        self._context = context
        self._has_been_called = False
        self._args = None
        self._return_value = None
        self._should_call_original = False

    def is_for(self, call):
        if self._has_been_called:
            return False

        if call.context != self._context:
            return False

        if self._args is not None and self._args != call.args:
            return False
        return True

    @property
    def called(self):
        return self._has_been_called

    def with_args(self, *kargs, **kwargs):
        self._args = (kargs, kwargs)
        return self

    def and_return(self, value):
        self._has_return_value = True
        self._return_value = value

    def and_call_original(self):
        self._should_call_original = True

    def validate(self, kargs, kwargs):
        print("Validating expectation {}...".format(self))
        self._has_been_called = True

        if self._args is None:
            return self._return_value

        message = "received unexpected arguments"
        failed = partial(assert_failed, self._context, message)
        (expected_kargs, expected_kwargs) = self._args

        if kargs != expected_kargs:
            raise AssertionError(failed(expected_kargs, kargs))

        if kwargs != expected_kwargs:
            raise AssertionError(failed(expected_kwargs, kwargs))

        return self._return_value

    @property
    def should_call_original(self):
        return self._should_call_original
