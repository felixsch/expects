import sys
import copy

from spec.helpers.util import nested_namedtuple
from spec.helpers import testers

from hypothesis.strategies import SearchStrategy, cacheable, defines_strategy, shared
from hypothesis.strategies import integers

from receives.context import Context, AttributeType, ObjectType


def make_context(instance, attribute):
    """ generate a instance on the fly taking care
        of the frame required
    """
    frame = sys._getframe(1)

    return Context(instance, attribute, frame)


possible_contexts = nested_namedtuple('possible_contexts', {
    'instance_method': {
        'object': testers.ATestClass(),
        'attribute': 'method',
        'valid': {
            'kargs': ('test'),
            'kwargs': {}
        },
        'invalid': {
            'kargs': (),
            'kwargs': {'invalid': True}
        },
        'types': {
            'attribute': AttributeType.Method,
            'object': ObjectType.Instance
        }
    },
    'class_method': {
        'object': testers.ATestClass,
        'attribute': 'class_method',
        'valid': {
            'kargs': ('test'),
            'kwargs': {}
        },
        'invalid': {
            'kargs': (),
            'kwargs': {'invalid': True}
        },
        'types': {
            'attribute': AttributeType.ClassMethod,
            'object': ObjectType.Class
        }
    },
})

possible_contexts_names = ['instance_method']


class AContext(SearchStrategy):
    """ Generates a receives.context with additional information
    """
    def do_draw(self, data):
        max = len(possible_contexts_names) - 1
        c_id = data.draw(integers(min_value=0, max_value=max))
        p_ctx = getattr(possible_contexts, possible_contexts_names[c_id])

        info = copy.deepcopy(p_ctx)
        setattr(info, 'ctx', make_context(info.object, info.attribute))
        return info


@cacheable
@defines_strategy
def a_context():
    """ draw a receives.context to test with
    """
    return shared(AContext(), 'spec.helper.a_context()')
