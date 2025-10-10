# User Guide

## Getting Started with mplhep

mplhep is a matplotlib wrapper designed for easy plotting in high energy physics (HEP). It provides:

- Pre-binned 1D and 2D histogram plotting functions
- HEP experiment style sheets (ATLAS, CMS, LHCb)
- Data-model comparison plotting utilities
- Label and text placement helpers

## Basic Usage

```python
import matplotlib.pyplot as plt
import mplhep as hep

# Apply a style
hep.style.use("CMS")

# Create some data
import numpy as np
data = np.random.normal(0, 1, 1000)

# Plot a histogram
fig, ax = plt.subplots()
hep.histplot(data, bins=50, ax=ax)
plt.show()
```

## Key Features

### Histogram Plotting
- `hep.histplot()` - Plot 1D histograms
- `hep.hist2dplot()` - Plot 2D histograms

### Style Sheets
- `hep.style.use("CMS")` - Apply CMS style
- `hep.style.use("ATLAS")` - Apply ATLAS style
- `hep.style.use("LHCb")` - Apply LHCb style

### Data-Model Comparisons
- `hep.plot_data_model_comparison()` - Compare data with model predictions
- Various comparison types: ratio, pull, difference, etc.

## Examples

Check out the [Gallery](gallery.md) for comprehensive examples of all plotting functions and comparison types.
