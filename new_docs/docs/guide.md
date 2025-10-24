# User Guide

This guide provides an overview of mplhep's core functionality and common usage patterns for creating publication-quality plots in high energy physics.

## Overview

`mplhep` is a matplotlib wrapper designed specifically for HEP plotting needs, providing:

- **Experiment styles** - Official styles for ATLAS, CMS, LHCb, ALICE, and DUNE experiments
- **Histogram plotting** - Functions for 1D and 2D pre-binned histograms with support for the [Unified Histogram Interface (UHI)](https://uhi.readthedocs.io/)
    - Functions will take `*np.histogram()`, `hist.Hist`, or `ROOT.TH1` objects.
- **Comparison plotters** - High-level functions for data-model comparisons with ratio, pull, and difference panels
- **Label/plotting utilities** - Experiment-specific label formatters with automatic positioning

Throughout this guide the following codeblock is assumed.
```python
import matplotlib.pyplot as plt
import numpy as np
import hist
np.random.seed(42)
import mplhep as mh
# mh.style.use('<as appropriate>')
```


## Experiment styles

Please see our [Homepage](index.md) for a quick demo and for experiment labeling options see [Labels and Text](#labels-and-text)

## 1D Histogram Plotting

`mh.histplot()` works with multiple histogram formats through the UHI protocol:

### Supported Input Formats


=== "Default"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




=== "plothist"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




=== "CMS"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




=== "ATLAS"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




=== "LHCb"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




=== "ALICE"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




=== "DUNE"

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "`numpy.histogram`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), ax=ax)
        ```

    === "`hist.Hist`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        data = np.random.normal(0, 1, 1000)
        h_obj = hist.new.Reg(40, -4, 4).Weight().fill(data)
        fig, ax = plt.subplots()
        mh.histplot(h_obj, ax=ax)
        # Note that errorbars are now automatically plotted because hist.Hist inputs objects has .variances() available
        ```


    === "`uproot.TH1`"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```




### Histogram Styles

Control the appearance with the `histtype` parameter. Select an experiment style and then choose a histogram type:


=== "Default"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




=== "plothist"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




=== "CMS"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




=== "ATLAS"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




=== "LHCb"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




=== "ALICE"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




=== "DUNE"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='step', label='Step histogram', ax=ax)
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', label='Data', ax=ax)
        ```

    === "Band"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='band', alpha=0.5, label='Band histogram', ax=ax)
        # Can be used to visualize uncertainties
        ```

    === "Bar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='bar', label='Bar histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

    === "Barstep"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```




### Multiple Histograms

Plot multiple histograms on the same axes with different stacking and sorting options:


=== "Default"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )

        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "plothist"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        txt_obj = mh.add_text('plothist', loc='over left')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "CMS"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        mh.cms.label(data=False)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "ATLAS"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        mh.atlas.label(data=False)
        mh.mpl_magic(soft_fail=True)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "LHCb"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        mh.lhcb.label(data=False)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "ALICE"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        mh.alice.label(data=False)
        mh.mpl_magic(soft_fail=True)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "DUNE"

    === "Overlay (buggy lol)"
        FXIME: Keeping this here temporarily

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        mh.dune.label(data=False)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Overlay"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by yield)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Sorted (by label - reversed)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms and fill them
        h1 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(-1, 0.8, 800))
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            alpha=0.7,
            label=['Background 1', 'Signal', 'Background 2'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




### Error Bars

Control error bar display with `yerr` and `w2method` parameters:


=== "Default"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "plothist"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "CMS"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "ATLAS"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "LHCb"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "ALICE"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "DUNE"

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Simple histogram with Weight storage for automatic errors
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.poisson(5, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=True, label='Data with Poisson errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set explicitly"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Simple histogram with custom error bars
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))
        custom_errors = np.minimum(np.sqrt(h.values()), np.random.uniform(0, 20, 20))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', yerr=custom_errors, label='Data with custom errors', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation method (`'sqrt'`/`'poisson'`)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Weighted histogram - errors from sqrt of sum of weights squared
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method='sqrt', label='Weighted data (sqrt method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Set yerr calculation function - full control"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Weighted histogram with custom error calculation
        h = hist.new.Reg(20, 0, 20).Weight().fill(np.random.normal(10, 5, 2000))

        # Custom error function: error = sqrt(sum(weights^2)) / 2
        def custom_w2_method(weights, variances):
            import numpy as np  # mkdocs: hide
            up = weights - np.ones_like(weights) * 0.2 * np.mean(weights)
            down = weights + np.ones_like(weights) * 0.2 * np.mean(weights)
            return up, down

        fig, ax = plt.subplots()
        mh.histplot(h, histtype='errorbar', w2method=custom_w2_method, label='Weighted data (custom error method)', ax=ax)
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```



### Normalization Options

Control histogram normalization with `density` and `binwnorm` parameters:


=== "Default"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
          # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "plothist"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('plothist')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "CMS"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('CMS')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "ATLAS"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ATLAS')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "LHCb"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('LHCb2')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "ALICE"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('ALICE')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```




