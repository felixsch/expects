from expects import expect, be, be_a, be_none, be_true, be_false, equal, contain

from receives import receives


class SomeClass():
    def __init__(self, value):
        self._value = value

    def method(self, othervalue):
        return self._value + othervalue


@receives
def test_instance_patching(receive):
    instance = SomeClass(1)

    receive(instance, 'method')
    receive(instance, 'method').with_args(10).and_call_original()
    receive(instance, 'method').with_args(42).and_return(7)
    receive(instance, 'method').with_args(42).and_call_original()

    expect(instance.method(1000)).to(be_none)
    expect(instance.method(10)).to(be(11))
    expect(instance.method(42)).to(be(7))
    expect(instance.method(42)).to(be(43))
