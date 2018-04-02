import sys
from expects import expect, be, be_none, equal

from conftest import Double
from receives.context import Context


# PRE -------------------------------------------------------------------------


def module_context():
    caller = sys._getframe(1).f_code.co_name
    return Context(caller, sys, "exit")


def class_context():
    caller = sys._getframe(1).f_code.co_name
    return Context(caller, Double, "double_method")


def instance_context(instance):
    caller = sys._getframe(1).f_code.co_name
    return Context(caller, instance, "double_method")


# TESTS -----------------------------------------------------------------------


def test_context_init():
    subject = module_context()

    expect(subject._caller_name).to(be("test_context_init"))
    expect(subject._object).to(be(sys))
    expect(subject._method_name).to(be("exit"))
    expect(subject._method).to(be_none)


def test_context_caller_name():
    subject = module_context()

    expect(subject.caller_name()).to(be("test_context_caller_name"))


def test_context_object_name():
    module_subject = module_context()
    class_subject = class_context()

    test_instance = Double()
    instance_subject = instance_context(test_instance)

    expect(module_subject.object_name()).to(equal("sys"))
    expect(class_subject.object_name()).to(equal("Double"))
    expect(instance_subject.object_name()).to(equal("test_instance"))


def test_context_method_name():
    subject = module_context()

    expect(subject.method_name()).to(equal("exit"))


def test_context_object():
    subject = module_context()

    expect(subject.object()).to(be(sys))


def test_context_set_method():
    subject = module_context()
    stub_method = "stub"

    subject.set_method(stub_method)
    expect(subject._method).to(be(stub_method))


def test_context_method():
    subject = module_context()
    stub_method = "stub"

    subject.set_method(stub_method)

    expect(subject.method()).to(be(stub_method))
