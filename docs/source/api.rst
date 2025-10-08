=============
API reference
=============

Plotting functions
==================

Primary functions.

.. autofunction:: mplhep.histplot

.. autofunction:: mplhep.hist2dplot

.. autofunction:: mplhep.funcplot

.. # List all modules when appropriately privatized
   .. automodule:: mplhep.plot
      :members:


Text functions
========================

Functions to annotate figures in a convenient way. Typically ``append_text`` can be used to place an additional artist after ``add_text``.

.. autofunction:: mplhep.label.add_text

.. autofunction:: mplhep.label.append_text


Experiment label helpers
========================

Experiment specific helpers.

For the effects of the ``label`` method, see also the gallery examples in :ref:`gallery-labels`.


.. autofunction:: mplhep.cms.label

.. autofunction:: mplhep.cms.text

.. autofunction:: mplhep.atlas.label

.. autofunction:: mplhep.atlas.text

.. autofunction:: mplhep.lhcb.label

.. autofunction:: mplhep.lhcb.text

.. autofunction:: mplhep.alice.label

.. autofunction:: mplhep.alice.text

.. autofunction:: mplhep.dune.label

.. autofunction:: mplhep.dune.text


Axes helpers
============

Use all helpers together

.. autofunction:: mplhep.mpl_magic

or one by one.

.. autofunction:: mplhep.plot.ylow

.. autofunction:: mplhep.plot.yscale_legend

.. autofunction:: mplhep.plot.yscale_anchored_text


Figure helpers
==============

.. autofunction:: mplhep.append_axes

.. autofunction:: mplhep.box_aspect

.. autofunction:: mplhep.make_square_add_cbar

.. autofunction:: mplhep.rescale_to_axessize

Legend helpers
==============

.. autofunction:: mplhep.sort_legend()


Styles
==================

See the :ref:`gallery-styles` section for an overview of the available styles.
