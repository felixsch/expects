from hypothesis.strategies import SearchStrategy, cacheable, defines_strategy, shared

from receives.receiver import Receiver


class AReceiver(SearchStrategy):
    """ Generates a receives.receiver for later usage
    """

    def do_draw(self, data):
        receiver = Receiver()
        return receiver


@cacheable
@defines_strategy
def a_receiver():
    return shared(AReceiver(), 'spec.helpers.a_receiver()')
