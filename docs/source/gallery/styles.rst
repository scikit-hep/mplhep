.. _gallery-styles:


Styles
===========

This page provides a gallery of available styles in mplhep. The styles are
sorted by the experiments they are associated with.

Styles can be used by calling :py:func:`mplhep.style.use(style)` with ``style``
on of the available styles in :py:mod:`mplhep.style`. In this gallery, only the most used
and actively maintained styles are shown.

The following plots are generated using :py:func:`~mplhep.histplot` and :py:func:`plt.plot(...)`
to plot the fit of a Gaussian distribution (for the signal peak) and an exponential
distribution (for the background) on top of a histogram.

All plots have additionally a legend, axis labels, and a title as well as

 - the text "Preliminary" at position 0 (see :ref:`gallery-labels` for more positions), using the experiment specific function if available (or none otherwise),
 - the year 2016
 - a luminosity of 9 :math:`fb^{-1}`
 - ``data=True`` to show that it's not simulation

to illustrate the visual appearance of the styles.

ATLAS
------------

ATLAS has two styles, the default one and the alternative one.


.. image:: ../../_static/_generated/ATLAS/fill/pos0.png
   :width: 45%

.. image:: ../../_static/_generated/ATLAS/step/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/ATLAS/errorbar/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/ATLAS/band/pos0.png
    :width: 45%

ATLAS alternative, named ``ATLASAlt``

.. image:: ../../_static/_generated/ATLASAlt/fill/pos0.png
   :width: 45%

.. image:: ../../_static/_generated/ATLASAlt/step/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/ATLASAlt/errorbar/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/ATLASAlt/band/pos0.png
    :width: 45%

CMS
------------

.. image:: ../../_static/_generated/CMS/fill/pos0.png
   :width: 45%

.. image:: ../../_static/_generated/CMS/step/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/CMS/errorbar/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/CMS/band/pos0.png
    :width: 45%

LHCb
------------

LHCb has two styles, the older one, :py:obj:`~mplhep.style.LHCb1`, and the newer one,
:py:obj:`~mplhep.style.LHCb2`.


LHCb1 style (old)

.. image:: ../../_static/_generated/LHCb1/fill/pos0.png
   :width: 45%

.. image:: ../../_static/_generated/LHCb1/step/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/LHCb1/errorbar/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/LHCb1/band/pos0.png
    :width: 45%

LHCb2 style

.. image:: ../../_static/_generated/LHCb2/fill/pos0.png
   :width: 45%

.. image:: ../../_static/_generated/LHCb2/step/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/LHCb2/errorbar/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/LHCb2/band/pos0.png
    :width: 45%


ALICE
------------

ALICE style

.. image:: ../../_static/_generated/ALICE/fill/pos0.png
   :width: 45%

.. image:: ../../_static/_generated/ALICE/step/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/ALICE/errorbar/pos0.png
    :width: 45%

.. image:: ../../_static/_generated/ALICE/band/pos0.png
    :width: 45%
