# User Guide

This guide provides an overview of mplhep's core functionality and common usage patterns for creating publication-quality plots in high energy physics.

## Overview

mplhep is a matplotlib wrapper designed specifically for HEP plotting needs, providing:

- **Histogram plotting** - Functions for 1D and 2D pre-binned histograms with support for the [Unified Histogram Interface (UHI)](https://uhi.readthedocs.io/)
- **Experiment styles** - Official styles for ATLAS, CMS, LHCb, ALICE, and DUNE experiments
- **Comparison plotters** - High-level functions for data-model comparisons with ratio, pull, and difference panels
- **Label utilities** - Experiment-specific label formatters with automatic positioning


## Basic Usage

### Simple Histogram Plot

The primary plotting function is `histplot()`, which accepts various histogram formats. Here's how it looks with different experiment styles:

=== "CMS"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)

    # Apply CMS style
    mh.style.use('CMS')

    # Generate sample data and create histogram
    data = np.random.normal(0, 1, 1000)
    fig, ax = plt.subplots()
    mh.histplot(*np.histogram(data, bins=50), ax=ax, label='Data')

    # Add CMS label
    mh.cms.label('Preliminary', data=True, lumi=100, com=13)
    ax.legend()
    ```

=== "ATLAS"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)

    # Apply ATLAS style
    mh.style.use('ATLAS')

    # Generate sample data and create histogram
    data = np.random.normal(0, 1, 1000)
    fig, ax = plt.subplots()
    mh.histplot(*np.histogram(data, bins=50), ax=ax, label='Data')

    # Add ATLAS label
    mh.atlas.label('Internal', data=True, lumi=150, com=13)
    mh.mpl_magic(soft_fail=True)
    ax.legend()
    ```

=== "LHCb"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)

    # Apply LHCb style
    mh.style.use('LHCb2')

    # Generate sample data and create histogram
    data = np.random.normal(0, 1, 1000)
    fig, ax = plt.subplots()
    mh.histplot(*np.histogram(data, bins=50), ax=ax, label='Data')

    # Add LHCb label
    mh.lhcb.label('Preliminary', data=True, lumi=50, com=13)
    ax.legend()
    ```

=== "ALICE"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)

    # Apply ALICE style
    mh.style.use('ALICE')

    # Generate sample data and create histogram
    data = np.random.normal(0, 1, 1000)
    fig, ax = plt.subplots()
    mh.histplot(*np.histogram(data, bins=50), ax=ax, label='Data')

    # Add ALICE label
    mh.alice.label('Preliminary', data=True, lumi=100, com=13)
    mh.mpl_magic(soft_fail=True)
    ax.legend()
    ```

=== "DUNE"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)

    # Apply DUNE style
    mh.style.use('DUNE')

    # Generate sample data and create histogram
    data = np.random.normal(0, 1, 1000)
    fig, ax = plt.subplots()
    mh.histplot(*np.histogram(data, bins=50), ax=ax, label='Data')

    # Add DUNE label
    mh.dune.label('Preliminary', data=True, lumi=100, com=13)
    ax.legend()
    ```

=== "PLOTHIST"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)

    # Apply PLOTHIST style
    mh.style.use('PLOTHIST')

    # Generate sample data and create histogram
    data = np.random.normal(0, 1, 1000)
    fig, ax = plt.subplots()
    mh.histplot(*np.histogram(data, bins=50), ax=ax, label='Data')

    # Add PLOTHIST label
    txt_obj = mh.add_text('PLOTHIST', loc='over left')
    mh.append_text('Demo', txt_obj, loc='right', fontsize='x-small')
    ax.legend()
    ```


## Histogram Plotting

### Supported Input Formats

`histplot()` works with multiple histogram formats through the UHI protocol:

```python
# 1. Raw data array (will be binned)
mh.histplot(data, bins=50)

# 2. Pre-computed histogram (counts, bins)
counts, bins = np.histogram(data, bins=50)
mh.histplot(counts, bins=bins)

# 3. UHI-compatible objects (hist, uproot, boost_histogram)
import hist
h = hist.Hist(hist.axis.Regular(50, -3, 3))
h.fill(data)
mh.histplot(h)
```

### Multiple Histograms

Plot multiple histograms on the same axes:

