from expects import expect, be, be_none, be_true, be_false, equal, contain

from spec.helper import set_trace, given
from spec.helpers.context import a_context

from receives.context import to_hash, determine_attribute_type
from receives.context import Context

from hypothesis.strategies import random_module, text


@given(random_module(), text())
def test_to_hash(m, t):
    expect(to_hash(m, t)).to(equal(to_hash(m, t)))


@given(a_context())
def test_determine_attribute_types(sample):
    attr = getattr(sample.object, sample.attribute)
    expect(determine_attribute_type(sample.object, attr)).to(be(sample.types.attribute))


@given(a_context())
def test_context_object(sample):
    expect(sample.ctx.object).to(be(sample.object))

# with description(determine_attribute_type) as self:
#     with before.each:
#         self.instance = TestClass()
#     with it('determines the right types'):
#         method = getattr(self.instance, "valid")
#         property = getattr(TestClass, "prop")
#         classmethod = getattr(TestClass, "classmethod")

#         expect(determine_attribute_type(self.instance, method)).to(be(AttributeType.Method))
#         expect(determine_attribute_type(self.instance, property)).to(be(AttributeType.Property))
#         expect(determine_attribute_type(TestClass, classmethod)).to(be(AttributeType.ClassMethod))


# with description(Context) as self:
#     with before.each:
#         self.instance = TestClass()
#         self.instance_context = make_context(self.instance, "valid")
#         self.class_context = make_context(TestClass, "valid")
#         self.module_context = make_context(receives.context, "to_hash")

#     with describe("#object"):
#         with it('returns the selected object'):
#             expect(self.instance_context.object).to(be(self.instance))

#     with describe('#object_type'):
#         with it('returns the type of the object'):
#             expect(self.class_context.object_type).to(be(ObjectType.Class))
#             expect(self.instance_context.object_type).to(be(ObjectType.Instance))
#             expect(self.module_context.object_type).to(be(ObjectType.Module))
