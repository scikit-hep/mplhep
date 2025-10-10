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
- `hep.histplot()` - Plot 1D histograms from arrays, histograms, or UHI objects
- `hep.hist2dplot()` - Plot 2D histograms

### Style Sheets
- `hep.style.use("CMS")` - Apply CMS experiment style
- `hep.style.use("ATLAS")` - Apply ATLAS experiment style
- `hep.style.use("LHCb")` - Apply LHCb experiment style

### Data-Model Comparisons
- `hep.plot_data_model_comparison()` - Compare data with model predictions
- Various comparison types: ratio, pull, difference, etc.

## Advanced Plotting

### Multiple Histograms

```python
# Plot multiple histograms with labels
hep.histplot([h1, h2], bins=bins, yerr=True, label=["MC1", "MC2"])
```

### Stacked Histograms

```python
# Stack multiple histograms
hep.histplot([h1, h2], bins=bins, stack=True, label=["Signal", "Background"])
```

### Error Bars and Uncertainty

```python
# Add error bars
hep.histplot(data, bins=bins, yerr=True, histtype='errorbar')
```

### Styling Options

```python
# Customize appearance
hep.histplot(data, bins=bins,
             histtype='fill',           # 'step', 'fill', 'errorbar'
             hatch='///',               # Pattern for filled histograms
             edgecolor='red',           # Edge color
             facecolor='none',          # Fill color
             alpha=0.7)                 # Transparency
```

### Density Normalization

```python
# Plot normalized histograms
hep.histplot([h1, h2], bins=bins, density=True, stack=True)
```

## Experiment Styles

mplhep provides pre-configured styles for major HEP experiments:

### CMS Style
```python
hep.style.use("CMS")
# Features: Specific fonts, colors, and layout conventions
```

### ATLAS Style
```python
hep.style.use("ATLAS")
# Features: ATLAS-specific styling and formatting
```

### LHCb Style
```python
hep.style.use("LHCb")
# Features: LHCb experiment conventions
```

## Data/Model Comparisons

### Basic Comparison
```python
# Compare data with model predictions
fig, (ax_main, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
hep.histplot(model, bins=bins, ax=ax_main, label="Model")
hep.histplot(data, bins=bins, ax=ax_main, histtype='errorbar', label="Data")
hep.ratio(data, model, bins=bins, ax=ax_ratio)
```

### Advanced Comparisons
```python
# Using the comparison utility
hep.comp.hists(data_hist, model_hist,
               comparison="ratio",      # "ratio", "pull", "difference"
               xlabel="Observable",
               ylabel="Events")
```

## Working with Histogram Objects

mplhep works seamlessly with various histogram formats:

### NumPy Arrays
```python
# Direct from arrays
data = np.random.normal(0, 1, 1000)
hep.histplot(data, bins=50)
```

### Pre-computed Histograms
```python
# From (values, bins) tuples
counts, bin_edges = np.histogram(data, bins=50)
hep.histplot(counts, bins=bin_edges)
```

### UHI-Compatible Objects
```python
# Works with hist, uproot, and other UHI libraries
import hist
h = hist.Hist(hist.axis.Regular(50, -3, 3))
h.fill(data)
hep.histplot(h)
```

## Best Practices

### Style Application
Apply styles at the beginning of your plotting script:
```python
import mplhep as hep
hep.style.use("CMS")  # Apply once at the start
```

### Error Handling
Always include appropriate error bars for data:
```python
hep.histplot(data, bins=bins, yerr=True)
```

### Labels and Legends
Use clear, descriptive labels:
```python
hep.histplot(data, label="Observed Data")
ax.legend()
```

### Axis Labels
Provide meaningful axis labels:
```python
ax.set_xlabel("Mass [GeV]")
ax.set_ylabel("Events / 10 GeV")
```

## Examples

Check out the [Gallery](gallery.md) for comprehensive examples of all plotting functions and comparison types.