```python
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(0.5, 1.2, 1000)

# Define bins once for consistent binning
bins = np.linspace(-4, 4, 50)
h1, _ = np.histogram(data1, bins=bins)
h2, _ = np.histogram(data2, bins=bins)

fig, ax = plt.subplots()
mh.histplot(
    [h1, h2],
    bins=bins,
    label=['Signal', 'Background'],
    ax=ax
)
ax.legend()
```

### Stacked Histograms

Create stacked histogram plots to show signal and background contributions:

=== "CMS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('CMS')

    # Generate signal and background data
    signal = np.random.normal(0, 1, 500)
    background = np.random.normal(0.5, 1.2, 800)
    bins = np.linspace(-4, 4, 30)
    h_sig, _ = np.histogram(signal, bins=bins)
    h_bkg, _ = np.histogram(background, bins=bins)

    # Create stacked histogram
    fig, ax = plt.subplots()
    mh.histplot(
        [h_sig, h_bkg],
        bins=bins,
        stack=True,
        label=['Signal', 'Background'],
        ax=ax
    )
    mh.cms.label(data=False)
    ax.legend()
    ax.set_xlabel('Observable')
    ax.set_ylabel('Events')
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

    # Generate signal and background data
    signal = np.random.normal(0, 1, 500)
    background = np.random.normal(0.5, 1.2, 800)
    bins = np.linspace(-4, 4, 30)
    h_sig, _ = np.histogram(signal, bins=bins)
    h_bkg, _ = np.histogram(background, bins=bins)

    # Create stacked histogram
    fig, ax = plt.subplots()
    mh.histplot(
        [h_sig, h_bkg],
        bins=bins,
        stack=True,
        label=['Signal', 'Background'],
        ax=ax
    )
    mh.atlas.label(data=False)
    mh.mpl_magic(soft_fail=True)
    ax.legend()
    ax.set_xlabel('Observable')
    ax.set_ylabel('Events')
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

    # Generate signal and background data
    signal = np.random.normal(0, 1, 500)
    background = np.random.normal(0.5, 1.2, 800)
    bins = np.linspace(-4, 4, 30)
    h_sig, _ = np.histogram(signal, bins=bins)
    h_bkg, _ = np.histogram(background, bins=bins)

    # Create stacked histogram
    fig, ax = plt.subplots()
    mh.histplot(
        [h_sig, h_bkg],
        bins=bins,
        stack=True,
        label=['Signal', 'Background'],
        ax=ax
    )
    mh.lhcb.label(data=False)
    ax.legend()
    ax.set_xlabel('Observable')
    ax.set_ylabel('Events')
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

    # Generate signal and background data
    signal = np.random.normal(0, 1, 500)
    background = np.random.normal(0.5, 1.2, 800)
    bins = np.linspace(-4, 4, 30)
    h_sig, _ = np.histogram(signal, bins=bins)
    h_bkg, _ = np.histogram(background, bins=bins)

    # Create stacked histogram
    fig, ax = plt.subplots()
    mh.histplot(
        [h_sig, h_bkg],
        bins=bins,
        stack=True,
        label=['Signal', 'Background'],
        ax=ax
    )
    mh.alice.label(data=False)
    mh.mpl_magic(soft_fail=True)
    ax.legend()
    ax.set_xlabel('Observable')
    ax.set_ylabel('Events')
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

    # Generate signal and background data
    signal = np.random.normal(0, 1, 500)
    background = np.random.normal(0.5, 1.2, 800)
    bins = np.linspace(-4, 4, 30)
    h_sig, _ = np.histogram(signal, bins=bins)
    h_bkg, _ = np.histogram(background, bins=bins)

    # Create stacked histogram
    fig, ax = plt.subplots()
    mh.histplot(
        [h_sig, h_bkg],
        bins=bins,
        stack=True,
        label=['Signal', 'Background'],
        ax=ax
    )
    mh.dune.label(data=False)
    ax.legend()
    ax.set_xlabel('Observable')
    ax.set_ylabel('Events')
    ```

=== "PLOTHIST"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('PLOTHIST')

    # Generate signal and background data
    signal = np.random.normal(0, 1, 500)
    background = np.random.normal(0.5, 1.2, 800)
    bins = np.linspace(-4, 4, 30)
    h_sig, _ = np.histogram(signal, bins=bins)
    h_bkg, _ = np.histogram(background, bins=bins)

    # Create stacked histogram
    fig, ax = plt.subplots()
    mh.histplot(
        [h_sig, h_bkg],
        bins=bins,
        stack=True,
        label=['Signal', 'Background'],
        ax=ax
    )
    txt_obj = mh.add_text('PLOTHIST', loc='over left')
    mh.append_text('Stacked', txt_obj, loc='right', fontsize='x-small')
    ax.legend()
    ax.set_xlabel('Observable')
    ax.set_ylabel('Events')
    ```

