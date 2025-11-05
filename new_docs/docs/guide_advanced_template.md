# To go further

This section covers advanced mplhep features and utilities..

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
