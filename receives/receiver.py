import sys

from receives import mocking
from receives.context import Context
from receives.expectation import empty_expectation


def receive(module_or_class, method_name):
    # get tests function name to later trace the the call stack
    caller = sys._getframe(1).f_code.co_name
    context = Context(caller, module_or_class, method_name)

    return Receiver(context)


def allow(module_or_class, method_name):
    caller = sys._getframe(1).f_code.co_name
    context = Context(caller, module_or_class, method_name)

    return Receiver(context, persistant=True)


class Receiver(object):
    def __init__(self, context, persistant=False):
        self._context = context
        self._expectations = []
        self._orginal_call = None

        self._prepare_object()
        self._prepare_expectation(persistant)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if mocking.has_method_mock(self._context):
            mocking.remove_method_mock(self._context, self._orginal_call)

    def __del__(self):
        if mocking.has_method_mock(self._context):
            mocking.remove_method_mock(self._context, self._orginal_call)

    def with_args(self, *kargs, **kwargs):
        expectation = self._last_expectation()
        expectation.set_args(kargs, kwargs)

        self._add_expecation(expectation)
        return self

    def and_return(self, value):
        expectation = self._last_expectation()
        expectation.set_return_value(value)

        self._add_expecation(expectation)
        return self

    def is_called(self, times):
        expectation = self._last_expectation()
        for _ in range(times):
            self._add_expecation(expectation)

    # private

    def _prepare_object(self):
        if not mocking.has_method_mock(self._context):
            call = mocking.add_method_mock(self._context,
                                           self,
                                           self._mocked_call)
            self._orginal_call = call

    def _prepare_expectation(self, persistant):
        receiver = mocking.get_receiver_for(self._context)
        expectation = empty_expectation(self._context, persistant)

        receiver._add_expecation(expectation)

    def _mocked_call(self, *kargs, **kwargs):
        receiver = mocking.get_receiver_for(self._context)

        expectation = receiver._next_expectation()
        expectation.evaluate(kargs, kwargs)

        return expectation.return_value()

    def _add_expecation(self, expectation):
        receiver = mocking.get_receiver_for(self._context)
        receiver._expectations.append(expectation)

    def _last_expectation(self):
        receiver = mocking.get_receiver_for(self._context)
        return receiver._expectations.pop()

    def _next_expectation(self):
        # the the first expectation in the list
        expectation = self._expectations.pop(0)
        if expectation.is_persistant():
            # append the expecatation again to the list
            self._expectations.append(expectation)
            # when there are more than the persistant expectation than add the
            # persistant expectation to the end of the list to make overwrites
            # work
            if len(self._expectations) > 1:
                return self._expectations.pop(0)
        # no more expectations in the list mark this method as invalid and
        # raise an error if called
        if not len(self._expectations):
            mocking.remove_method_mock(self._context, self._orginal_call)
        return expectation
