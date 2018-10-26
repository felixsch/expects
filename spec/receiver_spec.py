from expects import expect, be, be_a

from spec.helper import description, before, describe, it
from spec.helper import TestClass, MagicMock

from receives.receiver import Receiver, receives
from receives.mapping import Mapping
from receives.expectation import Expectation
from receives.patch import Patch


with description(Receiver) as self:
    with before.each:
        self.subject = Receiver()

    with describe('#__init__'):
        with it('creates a new mapping'):
            expect(self.subject._mapping).to(be_a(Mapping))

    with describe('#__call__'):
        with it('new creates patch'):
            expectation = self.subject(TestClass, "valid")

            expect(expectation).to(be_a(Expectation))
            expect(len(self.subject._mapping._patches)).to(be(1))

        with it('new creates patch'):
            expectation = self.subject(TestClass, "valid")
            class_patch = self.subject._mapping.find_by(TestClass, "valid")

            expect(class_patch).to(be_a(Patch))

            class_patch.new_expectation = MagicMock()
            self.subject(TestClass, "valid")

            class_patch.new_expectation.assert_called_once_with()

    with describe('#finalize'):
        with it('it calls the finalizer of the mapping'):
            mapping = self.subject._mapping
            mapping.finalize = MagicMock()

            self.subject.finalize()
            mapping.finalize.assert_called_once_with()


with describe(receives):
    with it('creates a decorator which injects the receiver to a method'):
        @receives
        def test_injection(receive):
            expect(receive).to(be_a(Receiver))
        test_injection()
