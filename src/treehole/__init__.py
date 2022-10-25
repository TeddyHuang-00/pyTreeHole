"""
A simple interface to PKU Hole

快速上手：

```py
from treehole import TreeHoleClient

client = TreeHoleClient("your token")
hole, timestamp = client.get_hole("hole ID")
print(hole)
```

"""

try:
    from importlib.metadata import PackageNotFoundError, version  # novm
except ImportError:  # Fallback for Python < 3.8
    from importlib_metadata import PackageNotFoundError, version  # novm

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "TreeHole"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .client import *
from .models import *
