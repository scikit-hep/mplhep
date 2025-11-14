# mplhep

A [matplotlib](https://matplotlib.org/) wrapper for easy plotting required in high energy physics (HEP). Primarily "prebinned" 1D & 2D histograms and matplotlib [style-sheets](https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html) carrying recommended plotting styles of large LHC experiments - ATLAS, CMS & LHCb. This project is published [on GitHub](https://github.com/scikit-hep/mplhep).

## Quick Start

### Installation

Install mplhep using pip:

```bash
pip install mplhep
```

### Simple Example

Here's a quick example showing the primary functionality

=== "Default"

    ```python
    # mkdocs: render
    # The mkdocs commands are auto hidden  # mkdocs: hide
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use()  # Style reset to default

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    txt_obj = mh.add_text("Default", loc='over left')
    mh.append_text("matplotlib style", txt_obj, loc='right')
    ```

=== "plothist"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use("plothist")

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    txt_obj = mh.add_text("plothist", loc='over left')
    mh.append_text("style", txt_obj, loc='right', fontsize='small')
    ```


=== "CMS"

    ```python
    # mkdocs: render
    # The mkdocs commands are auto hidden  # mkdocs: hide
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use("CMS")

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    mh.cms.label("Preliminary", data=False, lumi=100, com=15)  # ax can be implicit
    # mh.mpl_magic(soft_fail=True)  # Autofit label - not needed
    ```

=== "ATLAS"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use("ATLAS")

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    mh.atlas.label("Preliminary", data=False, lumi=100, com=15)  # ax can be implicit
    mh.mpl_magic(soft_fail=True)  # Autofit label
    ```

=== "LHCb"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use("LHCb2")

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    mh.lhcb.label("Preliminary", data=False, lumi=100, com=15)  # ax can be implicit
    mh.mpl_magic(soft_fail=True)  # Autofit label
    ```

=== "ALICE"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use("ALICE")

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    mh.alice.label("Preliminary", data=False, lumi=100, com=15)  # ax can be implicit
    mh.mpl_magic(soft_fail=True)  # Autofit label
    ```

=== "DUNE"

    ```python
    # mkdocs: render
    import matplotlib.pyplot as plt
    import mplhep as mh
    import numpy as np
    np.random.seed(42)
    # Set the plotting style
    mh.style.use("DUNE")

    # Create a plot
    fig, ax = plt.subplots()
    # Plot a pre-binned histogram
    mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
    # Add appropriate labels
    mh.dune.label("Preliminary", data=False, lumi=100, com=15)  # ax can be implicit
    # mh.mpl_magic(soft_fail=True)  # Autofit label - not needed
    ```

This creates a simple histogram with HEP-style formatting. Check out the [User Guide](guide.md) and the [Gallery](gallery.md) below for more advanced examples!


<!-- ## Executable codeblock with markdown-exec if we ever need it

```python exec="1" html="1" source="above" width="30"
#######################  mpl setup ######################### # markdown-exec: hide
from io import StringIO  # markdown-exec: hide
import matplotlib  # markdown-exec: hide
matplotlib.use("Agg")  # markdown-exec: hide
import numpy as np  # markdown-exec: hide
np.random.seed(42)  # markdown-exec: hide
############################################################ # markdown-exec: hide
import matplotlib.pyplot as plt
import numpy as np
import mplhep as mh
# Set the plotting style
mh.style.use("CMS")

# Create a plot
fig, ax = plt.subplots()
# Plot a pre-binned histogram
mh.histplot(*np.histogram(np.random.normal(0, 1, 1000)), ax=ax, label="Data")
# Add appropriate labels
mh.cms.label("Preliminary", data=False, lumi=100, com=15)
#######################  mpl setup ######################### # markdown-exec: hide
import sys  # markdown-exec: hide
sys.path.append('docs')  # markdown-exec: hide
import svg_utils  # markdown-exec: hide
svg = svg_utils.save_figure_as_resized_svg(fig, 50)  # markdown-exec: hide
print(svg)  # markdown-exec: hide
############################################################ # markdown-exec: hide
``` -->


## [User Guide](guide.md)

[Step-by-step instructions](guide.md) on how to use mplhep for your HEP plotting needs, explaining key features and functionalities.


## [Gallery](gallery.md)

A [collection of example plots](gallery.md) created using mplhep, showcasing various plot types.

## [API](api.md)

Comprehensive [reference documentation](api.md) for all functions, classes, and modules in mplhep.

## [Contributing](CONTRIBUTING.md)

A [guide to contributing](CONTRIBUTING.md) to the mplhep project, including setup instructions and coding guidelines.

## Getting Help

- Check the [GitHub repository](https://github.com/scikit-hep/mplhep) for issues
- Ask questions in the [scikit-hep discussions](https://github.com/scikit-hep/mplhep/discussions)
