from __future__ import annotations

from numbers import Real
from typing import TYPE_CHECKING, Any, Iterable, Sequence

import numpy as np
from uhi.numpy_plottable import ensure_plottable_histogram
from uhi.typing.plottable import PlottableAxis, PlottableHistogram

if TYPE_CHECKING:
    from numpy.typing import ArrayLike
else:
    ArrayLike = Any


def isLight(rgb):
    # check if rgb color light or dark based on luma
    r, g, b = rgb
    return (0.212 * r + 0.701 * g + 0.087 * b) > 0.5


def get_plottable_protocol_bins(
    axis: PlottableAxis,
) -> tuple[np.ndarray, np.ndarray | None]:
    out = np.arange(len(axis) + 1).astype(float)
    if isinstance(axis[0], tuple):  # Regular axis
        out[0] = axis[0][0]
        out[1:] = [axis[i][1] for i in range(len(axis))]  # type: ignore
        labels = None
    else:  # Categorical axis
        labels = np.array([axis[i] for i in range(len(axis))])
    return out, labels


def hist_object_handler(
    hist: (
        ArrayLike | PlottableHistogram | tuple[ArrayLike | None, ...] | list[ArrayLike]
    ),
    *bins: Sequence[float | None],
) -> PlottableHistogram:

    if not bins or all(b is None for b in bins):
        if isinstance(hist, list):
            if not bins and len(hist) > 0 and not isinstance(hist[0], (list, Real)):
                hist = tuple(hist)
            else:
                hist = (np.asarray(hist), None)
        elif isinstance(hist, np.ndarray):
            hist = (hist, None)
        hist_obj = ensure_plottable_histogram(hist)
    elif isinstance(hist, PlottableHistogram):
        raise TypeError("Cannot give bins with existing histogram")
    else:
        hist_obj = ensure_plottable_histogram((hist, *bins))

    if len(hist_obj.axes) not in {1, 2}:
        raise ValueError("Must have only 1 or 2 axes")

    return hist_obj


def process_histogram_parts(
    H: (
        ArrayLike | PlottableHistogram | Iterable[ArrayLike] | list[PlottableHistogram]
    ),
    *bins: Sequence[float | None],
):
    """
    Parameters
    ----------

        H : object
            Histogram object with containing values and optionally bins. Can be:

            - `np.histogram` tuple
            - PlottableHistogram object
            - `boost_histogram` classic (<0.13) histogram object
            - raw histogram values, provided `bins` is specified.

        A list of any of the above.

        *bins : Sequence[float], optional
            Histogram bins, if not part of ``h``. One iterable per histogram dimension.

    Returns
    -------
        values, bins: Iterator[Tuple[np.ndarray, np.ndarray]]
    """

    # Try to understand input
    if isinstance(H, list) and not isinstance(H[0], (Real)):
        return _process_histogram_parts_iter(H, *bins)
    else:
        return _process_histogram_parts_iter((H,), *bins)  # type: ignore


def _process_histogram_parts_iter(
    hists: Iterable[ArrayLike] | Iterable[PlottableHistogram],
    *bins: Sequence[float | None],
) -> Iterable[PlottableHistogram]:
    original_bins: tuple[Sequence[float], ...] = bins  # type: ignore

    for hist in hists:
        h = hist_object_handler(hist, *bins)
        current_bins: tuple[Sequence[float], ...] = tuple(get_plottable_protocol_bins(a)[0] for a in h.axes)  # type: ignore
        if any(b is None for b in original_bins):
            original_bins = current_bins
        if len(current_bins) != len(original_bins):
            msg = "Plotting multiple histograms must have the same dimensionality"
            raise ValueError(msg)
        for i in range(len(current_bins)):
            diff_lengths = len(original_bins[i]) != len(current_bins[i])
            if diff_lengths or not np.allclose(original_bins[i], current_bins[i]):
                msg = "Plotting multiple histograms with different binning is not supported"
                raise ValueError(msg)

        yield h


def get_histogram_axes_title(axis: Any) -> str:

    if hasattr(axis, "label"):
        return axis.label
    # Classic support for older hist, deprecated
    elif hasattr(axis, "title"):
        return axis.title
    elif hasattr(axis, "name"):
        return axis.name

    # No axis title found
    return ""
