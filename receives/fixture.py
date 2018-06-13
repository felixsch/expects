import json
import os
import inspect
import sys

from receives import util

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def fixture(path, format="plain"):
    caller = sys._getframe(1).f_code.co_name
    loader = FixtureLoader(path, caller)
    return loader.load(format)


class FixtureLoader(object):
    def __init__(self, path, caller):
        self._path = self._prepared_path(path, caller)

    def load(self, format="plain"):
        loader = self._select_loader(format)
        try:
            with open(self._path, "r") as fp:
                return loader(fp)
        except OSError as e:
            raise self._error(str(e))

    def _prepared_path(self, path, caller):
        if os.path.isabs(path):
            return self._path

        frame = util.find_frame(caller)
        module = inspect.getmodule(frame)
        workdir = os.path.dirname(os.path.realpath(module.__file__))

        return os.path.join(workdir, "fixtures", path)

    def _select_loader(self, format):
        loaders = {
            "plain": (lambda fp: fp.read()),
            "json": json.load
        }

        if YAML_AVAILABLE:
            loaders["yaml"] = yaml.load

        if format not in loaders.keys():
            raise AssertionError("Invalid format {}. Checkout the "
                                 "documentation for all formats supported "
                                 "by receives."
                                 .format(format))
        return loaders[format]

    def _error(self, msg):
        return AssertionError("Could not read fixture {}: {}"
                              .format(self._path, msg))
