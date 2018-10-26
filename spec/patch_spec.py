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
        with context('valid input'):
            with it('runs and validates against the input'):
                self.subject.was_called = MagicMock()
                ex = self.subject.new_expectation()
                ex.with_args('foo').and_return('returnvalue')

                value = patch.patch_evaluate(self.subject, ('foo',), {})
                expect(value).to(equal('returnvalue'))
                expect(self.subject.was_called.called).to(be_true)

            with it('returns None if there is no expectation'):
                self.subject.was_called = MagicMock()

                expect(patch.patch_evaluate(self.subject, (), {})).to(be_none)
                expect(self.subject.was_called.called).to(be_true)

            with it('calles the original call'):
                self.subject.patch()
                self.subject.was_called = MagicMock()
                ex = self.subject.new_expectation()
                ex.with_args('moep').and_call_original()

                value = patch.patch_evaluate(self.subject, ('moep',), {})

                expect(self.subject.was_called.called).to(be_true)
                expect(value).to(equal('moep'))


with description(patch.patch_find_class_patch):
    with before.each:
        self.testclass = TestClass()
        self.mapping = Mapping()

    with describe('finds the class of an instance'):
        with context('a class patch is set'):
            with it('returns the class patch'):
                class_context = make_context(TestClass, "valid")
                instance_context = make_context(self.testclass, "valid")
                class_patch = self.mapping.create_patch(class_context)
                instance_patch = self.mapping.create_patch(instance_context)

                expect(patch.patch_find_class_patch(instance_patch)).to(be(class_patch))

        with context('no class patch is set'):
            with it('returns None'):
                instance_context = make_context(self.testclass, "valid")
                instance_patch = self.mapping.create_patch(instance_context)

                expect(patch.patch_find_class_patch(instance_patch)).to(be_none)

        with context('a class patch as argument'):
            with it('returns None'):
                class_context = make_context(TestClass, "valid")
                instance_context = make_context(self.testclass, "valid")
                class_patch = self.mapping.create_patch(class_context)
                instance_patch = self.mapping.create_patch(instance_context)

                expect(patch.patch_find_class_patch(class_patch)).to(be_none)


with describe(patch.patch_handle_instance):
    with before.each:
        self.testclass = TestClass()
        self.mapping = Mapping()
        self.instance_context = make_context(self.testclass, "valid")
        self.class_context = make_context(TestClass, "valid")

    with context('without class patch'):
        with it('evaluates the class patch'):
            instance_patch = self.mapping.create_patch(self.instance_context)

            expect(patch.patch_handle_instance(instance_patch)).to(be_none)
            expect(instance_patch._call_count).to(be(1))

    with context('with class patch without expectation'):
        with it('evaluates the class patch'):
            class_patch = self.mapping.create_patch(self.class_context)
            instance_patch = self.mapping.create_patch(self.instance_context)

            expect(patch.patch_handle_instance(instance_patch)).to(be_none)
            expect(instance_patch._call_count).to(be(1))
            expect(class_patch._expected_call_count).to(be(1))

    with context('with class patch with expectation'):
        with it('evaluates the class patch'):
            class_patch = self.mapping.create_patch(self.class_context)
            instance_patch = self.mapping.create_patch(self.instance_context)

            expt = class_patch.new_expectation()
            expt.and_return('foo')

            expect(patch.patch_handle_instance(instance_patch)).to(be('foo'))
            expect(class_patch._call_count).to(be(1))
            expect(class_patch._expected_call_count).to(be(1))
            expect(instance_patch._call_count).to(be(1))
            expect(instance_patch._expected_call_count).to(be(1))

    with context('with class patch and expectation and original call'):
        with it('evaluates the class patch and runs the instance method'):
            class_patch = self.mapping.create_patch(self.class_context)
            class_patch.patch()
            instance_patch = self.mapping.create_patch(self.instance_context)
            instance_patch.patch()

            expt = class_patch.new_expectation()
            expt.and_call_original()

            expect(patch.patch_handle_instance(instance_patch, 'moep')).to(be('moep'))
            expect(class_patch._call_count).to(be(1))
            expect(class_patch._expected_call_count).to(be(1))
            expect(instance_patch._call_count).to(be(1))
            expect(instance_patch._expected_call_count).to(be(1))


