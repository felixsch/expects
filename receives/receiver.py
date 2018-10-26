import sys

from receives.mapping import Mapping
from receives.context import Context


class Receiver():
    def __init__(self):
        self._mapping = Mapping()

    def __call__(self, obj, attribute):
        patch = self._mapping.find_by(obj, attribute)

        if patch is not None:
            return patch.new_expectation()

        caller_frame = sys._getframe(1)

        context = Context(obj, attribute, caller_frame)
        patch = self._mapping.create_patch(context)
        patch.patch()

        return patch.new_expectation()

    def finalize(self):
        self._mapping.finalize()


def receives(func):
    """ Decorate a method to enable method mocking
    """
    def call_receiver(*kargs, **kwargs):
        receiver = Receiver()
        kwargs['receive'] = receiver
        result = func(*kargs, **kwargs)
        receiver.finalize()
        return result
    return call_receiver
