from receives.context import to_hash, ObjectType
from receives.patch import Patch
from receives.error import Bug


class Mapping():
    def __init__(self):
        self._patches = []

    def find_by(self, obj, attribute_name):
        needle = to_hash(obj, attribute_name)

        for patch in self._patches:
            if hash(patch.ctx) == needle:
                return patch
        return None

    def is_already_patched(self, context):
        return self.find_by(context.object, context.attribute_name) is not None

    def find_class_patch(self, context):
        if context.object_type != ObjectType.Instance:
            return None
        return self.find_by(context.base_class, context.attribute_name)

    def find_instance_patch(self, context):
        if context.object_type != ObjectType.Class:
            return None
        for patch in self._patches:
            # Check if the base class of the patched object is actually the
            # class context object where searching
            if patch.ctx.base_class == context.object and patch.ctx.attribute_name == context.attribute_name:
                return patch
        return None

    def create_patch(self, context):
        if self.is_already_patched(context):
            raise Bug("There is already a context for this instance")

        # In case there is already a class patch replace the patch_handler with
        # the instance one.
        class_patch = self.find_class_patch(context)
        if class_patch:
            class_patch.unpatch()

        instance_patch = self.find_instance_patch(context)
        if instance_patch is not None:
            raise AssertionError("class should be patched after an instance was "
                                 "created. This behaviour is not supported by "
                                 "receives.")

        patch = Patch(self, context)
        self._patches.append(patch)
        return patch

    def finalize(self):
        # Run the finalization in reversed order so that the instances patches
        # are finalized before the class patches
        for patch in reversed(self._patches):
            patch.finalize()
