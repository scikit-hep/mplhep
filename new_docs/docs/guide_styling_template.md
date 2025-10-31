# Styling and Customization

This section covers additional information about styling.

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

### Setting experiment styles

Styles are applied globally using [`mh.style.use()`][mplhep.style.use], which is just a thin wrapper on `plt.style.use()`, with some extra goodies:

{{TABS_START}}
{{TAB_HEADER}}

    === "Style by name"

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}

        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```

    === "Style as a dict"

        Styles are simple dictionaries that configure `mpl.rcParams`.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use({{STYLE_DICT}})

        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        print({{STYLE_DICT}})
        ```

        ```python exec="on" result="python"
        import mplhep as mh
        print({{STYLE_DICT}})
        ```

    === "With customizations"

        By passing a list `["CMS", {...}]` users can overwrite settings as they see fit.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        import hist  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        mh.style.use([{{STYLE_DICTv2}}, {"font.size": 10,}])

        fig, ax = plt.subplots()
        mh.histplot([1, 2, 3, 6, 3, 5, 2, 1], ax=ax)
        ```


{{TABS_END}}


!!! warning
    Due to matplotlib limitations, `with plt.style.context()` does not work reliably with mplhep styles, especially for fonts. Use [`mh.style.use()`][mplhep.style.use] globally instead.


### Setting experiment labels

Each experiment style comes with a matching label function that formats experiment names, status text, and run information according to that experiment's guidelines:

{{TABS_START}}
{{TAB_HEADER}}

    === "loc=0 (Above axes)"

        Default for most experiments. Label appears above the plot area, left aligned.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_LOC_0}}
        ```

    === "loc=1 (Top left, single line)"

        Compact single-line format in the top left corner.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_LOC_1}}
        ```

    === "loc=2 (Top left, multiline)"

        Multiline format in the top left corner.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_LOC_2}}
        ```

    === "loc=3 (Split layout)"

        Experiment name above axes, secondary text in corner.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_LOC_3}}
        ```

    === "loc=4 (Style-specific)"

        Style-specific layout (e.g., ATLAS places luminosity below).

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_LOC_4}}
        ```

{{TABS_END}}

### Configuring experiment labels

Additional configuration options for experiment labels:

{{TABS_START}}
{{TAB_HEADER}}

    === "Common configurations"

        Combine multiple standard parameters for complete label information.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_COMMON_CONFIG}}
        ```

    === "Fully customized"

        Use `llabel` and `rlabel` for complete control over label content.

        ```python
        # mkdocs: render
        # mkdocs: align=left
        import matplotlib.pyplot as plt  # mkdocs: hide
        import mplhep as mh  # mkdocs: hide
        import numpy as np  # mkdocs: hide
        np.random.seed(42)  # mkdocs: hide
        {{STYLE_USE_CODE}}  # mkdocs: hide
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4])
        {{LABEL_CUSTOM}}
        ```

{{TABS_END}}