=== "DUNE"

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Density"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'density': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Density')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "Bin Width Normalized"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use('DUNE')  # mkdocs: hide
        # Create histograms with different binning schemes
        bins1 = np.r_[np.linspace(-4, 0, 30)[:-1], np.linspace(0, 4, 10)]  # Variable binning
        bins2 = np.linspace(-4, 4, 40)  #  Regular binning
        h1 = hist.new.Var(bins1).Weight().fill(np.random.normal(0, 1, 2000))
        h2 = hist.new.Var(bins2).Weight().fill(np.random.normal(0, 1, 2000))

        # Plot
        kwargs = {'binwnorm': True}
        fig, ax = plt.subplots()
        mh.histplot(h1, histtype='fill', alpha=0.7, label='Variable bins (same data)', ax=ax, **kwargs)
        mh.histplot(h2, histtype='fill', alpha=0.7, label='Regular bins (same data)', ax=ax, **kwargs)

        # Style
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events / Bin Width')
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```



## 2D Histograms

Use `hist2dplot()` for 2D histogram visualization:


=== "Default"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)


    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```




=== "plothist"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('plothist')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```




=== "CMS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('CMS')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```




=== "ATLAS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('ATLAS')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```




=== "LHCb"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('LHCb2')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```




=== "ALICE"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('ALICE')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```




=== "DUNE"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('DUNE')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```



## Comparisons

mplhep provides dedicated comparison plotters in the `comp` module for creating plots with different comparison panels. The following functions are available:

- `comp.hists()`: compare two histograms, plot the main plot and a comparison panel.
- `comp.data_model()`: compare a model made of histograms or functions to data, plot the main plot and a comparison panel.
- `comp.comparison()`: to only plot the comparison panel given two histograms.
- `comp.get_comparison()`: to get the `[values, lower_uncertainties, upper_uncertainties]` for a given comparison type.

### Two histograms

To compare two histograms, use `mh.comp.hists()`:

The `comparison` parameter accepts:

- `'ratio'`: $\frac{\text{h1}}{\text{h2}}$
- `'pull'`: $\frac{\text{h1} - \text{h2}}{\sqrt{\sigma_{\text{h1}}^2 + \sigma_{\text{h2}}^2}}$
- `'difference'`: $\text{h1} - \text{h2}$
- `'relative_difference'`: $\frac{\text{h1} - \text{h2}}{\text{h2}}$
- `'asymmetry'`: $\frac{\text{h1} - \text{h2}}{\text{h1} + \text{h2}}$
- `'efficiency'`: $\frac{\text{h1}}{\text{h2}}$ (with uncertainties from [eq.19 here](https://arxiv.org/pdf/physics/0701199v1))
- `'split_ratio'`: same as ratio, but the uncertainties of `h1` and `h2` are shown separately in the comparison panel (used extensively in data/model comparisons, see next section)



=== "Default"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)


        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )

        ```




=== "plothist"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```




=== "CMS"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.cms.label(data=True, ax=ax_main)
        ```




=== "ATLAS"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.atlas.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```




=== "LHCb"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.lhcb.label(data=True, ax=ax_main)
        ```




=== "ALICE"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.alice.label(data=True, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```




=== "DUNE"

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='split_ratio',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='pull',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='relative_difference',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x1 = np.random.normal(0, 1, 1000)
        x2 = np.random.normal(0, 1.05, 1000)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='asymmetry',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        import hist
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate sample data and model
        x2 = np.random.normal(0, 1, 1000)
        x1 = np.random.choice(x2, size=500, replace=False)
        h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1) # h1 needs to be a subset of h2
        h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.hists(
            h1,
            h2,
            comparison='efficiency',
            xlabel='Observable [GeV]',
            ylabel='Events',
            h1_label='h1',
            h2_label='h2'
        )
        mh.dune.label(data=True, ax=ax_main)
        ```





### Data-MC

To compare data to a model made of multiple components (e.g. signal, backgrounds...), use `mh.comp.data_model()`. The function is very flexible, it can accept any number of stacked and/or unstacked components, either as histograms or functions. It will then compare the sum of the components to the data, with the comparison of your choice. The default comparison is the `split_ratio` between the model and the data. It can take any comparison method available in `mh.comp.hists()`.



=== "Default"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)


        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )

        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)


        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )

        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)


        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )

        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)


        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )

        ```




=== "plothist"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)
        mh.style.use('plothist')

        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)
        mh.style.use('plothist')

        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```




