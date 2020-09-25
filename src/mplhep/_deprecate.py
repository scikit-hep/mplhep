import collections
import warnings

# Adapted from:
# https://github.com/scikit-hep/iminuit/blob/develop/iminuit/_deprecated.py
# https://github.com/matplotlib/matplotlib/blob/717d1fa3e51e8d397030882779244f8fa33caae9/lib/matplotlib/cbook/deprecation.py


class deprecate(object):
    """
    Decorator indicating that function is being deprecated.
    """

    def __init__(self, reason):
        self._reason = reason

    def __call__(self, func):
        def decorated_func(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(
                "``{0}`` is deprecated: {1}".format(func.__name__, self._reason),
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = "deprecated: " + self._reason
        return decorated_func


class deprecate_parameter(object):
    """
    Decorator indicating that parameter *name* is being deprecated.
    """

    def __init__(self, name, reason=""):
        self._name = name
        self._reason = reason

    def __call__(self, func):
        def decorated_func(*args, **kwargs):
            if self._name in kwargs.keys():
                warnings.simplefilter("always", DeprecationWarning)
                warnings.warn(
                    'kwarg "{0}" in function ``{1}`` is deprecated and may be removed in future versions: {2}'.format(
                        self._name, func.__name__, self._reason
                    ),
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = func.__doc__
        return decorated_func


class deprecated_dict(collections.abc.MutableMapping):
    """
    A dictionary that emits a deprecation warning. NOT a decorator!
    """

    def __init__(self, *args, **kwargs):
        self.store = dict()
        message = kwargs.pop("message")
        if message is not None:
            self.message = message
        else:
            self.message = "This dict is deprecated, please use another one instead"

    def __getitem__(self, key):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(self.message, category=DeprecationWarning, stacklevel=1)
        warnings.simplefilter("default", DeprecationWarning)
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(self.message, category=DeprecationWarning, stacklevel=1)
        warnings.simplefilter("default", DeprecationWarning)
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
