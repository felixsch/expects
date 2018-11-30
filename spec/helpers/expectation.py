from hypothesis.strategies import SearchStrategy, cacheable, defines_strategy, shared

from spec.helpers.context import a_context

from receives.expectation import Expectation


class AExpectation(SearchStrategy):
    """ Generates a receives.expectation for later usage
    """

    def do_draw(self, data):
        context = data.draw(a_context())
        expectation = Expectation(context.ctx)
        return expectation


@cacheable
@defines_strategy
def a_expectation():
    return shared(AExpectation(), 'spec.helpers.a_expectation()')
