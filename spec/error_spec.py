from expects import expect, be, be_none, be_true, be_false, equal, contain

from spec.helper import description, before, describe, it, context
from spec.helper import TestClass, make_context
from spec.helper import MagicMock, raises

from receives.mapping import Mapping
from receives import error


with describe(error.colors) as self:
    with it('defines color codes'):
        expect(error.colors.RED).to(equal("\033[0;31m"))
        expect(error.colors.GREEN).to(equal("\033[0;32m"))
        expect(error.colors.CLEAR).to(equal("\033[0m"))


with describe(error.Bug):
    with it('is a child class of AssertionError'):
        expect(error.Bug.__bases__).to(contain(AssertionError))


with describe(error.assert_failed):
    with before.each:
        self.context = make_context(Mapping, "find_by")

    with it('returns the assertion message'):
        expected = "expected:\n  " + error.colors.GREEN + "value_a" + error.colors.CLEAR
        got = "got instead:\n  " + error.colors.RED + "value_b" + error.colors.CLEAR

        result = error.assert_failed(self.context, "test_message", "value_a", "value_b")

        expect(result).to(contain("Mapping.find_by test_message:"))
        expect(result).to(contain(expected))
        expect(result).to(contain(got))