### Histogram Styles

Control the appearance with the `histtype` parameter. Select an experiment style and then choose a histogram type:

=== "CMS"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('CMS')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='step', label='Step histogram', ax=ax)
        mh.cms.label(data=False)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('CMS')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        mh.cms.label(data=False)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('CMS')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='errorbar', yerr=True, label='Data', ax=ax)
        mh.cms.label(data=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

=== "ATLAS"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('ATLAS')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='step', label='Step histogram', ax=ax)
        mh.atlas.label(data=False)
        mh.mpl_magic(soft_fail=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('ATLAS')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        mh.atlas.label(data=False)
        mh.mpl_magic(soft_fail=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('ATLAS')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='errorbar', yerr=True, label='Data', ax=ax)
        mh.atlas.label(data=True)
        mh.mpl_magic(soft_fail=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

=== "LHCb"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('LHCb2')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='step', label='Step histogram', ax=ax)
        mh.lhcb.label(data=False)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('LHCb2')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        mh.lhcb.label(data=False)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('LHCb2')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='errorbar', yerr=True, label='Data', ax=ax)
        mh.lhcb.label(data=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

=== "ALICE"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('ALICE')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='step', label='Step histogram', ax=ax)
        mh.alice.label(data=False)
        mh.mpl_magic(soft_fail=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('ALICE')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        mh.alice.label(data=False)
        mh.mpl_magic(soft_fail=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('ALICE')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='errorbar', yerr=True, label='Data', ax=ax)
        mh.alice.label(data=True)
        mh.mpl_magic(soft_fail=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

=== "DUNE"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('DUNE')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='step', label='Step histogram', ax=ax)
        mh.dune.label(data=False)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('DUNE')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        mh.dune.label(data=False)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('DUNE')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='errorbar', yerr=True, label='Data', ax=ax)
        mh.dune.label(data=True)
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

=== "PLOTHIST"

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('PLOTHIST')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='step', label='Step histogram', ax=ax)
        txt_obj = mh.add_text('PLOTHIST', loc='over left')
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Fill"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('PLOTHIST')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='fill', alpha=0.5, label='Filled histogram', ax=ax)
        txt_obj = mh.add_text('PLOTHIST', loc='over left')
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

    === "Errorbar"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt
        import mplhep as mh
        import numpy as np
        np.random.seed(42)
        mh.style.use('PLOTHIST')

        data = np.random.normal(0, 1, 1000)
        fig, ax = plt.subplots()
        mh.histplot(*np.histogram(data, bins=40), histtype='errorbar', yerr=True, label='Data', ax=ax)
        txt_obj = mh.add_text('PLOTHIST', loc='over left')
        ax.legend()
        ax.set_xlabel('Observable')
        ax.set_ylabel('Events')
        ```

### Error Bars

Add statistical uncertainties:

```python
# Automatic Poisson errors
mh.histplot(h, bins, yerr=True)

# Custom errors
errors = np.sqrt(h)  # Or your own error calculation
mh.histplot(h, bins, yerr=errors)
```

### Density Normalization

Normalize histograms to unit area:

```python
mh.histplot([h1, h2], bins=bins, density=True, label=['Data', 'MC'])
```

## 2D Histograms

Use `hist2dplot()` for 2D histogram visualization:

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
    mh.cms.label(data=False)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
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
    mh.atlas.label(data=False)
    mh.mpl_magic(soft_fail=True)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
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
    mh.lhcb.label(data=False)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
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
    mh.alice.label(data=False)
    mh.mpl_magic(soft_fail=True)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
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
    mh.dune.label(data=False)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ```

