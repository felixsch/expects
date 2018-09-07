import sys

def current_module():
    caller_frame = sys._getframe(1)
    name = caller_frame.f_globals['__name__']
    return sys.modules[name]
