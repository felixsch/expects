import inspect


def current_module():
    frame = inspect.stack()[1]
    return inspect.getmodule(frame[0])
