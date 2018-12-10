from expects import expect, be, be_a, be_none, be_true, be_false, be_callable, equal, contain

from spec.helper import debug, given, settings, MagicMock
from spec.helpers.context import a_context
from spec.helpers.receiver import a_receiver

from receives.mapping import Mapping
from receives.expectation import Expectation
from receives.receiver import Receiver, receives


@given(a_receiver())
def test_receiver_init(receiver):
    expect(receiver._mapping).to(be_a(Mapping))


@given(a_receiver(), a_context())
def test_receiver_call_unknown(receiver, sample):
    orig_call = getattr(sample.object, sample.attribute)
    expect(receiver(sample.object, sample.attribute)).to(be_a(Expectation))
    expect(receiver._mapping.is_already_patched(sample.ctx)).to(be_true)
    expect(getattr(sample.object, sample.attribute)).to_not(be(orig_call))


@given(a_receiver(), a_context())
def test_receiver_call_known(receiver, sample):
    first = receiver(sample.object, sample.attribute)
    second = receiver(sample.object, sample.attribute)

    expect(first._context).to(be(second._context))


@given(a_receiver())
def test_receiver_finalize(receiver):
    receiver._mapping.finalize = MagicMock()
    receiver.finalize()
    receiver._mapping.finalize.assert_called_once()


def try_receives(receive):
    expect(receive).to(be_a(Receiver))


def test_receives():
    callable = receives(try_receives)
    expect(callable).to(be_callable)
    callable()
