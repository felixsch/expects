from expects import expect, be, be_a, be_none, be_true, be_false, equal, contain, raise_error

from spec.helper import debug, given, settings
from spec.helpers.expectation import a_expectation

from hypothesis import assume
from hypothesis.strategies import text, randoms


@given(a_expectation(), text(), text())
def test_expectation_with_args(expectation, str1, str2):
    expect(expectation.with_args(str1, test=str2)).to(be(expectation))
    expect(expectation._args).to(equal(((str1,), {'test': str2})))


@given(a_expectation(), randoms())
def test_expectation_and_return(expectation, return_value):
    expect(expectation.and_return(return_value)).to(be_none)
    expect(expectation._return_value).to(equal(return_value))


@given(a_expectation())
def test_expectation_and_call_original(expectation):
    expect(expectation._should_call_original).to(be_false)
    expect(expectation.and_call_original()).to(be_none)
    expect(expectation._should_call_original).to(be_true)


@given(a_expectation())
def test_expectation_should_call_original(expectation):
    expect(expectation.should_call_original).to(be_false)
    expectation.and_call_original()
    expect(expectation.should_call_original).to(be_true)


@given(a_expectation(), randoms())
def test_expectation_validate_no_args(expectation, return_value):
    expect(expectation.validate((), {})).to(be_none)
    expectation.and_return(return_value)
    expect(expectation.validate((), {})).to(equal(return_value))


@given(a_expectation(), text(), text())
def test_expectation_validate_kargs_mismatch(expectation, str1, str2):
    assume(str1 != str2)
    expectation.with_args(str1)
    expect(lambda: expectation.validate((str2), {})).to(raise_error(AssertionError))


@given(a_expectation(), text(), text())
def test_expectation_validate_kwargs_mismatch(expectation, str1, str2):
    assume(str1 != str2)
    expectation.with_args(test=str1)
    expect(lambda: expectation.validate((), {'test': str2})).to(raise_error(AssertionError))
    expect(lambda: expectation.validate((), {'foo': str1})).to(raise_error(AssertionError))


@given(a_expectation(), text(), text(), randoms())
def test_expectation_validate_valid_args(expectation, str1, str2, return_value):
    expectation.with_args(str1)
    expect(expectation.validate((str1,), {})).to(be_none)


