from __future__ import annotations

import matplotlib
from packaging.version import parse as parse_version

if parse_version(matplotlib.__version__) < parse_version("3.8.0"):
    from matplotlib import docstring  # type: ignore[attr-defined]
else:
    from matplotlib import _docstring as docstring  # type: ignore[attr-defined]


__all__ = ("docstring",)
