from expects import expect, be, be_a, be_none, be_true, be_false, be_callable, equal, contain

from receives.pytest import receive
from receives.receiver import Receiver


def test_pytest_receive(receive):
    expect(receive).to(be_a(Receiver))
