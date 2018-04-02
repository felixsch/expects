import sys
from pytest import raises
from conftest import not_raises
from expects import expect, be, be_true, be_false, be_empty, be_a, be_none

from receives.context import Context
from receives.receiver import Receiver, receive, allow
from receives import mocking


# PRE -------------------------------------------------------------------------


class TestClass():
    def some_function(self, number, extra_number=0):
        return number + extra_number


def instance_context():
    caller = sys._getframe(1).f_code.co_name
    inst = TestClass()
    return Context(caller, inst, "some_function")


# TESTS -----------------------------------------------------------------------

def test_receive():
    inst = TestClass()

    receiver = receive(inst, "some_function")
    expect(receiver).to(be_a(Receiver))
    expect(receiver._context.caller_name()).to(be("test_receive"))
    expect(receiver._last_expectation().is_persistant()).to(be_false)


def test_allow():
    inst = TestClass()

    receiver = allow(inst, "some_function")
    expect(receiver).to(be_a(Receiver))
    expect(receiver._context.caller_name()).to(be("test_allow"))
    expect(receiver._last_expectation().is_persistant()).to(be_true)


def test_receiver_init():
    context = instance_context()
    subject = Receiver(context)

    expect(subject._context).to(be(context))
    expect(subject._expectations).to_not(be_empty)
    expect(mocking.has_mock_table(context)).to(be_true)
    expect(mocking.has_method_mock(context)).to(be_true)


def test_receiver_with_args():
    inst = TestClass()

    value = receive(inst, "some_function").with_args(1)
    expect(value).to(be_a(Receiver))

    with not_raises(AssertionError):
        inst.some_function(1)
    expect(inst.some_function(1)).to(be(1))

    receive(inst, "some_function").with_args(1, extra_number=9)
    with not_raises(AssertionError):
        inst.some_function(1, extra_number=9)

    receive(inst, "some_function").with_args(1, extra_number=9)
    with raises(AssertionError):
        inst.some_function(2)

    receive(inst, "some_function").with_args(extra_number=9)
    with not_raises(AssertionError):
        inst.some_function(extra_number=9)


def test_receiver_and_return():
    inst = TestClass()

    value = receive(inst, "some_function")
    expect(value).to(be_a(Receiver))

    expect(inst.some_function(1, 2, 3, 4)).to(be_none)

    receive(inst, "some_function").and_return(9)
    with not_raises(AssertionError):
        inst.some_function(1, 2, 3, 3, not_existing="kwarg")

    receive(inst, "some_function").and_return(9)
    expect(inst.some_function(1, 2, 3)).to(be(9))


def test_receiver_is_called():
    inst = TestClass()

    value = receive(inst, "some_function").is_called(2)
    expect(value).to(be_none)

    expect(inst.some_function(1)).to(be_none)
    expect(inst.some_function(1)).to(be_none)
    expect(inst.some_function(1)).to(be(1))
