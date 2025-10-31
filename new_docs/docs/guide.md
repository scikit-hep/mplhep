# User Guide

Welcome to the mplhep user guide! This documentation is organized into focused sections to help you find what you need quickly.

???+ tip "Prerequisites"
    Throughout this guide the following codeblock is assumed.
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    import hist
    np.random.seed(42)
    import mplhep as mh
    mh.style.use('<as appropriate>')
    ```

### [**Histogram Plotting**](guide_basic_plotting.md)
Functions for 1D and 2D pre-binned histograms with support for the [Unified Histogram Interface (UHI)](https://uhi.readthedocs.io/)

- [1D Histogram Plotting](guide_basic_plotting.md#1d-histogram-plotting)
    - [Supported Input Formats](guide_basic_plotting.md#supported-input-formats)
    - [Histogram Styles](guide_basic_plotting.md#histogram-styles)
    - [Multiple Histograms](guide_basic_plotting.md#multiple-histograms)
    - [Error Bars](guide_basic_plotting.md#error-bars)
    - [Normalization Options](guide_basic_plotting.md#normalization-options)
- [2D Histograms](guide_basic_plotting.md#2d-histograms)

### [**Comparison Plotting**](guide_comparisons.md)
High-level functions for data-model comparisons.

- [Compare two histograms](guide_comparisons.md#two-histograms)
- [Data-MC comparison](guide_comparisons.md#data-mc)
    - [Showcasing more options](guide_comparisons.md#showcasing-more-options)
- [Additional examples](guide_comparisons.md#additional-examples)

### [**Styling**](guide_styling.md)
Official styles for ATLAS, CMS, LHCb, ALICE, and DUNE experiments

- [Setting experiment styles](guide_styling.md#setting-experiment-styles)
- [Setting experiment labels](guide_styling.md#setting-experiment-labels)
- [Configuring experiment labels](guide_styling.md#configuring-experiment-labels)

### [**To go further**](guide_advanced.md)
Utility functions, experiment-specific label formatters, UHI integration, and best practices

- [Text placement](guide_advanced.md#generic-text)
- [Working with UHI Histograms](guide_advanced.md#working-with-uhi-histograms)
- [Best practices](guide_advanced.md#best-practices)

## More Info

- **[API Reference](api.md)** - Detailed documentation of all functions and parameters
- **[Gallery](gallery.md)** - Visual examples of all plot types
- **[Contributing](contributing.md)** - Information on development and testing