=== "PLOTHIST"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('PLOTHIST')

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    txt_obj = mh.add_text('PLOTHIST', loc='upper left')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ```

## Data-Model Comparisons

### Using Comparison Functions

mplhep provides dedicated comparison plotters in the `comp` module for creating plots with ratio, pull, or difference panels. Use `mh.comp.hists()` to compare two histograms:

=== "CMS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('CMS')

    # Generate sample data and model
    data_vals = np.random.normal(0, 1, 1000)
    model_vals = np.random.normal(0, 1.05, 1000)
    bins = np.linspace(-4, 4, 25)
    data_hist = np.histogram(data_vals, bins=bins)
    model_hist = np.histogram(model_vals, bins=bins)

    # Create comparison plot with ratio panel
    fig, ax_main, ax_comp = mh.comp.hists(
        data_hist,
        model_hist,
        comparison='ratio',
        xlabel='Observable [GeV]',
        ylabel='Events',
        h1_label='Data',
        h2_label='Model'
    )
    mh.cms.label(data=True, ax=ax_main)
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

    # Generate sample data and model
    data_vals = np.random.normal(0, 1, 1000)
    model_vals = np.random.normal(0, 1.05, 1000)
    bins = np.linspace(-4, 4, 25)
    data_hist = np.histogram(data_vals, bins=bins)
    model_hist = np.histogram(model_vals, bins=bins)

    # Create comparison plot with ratio panel
    fig, ax_main, ax_comp = mh.comp.hists(
        data_hist,
        model_hist,
        comparison='ratio',
        xlabel='Observable [GeV]',
        ylabel='Events',
        h1_label='Data',
        h2_label='Model'
    )
    mh.atlas.label(data=True, ax=ax_main)
    mh.mpl_magic(soft_fail=True)
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

    # Generate sample data and model
    data_vals = np.random.normal(0, 1, 1000)
    model_vals = np.random.normal(0, 1.05, 1000)
    bins = np.linspace(-4, 4, 25)
    data_hist = np.histogram(data_vals, bins=bins)
    model_hist = np.histogram(model_vals, bins=bins)

    # Create comparison plot with ratio panel
    fig, ax_main, ax_comp = mh.comp.hists(
        data_hist,
        model_hist,
        comparison='ratio',
        xlabel='Observable [GeV]',
        ylabel='Events',
        h1_label='Data',
        h2_label='Model'
    )
    mh.lhcb.label(data=True, ax=ax_main)
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

    # Generate sample data and model
    data_vals = np.random.normal(0, 1, 1000)
    model_vals = np.random.normal(0, 1.05, 1000)
    bins = np.linspace(-4, 4, 25)
    data_hist = np.histogram(data_vals, bins=bins)
    model_hist = np.histogram(model_vals, bins=bins)

    # Create comparison plot with ratio panel
    fig, ax_main, ax_comp = mh.comp.hists(
        data_hist,
        model_hist,
        comparison='ratio',
        xlabel='Observable [GeV]',
        ylabel='Events',
        h1_label='Data',
        h2_label='Model'
    )
    mh.alice.label(data=True, ax=ax_main)
    mh.mpl_magic(soft_fail=True)
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

    # Generate sample data and model
    data_vals = np.random.normal(0, 1, 1000)
    model_vals = np.random.normal(0, 1.05, 1000)
    bins = np.linspace(-4, 4, 25)
    data_hist = np.histogram(data_vals, bins=bins)
    model_hist = np.histogram(model_vals, bins=bins)

    # Create comparison plot with ratio panel
    fig, ax_main, ax_comp = mh.comp.hists(
        data_hist,
        model_hist,
        comparison='ratio',
        xlabel='Observable [GeV]',
        ylabel='Events',
        h1_label='Data',
        h2_label='Model'
    )
    mh.dune.label(data=True, ax=ax_main)
    ```

=== "PLOTHIST"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('PLOTHIST')

    # Generate sample data and model
    data_vals = np.random.normal(0, 1, 1000)
    model_vals = np.random.normal(0, 1.05, 1000)
    bins = np.linspace(-4, 4, 25)
    data_hist = np.histogram(data_vals, bins=bins)
    model_hist = np.histogram(model_vals, bins=bins)

    # Create comparison plot with ratio panel
    fig, ax_main, ax_comp = mh.comp.hists(
        data_hist,
        model_hist,
        comparison='ratio',
        xlabel='Observable [GeV]',
        ylabel='Events',
        h1_label='Data',
        h2_label='Model'
    )
    txt_obj = mh.add_text('PLOTHIST', loc='over left', ax=ax_main)
    ```

### Available Comparison Types

The `comparison` parameter accepts:

- `'ratio'` - Data/Model ratio
- `'pull'` - (Data - Model) / uncertainty
- `'difference'` - Data - Model
- `'relative_difference'` - (Data - Model) / Model
- `'asymmetry'` - (Data - Model) / (Data + Model)
- `'efficiency'` - Data / Model as efficiency plot
- `'split_ratio'` - Separate upper/lower ratio panels

### Data-Model with Stacked Backgrounds

For complex data-model comparisons with multiple background components, use `mh.comp.data_model()`:

```python
# Generate signal, backgrounds, and data
bins = np.linspace(-3, 3, 15)
signal = np.histogram(np.random.normal(-0.5, 0.5, 300), bins=bins)
bkg1 = np.histogram(np.random.normal(0, 1, 800), bins=bins)
bkg2 = np.histogram(np.random.exponential(0.5, 400) - 1.5, bins=bins)
# Data is sum with Poisson fluctuations
data_counts = np.random.poisson(signal[0] + bkg1[0] + bkg2[0])
data = (data_counts, bins)

