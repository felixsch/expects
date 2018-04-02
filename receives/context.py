import inspect


class Context(object):
    def __init__(self, caller_name, base_object, method_to_mock):
        self._caller_name = caller_name
        self._object = base_object
        self._method_name = method_to_mock
        self._method = None

    def caller_name(self):
        return self._caller_name

    def object_name(self):
        if inspect.ismodule(self._object):
            return self._object.__name__
        if inspect.isclass(self._object):
            return self._object.__name__
        return self._instance_name()

    def method_name(self):
        return self._method_name

    def object(self):
        return self._object

    def set_method(self, method):
        self._method = method

    def method(self):
        return self._method

    # private

    def _instance_name(self):
        frameinfos = inspect.getouterframes(inspect.currentframe())
        for frameinfo in frameinfos:
            if frameinfo.function == self._caller_name:
                return self._extract_instance_name(frameinfo.frame)
        return None

    def _extract_instance_name(self, frame):
        for name, obj in frame.f_locals.items():
            if obj == self._object:
                return name
        return self._object.__class__.__name__
