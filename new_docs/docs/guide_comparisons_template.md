# Comparing histograms

mplhep provides dedicated comparison plotters in the `mh.comp` module for creating plots with different comparison panels. The following functions are available:

- [`mh.comp.hists()`][mplhep.comp.hists]: compare two histograms, plot the main plot and a comparison panel.
- [`mh.comp.data_model()`][mplhep.comp.data_model]: compare a model made of histograms or functions to data, plot the main plot and a comparison panel.
- [`mh.comp.comparison()`][mplhep.comp.comparison]: to only plot the comparison panel given two histograms.
- [`mh.comp.get_comparison()`][mplhep.comp.get_comparison]: to get the `[values, lower_uncertainties, upper_uncertainties]` for a given comparison type.

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

### Comparing two histograms

#### Available methods

To compare two histograms, use [`mh.comp.hists()`][mplhep.comp.hists]. This function takes two histograms as input and creates a figure with a main plot showing both histograms and a comparison panel below it.

The `comparison` parameter accepts:

- `ratio`: $\frac{\text{h1}}{\text{h2}}$
- `split_ratio`: same as ratio, but the uncertainties of `h1` and `h2` are shown separately in the comparison panel (used extensively in data/model comparisons, see [below](#data-mc))
- `pull`: $\frac{\text{h1} - \text{h2}}{\sqrt{\sigma_{\text{h1}}^2 + \sigma_{\text{h2}}^2}}$
- `difference`: $\text{h1} - \text{h2}$
- `relative_difference`: $\frac{\text{h1} - \text{h2}}{\text{h2}}$
- `asymmetry`: $\frac{\text{h1} - \text{h2}}{\text{h1} + \text{h2}}$
- `efficiency`: $\frac{\text{h1}}{\text{h2}}$ (with uncertainties from [eq.19 here](https://arxiv.org/pdf/physics/0701199v1))


{{TABS_START}}
{{TAB_HEADER}}

    === "Ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Split ratio"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Pull"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Relative difference"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Asymmetry"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Efficiency"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

{{TABS_END}}


#### Only plot the comparison panel

To only plot the comparison panel given two histograms, use [`mh.comp.comparison()`][mplhep.comp.comparison]. This function takes two histograms as input and creates a figure with only the comparison panel.


{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import matplotlib.pyplot as plt  # mkdocs: hide
    import mplhep as mh  # mkdocs: hide
    import numpy as np  # mkdocs: hide
    import hist  # mkdocs: hide
    np.random.seed(42)  # mkdocs: hide
    {{STYLE_USE_CODE}}  # mkdocs: hide
    # Generate sample data and model
    x1 = np.random.normal(0, 1, 1000)
    x2 = np.random.normal(0, 1.05, 1000)
    h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
    h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

    # Create comparison panel only
    fig, ax = plt.subplots()

    mh.comp.comparison(
        h1,
        h2,
        comparison='ratio',
        xlabel='Observable [GeV]',
        h1_label='h1',
        h2_label='h2',
        ax=ax
    )
    {{LABEL_CODE_LUMI_OPEN}}{{MAGIC_CODE_INLINE}}
    ```

{{TABS_END}}

To get the `[values, lower_uncertainties, upper_uncertainties]` for a given comparison type without plotting, use [`mh.comp.get_comparison()`][mplhep.comp.get_comparison]:

```python
values, lower_uncertainties, upper_uncertainties = mh.comp.get_comparison(
    h1,
    h2,
    comparison='ratio'
)
```


### Data-MC comparison

To compare data to a model made of multiple components (e.g. signal, backgrounds...), use [`mh.comp.data_model()`][mplhep.comp.data_model]. The function is very flexible, it can accept any number of stacked and/or unstacked components, either as histograms or functions. It will then compare the sum of the components to the data, with the comparison of your choice. The default comparison is the `split_ratio` between the model and the data. It can take any comparison method available in [`mh.comp.hists()`][mplhep.comp.hists].


{{TABS_START}}
{{TAB_HEADER}}

    === "Stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Functions, stacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import scipy  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Functions, mixed stacked and unstacked"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        from scipy.stats import norm  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

{{TABS_END}}

!!! tip
    To only plot the model, without data or comparison panel, use [`mh.model()`][mplhep.plot.model]. It takes the same arguments as [`mh.comp.data_model()`][mplhep.comp.data_model], except for the `data_hist` and `comparison` parameters.

#### Showcasing more options

[`mh.comp.data_model()`][mplhep.comp.data_model] is very flexible and can be customized further. For more examples and details, see the [API Reference](api.md#mplhep.comp.data_model) and the [Gallery](gallery.md). Here is a selection of additional examples showcasing some of the available options.

{{TABS_START}}
{{TAB_HEADER}}

    === "Different comparison"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Remove MC uncertainties"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Model kwargs"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

    === "Plot only 1 ax"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
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
        {{LABEL_CODE_LUMI}}{{MAGIC_CODE_INLINE_NESTED}}
        ```

{{TABS_END}}

### Additional examples

The functions are very flexible, here is some additional examples showcasing more options and use cases. For more details, see the [API Reference](api.md) and the [Gallery](gallery.md).

{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
        # mkdocs: align=left
    import numpy as np  # mkdocs: hide
    import hist  # mkdocs: hide
    import mplhep as mh  # mkdocs: hide
    np.random.seed(42)  # mkdocs: hide
    {{STYLE_USE_CODE}}  # mkdocs: hide
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

    for ax in axes:
        ax.set_xlim(0, 1)

    axes[0].set_ylabel("Normalized Entries")
    axes[0].legend()
    axes[1].set_ylabel("Ratio")
    axes[2].set_ylabel("Pull")
    axes[-1].set_xlabel("Feature")

    fig.align_ylabels() # Align y labels
    ax_main = axes[0]  # mkdocs: hide

    {{LABEL_CODE_AX}}{{MAGIC_CODE_INLINE}}
    ```

{{TABS_END}}
