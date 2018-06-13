import inspect
import sys


def find_frame(caller):
    frameinfos = inspect.getouterframes(inspect.currentframe())
    try:
        for frameinfo in frameinfos:
            name, frame = extract_frame(frameinfo)
            if name == caller:
                return frame
        return None
    finally:
        del frameinfos


def extract_frame(frameinfo):
    if sys.version_info.major > 2 and sys.version_info.minor > 4:
        return (frameinfo.function, frameinfo.frame)
    return (frameinfo[3], frameinfo[0])
