.. _installing-mplhep:

Install
=================

Quick start
-----------
If you are already familiar with python environment and have ran ``pip install mplhep``,
primary functionality can be accessed as follows:

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   import mplhep as hep

   # Load style sheet
   plt.style.use(hep.style.CMS)  # or ATLAS/LHCb2

   h, bins = np.histogram(np.random.random(1000))
   fig, ax = plt.subplots()
   hep.histplot(h, bins)

Will feature binder

..
  To try mplhep now, without installing anything, you can experiment with our
  `hosted tutorial notebooks <binder link>`_.

Platform support
----------------
mplhep is a python package distributed via `PyPI <https://pypi.org/project/mplhep>`_.
Python version 3.6 or newer is preferred, but a semi-maintained version of mplhep will run in python 2.7 or newer.

.. note:: Python 2 end-of-life is Jan. 1, 2020. All major scientific python packages will no longer provide support for python 2 by that date: https://python3statement.org/

All functional features in each supported python version are routinely tested.
You can see the python version you have installed by typing the following at the command prompt:

>>> python --version

or, in some cases, if both python 2 and 3 are available, you can find the python 3 version via:

>>> python3 --version

Install mplhep
--------------
To install mplhep you likely want to place it where your matplotlib installation is:

   - default ``pip install mplhep`` installs system-wide or whichever virtual environment is currently sourced
   - if you do not have administrator permissions, install as local user with ``pip install --user mplhep``
   - if you prefer to not place mplhep in your global environment, you can set up a `virtual environment <https://docs.python.org/3/library/venv.html>`_, and use the venv-provided pip
   - if you use `Conda <https://docs.conda.io/projects/conda/en/latest/index.html>`_,  simply activate the environment you wish to use and install via the conda-provided pip.
   - it will soon be possible to install from conda-forge ``conda install mplhep``

To update a previously installed mplhep to a newer version, use: ``pip install --upgrade mplhep``.
