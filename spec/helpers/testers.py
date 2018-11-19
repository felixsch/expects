

# A simple module level method
def a_test_function(string):
    return "{}".format(string)


# A test class implementing all different supported method types by receives
class ATestClass():
    @classmethod
    def class_method(cls):
        return cls

    def __init__(self):
        self._rw_property_value = 42

    def method(self, string):
        return string

    def method2(self, string, optional=None):
        if optional is not None:
            return "{}-{}".format(string, optional)
        return string

    @property
    def ro_property(self):
        return 42

    @property
    def rw_property(self):
        return self._rw_property_value

    @rw_property.setter
    def rw_property(self, value):
        self._rw_property_value = value