=== "CMS"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)
        mh.style.use('CMS')

        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)
        mh.style.use('CMS')

        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```




=== "ATLAS"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```




=== "LHCb"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```




=== "ALICE"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)
        mh.style.use('ALICE')

        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)
        mh.style.use('ALICE')

        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```




=== "DUNE"

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # The function will automatically sum the stacked and unstacked components
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        import scipy
        np.random.seed(42)
        mh.style.use('DUNE')

        # Define component functions
        def f_signal(x):
            return 200 * scipy.stats.norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * scipy.stats.norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1, f_signal],
            stacked_labels=['Bkg 2', 'Bkg 1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        from scipy.stats import norm
        np.random.seed(42)
        mh.style.use('DUNE')

        # Define component functions
        def f_signal(x):
            return 200 * norm.pdf(x, loc=0.5, scale=3)
        def f_bkg1(x):
            return 500 * norm.pdf(x, loc=-1.5, scale=4)
        def f_bkg2(x):
            return 500 * norm.pdf(x, loc=-1., scale=1.8)

        # For mkdocs  # mkdocs: hide
        f_signal = lambda x: 200 * (1 / (3 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x - 0.5) / 3)**2))  # mkdocs: hide
        f_bkg1   = lambda x: 500 * (1 / (4 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.5) / 4)**2))  # mkdocs: hide
        f_bkg2   = lambda x: 500 * (1 / (1.8 * (2 * 3.14)**0.5)) * (2.71828 ** (-0.5 * ((x + 1.0) / 1.8)**2))  # mkdocs: hide
        # mkdocs: hide
        # Generate data histogram
        x_data = np.concatenate([np.random.normal(-1.5, 4, 1500), np.random.normal(-1., 1.8, 2000)])
        data_hist = hist.new.Regular(50, -8, 8).Weight().fill(x_data)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=data_hist,
            stacked_components=[f_bkg2, f_bkg1,],
            stacked_labels=['Bkg 2', 'Bkg 1'],
            unstacked_components=[f_signal],
            unstacked_labels=['Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```



### Showcasing more options

`mh.comp.hists()` is very flexible and can be customized further. For more examples and details, see the [API Reference](api.md#mplhep.comp.hists) and the [Gallery](gallery.md). Here is a selection of additional examples showcasing some of the available options.


=== "Default"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)


        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )

        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)


        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )

        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)


        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )

        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)


        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )

        ```




=== "plothist"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('plothist')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )
        txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
        ```




=== "CMS"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('CMS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )
        mh.cms.label(data=True, lumi=100, ax=ax_main)
        ```




=== "ATLAS"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ATLAS')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )
        mh.atlas.label(data=True, lumi=150, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```




=== "LHCb"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('LHCb2')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )
        mh.lhcb.label(data=True, lumi=50, ax=ax_main)
        ```




=== "ALICE"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('ALICE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )
        mh.alice.label(data=True, lumi=100, ax=ax_main)
        mh.mpl_magic(soft_fail=True)
        ```




