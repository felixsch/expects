import sys
from pytest import raises
from expects import expect, equal, be, be_true, be_false

from receives.context import Context
from receives import mocking


# PRE -------------------------------------------------------------------------


class ClassWithoutMockTable():
    def some_function(self):
        return 1


class ClassWithMockTable():
    __mock_table__ = {}

    def some_function(self):
        return 1


def replacement():
    return 42


def context_with_mock_table():
    caller = sys._getframe(1).f_code.co_name
    inst = ClassWithMockTable()
    return Context(caller, inst, "some_function")


def context_without_mock_table():
    caller = sys._getframe(1).f_code.co_name
    inst = ClassWithoutMockTable()
    return Context(caller, inst, "some_function")


# TESTS -----------------------------------------------------------------------


def test_mock_table():
    expect(mocking.MOCK_TABLE).to(equal("__mock_table__"))


def test_has_mocking_table():
    subject_without = context_without_mock_table()
    subject_with = context_with_mock_table()

    expect(mocking.has_mock_table(subject_without)).to(be_false)
    expect(mocking.has_mock_table(subject_with)).to(be_true)


def test_has_method_mock():
    subject = context_without_mock_table()

    expect(mocking.has_method_mock(subject)).to(be_false)
    mocking.add_method_mock(subject, subject, replacement)
    expect(mocking.has_method_mock(subject)).to(be_true)


def test_add_method_mock():
    subject = context_without_mock_table()

    expect(mocking.has_mock_table(subject)).to(be_false)
    expect(mocking.has_method_mock(subject)).to(be_false)
    expect(subject.object().some_function()).to(be(1))
    mocking.add_method_mock(subject, subject, replacement)

    expect(mocking.has_mock_table(subject)).to(be_true)
    expect(mocking.has_method_mock(subject)).to(be_true)
    expect(mocking.get_receiver_for(subject)).to(be(subject))
    expect(subject.object().some_function()).to(be(42))


def test_set_method_mock():
    subject = context_without_mock_table()

    def another_replacement():
        return 10

    mocking.add_method_mock(subject, subject, replacement)
    expect(subject.object().some_function()).to(be(42))

    call = mocking.set_method_mock(subject, another_replacement)
    expect(call).to(be(replacement))
    expect(subject.object().some_function()).to(be(10))


def test_remove_method_mock():
    subject = context_without_mock_table()

    old_call = mocking.add_method_mock(subject, subject, replacement)
    expect(subject.object().some_function()).to(be(42))

    mocking.remove_method_mock(subject, old_call)
    expect(mocking.has_method_mock(subject)).to(be_false)
    expect(subject.object().some_function()).to(be(1))


def test_get_receiver_for():
    subject = context_without_mock_table()

    with raises(RuntimeError):
        mocking.get_receiver_for(subject)

    mocking.add_method_mock(subject, subject, replacement)
    expect(mocking.get_receiver_for(subject)).to(be(subject))
