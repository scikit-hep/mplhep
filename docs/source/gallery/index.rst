===========
Gallery
===========

.. toctree::
   :maxdepth: 2

   styles
   labels

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

    # allstyle = [s for s in mplhep.style.__all__
    #             if s != "use" and not s.lower().endswith("tex")
    #             and "_" not in s
    #             and s != "LHCb"  # we want LHCb1 or LHCb2
    #     ]
    # the upper one contains all possible styles, needed?
    allstyle = ["ATLAS", "ATLASAlt", "CMS", "LHCb1", "LHCb2", "ALICE"]
    allstyle = sorted(allstyle, key=lambda s: s.lower())
    # allstyle = sorted(allstyle, key=lambda s: s.lower().endswith("tex"))
    allstyle = sorted(allstyle, key=lambda s: s.lower().endswith("alt"))
    here = Path("__file__").parent.resolve()  # jupyter workaround, use string


    with Path(here / '_static/bkg_sig_plot.yaml').resolve().open() as f:
       plotdata = yaml.load(f, Loader=yaml.FullLoader)
    for i, style in enumerate(allstyle):
        plt.style.use(getattr(mplhep.style, style))

        plot = plotdata.copy()
        x = np.asarray(plot.pop('x'))
        data = tuple(plot.pop('Data'))
        for i, histtype in enumerate(['fill', 'step', 'errorbar', 'band']):
            for position in range(5):
                plt.figure()
                ax = plt.gca()
                title = f"{style} {histtype}"
                ax.set_title(title, y=1.02)
                mplhep.histplot(data, histtype=histtype, label='Data', ax=ax)
                for label, y in plot.items():
                   ax.plot(x, np.asarray(y), label=label)

                kwargs = dict(label="Preliminary", data=True, ax=ax, year=2016, loc=position, lumi=9)
                if "atlas" in style.lower():
                    mplhep.atlas.label(**kwargs)
                elif "cms" in style.lower():
                    mplhep.cms.label(**kwargs)
                elif "lhcb" in style.lower():
                    mplhep.lhcb.label(**kwargs)
                ax.legend()
                ax.set_xlabel('$m_{\mu\mu}$ [GeV]')
                ax.set_ylabel('Events')
                path = Path(f"_static/_generated/{style}/{histtype}/pos{position}.png")
                path.parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(path)
                plt.close()
