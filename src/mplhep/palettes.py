from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def cubehelix_palette(
    ncolors: int = 7,
    start: float = 1.5,
    rotation: float = 1.5,
    gamma: float = 1.0,
    hue: float = 0.8,
    lightest: float = 0.8,
    darkest: float = 0.3,
    reverse: bool = True,
) -> list[tuple[float, float, float]]:
    """
    Make a sequential palette from the cubehelix system, in which the perceived brightness is linearly increasing.
    This code is adapted from seaborn, which implements equation (2) of reference [1] below.

    Parameters
    ----------
    ncolors : int, optional
        Number of colors in the palette.
    start : float, 0 <= start <= 3, optional
        Direction of the predominant colour deviation from black
        at the start of the colour scheme (1=red, 2=green, 3=blue).
    rotation : float, optional
        Number of rotations around the hue wheel over the range of the palette.
    gamma : float, 0 <= gamma, optional
        Gamma factor to emphasize darker (gamma < 1) or lighter (gamma > 1)
        colors.
    hue : float, 0 <= hue <= 1, optional
        Saturation of the colors.
    darkest : float, 0 <= darkest <= 1, optional
        Intensity of the darkest color in the palette.
    lightest : float, 0 <= lightest <= 1, optional
        Intensity of the lightest color in the palette.
    reverse : bool, optional
        If True, the palette will go from dark to light.

    Returns
    -------
    list[tuple[float, float, float]]
        The generated palette of colors represented as a list of RGB tuples.

    References
    ----------
    [1] Green, D. A. (2011). "A colour scheme for the display of astronomical
    intensity images". Bulletin of the Astromical Society of India, Vol. 39,
    p. 289-295.
    """

    def f(x0, x1):
        # Adapted from matplotlib
        def color(lambda_):
            # emphasise either low intensity values (gamma < 1),
            # or high intensity values (gamma > 1)
            lambda_gamma = lambda_**gamma

            # Angle and amplitude for the deviation
            # from the black to white diagonal
            # in the plane of constant perceived intensity
            a = hue * lambda_gamma * (1 - lambda_gamma) / 2

            phi = 2 * np.pi * (start / 3 + rotation * lambda_)

            return lambda_gamma + a * (x0 * np.cos(phi) + x1 * np.sin(phi))

        return color

    cdict = {
        "red": f(-0.14861, 1.78277),
        "green": f(-0.29227, -0.90649),
        "blue": f(1.97294, 0.0),
    }

    cmap = mpl.colors.LinearSegmentedColormap("cubehelix", cdict)  # type: ignore[arg-type]

    x = np.linspace(lightest, darkest, int(ncolors))
    pal = cmap(x)[:, :3].tolist()
    if reverse:
        pal = pal[::-1]
    return [tuple(c) for c in pal]


def get_color_palette(
    cmap: str, N: int
) -> list[str] | list[tuple[float, float, float]]:
    """
    Get N different colors from a chosen colormap.

    Parameters
    ----------
    cmap : str
        The name of the colormap to use. Use "ggplot" get the cycle of the plothist style. Use "cubehelix" to get the cubehelix palette with default settings. Can also be any colormap from matplotlib (we recommend "viridis", "coolwarm" or "YlGnBu_r").
    N : int
        The number of colors to sample.

    Returns
    -------
    list[str] or list[tuple[float, float, float]]
        A list of colors. If "ggplot" is selected, returns a list of hex color strings.
        Otherwise, returns a list of RGB color tuples.

    References
    ----------
    ggplot colormap: https://matplotlib.org/stable/gallery/style_sheets/ggplot.html
    Matplotlib colormaps: https://matplotlib.org/stable/gallery/color/colormap_reference.html

    See also
    --------
    cubehelix_palette : Make a sequential palette from the cubehelix system.
    """
    if N < 1:
        msg = "The number of colors asked should be >0."
        raise ValueError(msg)

    if cmap == "ggplot":
        if N > 7:
            msg = f"Only 7 colors are available in the ggplot style cycle ({N} asked)."
            raise ValueError(msg)
        return [
            "#348ABD",
            "#E24A33",
            "#988ED5",
            "#777777",
            "#FBC15E",
            "#8EBA42",
            "#FFB5B8",
        ][0:N]

    if cmap == "cubehelix":
        return cubehelix_palette(N)

    if N < 2:
        msg = "The number of colors asked should be >1 to sequence matplotlib palettes."
        raise ValueError(msg)

    plt_cmap = plt.get_cmap(cmap)
    plt_cmap = plt_cmap(np.linspace(0, 1, N))
    return [tuple(k) for k in plt_cmap]
