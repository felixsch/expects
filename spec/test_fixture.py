from expects import expect, be, be_none, equal

from receives.fixture import fixture, FixtureLoader

import receives
import builtins

import pytest
import sys

def test_fixture_loader_init():
    print("init test")
    caller = "test_fixture_loader_init"
    filename = "json.fixture"
    print("add recevie")
    test()

    print("init subject")
    subject = FixtureLoader(filename, caller)

    print("expect")
    #expect(subject._path).to(be("/sample/path"))
    print("done")


#def test_fixture_loader_load():
#    caller = "test_fixture_loader_init"
#    filename = "json.fixture"
#    receive(FixtureLoader, "_prepared_path").with_args(filename, caller).and_return("/sample/path")
#    receive(receives, "open").with_args("/sample/path/json.fixture").and_return(fake_file("foo"))

#    #import pdb; pdb.set_trace()

#    subject = FixtureLoader(filename, caller)



#    pass


def test_fixture_loader__prepared_path():
    pass


def test_fixture_loader__select_loader():
    pass


def test_fixture_loader__error():
    pass