=== "DUNE"

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            comparison='pull'  # Accept any comparison from mh.comp.comparison()
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            model_uncertainty=False,  # Set the model uncertainty to zero
            comparison='pull', # The pull formula is updated automatically
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comp = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1],
            stacked_labels=['Bkg2', 'Bkg1'],
            stacked_colors=['grey', 'lightblue'],
            unstacked_components=[h_signal],
            unstacked_labels=['Signal'],
            unstacked_colors=['red'],
            model_sum_kwargs={"show": True, "label": "Total Model", "color": "violet"}, # Just like stacked_components_kwargs and unstacked_components_kwargs, you can pass kwargs for the model sum line
            xlabel='Observable [GeV]',
            ylabel='Events'
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt
        import numpy as np
        import hist
        import mplhep as mh
        np.random.seed(42)
        mh.style.use('DUNE')

        # Generate signal, backgrounds, and data
        x1 = np.random.normal(0, 1, 1400)
        x2 = np.random.normal(1, 0.5, 1000)
        x3 = np.random.exponential(0.5, 900) - 1.5
        data_x = np.random.choice([*x1, *x2, *x3], size=3500, replace=True)
        h_bkg1 = hist.new.Reg(25, -3, 5).Weight().fill(x1)
        h_bkg2 = hist.new.Reg(25, -3, 5).Weight().fill(x2)
        h_signal = hist.new.Reg(25, -3, 5).Weight().fill(x3)
        h_data = hist.new.Reg(25, -3, 5).Weight().fill(data_x)

        # Create comparison plot
        fig, ax_main, ax_comparison = mh.comp.data_model(
            data_hist=h_data,
            stacked_components=[h_bkg2, h_bkg1, h_signal],
            stacked_labels=['Bkg2', 'Bkg1', 'Signal'],
            xlabel='Observable [GeV]',
            ylabel='Events',
            plot_only='ax_main'  # Only plot the comparison axis (works with 'ax_comparison' as well).
        )
        mh.dune.label(data=True, lumi=100, ax=ax_main)
        ```



### Additional examples

The functions are very flexible, here is some additional examples showcasing more options and use cases. For more details, see the [API Reference](api.md) and the [Gallery](gallery.md).


=== "Default"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)


    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide


    ```




=== "plothist"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)
    mh.style.use('plothist')

    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)
    ```




=== "CMS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)
    mh.style.use('CMS')

    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    mh.cms.label(data=True, ax=ax_main)
    ```




=== "ATLAS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)
    mh.style.use('ATLAS')

    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    mh.atlas.label(data=True, ax=ax_main)
    mh.mpl_magic(soft_fail=True)
    ```




=== "LHCb"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)
    mh.style.use('LHCb2')

    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    mh.lhcb.label(data=True, ax=ax_main)
    ```




=== "ALICE"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)
    mh.style.use('ALICE')

    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    mh.alice.label(data=True, ax=ax_main)
    mh.mpl_magic(soft_fail=True)
    ```




=== "DUNE"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np
    import hist
    import mplhep as mh
    np.random.seed(42)
    mh.style.use('DUNE')

    # Generate training and testing histograms for two classes
    x1_train = np.random.normal(0, 0.3, 2000)
    x1_test = np.random.normal(0, 0.3, 1000)
    x2_train = np.random.normal(1, 0.3, 2000)
    x2_test = np.random.normal(1, 0.3, 1000)
    h1_train = hist.new.Regular(30, 0, 1).Weight().fill(x1_train)
    h2_train = hist.new.Regular(30, 0, 1).Weight().fill(x2_train)
    h1_test = hist.new.Regular(30, 0, 1).Weight().fill(x1_test)
    h2_test = hist.new.Regular(30, 0, 1).Weight().fill(x2_test)

    # Since we have the histogram objects, we can normalize them directly
    h1_train /= h1_train.sum().value
    h2_train /= h2_train.sum().value
    h1_test /= h1_test.sum().value
    h2_test /= h2_test.sum().value

    # Using the wrapper around subplots
    fig, axes = mh.subplots(nrows=3)

    colors = ["C0", "C1"]
    labels = ["Bkg", "Signal"]

    # Plotting on the main axis
    for k_hist, h in enumerate([h1_train, h2_train, h1_test, h2_test]):
        color = colors[k_hist % 2]
        label = labels[k_hist % 2]
        yerr = False if k_hist < 2 else True # To make the plot less busy

        mh.histplot(
            h,
            color=color,
            label=label + (" $_{Train}$" if k_hist <2 else " $_{Test}$"),
            ax=axes[0],
            yerr=yerr,
            histtype="step" if k_hist < 2 else "errorbar",
        )

    # Plotting comparisons on the other axes
    mh.comp.comparison(
        h1_train,
        h1_test,
        ax=axes[1],
        comparison="ratio",
        h1_label="Train",
        h2_label="Test",
        color=colors[0],
    )

    mh.comp.comparison(
        h2_train,
        h2_test,
        ax=axes[2],
        comparison="pull",
        h1_label="Train",
        h2_label="Test",
        color=colors[1],
    )

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    mh.dune.label(data=True, ax=ax_main)
    ```



## Styling and Customization

### Applying Styles

