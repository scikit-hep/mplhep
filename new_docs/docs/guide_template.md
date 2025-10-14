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

{{TABS_START}}
{{TAB_HEADER}}

    === "Array-Like"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
        from skhep_testdata import data_path  # mkdocs: hide
        uproot_file_name = data_path("uproot-hepdata-example.root")  # mkdocs: hide
        import uproot

        file = uproot.open(uproot_file_name)
        h_root = file['hpx']
        fig, ax = plt.subplots()
        mh.histplot(h_root, ax=ax)
        ```

{{TABS_END}}


### Histogram Styles

Control the appearance with the `histtype` parameter. Select an experiment style and then choose a histogram type:

{{TABS_START}}
{{TAB_HEADER}}

    === "Step"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
        h = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0, 1, 1000))
        fig, ax = plt.subplots()
        mh.histplot(h, histtype='barstep', label='Barstep histogram', ax=ax)
        # For more `mpl.hist`-like plots
        ```

{{TABS_END}}


### Multiple Histograms

Plot multiple histograms on the same axes with different stacking and sorting options:

{{TABS_START}}
{{TAB_HEADER}}

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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_NODATA}}{{MAGIC_CODE_INLINE_NESTED}}
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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

{{TABS_END}}


### Error Bars

Control error bar display with `yerr` and `w2method` parameters:

{{TABS_START}}
{{TAB_HEADER}}

    === "Automatic (Poisson)"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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

{{TABS_END}}

### Normalization Options

Control histogram normalization with `density` and `binwnorm` parameters:

{{TABS_START}}
{{TAB_HEADER}}

    === "Nominal"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{STYLE_USE_CODE}}  # mkdocs: hide
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

{{TABS_END}}

## 2D Histograms

Use `hist2dplot()` for 2D histogram visualization:

{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    {{STYLE_USE_CODE}}

    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Varaible 1')
    ax.set_ylabel('Variable 2')
    ```

{{TABS_END}}

# FIXME: This section is under development

## Data-Model Comparisons

### Using Comparison Functions

mplhep provides dedicated comparison plotters in the `comp` module for creating plots with ratio, pull, or difference panels. Use `mh.comp.hists()` to compare two histograms:

{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    {{STYLE_USE_CODE}}

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
    {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE}}
    ```

{{TABS_END}}

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
fig, (ax_main, ax_comp) = plt.subplots(
    nrows=2,
    figsize=(10, 10),
    gridspec_kw={"height_ratios": [3, 1]},
)
fig.subplots_adjust(hspace=0)
fig, ax_main, ax_comp = mh.comp.data_model(
    fig = fig, ax_main=ax_main, ax_comparison=ax_comp,
    data_hist=data,
    stacked_components=[signal, bkg1, bkg2],
    stacked_labels=['Signal', 'Bkg 1', 'Bkg 2'],
    comparison='ratio',
    xlabel='m [GeV]',
    ylabel='Events'
)
mh.cms.label(data=True, lumi=100, ax=ax_main)
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
