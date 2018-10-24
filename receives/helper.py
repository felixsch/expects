import sys
import inspect
from types import CodeType


def current_module():
    frame = inspect.stack()[1]
    return inspect.getmodule(frame[0])
