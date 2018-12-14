
class Call():
    def __init__(self, context, kargs, kwargs):
        self._context = context
        self._kargs = kargs
        self._kwargs = kwargs

    @property
    def context(self):
        return self._context

    @property
    def args(self):
        return self._kargs, self._kwargs
