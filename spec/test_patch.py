from expects import expect, be, be_none, be_true, be_a, be_false, equal, raise_error
from expects import be_callable

from spec.helper import description, before, describe, it, context
from spec.helper import TestClass, make_context
from spec.helper import MagicMock, raises
from spec import helper

from functools import partial

from receives.mapping import Mapping
from receives.error import Bug
from receives import patch


from mamba import fit

with description(patch.Patch) as self:

    with before.each:
        self.testclass = TestClass()
        self.context = make_context(self.testclass, "valid")
        self.mapping = Mapping()
        self.subject = patch.Patch(self.mapping, self.context)

    with describe('#__init__'):
        with it('initializes patch object'):
            expect(self.subject._expected_call_count).to(equal(0))
            expect(self.subject._original_call).to(be_none)
            expect(self.subject._expectations).to(equal([]))
            expect(self.subject._call_count).to(equal(0))
            expect(self.subject._mapping).to(be(self.mapping))
            expect(self.subject._ctx).to(be(self.context))
            expect(self.subject._call_handler).to(be_none)

    with describe('#mapping'):
        with it('returns the actual mapping'):
            expect(self.subject.mapping).to(be(self.mapping))

    with describe('#ctx'):
        with it('returns the actual context'):
            expect(self.subject.ctx).to(be(self.context))

    with describe('#_select_call_handler'):
        with context('property'):
            with it('returns a fake property'):
                subject = patch.Patch(self.mapping, make_context(TestClass, "prop"))
                expect(subject._select_call_handler()).to(be_a(property))

            with it('raises if a property on a instance'):
                subject = patch.Patch(self.mapping, make_context(self.testclass, "prop"))
                with raises(AssertionError):
                    subject._select_call_handler()

        with context('instance'):
            with it('returns the method call for an instance method'):
                expect(self.subject._select_call_handler()).to(be_a(partial))
                expect(self.subject._select_call_handler().func).to(be(patch.patch_handle_instance))
                expect(self.subject._select_call_handler().args).to(equal((self.subject,)))

        with context('function'):
            with it('returns the method call for a normal function'):
                subject = patch.Patch(self.mapping, make_context(helper, 'test_function'))
                expect(subject._select_call_handler()).to(be_a(partial))
                expect(subject._select_call_handler().func).to(be(patch.patch_handle_default))
                expect(subject._select_call_handler().args).to(equal((subject,)))

        with context('class'):
            with it('returns the method call for a class method'):
                subject = patch.Patch(self.mapping, make_context(TestClass, "valid"))
                expect(subject._select_call_handler()).to(be_callable)
                expect(subject._select_call_handler().__name__).to(be('wrap'))

    with describe('#call_handler'):
        with it('creates a new call handler when called first'):
            self.subject._select_call_handler = MagicMock()
            self.subject.call_handler
            self.subject._select_call_handler.assert_called_once_with()

        with it('does return the already created call handler'):
            self.subject.call_handler
            self.subject._select_call_handler = MagicMock()
            self.subject.call_handler
            expect(self.subject._select_call_handler.called).to(be_false)

    with describe('#original_call'):
        with it('returns None if not patched yet'):
            expect(self.subject.original_call).to(be_none)

        with it('returns the original_call'):
            original_call = getattr(self.testclass, "valid")
            self.subject.patch()
            expect(self.subject.original_call).to(equal(original_call))

    with describe('#was_called'):
        with it('returns initially 0'):
            expect(self.subject._call_count).to(equal(0))
            self.subject.was_called()
            expect(self.subject._call_count).to(equal(1))

    with describe('#expect_one_more_call'):
        with it('was called but requires one more call'):
            expect(self.subject._call_count).to(equal(0))
            expect(self.subject._expected_call_count).to(equal(0))
            self.subject.expect_one_more_call()
            expect(self.subject._call_count).to(equal(1))
            expect(self.subject._expected_call_count).to(equal(1))

    with describe('#patch'):
        with it('replaces the to be patched method'):
            orig_call = self.testclass.valid

            self.subject.patch()
            expect(self.testclass.valid).to(be(self.subject.call_handler))
            expect(self.subject._original_call).to(equal(orig_call))

    with describe('#unpatch'):
        with it('unpatches the method if it was set'):
            orig_call = self.testclass.valid

            self.subject.patch()
            expect(self.testclass.valid).to(be(self.subject.call_handler))

            self.subject.unpatch()
            expect(self.testclass.valid).to(equal(orig_call))

    with describe('#finalize'):
        with it('restors the old method and checks for call counts'):
            self.subject.unpatch = MagicMock()
            expect(lambda: self.subject.finalize()).not_to(raise_error(AssertionError))
            self.subject.unpatch.assert_called_once_with()

        with it('raises an assertion exception if call counts do not match'):
            self.subject._call_count = 0
            self.subject._expected_call_count = 1

            expect(lambda: self.subject.finalize()).to(raise_error(AssertionError))

    with describe('#new_expectation'):
        with it('creates a new expectation'):
            ex = self.subject.new_expectation()
            expect(ex._context).to(be(self.context))
            expect(self.subject._expectations).to(equal([ex]))
            expect(self.subject._expected_call_count).to(be(1))

    with describe('#has_expectations'):
        with it('returns false if now expectation was added'):
            expect(self.subject.has_expectations()).to(be_false)

        with it('returns true if expectations were added'):
            self.subject.new_expectation()
            expect(self.subject.has_expectations()).to(be_true)

    with describe('#next_expectation'):
        with context('has expectations'):
            with it('returns the next expectation'):
                ex = self.subject.new_expectation()
                self.subject.new_expectation()
                expect(self.subject.next_expectation()).to(be(ex))
        with context('has no expectation'):
            with it('raises an error'):
                expect(lambda: self.subject.next_expectation()).to(raise_error(Bug))


# Handler methods

with description(patch.patch_evaluate):
    with before.each:
        self.testclass = TestClass()
        self.context = make_context(self.testclass, "valid")
        self.mapping = Mapping()
        self.subject = patch.Patch(self.mapping, self.context)

    with describe('runs the generic evaluation'):
        with it(''):
            print('foo')

