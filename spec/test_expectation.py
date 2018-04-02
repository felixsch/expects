import pytest
import sys

from pytest import raises
from conftest import not_raises
from expects import expect, be, be_a, be_none, be_false, be_true, equal

from receives.expectation import Expectation, empty_expectation
from receives.context import Context


# PRE -------------------------------------------------------------------------


def expectation():
    caller = sys._getframe(1).f_code.co_name
    context = Context(caller, pytest, "test_method")
    return Expectation(context, persistant=False)


def persistant_expectation():
    caller = sys._getframe(1).f_code.co_name
    context = Context(caller, pytest, "test_method")
    return Expectation(context, persistant=True)


def test_pre():
    subject = expectation()
    expect(subject._context.caller_name()).to(be("test_pre"))


# TESTS -----------------------------------------------------------------------


def test_expectation_init():
    subject = expectation()

    expect(subject._kargs).to(be_none)
    expect(subject._kwargs).to(be_none)
    expect(subject._return_value).to(be_none)
    expect(subject._persistant).to(be_false)


def test_expectation_evaluate():
    subject = expectation()

    kargs = [1, "", "a string", {}]
    kwargs = {"foo": True, "bar": "baz"}

    with not_raises(AssertionError):
        subject.evaluate(None, None)
        subject.evaluate([1, 2, 3, 4], None)
        subject.evaluate(None, {"foo": "bar"})

    # with kargs
    subject.set_args(kargs, None)

    with not_raises(AssertionError):
        subject.evaluate(kargs, None)

    with raises(AssertionError):
        subject.evaluate(None, None)
        subject.evaluate([], None)
        subject.evaluate(kargs, {"foo": "bar"})

    subject._kargs = None

    # with kwargs
    subject._kwargs = kwargs

    with not_raises(AssertionError):
        subject.evaluate(None, kwargs)

    with raises(AssertionError):
        subject.evaluate(None, None)
        subject.evaluate(None, {})
        subject.evaluate(None, {"not": "the same"})
        subject.evaluate([], kwargs)

    # with both set
    subject._kwargs = kwargs

    with not_raises(AssertionError):
        subject.evaluate(kargs, kwargs)

    with raises(AssertionError):
        subject.evaluate([], kwargs)
        subject.evaluate(kargs, {})


def test_expectation_is_persistant():
    subject = expectation()
    persistant_subject = persistant_expectation()

    expect(subject.is_persistant()).to(be_false)
    expect(persistant_subject.is_persistant()).to(be_true)


def test_expectation_return_value():
    value = "some_value"
    subject = expectation()
    subject_with_value = expectation()
    subject_with_value._return_value = value

    expect(subject.return_value()).to(be_none)
    expect(subject_with_value.return_value()).to(equal(value))


def test_expectation_set_args():
    subject = expectation()

    subject.set_args([1], {"foo": "bar"})
    expect(subject._kargs).to(equal([1]))
    expect(subject._kwargs).to(equal({"foo": "bar"}))


def test_expectation_set_return_value():
    subject = expectation()

    subject.set_return_value(42)
    expect(subject.return_value()).to(equal(42))


def test_empty_expectation():
    stub_context = "stub_context"

    expect(empty_expectation(stub_context)).to(be_a(Expectation))
