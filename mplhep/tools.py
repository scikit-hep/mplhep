import os
import collections
import warnings

import matplotlib as mpl


# Backup options
def hardcopy_styles():
    path = os.path.abspath(__file__)
    pkg_dir = "/" + "/".join(path.split("/")[:-1])
    os.system('cp -r {}/stylelib/ '.format(pkg_dir) +
              os.path.join(mpl.get_configdir() + '/'))


def hardcopy_fonts():
    path = os.path.abspath(__file__)
    pkg_dir = "/" + "/".join(path.split("/")[:-1])
    os.system('cp -r {}/fonts/firasans/* '.format(pkg_dir) +
              os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
    os.system('cp -r {}/fonts/firamath/* '.format(pkg_dir) +
              os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
    os.system('cp -r {}/fonts/texgyreheros/* '.format(pkg_dir) +
              os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
    os.system('rm ' + os.path.join(mpl.get_cachedir() + '/font*'))


class DeprecDict(collections.abc.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        message = kwargs.pop('message')
        if message is not None:
            self.message = message
        else:
            self.message = "This dict is deprecated, please use another one instead"

    def __getitem__(self, key):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(self.message, category=DeprecationWarning, stacklevel=1)
        warnings.simplefilter('default', DeprecationWarning)
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(self.message, category=DeprecationWarning, stacklevel=1)
        warnings.simplefilter('default', DeprecationWarning)
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
