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
    'instance': {
        'object': testers.ATestClass(),
        'object_name': 'ATestClass',
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
    'class': {
        'object': testers.ATestClass,
        'object_name': 'ATestClass',
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
    'property': {
        'object': testers.ATestClass,
        'object_name': 'ATestClass',
        'attribute': 'ro_property',
        'valid': {
            'kargs': (),
            'kwargs': {}
        },
        'invalid': {
            'kargs': (),
            'kwargs': {'invalid': True}
        },
        'types': {
            'attribute': AttributeType.Property,
            'object': ObjectType.Class
        }
    },
    'rw_property': {
        'object': testers.ATestClass,
        'object_name': 'ATestClass',
        'attribute': 'ro_property',
        'valid': {
            'kargs': (8),
            'kwargs': {}
        },
        'invalid': {
            'kargs': (),
            'kwargs': {'invalid': True}
        },
        'types': {
            'attribute': AttributeType.Property,
            'object': ObjectType.Class
        }
    },
    'module': {
        'object': testers,
        'object_name': 'spec.helpers.testers',
        'attribute': 'a_test_function',
        'valid': {
            'kargs': ("test"),
            'kwargs': {}
        },
        'invalid': {
            'kargs': (),
            'kwargs': {'invalid': True}
        },
        'types': {
            'attribute': AttributeType.Method,
            'object': ObjectType.Module
        }
    },
})

possible_contexts_names = ['instance', 'class', 'property', 'rw_property', 'module']


class AContext(SearchStrategy):
    """ Generates a receives.context with additional information
    """

    def __init__(self, context_names):
        SearchStrategy.__init__(self)
        self._context_names = context_names

    def do_draw(self, data):
        contexts = self._fetch_contexts(self._context_names)
        max = len(contexts) - 1
        c_id = data.draw(integers(min_value=0, max_value=max))

        info = copy.deepcopy(contexts[c_id])
        setattr(info, 'ctx', make_context(info.object, info.attribute))
        return info

    def _fetch_contexts(self, context_names):
        contexts = []
        for name in context_names:
            contexts.append(getattr(possible_contexts, name))
        return contexts


@cacheable
@defines_strategy
def a_context(context_names=possible_contexts_names):
    """ draw a receives.context to test with
    """
    return shared(AContext(context_names), 'spec.helper.a_context()')


@cacheable
@defines_strategy
def a_specific_context(context_type):
    return AContext([context_type])
