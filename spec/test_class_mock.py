import pprint
from pytest import raises
from expects import expect, equal, be

from receives import receive, allow


# PRE -------------------------------------------------------------------------


class TestClass():
    def methodA(self, string):
        return string

    def methodB(self, number, string):
        return "{}:{}".format(self.methodA(string), number)

    @classmethod
    def methodC(klass, string):
        return string


def execute_class(number, string):
    inst = TestClass()
    return inst.methodB(number, string)


# TESTS -----------------------------------------------------------------------


def test_instance_mocking():
    receive(TestClass, "methodA").and_return("foo")
    expect(execute_class(1, "hello")).to(equal("foo:1"))
    expect(execute_class(1, "hello")).to(equal("hello:1"))

    receive(TestClass, "methodB").with_args(1, "hello").and_return(12)
    expect(execute_class(1, "hello")).to(be(12))

    receive(TestClass, "methodA").with_args("hello").and_return("foo")
    with raises(AssertionError):
        execute_class(1, "not hello")


def test_instance_persistant_mocking():
    with allow(TestClass, "methodA").and_return("foo"):
        expect(execute_class(1, "hello")).to(equal("foo:1"))
        expect(execute_class(1, "hello")).to(equal("foo:1"))
        expect(execute_class(1, "hello")).to(equal("foo:1"))
    expect(execute_class(1, "hello")).to(equal("hello:1"))


def test_class_method_mocking():
    receive(TestClass, "methodC").and_return(1)
    expect(TestClass.methodC("hello")).to(be(1))
    expect(TestClass.methodC("hello")).to(be("hello"))


def test_std_class_mocking():
    receive(pprint.PrettyPrinter, "pprint").and_return(1)

    pp = pprint.PrettyPrinter()
    expect(pp.pprint([])).to(be(1))
