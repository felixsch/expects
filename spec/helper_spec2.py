from expects import expect, be, be_a, be_none, be_true, be_false, be_callable, equal, contain

from receives.helper import current_module
import sys


def test_current_module():
    expect(current_module()).to(be(sys.modules[__name__]))
