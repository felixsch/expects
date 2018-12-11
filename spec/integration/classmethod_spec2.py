from expects import expect, be, be_a, be_none, be_true, be_false, equal, contain
from expects import raise_error

from receives import receives


class SomeClass():
    def __init__(self, value):
        self._value = value

    @classmethod
    def classmethod(cls, value):
        return value


@receives
def test_class_method_patching(receive):
    receive(SomeClass, 'classmethod').and_return(1)
    receive(SomeClass, 'classmethod').and_call_original()

    expect(SomeClass.classmethod(42)).to(be(1))
    expect(SomeClass.classmethod(10)).to(be(10))


@receives
def test_class_method_instance_patching(receive):
    receive(SomeClass, 'classmethod').and_return(42)

    instance = SomeClass(1)

    expect(instance.classmethod(1)).to(be(42))


@receives
def test_class_method_class_and_instance_patching(receive):
    receive(SomeClass, 'classmethod').and_return(10)

    instance = SomeClass(1)

    receive(instance, 'classmethod').and_return(42)

    expect(SomeClass.classmethod(1)).to(be(10))
    expect(instance.classmethod(1)).to(be(42))