Styles are applied globally using `mh.style.use()`:

```python
# Single style
mh.style.use('CMS')

# Multiple styles (later styles override earlier ones)
mh.style.use(['CMS', 'fira', 'firamath'])
```

!!! warning
    Due to matplotlib limitations, `plt.style.context()` does not work reliably with mplhep styles, especially for fonts. Use `mh.style.use()` globally instead.

### Customizing Plots

All mplhep plotting functions return matplotlib artist objects, allowing further customization:

```python
# histplot returns artists that can be modified
artists = mh.histplot(h, bins, label='Data')

# Modify the artists
for artist in artists:
    if hasattr(artist, 'set_linewidth'):
        artist.set_linewidth(2)
```

### Font Customization

Combine experiment styles with font styles:

```python
# Use CMS style with Fira fonts
mh.style.use(['CMS', 'fira', 'firamath'])

# Use ATLAS style with different fonts
mh.style.use(['ATLAS', 'sans-serif'])
```

## Labels and Text

### Experiment Labels

Each experiment has specific label formatting:

```python
# CMS label with common options
mh.cms.label(
    'Preliminary',      # Label text: 'Preliminary', 'Supplementary', 'Work in Progress'
    data=True,          # Include 'Data' if True, 'Simulation' if False
    lumi=100,           # Luminosity in fb^-1
    com=13,             # Center-of-mass energy in TeV
    ax=ax               # Axes (optional, uses current axes if not provided)
)

# ATLAS label
mh.atlas.label('Internal', data=True, lumi=150, com=13)

# Custom positioning
mh.cms.label('Preliminary', loc=0)  # Loc parameter for positioning
```

### Generic Text

For custom text placement:

```python
# Add text at specific location
txt = mh.add_text('Custom Text', loc='upper right')

# Append additional text
mh.append_text('Additional info', txt, loc='below')
```

## Working with UHI Histograms

mplhep fully supports the [Unified Histogram Interface](https://uhi.readthedocs.io/), making it compatible with modern histogram libraries:

```python
import hist
import boost_histogram as bh

# Using hist library
h = hist.Hist(hist.axis.Regular(50, -3, 3, name='x', label='Observable [GeV]'))
h.fill(data)
mh.histplot(h)  # Automatically uses axis labels

# Using boost_histogram
h_boost = bh.Histogram(bh.axis.Regular(50, -3, 3))
h_boost.fill(data)
mh.histplot(h_boost)

# From ROOT files via uproot
import uproot
file = uproot.open('data.root')
h_root = file['histogram_name']
mh.histplot(h_root)
```

## Examples and Gallery

For comprehensive examples of all plotting functions and comparison types, see the [Gallery](gallery.md).

Common example categories:

- [1D Histogram Comparisons](gallery.md#1d-histogram-comparisons) - Ratio, pull, difference, efficiency plots
- [Model Comparisons](gallery.md#model-comparisons) - Data-model comparisons with stacked backgrounds

## Best Practices

### Consistent Binning

When plotting multiple histograms together, ensure they share the same binning:

```python
# Define bins once
bins = np.linspace(-4, 4, 41)

# Use same bins for all histograms
h1 = np.histogram(data1, bins=bins)
h2 = np.histogram(data2, bins=bins)

mh.histplot([h1[0], h2[0]], bins=bins)
```

### Error Representation

Always show uncertainties for data:

```python
# For data points
mh.histplot(data_hist, bins=bins, yerr=True, histtype='errorbar', label='Data')

# For Monte Carlo, consider filled uncertainty bands
mh.histplot(mc_hist, bins=bins, histtype='fill', alpha=0.3, label='MC')
```

### Axis Labels with Units

Include units in axis labels following HEP conventions:

```python
ax.set_xlabel('Mass [GeV]')
ax.set_ylabel('Events / 5 GeV')  # Include bin width
```

### Using Legends

Place legends appropriately and use clear labels:

```python
mh.histplot([h1, h2], bins=bins, label=['Signal', 'Background'])
ax.legend(loc='upper right', frameon=False)
```

### Style Consistency

Apply styles at the beginning of your script, not in functions:

```python
# At the top of your script
import mplhep as mh
mh.style.use('CMS')

# Then create all plots
# ...
```

## Further Reading

- **[API Reference](api.md)** - Detailed documentation of all functions and parameters
- **[Gallery](gallery.md)** - Visual examples of all plot types
- **[Contributing](contributing.md)** - Information on development and testing
