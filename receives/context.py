from enum import Enum
import inspect



class ObjectType(Enum):
    Variable = "variable"
    Module = "module"
    Method = "method"
    Class = "class"
    Instance = "instance"


class AttributeType(Enum):
    Method = "method"
    Property = "property"
    ClassMethod = "classmethod"


def to_hash(obj, attribute):
    return hash((obj, attribute))


def determine_attribute_type(obj, attribute):
    if isinstance(attribute, property):
        return AttributeType.Property
    if inspect.isclass(obj) and inspect.ismethod(attribute) and attribute.__self__ is obj:
        return AttributeType.ClassMethod
    return AttributeType.Method


def determine_object_type(obj):
    if not hasattr(obj, '__dict__'):
        return ObjectType.Variable
    if inspect.ismodule(obj):
        return ObjectType.Module
    if inspect.isroutine(obj):
        return ObjectType.Method
    if inspect.isclass(obj):
        return ObjectType.Class
    else:
        return ObjectType.Instance


class Context():
    def __init__(self, obj, attribute_name, caller_frame):
        self._object = obj
        self._attribute_name = attribute_name
        self._caller_frame = caller_frame

        self._object_type = determine_object_type(self.object)

        attribute = getattr(self.object, self.attribute_name)
        self._attribute_type = determine_attribute_type(self.object, attribute)

    def __eq__(self, other):
        return self._object == other._object and self._attribute_name == other._attribute_name

    def is_instance(self):
        if self._object_type == ObjectType.Instance:
            return True
        return False

    def get_base_context(self):
        if not self.is_instance():
            return None
        return Context(self.base_class(), self.attribute_name, None)

    @property
    def object(self):
        return self._object

    @property
    def object_type(self):
        return self._object_type

    @property
    def object_name(self):
        if self.object_type == ObjectType.Module:
            return self.object.__name__
        if self.object_type == ObjectType.Class:
            return self.object.__name__

        return self._extract_instance_name(self._caller_frame)

    def _extract_instance_name(self, frame):
        for name, obj in frame.f_locals.items():
            if obj == self._object:
                return name
        return self._object.__class__.__name__

    @property
    def base_class(self):
        # Removed this check if the implementation runs into an issue. If it's
        # the case add the test to context_spec.py and reenable this lines!
        #
        # if not hasattr(self.object, "__class__"):
        #     return None
        return self.object.__class__

    @property
    def attribute_name(self):
        return self._attribute_name

    @property
    def attribute_type(self):
        return self._attribute_type

    def __hash__(self):
        return to_hash(self.object, self.attribute_name)
