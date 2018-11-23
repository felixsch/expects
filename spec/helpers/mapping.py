from hypothesis.strategies import SearchStrategy, cacheable, defines_strategy, shared

from receives.mapping import Mapping


class AMapping(SearchStrategy):
    """ Generates a receives.mapping for later usage
    """

    def do_draw(self, data):
        mapping = Mapping()
        return mapping


@cacheable
@defines_strategy
def a_mapping():
    return shared(AMapping(), 'spec.helpers.a_mapping()')
