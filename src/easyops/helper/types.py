import io
import sys

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

if PY3:
    unicode = str
    bytes = builtins.bytes
    file = io.IOBase
else:
    unicode = builtins.unicode
    bytes = str
    file = builtins.file