with describe(patch.patch_handle_instance_method):
    with before.each:
        self.mapping = Mapping()
        self.class_context = make_context(TestClass, "valid")

    with it('evaluates the class expectation if a instance is created'):
        class_patch = self.mapping.create_patch(self.class_context)
        class_patch.new_expectation().and_return('foo')
        class_patch.patch()
        testclass = TestClass()

        expect(patch.patch_handle_instance_method(class_patch, testclass, ('moep',), {})).to(be('foo'))
        class_patch.unpatch()

    with it('evaluates and calls the original call'):
        class_patch = self.mapping.create_patch(self.class_context)
        class_patch.new_expectation().and_call_original()
        class_patch.patch()
        testclass = TestClass()

        expect(patch.patch_handle_instance_method(class_patch, testclass, ('moep',), {})).to(be('moep'))
        class_patch.unpatch()


with describe(patch.patch_handle_default):
    with before.each:
        self.mapping = Mapping()
        self.func_context = make_context(helper, "test_function")

    with it('patches runs a normal evaluation'):
        func_patch = self.mapping.create_patch(self.func_context)
        func_patch.new_expectation().and_return('foo')

        expect(patch.patch_handle_default(func_patch)).to(be('foo'))


with describe(patch.patch_handle_property_set):
    with before.each:
        self.mapping = Mapping()
        self.prop_context = make_context(TestClass, "prop2")
        self.prop_patch = self.mapping.create_patch(self.prop_context)

    with it('evaluates the setter without calling original'):
        self.prop_patch.new_expectation().with_args(1000)
        self.prop_patch.patch()
        testclass = TestClass()

        expect(patch.patch_handle_property_set(self.prop_patch, testclass, 1000)).to(be(None))
        expect(testclass.prop2_value).to(be(42))

        self.prop_patch.unpatch()

    with it('evaluates the setter and calls the original'):
        self.prop_patch.new_expectation().with_args(1000).and_call_original()
        self.prop_patch.patch()
        testclass = TestClass()

        expect(patch.patch_handle_property_set(self.prop_patch, testclass, 1000)).to(be(None))
        expect(testclass.prop2_value).to(be(1000))

        self.prop_patch.unpatch()

with describe(patch.patch_handle_property_get):
    with before.each:
        self.mapping = Mapping()
        self.prop_context = make_context(TestClass, "prop2")
        self.prop_patch = self.mapping.create_patch(self.prop_context)

    with it('evaluates the getter without calling original'):
        self.prop_patch.new_expectation().and_return(1000)
        self.prop_patch.patch()
        testclass = TestClass()

        expect(patch.patch_handle_property_get(self.prop_patch, testclass)).to(be(1000))
        self.prop_patch.unpatch()

    with it('evaluates the getther with calling original'):
        self.prop_patch.new_expectation().and_call_original()
        self.prop_patch.patch()
        testclass = TestClass()

        expect(patch.patch_handle_property_get(self.prop_patch, testclass)).to(be(42))
        self.prop_patch.unpatch()


with describe(patch.patch_fake_property):
    with before.each:
        self.mapping = Mapping()

    with it('returns a fake property without a setter'):
        self.prop_context = make_context(TestClass, "prop")
        self.prop_patch = self.mapping.create_patch(self.prop_context)
        prop = patch.patch_fake_property(self.prop_patch)

        expect(prop).to(be_a(property))
        expect(prop.fset).to(be_none)
        expect(prop.fget).to(be_a(partial))

    with it('returns a fake'):
        self.prop_context = make_context(TestClass, "prop2")
        self.prop_patch = self.mapping.create_patch(self.prop_context)
        prop = patch.patch_fake_property(self.prop_patch)

        expect(prop).to(be_a(property))
        expect(prop.fset).to(be_a(partial))
        expect(prop.fget).to(be_a(partial))
