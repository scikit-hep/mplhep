===========
Styles
===========

Comparison of different styles.

Group images
------------


.. jupyter-execute::
   :hide-code:
   :hide-output:

   import matplotlib.pyplot as plt
   import mplhep
   import numpy as np
   from pathlib import Path
   import yaml

   x = np.linspace(0, 10, 100)
   y = np.sin(x)



.. jupyter-execute::
   :hide-code:

   allstyle = [s for s in mplhep.style.__all__ if s != "use" and not s.lower().endswith("tex")]
   allstyle = sorted(allstyle, key=lambda s: s.lower())
   # allstyle = sorted(allstyle, key=lambda s: s.lower().endswith("tex"))
   allstyle = sorted(allstyle, key=lambda s: s.lower().endswith("alt"))
   here = Path.cwd()

   with open(here / 'source/_static/bkg_sig_plot.yaml') as f:
       plotdata = yaml.load(f, Loader=yaml.FullLoader)
   for i, style in enumerate(allstyle):
       try:
           plt.style.use(getattr(mplhep.style, style))
       except Exception as e:
            continue
       plot = plotdata.copy()
       x = plot.pop('x')
       data = plot.pop('Data')
       mplhep.histplot(data, histtype='errorbar', label='Data')
       for label, y in plot.items():
           plt.plot(x, y, label=label)
       plt.legend()
