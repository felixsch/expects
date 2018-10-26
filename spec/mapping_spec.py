from expects import expect, be, be_none, be_true, be_false, equal

from spec.helper import description, before, describe, it, context
from spec.helper import TestClass, make_context
from spec.helper import MagicMock, raises

from receives.mapping import Mapping
from receives.error import Bug


with description(Mapping) as self:

    with before.each:
        self.subject = Mapping()
        self.inst = TestClass()
        self.c_ctx = make_context(TestClass, "valid")
        self.i_ctx = make_context(self.inst, "valid")

    with describe('#__init__'):
        with it('creates a new mapping without patches'):
            expect(self.subject._patches).to(equal([]))

    with describe('#find_by'):
        with it('a valid search'):
            patch = self.subject.create_patch(self.i_ctx)

            expect(self.subject.find_by(self.i_ctx.object,
                                        self.i_ctx.attribute_name)).to(be(patch))

        with it('a invalid search'):
            expect(self.subject.find_by(self.inst, "invalid")).to(be_none)

    with describe('#is_already_patched'):
        with it('is not patched yet'):
            expect(self.subject.is_already_patched(self.c_ctx)).to(be_false)
            expect(self.subject.is_already_patched(self.i_ctx)).to(be_false)

        with it('is already patched'):
            self.subject.create_patch(self.c_ctx)
            self.subject.create_patch(self.i_ctx)

            expect(self.subject.is_already_patched(self.c_ctx)).to(be_true)
            expect(self.subject.is_already_patched(self.i_ctx)).to(be_true)

    with describe('#find_class_patch'):
        with it('has class mappings'):
            i_ctx_invalid = make_context(self.inst, "invalid")
            patch = self.subject.create_patch(self.c_ctx)

            self.subject.create_patch(self.i_ctx)
            self.subject.create_patch(i_ctx_invalid)

            expect(self.subject.find_class_patch(self.i_ctx)).to(be(patch))
            expect(self.subject.find_class_patch(self.c_ctx)).to(be_none)
            expect(self.subject.find_class_patch(i_ctx_invalid)).to(be_none)

    with describe('#find_instance_patch'):
        with it('has instance mappings'):
            self.subject.create_patch(self.c_ctx)
            patch = self.subject.create_patch(self.i_ctx)

            expect(self.subject.find_instance_patch(self.c_ctx)).to(be(patch))
            expect(self.subject.find_instance_patch(self.i_ctx)).to(be_none)
            expect(self.subject.find_instance_patch(make_context(TestClass, "invalid"))).to(be_none)

    with describe('#create_patch'):
        with context('patch already exist'):
            with it('creates double patch for same context'):
                self.subject.create_patch(self.c_ctx)
                with raises(Bug):
                    self.subject.create_patch(self.c_ctx)

            with it('unpatches applied class patches'):
                c_patch = self.subject.create_patch(self.c_ctx)
                c_patch.unpatch = MagicMock()
                i_patch = self.subject.create_patch(self.i_ctx)
                c_patch.unpatch.assert_called_once_with()

            with it('raises if instance patch already exists'):
                self.subject.create_patch(self.i_ctx)
                with raises(AssertionError):
                    self.subject.create_patch(self.c_ctx)

        with context('patch does not exist'):
            with it('creates a new patch'):
                expect(self.subject._patches).to(equal([]))
                i_patch = self.subject.create_patch(self.i_ctx)
                expect(self.subject._patches[0]).to(be(i_patch))

    with describe('#finalize'):
        with it('finalizes all patches'):
            c_patch = self.subject.create_patch(self.c_ctx)
            c_patch.finalize = MagicMock()

            i_patch = self.subject.create_patch(self.i_ctx)
            i_patch.finalize = MagicMock()

            self.subject.finalize()
            c_patch.finalize.assert_called_once_with()
            i_patch.finalize.assert_called_once_with()
