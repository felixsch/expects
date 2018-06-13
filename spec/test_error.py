import sys

from expects import expect, equal, contain

from receives.error import assert_failed, colors
from receives.context import Context


# PRE -------------------------------------------------------------------------


def context():
    caller = sys._getframe(1).f_code.co_name
    return Context(caller, colors, "test_method")


# TESTS -----------------------------------------------------------------------


def test_colors():
    expect(colors.RED).to(equal("\033[0;31m"))
    expect(colors.GREEN).to(equal("\033[0;32m"))
    expect(colors.CLEAR).to(equal("\033[0m"))


def test_assert_failed():
    message = assert_failed(context(), "test assertion", [1, 2], [])

    expect(message).to(contain("colors"))
    expect(message).to(contain("test_method"))
    expect(message).to(contain("test assertion"))
    expect(message).to(contain("[1, 2]"))
    expect(message).to(contain("[]"))