# Create comparison plot
fig, ax_main, ax_comp = mh.comp.data_model(
    data_hist=data,
    stacked_components=[signal, bkg1, bkg2],
    stacked_labels=['Signal', 'Bkg 1', 'Bkg 2'],
    comparison='ratio',
    xlabel='m [GeV]',
    ylabel='Events'
)
mh.cms.label(data=True, lumi=100, ax=ax_main)
```

<!-- Interactive examples commented out due to y-label fitting issues in mkdocs rendering
=== "CMS"

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    mh.style.use('CMS')

    # Generate signal, backgrounds, and data
    bins = np.linspace(-3, 3, 15)
    signal = np.histogram(np.random.normal(-0.5, 0.5, 300), bins=bins)
    bkg1 = np.histogram(np.random.normal(0, 1, 800), bins=bins)
    bkg2 = np.histogram(np.random.exponential(0.5, 400) - 1.5, bins=bins)
    # Data is sum with Poisson fluctuations
    data_counts = np.random.poisson(signal[0] + bkg1[0] + bkg2[0])
    data = (data_counts, bins)

    # Create comparison plot
    fig, ax_main, ax_comp = mh.comp.data_model(
        data_hist=data,
        stacked_components=[signal, bkg1, bkg2],
        stacked_labels=['Signal', 'Bkg 1', 'Bkg 2'],
        comparison='ratio',
        xlabel='m [GeV]',
        ylabel='Events'
    )
    mh.cms.label(data=True, lumi=100, ax=ax_main)
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

    # Generate signal, backgrounds, and data
    bins = np.linspace(-3, 3, 15)
    signal = np.histogram(np.random.normal(-0.5, 0.5, 300), bins=bins)
    bkg1 = np.histogram(np.random.normal(0, 1, 800), bins=bins)
    bkg2 = np.histogram(np.random.exponential(0.5, 400) - 1.5, bins=bins)
    # Data is sum with Poisson fluctuations
    data_counts = np.random.poisson(signal[0] + bkg1[0] + bkg2[0])
    data = (data_counts, bins)

    # Create comparison plot
    fig, ax_main, ax_comp = mh.comp.data_model(
        data_hist=data,
        stacked_components=[signal, bkg1, bkg2],
        stacked_labels=['Signal', 'Bkg 1', 'Bkg 2'],
        comparison='ratio',
        xlabel='m [GeV]',
        ylabel='Events'
    )
    mh.atlas.label(data=True, lumi=150, ax=ax_main)
    mh.mpl_magic(soft_fail=True)
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

    # Generate signal, backgrounds, and data
    bins = np.linspace(-3, 3, 15)
    signal = np.histogram(np.random.normal(-0.5, 0.5, 300), bins=bins)
    bkg1 = np.histogram(np.random.normal(0, 1, 800), bins=bins)
    bkg2 = np.histogram(np.random.exponential(0.5, 400) - 1.5, bins=bins)
    # Data is sum with Poisson fluctuations
    data_counts = np.random.poisson(signal[0] + bkg1[0] + bkg2[0])
    data = (data_counts, bins)

    # Create comparison plot
    fig, ax_main, ax_comp = mh.comp.data_model(
        data_hist=data,
        stacked_components=[signal, bkg1, bkg2],
        stacked_labels=['Signal', 'Bkg 1', 'Bkg 2'],
        comparison='ratio',
        xlabel='m [GeV]',
        ylabel='Events'
    )
    mh.lhcb.label(data=True, lumi=50, ax=ax_main)
    ```
-->

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
