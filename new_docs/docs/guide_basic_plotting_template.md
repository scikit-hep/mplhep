# Basic Plotting

This section covers the core plotting functionality of mplhep for plotting 1D and 2D histograms.

??? tip "Prerequisites"
    Throughout this guide the following codeblock is assumed.
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    import hist
    np.random.seed(42)
    import mplhep as mh
    # mh.style.use('<as appropriate>')
    ```


## 1D Histogram Plotting

[`mh.histplot()`][mplhep.histplot] works with multiple histogram formats through the UHI protocol:

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
        # If only one histogram is provided, it will be treated as "fill" histtype, if multiple data are given the bars are arranged side by side (see next section)
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
        # If one histogram is provided, it will be treated as "step" histtype. If multiple data are given the bars are arranged side by side (see next section)
        ```

{{TABS_END}}


### Multiple Histograms

#### Stack

[`mh.histplot()`][mplhep.histplot] supports plotting multiple histograms in one call. They can be stacked using the `stack=True` parameter:

{{TABS_START}}
{{TAB_HEADER}}

    === "Unstacked fill"

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
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            alpha=0.7,
            label=['Background 1', 'Background 2', 'Signal'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```


    === "Stacked fill"

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
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            label=['Background 1', 'Background 2', 'Signal'],
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
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='yield',
            label=['Background 1', 'Background 2', 'Signal'],
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
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='label',
            label=['Background 1', 'Background 2', 'Signal'],
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
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='fill',
            stack=True,
            sort='l_r',
            label=['Background 1', 'Background 2', 'Signal'],
            ax=ax
        )
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

    === "With errorbars"

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
        h2 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(2, 0.6, 600))
        h3 = hist.new.Reg(40, -4, 4).Weight().fill(np.random.normal(0.5, 1.2, 1200))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            stack=True,
            label=['Background 1', 'Background 2', 'Signal'],
            ax=ax
        )
        {{LABEL_CODE_NODATA}}{{MAGIC_CODE_INLINE_NESTED}}
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        ```

{{TABS_END}}

#### Side by Side

When plotting multiple histograms, the `histtype` can be set to `'bar'` or `'barstep'` to create side-by-side bar plots, just like `matplotlib`:

{{TABS_START}}
{{TAB_HEADER}}

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
        # Create histograms and fill them
        h1 = hist.new.Reg(6, 0, 6).Weight().fill(np.random.poisson(0.5, 200))
        h2 = hist.new.Reg(6, 0, 6).Weight().fill(np.random.poisson(1.0, 300))
        h3 = hist.new.Reg(6, 0, 6).Weight().fill(np.random.poisson(1.2, 500))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='bar',
            label=['$h_1$', '$h_2$', '$h_3$'],
            ax=ax
        )
        {{LABEL_CODE_NODATA}}{{MAGIC_CODE_INLINE_NESTED}}
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        # Optional: move the x-ticks to the bin centers
        ax.set_xticks(h1.axes[0].centers)
        ax.set_xticklabels([x+0.5 for x in h1.axes[0].centers])
        ax.minorticks_off()
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
        # Create histograms and fill them
        h1 = hist.new.Reg(6, 0, 6).Weight().fill(np.random.poisson(0.5, 200))
        h2 = hist.new.Reg(6, 0, 6).Weight().fill(np.random.poisson(1.0, 300))
        h3 = hist.new.Reg(6, 0, 6).Weight().fill(np.random.poisson(1.2, 500))

        fig, ax = plt.subplots()
        mh.histplot(
            [h1, h2, h3],
            histtype='barstep',
            label=['$h_1$', '$h_2$', '$h_3$'],
            ax=ax
        )
        {{LABEL_CODE_NODATA}}{{MAGIC_CODE_INLINE_NESTED}}
        ax.legend(loc='upper right')
        mh.yscale_legend(soft_fail=True)
        # Optional: move the x-ticks to the bin centers
        ax.set_xticks(h1.axes[0].centers)
        ax.set_xticklabels([x+0.5 for x in h1.axes[0].centers])
        ax.minorticks_off()
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

Use [`mh.hist2dplot()`][mplhep.hist2dplot] for 2D histogram visualization:

{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt  # mkdocs: hide
    import mplhep as mh  # mkdocs: hide
    import numpy as np  # mkdocs: hide
    np.random.seed(42)  # mkdocs: hide
    {{STYLE_USE_CODE}}  # mkdocs: hide
    # Generate 2D data
    x = np.random.normal(0, 1, 5000)
    y = np.random.normal(0, 1, 5000)
    H, xedges, yedges = np.histogram2d(x, y, bins=30)

    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, ax=ax, cbar=True)
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ```

{{TABS_END}}
