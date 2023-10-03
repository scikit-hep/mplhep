===========
Styles
===========

Comparison of different styles.

.. jupyter-execute::
   :hide-code:
   :hide-output:

   import matplotlib.pyplot as plt
   import mplhep
   x = np.linspace(0, 10, 100)
   y = np.sin(x)

CMS style

.. jupyter-execute::

   plt.style.use(mplhep.style.CMS)
   plt.plot(x, y)

ATLAS style

.. jupyter-execute::

   plt.style.use(mplhep.style.ATLAS)
   plt.plot(x, y)

LHCb1 style

.. jupyter-execute::

   plt.style.use(mplhep.style.LHCb1)
   plt.plot(x, y)

LHCb2 style

.. jupyter-execute::

   plt.style.use(mplhep.style.LHCb2)
   plt.plot(x, y)

ALICE style

.. jupyter-execute::

   plt.style.use(mplhep.style.ALICE)
   plt.plot(x, y)
