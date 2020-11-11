import warnings


# Adapted from:
# https://github.com/scikit-hep/iminuit/blob/develop/iminuit/_deprecated.py
# https://github.com/matplotlib/matplotlib/blob/717d1fa3e51e8d397030882779244f8fa33caae9/lib/matplotlib/cbook/deprecation.py


class deprecate:
    """
    Decorator indicating that function is being deprecated.
    """

    def __init__(self, reason: str, warn_once: bool = True, warning=FutureWarning):
        self._already_warned = False
        self._warn_once = warn_once
        self._warning = warning
        self._reason = reason

    def __call__(self, func):
        def decorated_func(*args, **kwargs):
            if not (self._warn_once and self._already_warned):
                warnings.warn(
                    "``{0}`` is deprecated: {1}".format(func.__name__, self._reason),
                    category=self._warning,
                    stacklevel=2,
                )
                self._already_warned = True
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = "deprecated: " + self._reason
        return decorated_func


class deprecate_parameter:
    """
    Decorator indicating that parameter *name* is being deprecated.
    """

    def __init__(self, name, reason="", warn_once: bool = True, warning=FutureWarning):
        self._warning = warning
        self._already_warned = False
        self._warn_once = warn_once
        self._name = name
        self._reason = reason

    def __call__(self, func):
        def decorated_func(*args, **kwargs):
            if self._name in kwargs.keys():
                if not (self._warn_once and self._already_warned):
                    warnings.warn(
                        'kwarg "{0}" in function ``{1}`` is deprecated and may be removed in future versions: {2}'.format(
                            self._name, func.__name__, self._reason
                        ),
                        category=self._warning,
                        stacklevel=2,
                    )
                    self._already_warned = True
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = func.__doc__
        return decorated_func


_NoArgumentGiven = object()


class deprecated_dict(dict):
    """
    A dictionary that emits a deprecation warning. NOT a decorator!
    """

    __slots__ = (
        "message",
        "_already_warned",
        "_warn_once",
        "_warning",
    )  # no __dict__ - would be redundant

    def __init__(
        self,
        *args,
        message: str = None,
        warn_once: bool = True,
        warning=FutureWarning,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._warn_once = warn_once
        self._already_warned = False
        self._warning = warning
        if message is not None:
            self.message = message
        else:
            self.message = "This dict is deprecated, please use another one instead"

    def __getitem__(self, key):
        self._warn_deprecation()
        return super().__getitem__(key)

    def _warn_deprecation(self):
        if not (self._warn_once and self._already_warned):
            warnings.warn(self.message, category=self._warning, stacklevel=1)
            self._already_warned = True

    def __setitem__(self, key, value):
        self._warn_deprecation()
        super().__setitem__(key, value)

    def __delitem__(self, key):
        super().__delitem__(key)

    def __iter__(self):
        self._warn_deprecation()
        return super().__iter__()

    def __len__(self):
        return super().__len__()

    # Not included in the mapping
    def get(self, k, default=None):
        return super().get(k, default)

    def setdefault(self, k, default=None):
        self._warn_deprecation()
        return super().setdefault(k, default)

    def pop(self, k, default=_NoArgumentGiven):
        self._warn_deprecation()
        if default is _NoArgumentGiven:
            return super().pop(k)
        return super().pop(k, default)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def __contains__(self, k):
        self._warn_deprecation()
        return super().__contains__(k)

    def copy(self):  # don't delegate w/ super - dict.copy() -> dict
        return type(self)(self)

    @classmethod
    def fromkeys(cls, keys, v=None):
        return super().fromkeys(keys, v)

    def __repr__(self):
        return super().__repr__()
