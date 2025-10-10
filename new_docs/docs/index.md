# mplhep

A [matplotlib](https://matplotlib.org/) wrapper for easy plotting required in high energy physics (HEP). Primarily "prebinned" 1D & 2D histograms and matplotlib [style-sheets](https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html) carrying recommended plotting styles of large LHC experiments - ATLAS, CMS & LHCb. This project is published [on GitHub](https://github.com/scikit-hep/mplhep).

## Quick Start

### Installation

Install mplhep using pip:

```bash
pip install mplhep
```

Or with conda:

```bash
conda install -c conda-forge mplhep
```

### Simple Plot Example

Here's a quick example to get you started:

<!-- ```python exec="1" html="1" result="above" -->
```python
# mkdocs: render
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np

# Set the plotting style (optional)
hep.style.use("CMS")

# Create some sample data
data = np.random.normal(0, 1, 1000)

# Create a histogram
fig, ax = plt.subplots(figsize=(8, 6))
hep.histplot(*np.histogram(data), ax=ax, label="Data")

# Add labels and styling
ax.set_xlabel("Observable")
ax.set_ylabel("Events")
ax.legend()

```

This creates a simple histogram with HEP-style formatting. Check out the [Gallery](gallery.md) for more advanced examples!

## Getting Started

- [Install](install.md)
- [User Guide](guide.md)

## Gallery

- [Gallery Overview](gallery.md)
- [1D Histogram Comparisons](gallery.md#1d-histogram-comparisons)
- [Model Comparisons](gallery.md#model-comparisons)

## Reference

- [API](api.md)
