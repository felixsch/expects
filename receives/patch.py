from functools import partial

from receives.error import Bug
from receives.expectation import Expectation
from receives.context import AttributeType, ObjectType


class Patch():
    def __init__(self, mapping, context):
        self._expected_call_count = 0
        self._original_call = None
        self._expectations = []
        self._call_count = 0
        self._mapping = mapping
        self._ctx = context
        self._call_handler = None

    @property
    def mapping(self):
        return self._mapping

    @property
    def ctx(self):
        return self._ctx

    @property
    def call_handler(self):
        if self._call_handler is None:
            self._call_handler = self._select_call_handler()

        return self._call_handler

    def _select_call_handler(self):
        # at class level
        if self.ctx.attribute_type == AttributeType.Property:
            return patch_fake_property(self)

        if self.ctx.object_type == ObjectType.Instance:
            method_type = getattr(self.ctx.object.__class__, self.ctx.attribute_name)
            # at instance level
            if isinstance(method_type, property):
                raise AssertionError("Properties can not be mocked on per instance basis")
            return partial(patch_handle_instance, self)

        if self.ctx.object_type == ObjectType.Class and self.ctx.attribute_type == AttributeType.Method:
            def wrap(cls, *kargs, **kwargs):
                return patch_handle_instance_method(self, cls, kargs, kwargs)
            return wrap

        return partial(patch_handle_default, self)

    @property
    def original_call(self):
        return self._original_call

    def was_called(self):
        self._call_count += 1

    def expect_one_more_call(self):
        self._call_count += 1
        self._expected_call_count += 1

    def patch(self):
        self._original_call = getattr(self.ctx.object, self.ctx.attribute_name)
        setattr(self.ctx.object, self.ctx.attribute_name, self.call_handler)

    def unpatch(self):
        if self.original_call is not None:
            setattr(self.ctx.object, self.ctx.attribute_name, self.original_call)

    def finalize(self):
        self.unpatch()
        if self._expected_call_count != self._call_count:
            raise AssertionError("Expected {}.{} to run {} times but run {} times."
                                 .format(self.ctx.object_name,
                                         self.ctx.attribute_name,
                                         self._expected_call_count,
                                         self._call_count))

    def has_expectations(self):
        return len(self._expectations) > 0

    def next_expectation(self):
        try:
            return self._expectations.pop(0)
        except IndexError:
            raise Bug("Mock without expectation wants to validate itself")

    def new_expectation(self):
        expectation = Expectation(self.ctx)
        self._expectations.append(expectation)
        self._expected_call_count += 1
        return expectation


def patch_evaluate(patch, kargs, kwargs, eval_original_call=None):
    patch.was_called()

    if not patch.has_expectations():
        return None

    expectation = patch.next_expectation()

    if not expectation.should_call_original:
        return expectation.validate(kargs, kwargs)

    if not eval_original_call:
        return patch.original_call(*kargs, **kwargs)

    return eval_original_call(kargs, kwargs)


def patch_find_class_patch(patch):
    return patch.mapping.find_by(patch.ctx.base_class, patch.ctx.attribute_name)


def patch_handle_instance(patch, *kargs, **kwargs):
    class_patch = patch_find_class_patch(patch)

    # there is no class patching set
    if class_patch is None:
        return patch_evaluate(patch, kargs, kwargs)

    # There is a class patch without expectations
    # fall back to the instance patching but make sure
    # that the class_patch knows about the call attempt
    if not class_patch.has_expectations():
        class_patch.expect_one_more_call()
        return patch_evaluate(patch, kargs, kwargs)

    # We evaluate the class patch and inform the instance
    # patch that call was done one more time
    patch.expect_one_more_call()

    # in case the original call should be called we call the original
    # call from the instance not the class
    def eval(kargs, kwargs):
        return patch.original_call(*kargs, **kwargs)

    return patch_evaluate(class_patch, kargs, kwargs, eval_original_call=eval)


def patch_handle_instance_method(patch, cls, kargs, kwargs):
    def eval(kargs, kwargs):
        return patch.original_call(cls, *kargs, **kwargs)
    return patch_evaluate(patch, kargs, kwargs, eval_original_call=eval)


def patch_handle_default(patch, *kargs, **kwargs):
    return patch_evaluate(patch, kargs, kwargs)


def patch_handle_property_get(patch, *kargs, **kwargs):
    def eval(kargs, kwargs):
        return patch.original_call.__get__(*kargs, **kwargs)
    return patch_evaluate(patch, kargs, kwargs, eval_original_call=eval)


def patch_handle_property_set(patch, *kargs_, **kwargs_):
    def eval(kargs, kwargs):
        return patch.original_call.__set__(*kargs_, **kwargs_)
    return patch_evaluate(patch, kargs_[1:], kwargs_, eval_original_call=eval)


def patch_fake_property(patch):
    prop = getattr(patch.ctx.object, patch.ctx.attribute_name)
    fake_get = partial(patch_handle_property_get, patch)
    fake_set = partial(patch_handle_property_set, patch)

    if prop.fset:
        return property(fake_get, fake_set)
    return property(fake_get)
