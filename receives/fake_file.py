import sys

# renamed in python 3
if sys.version_info.major < 3:
    from StringIO import StringIO
else:
    from io import StringIO


def fake_file(content):
    fake = StringIO()
    fake.write(content)
    return fake
