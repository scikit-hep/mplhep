from __future__ import annotations

import sys
from typing import Any, Callable, TypeVar

if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeAlias
else:
    from typing_extensions import ParamSpec, TypeAlias

T = TypeVar("T")
P = ParamSpec("P")
WrappedFuncDeco: TypeAlias = Callable[[Callable[..., Any]], Callable[..., Any]]


def copy_doc(
    copy_func: Callable[..., Any],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Copies the doc string of the given function to another.
    This function is intended to be used as a decorator.

    .. code-block:: python3

        def foo():
            '''This is a foo doc string'''
            ...

        @copy_doc(foo)
        def bar():
            ...
    """

    def wrapped(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__doc__ = copy_func.__doc__
        return func

    return wrapped


class DocstringCopier:
    """A docstring copying mechanism that works with both Sphinx and MkDocs."""

    def copy(self, source_func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator to copy docstring from source function to target function."""

        def decorator(target_func: Callable[..., Any]) -> Callable[..., Any]:
            # Copy the docstring at decoration time
            target_func.__doc__ = source_func.__doc__
            return target_func

        return decorator


def filter_deprecated(obj):
    """Filter out objects that have __deprecated__ attribute set to True.

    This function is used by MkDocs to automatically exclude deprecated functions
    from the API documentation.
    """
    return not getattr(obj, "__deprecated__", False)


# Create a singleton instance for backward compatibility
docstring = DocstringCopier()

__all__ = ("docstring", "copy_doc", "filter_deprecated")
