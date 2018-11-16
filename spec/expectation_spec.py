
from expects import expect, be, be_none, be_true, be_a, be_false, equal, raise_error
from expects import be_callable

from spec.helper import description, before, describe, it, context
from spec.helper import TestClass, make_context
from spec.helper import MagicMock, raises
from spec import helper

from functools import partial

from receives.expectation import Expectation

with description(Expectation) as self:
    with before.each:
        self.testclass = TestClass()
        self.context = make_context(self.testclass, "valid")
        self.subject = Expectation(self.context)

    with describe("#validate"):
        with it('does not validate if there are no args set'):
            expect(lambda: self.subject.validate(("foo",), {"hello": "world"})).not_to(raise_error(AssertionError))
            expect(self.subject.validate((), {})).to(be_none)

        with it('raises if kargs do not match'):
            self.subject.with_args("foo")

            expect(lambda: self.subject.validate(("foo",), {})).not_to(raise_error(AssertionError))

            expect(lambda: self.subject.validate(("baz",), {})).to(raise_error(AssertionError))
            expect(lambda: self.subject.validate(("foo",), {"hello": "world"})).to(raise_error(AssertionError))

        with it('raises if kwargs do not match'):
            self.subject.with_args(hello="world")

            expect(lambda: self.subject.validate((), {"hello": "world"})).not_to(raise_error(AssertionError))

            expect(lambda: self.subject.validate((), {"x": "y"})).to(raise_error(AssertionError))
            expect(lambda: self.subject.validate((1,), {"hello": "world"})).to(raise_error(AssertionError))

    with describe("#with_args"):
        with it('sets kargs and kwargs expectation'):
            kargs = (1, "foo")
            kwargs = {"hello": "world"}

            self.subject.with_args(*kargs, **kwargs)
            expect(self.subject.validate(kargs, kwargs)).to_not(raise_error(AssertionError))
