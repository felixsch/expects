from expects import expect, be, be_a, be_none, be_true, be_false, equal, contain
from expects import raise_error

from receives import receives


class SomeClass():
    def __init__(self, value):
        self._value = value

    def method(self, othervalue):
        return self._value + othervalue


@receives
def test_class_patching(receive):
    receive(SomeClass, 'method').and_return(1)
    receive(SomeClass, 'method').and_call_original()
    receive(SomeClass, 'method').with_args(1).and_call_original()
    receive(SomeClass, 'method').with_args(1).and_return(0)

    instance = SomeClass(1)

    expect(instance.method(42)).to(be(1))
    expect(instance.method(1000)).to(equal(1001))
    expect(instance.method(1)).to(be(2))
    expect(instance.method(1)).to(be(0))


@receives
def test_class_and_instance_patching(receive):
    receive(SomeClass, 'method').and_return(10)

    instance = SomeClass(1)

    receive(instance, 'method').and_return(1)

    expect(instance.method(1)).to(be(10))
    expect(instance.method(1000)).to(be(1))


@receives
def run_invalid_setup(receive):
    instance = SomeClass(1)
    receive(instance, 'method').and_return(10)
    receive(SomeClass, 'method').and_return(1)


def test_check_for_class_after_instance_patching():
    expect(lambda: run_invalid_setup()).to(raise_error(AssertionError))
