# Utilities

This section covers advanced mplhep features and utilities.

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

## Text placement

### Add text

[mh.add_text][mplhep.add_text] will add text to a specified location on the axis. It has flexible positioning options, that are accessible via the `loc` argument, or the `x` and `y` arguments.

{{TABS_START}}
{{TAB_HEADER}}

    === "loc argument"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()

        locs = [
            "upper left", # or "top left"
            "upper right", # or "top right"
            "lower left", # or "bottom left"
            "lower right", # or "bottom right"
            "over left",
            "over right",
            "under left",
            "under right",
        ]

        for loc in locs:
            mh.add_text(
                f'Text with\nloc="{loc}"',
                loc=loc,
                ax=ax,
            )
        ```

    === "x and y arguments"

        ```python
        # mkdocs: render
            # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()

        positions = [
            ("right_in", "top_in"),
            ("left_in", "top_in"),
            ("left_in", "bottom_in"),
            ("right_in", "bottom_in"),
            ("right", "top_out"),
            ("left", "top_out"),
            ("right_out", "top_in"),
            ("right_out", "bottom_in"),
            ("right", "bottom_out"),
            ("left", "bottom_out"),
        ]

        for x, y in positions:
            mh.add_text(
                f'Text with\nx="{x}"\ny="{y}"',
                x=x,
                y=y,
                ax=ax,
            )
        ```

{{TABS_END}}

### Append text

[mh.append_text][mplhep.append_text] appends additional text relative to an existing text object created with [mh.add_text][mplhep.add_text]. The new text can be positioned above, below, left, or right of the existing text.

```python
# Add text at specific location
txt = mh.add_text('Custom Text', loc='upper right')

# Append additional text
mh.append_text('Additional info', txt, loc='below')
```

## Subplot creation

[mh.subplots][mplhep.subplots] is a wrapper around `plt.subplots` to create a figure with multiple subplots. It conveniently adjusts the figure size and spacing between subplots if multiple rows are requested.

```python
fig, axes = mh.subplots(nrows=6)
# Will scale the figure, and add spacing between rows and remove the xlabels on inner plots.
```

## Save variations

[mh.savelabels][mplhep.savelabels] automatically generates multiple versions of a plot with different experiment label text variations, useful for creating preliminary and final versions of plots.

```python
mh.savelabels('test.png')
# Produces: test.png, test_pas.png, test_supp.png, test_wip.png, with no label, 'Preliminary', 'Supplementary', and 'Work in Progress' labels respectively.

mh.savelabels('test', labels=[("FOO", "foo.pdf"), ("BAR", "bar")])
# Produces: foo.pdf, test_bar.png
```

## Fit y-label

[mh.set_fitting_ylabel_fontsize][mplhep.set_fitting_ylabel_fontsize] adjusts the y-axis label font size to fit within the figure when there are long y-axis labels.

```python
mh.set_fitting_ylabel_fontsize(ax)
```

## mpl_magic

The function [mh.mpl_magic][mplhep.mpl_magic] applies several common mplhep utilities to a given axis:

- [mh.set_ylow][mplhep.set_ylow]: Sets a minimum y-axis limit based on data.
- [mh.yscale_legend][mplhep.yscale_legend]: Rescales the y-axis to fit the legend.
- [mh.yscale_anchored_text][mplhep.yscale_anchored_text]: Rescales the y-axis to fit anchored text.

```python
mh.mpl_magic(ax)
```

You can also call these functions individually as needed.

## Axes manipulation

### Add colorbar axis

[mh.make_square_add_cbar][mplhep.make_square_add_cbar] creates a square axis and adds a colorbar axis to the right, useful for 2D histograms.

```python
ax_colorbar = mh.make_square_add_cbar(ax)
# ax is now square, and ax_colorbar is the colorbar axis.
```

### Add axis

[mh.append_axes][mplhep.append_axes] appends a new axis to an existing axis in a specified direction (top, bottom, left, right).

```python
ax_new = mh.append_axes(ax, position='top', size=2, pad=0.3)
# Adds a new axis above ax with height 2 inches and 0.3 inch padding.
```

## plt.hist wrapper

[mh.hist][mplhep.hist] is a drop-in replacement for [mh.histplot][mplhep.histplot] which runs the `np.histogram` function before plotting. It provides a convenient way to create a histogram of raw data values and benefits from the extended features of [mh.histplot][mplhep.histplot], such as automatic error bar calculation, bin-width normalization and HEP-style plotting options.

!!! warning
    [mh.hist][mplhep.hist] does not return a histogram object compatible with the Unified Histogram Interface (UHI), thus cannot be used directly with other mplhep histogram plotting functions.

```python
data = np.random.normal(100, 15, 1000)
mh.hist(data, bins=50, range=(50, 150))

# Multiple datasets
data1 = np.random.normal(100, 15, 1000)
data2 = np.random.normal(120, 15, 1000)
mh.hist([data1, data2], bins=50, label=['Dataset 1', 'Dataset 2'])
```
