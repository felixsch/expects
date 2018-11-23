from expects import expect, be, be_a, be_none, be_true, be_false, equal, contain

from spec.helper import debug, given, settings
from spec.helpers.context import a_context, a_specific_context
from spec.helpers.mapping import a_mapping

from receives.context import to_hash, determine_attribute_type, determine_object_type
from receives.context import Context, ObjectType

from hypothesis.strategies import random_module, text


@given(a_mapping())
def test_mapping_init(mapping):
    expect(mapping._patches).to(equal([]))


@settings(max_examples=1)
@given(a_mapping(), a_specific_context('instance'), a_specific_context('module'))
def test_mapping_find_by(mapping, instance, module):
    patch = mapping.create_patch(instance.ctx)
    expect(mapping.find_by(instance.object, instance.attribute)).to(be(patch))
    expect(mapping.find_by(module.object, module.attribute)).to(be_none)


@given(a_mapping(), a_specific_context('instance'), a_specific_context('class'))
def test_mapping_is_already_patched(mapping, context1, context2):
    mapping.create_patch(context1.ctx)
    expect(mapping.is_already_patched(context1.ctx)).to(be_true)
    expect(mapping.is_already_patched(context2.ctx)).to(be_false)


@given(a_mapping(), a_specific_context('instance'), a_specific_context('class'))
def test_mapping_find_class_patch(mapping, instance, klass):
    patch = mapping.create_patch(klass.ctx)
    expect(mapping.find_class_patch(instance.ctx)).to(be(patch))


@given(a_mapping(), a_specific_context('instance'), a_specific_context('class'))
def test_mapping_find_instance_patch(mapping, instance, klass):
    patch = mapping.create_patch(instance.ctx)
    expect(mapping.find_instance_patch(klass.ctx)).to(be(patch))
    expect(mapping.find_instance_patch(instance.ctx)).to(be_none)


