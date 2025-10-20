from __future__ import annotations

from numbers import Real
from typing import TYPE_CHECKING, Any, Iterable, Sequence

import numpy as np
from uhi.numpy_plottable import (
    Kind,
    NumPyPlottableHistogram,
    ensure_plottable_histogram,
)
from uhi.typing.plottable import PlottableAxis, PlottableHistogram

if TYPE_CHECKING:
    pass

ArrayLike = Any

import copy
import inspect
import logging
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import markers
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredText
from matplotlib.patches import Patch, Rectangle
from matplotlib.path import Path
from matplotlib.text import Text

logger = logging.getLogger(__name__)

_DEBUG_OVERLAP = False


def _get_plottable_protocol_bins(
    axis: PlottableAxis,
) -> tuple[np.ndarray, np.ndarray | None]:
    out: np.ndarray = np.arange(len(axis) + 1).astype(float)
    if isinstance(axis[0], tuple):  # Regular axis
        out[0] = axis[0][0]
        out[1:] = [axis[i][1] for i in range(len(axis))]  # type: ignore[index]
        labels = None
    else:  # Categorical axis
        labels = np.array([axis[i] for i in range(len(axis))])
    return out, labels


def _hist_object_handler(
    hist_like: (
        ArrayLike | PlottableHistogram | tuple[ArrayLike | None, ...] | list[ArrayLike]
    ),
    *bins: Sequence[float | None],
) -> PlottableHistogram:
    if not bins or all(b is None for b in bins):
        if isinstance(hist_like, list):
            if (
                not bins
                and len(hist_like) > 0
                and not isinstance(hist_like[0], (list, Real))
            ):
                hist_like = tuple(hist_like)
            else:
                hist_like = (np.asarray(hist_like), None)
        elif isinstance(hist_like, np.ndarray):
            hist_like = (hist_like, None)
        hist_obj = ensure_plottable_histogram(hist_like)
    elif isinstance(hist_like, PlottableHistogram):
        hist_obj = hist_like
    else:
        hist_obj = ensure_plottable_histogram((hist_like, *bins))

    if len(hist_obj.axes) not in {1, 2}:
        msg = "Must have only 1 or 2 axes"
        raise ValueError(msg)

    return hist_obj


def _process_histogram_parts_iter(
    hists: Iterable[ArrayLike] | Iterable[PlottableHistogram],
    *bins: Sequence[float | None],
) -> Iterable[PlottableHistogram]:
    original_bins: tuple[Sequence[float], ...] = bins  # type: ignore[assignment]

    for hist_like in hists:
        h = _hist_object_handler(hist_like, *bins)
        current_bins: tuple[Sequence[float], ...] = tuple(
            _get_plottable_protocol_bins(a)[0]  # type: ignore[misc]
            for a in h.axes  # type: ignore[misc]
        )
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


def _check_counting_histogram(hist_list):
    """
    Check that the histograms in the list are counting histograms.

    Parameters
    ----------
    hist_list : list of PlottableHistogram

    Raise
    -----
    ValueError
        If the histogram is not a counting histogram.

    """
    if not isinstance(hist_list, list):
        hist_list = [hist_list]
    for hist_obj in hist_list:
        if hist_obj.kind != Kind.COUNT:
            msg = f"The histogram must be a counting histogram, but the input histogram has kind {hist_obj.kind}."
            raise ValueError(msg)


def _invert_collection_order(ax, n=0):
    """
    Invert the order of the collection objects in an Axes instance.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    n : int, optional
        The number of collections to keep in the original order. Default is 0.

    """
    # Retrieve the list of collection objects
    collections = list(ax.collections)

    # Separate the first n collections and reverse the rest
    first_n = collections[:n]
    rest = collections[n:]
    rest.reverse()

    # Remove all collections and re-add them in the new order
    for collection in ax.collections:
        collection.remove()
    for collection in first_n + rest:
        ax.add_collection(collection)


def _isLight(rgb):
    # check if rgb color light or dark based on luma
    r, g, b = rgb
    return (0.212 * r + 0.701 * g + 0.087 * b) > 0.5


def _process_histogram_parts(
    H: ArrayLike | PlottableHistogram | Iterable[ArrayLike] | list[PlottableHistogram],
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
    if (isinstance(H, (list, np.ndarray))) and not isinstance(H[0], (Real)):
        return _process_histogram_parts_iter(H, *bins)
    return _process_histogram_parts_iter((H,), *bins)  # type: ignore[arg-type]


def _get_plottables(
    H,
    bins=None,
    yerr: ArrayLike | bool | None = None,
    w2=None,
    w2method=None,
    flow="hint",
    stack=False,
    density=False,
    binwnorm=None,
    xoffsets=False,
):
    """
    Generate plottable histograms from various histogram data sources.

    Parameters
    ----------
    H : object
        Histogram object with containing values and optionally bins. Can be:

        - `np.histogram` tuple
        - PlottableProtocol histogram object
        - `boost_histogram` classic (<0.13) histogram object
        - raw histogram values, provided `bins` is specified.

        Or list thereof.
    bins : iterable, optional
        Histogram bins, if not part of ``H``.
    yerr : iterable or bool, optional
        Histogram uncertainties. Following modes are supported:
        - True, sqrt(N) errors or poissonian interval when ``w2`` is specified
        - shape(N) array of for one sided errors or list thereof
        - shape(Nx2) array of for two sided errors or list thereof
    w2 : iterable, optional
        Sum of the histogram weights squared for poissonian interval error
        calculation
    w2method: callable, optional
        Function calculating CLs with signature ``low, high = fcn(w, w2)``. Here
        ``low`` and ``high`` are given in absolute terms, not relative to w.
        Default is ``None``. If w2 has integer values (likely to be data) poisson
        interval is calculated, otherwise the resulting error is symmetric
        ``sqrt(w2)``. Specifying ``poisson`` or ``sqrt`` will force that behaviours.
    flow :  str, optional { "show", "sum", "hint", "none"}
        Whether plot the under/overflow bin. If "show", add additional under/overflow bin.
        If "sum", add the under/overflow bin content to first/last bin.
    stack : bool, optional
        Whether to stack or overlay non-axis dimension (if it exists). N.B. in
        contrast to ROOT, stacking is performed in a single call aka
        ``histplot([h1, h2, ...], stack=True)`` as opposed to multiple calls.
    density : bool, optional
        If true, convert sum weights to probability density (i.e. integrates to 1
        over domain of axis) (Note: this option conflicts with ``binwnorm``)
    binwnorm : float, optional
        If true, convert sum weights to bin-width-normalized, with unit equal to
            supplied value (usually you want to specify 1.)
    xoffsets : bool | float | iterable, optional
        Offset for x-axis values.

    Returns
    -------
    plottables : list of EnhancedPlottableHistogram
        Processed histogram objects ready for plotting.
    (flow_bins, underflow, overflow) : tuple
        Flow bin information for handling underflow and overflow values.
    """
    plottables = []
    flow_bins = np.copy(bins)

    hists = list(_process_histogram_parts(H, bins))
    final_bins, _ = _get_plottable_protocol_bins(hists[0].axes[0])

    if xoffsets is True:
        parsed_offsets = []
        widths = np.diff(final_bins)
        sub_bin_width = widths / (len(hists) + 1)
        for i in range(len(hists)):
            parsed_offsets.append(sub_bin_width * (i + 1))
        xoffsets = parsed_offsets
    else:
        xoffsets = [None] * len(hists)
    for h, xoffset in zip(hists, xoffsets):
        value, variance = np.copy(h.values()), h.variances()
        if has_variances := variance is not None:
            variance = np.copy(variance)
        underflow, overflow = 0.0, 0.0
        underflowv, overflowv = 0.0, 0.0
        # One sided flow bins - hist (uproot hist does not have the over- or underflow traits)
        if (
            hasattr(h, "axes")
            and (traits := getattr(h.axes[0], "traits", None)) is not None
            and hasattr(traits, "underflow")
            and hasattr(traits, "overflow")
        ):
            if traits.overflow:
                overflow = np.copy(h.values(flow=True))[-1]
                if has_variances:
                    overflowv = np.copy(h.variances(flow=True))[-1]
            if traits.underflow:
                underflow = np.copy(h.values(flow=True))[0]
                if has_variances:
                    underflowv = np.copy(h.variances(flow=True))[0]
        # Both flow bins exist - uproot
        elif hasattr(h, "values") and "flow" in inspect.getfullargspec(h.values).args:
            if len(h.values()) + 2 == len(
                h.values(flow=True)
            ):  # easy case, both over/under
                underflow, overflow = (
                    np.copy(h.values(flow=True))[0],
                    np.copy(h.values(flow=True))[-1],
                )
                if has_variances:
                    underflowv, overflowv = (
                        np.copy(h.variances(flow=True))[0],
                        np.copy(h.variances(flow=True))[-1],
                    )

        # Set plottables
        if flow in ("none", "hint"):
            plottables.append(
                EnhancedPlottableHistogram(
                    value, edges=final_bins, variances=variance, xoffsets=xoffset
                )
            )
        elif flow == "show":
            _flow_bin_size: float = np.max(
                [0.05 * (final_bins[-1] - final_bins[0]), np.mean(np.diff(final_bins))]
            )
            flow_bins = np.copy(final_bins)
            if underflow > 0:
                flow_bins = np.r_[flow_bins[0] - _flow_bin_size, flow_bins]
                value = np.r_[underflow, value]
                if has_variances:
                    variance = np.r_[underflowv, variance]
            if overflow > 0:
                flow_bins = np.r_[flow_bins, flow_bins[-1] + _flow_bin_size]
                value = np.r_[value, overflow]
                if has_variances:
                    variance = np.r_[variance, overflowv]
            plottables.append(
                EnhancedPlottableHistogram(
                    value, edges=flow_bins, variances=variance, xoffsets=xoffset
                )
            )
        elif flow == "sum":
            if underflow > 0:
                value[0] += underflow
                if has_variances:
                    variance[0] += underflowv
            if overflow > 0:
                value[-1] += overflow
                if has_variances:
                    variance[-1] += overflowv
            plottables.append(
                EnhancedPlottableHistogram(
                    value, edges=final_bins, variances=variance, xoffsets=xoffset
                )
            )
        else:
            plottables.append(
                EnhancedPlottableHistogram(
                    value, edges=final_bins, variances=variance, xoffsets=xoffset
                )
            )

    if w2 is not None:
        for _w2, _plottable in zip(
            np.array(w2).reshape(len(plottables), len(final_bins) - 1), plottables
        ):
            _plottable.set_variances(_w2)
            _plottable.method = w2method

    for _plottable in plottables:
        if _plottable.variances() is not None:
            _plottable.method = w2method

    if w2 is not None and yerr is not None:
        msg = "Can only supply errors or w2"
        raise ValueError(msg)

    _yerr_plottables(plottables, final_bins, yerr)
    _norm_stack_plottables(plottables, final_bins, stack, density, binwnorm)

    return plottables, (flow_bins, underflow, overflow)


def _yerr_plottables(plottables, bins, yerr=None):
    """
    Calculate and format y-axis errors for Plottables.

    Parameters
    ----------
    plottables : list of EnhancedPlottableHistogram
        List of EnhancedPlottableHistogram objects.
    bins : iterable
        EnhancedPlottableHistogram bins.
    yerr : iterable or bool, optional
        Histogram uncertainties. Following modes are supported:
        - True, sqrt(N) errors or poissonian interval when ``w2`` is specified
        - shape(N) array of for one sided errors or list thereof
        - shape(Nx2) array of for two sided errors or list thereof

    Raises
    ------
    ValueError
        If `yerr` has an unrecognized format.
    """

    _yerr: np.ndarray | None
    if yerr is not None:
        # yerr is array
        if hasattr(yerr, "__len__"):
            _yerr = np.asarray(yerr)
        # yerr is a number
        elif isinstance(yerr, (int, float)) and not isinstance(yerr, bool):
            _yerr = np.ones((len(plottables), len(bins) - 1)) * yerr
        # yerr is automatic
        else:
            _yerr = None
            for _plottable in plottables:
                _plottable.errors(assume_variances_equal_values=True)
    else:
        _yerr = None
    if _yerr is not None:
        assert isinstance(_yerr, np.ndarray)
        if _yerr.ndim == 3:
            # Already correct format
            pass
        elif _yerr.ndim == 2 and len(plottables) == 1:
            # Broadcast ndim 2 to ndim 3
            if _yerr.shape[-2] == 2:  # [[1,1], [1,1]]
                _yerr = _yerr.reshape(len(plottables), 2, _yerr.shape[-1])
            elif _yerr.shape[-2] == 1:  # [[1,1]]
                _yerr = np.tile(_yerr, 2).reshape(len(plottables), 2, _yerr.shape[-1])
            else:
                msg = "yerr format is not understood"
                raise ValueError(msg)
        elif _yerr.ndim == 2:
            # Broadcast yerr (nh, N) to (nh, 2, N)
            _yerr = np.tile(_yerr, 2).reshape(len(plottables), 2, _yerr.shape[-1])
        elif _yerr.ndim == 1:
            # Broadcast yerr (1, N) to (nh, 2, N)
            _yerr = np.tile(_yerr, 2 * len(plottables)).reshape(
                len(plottables), 2, _yerr.shape[-1]
            )
        else:
            msg = "yerr format is not understood"
            raise ValueError(msg)

        assert _yerr is not None
        for yrs, _plottable in zip(_yerr, plottables):
            _plottable.fixed_errors(*yrs)


def _norm_stack_plottables(plottables, bins, stack=False, density=False, binwnorm=None):
    """
    Normalize and stack histogram data with optional density or bin-width normalization.

    Parameters
    ----------
    plottables : list of EnhancedPlottableHistogram
        List of EnhancedPlottableHistogram objects.
    bins : iterable
        EnhancedPlottableHistogram bins.
    stack : bool, optional
        Whether to stack or overlay non-axis dimension (if it exists). N.B. in
        contrast to ROOT, stacking is performed in a single call aka
        ``histplot([h1, h2, ...], stack=True)`` as opposed to multiple calls.
    density : bool, optional
        If true, convert sum weights to probability density (i.e. integrates to 1
        over domain of axis) (Note: this option conflicts with ``binwnorm``)
    binwnorm : float, optional
        If true, convert sum weights to bin-width-normalized, with unit equal to
            supplied value (usually you want to specify 1.)

    Raises
    ------
    ValueError
        If both `density` and `binwnorm` are set, as they are mutually exclusive.

    Notes
    -----
    Density and bin-width normalization cannot both be applied simultaneously.
    For stacked histograms, this function uses an external utility to compute
    the cumulative stacked values.
    """

    if density is True and binwnorm is not None:
        msg = "Can only set density or binwnorm."
        raise ValueError(msg)
    if density is True:
        if stack:
            _total = np.sum(
                np.array([plottable.values() for plottable in plottables]), axis=0
            )
            for plottable in plottables:
                plottable.flat_scale(1.0 / np.sum(np.diff(bins) * _total))
        else:
            for plottable in plottables:
                plottable.density()
    elif binwnorm is not None:
        for plottable, norm in zip(
            plottables, np.broadcast_to(binwnorm, (len(plottables),))
        ):
            plottable.flat_scale(norm)
            plottable.binwnorm()

    # Stack
    if stack and len(plottables) > 1:
        _stack(*plottables)
        # Reset errors so they get recalculated with stacked values and updated variances
        for plottable in plottables:
            plottable._errors_present = False


def _get_histogram_axes_title(axis: Any) -> str:
    if hasattr(axis, "label"):
        return axis.label
    # Classic support for older hist, deprecated
    if hasattr(axis, "title"):
        return axis.title
    if hasattr(axis, "name"):
        return axis.name

    # No axis title found
    return ""


def _make_plottable_histogram(hist_like, **kwargs):
    """
    Convert a histogram to a plottable histogram.

    Parameters
    ----------
    hist_like : Histogram object (e.g. Hist, boost_histogram, np.histogram, TH1)
        The histogram to be converted.
    **kwargs : dict, optional
        Additional keyword arguments to pass to the EnhancedPlottableHistogram constructor.

    Returns
    -------
    EnhancedPlottableHistogram
        The converted plottable histogram.

    Raises
    ------
    ValueError
        If the input histogram is not 1D.
    """
    if isinstance(hist_like, EnhancedPlottableHistogram):
        if kwargs:
            warnings.warn(
                "Additional keyword arguments are ignored when converting an already plottable histogram.",
                stacklevel=2,
            )
        return hist_like

    hist_obj = ensure_plottable_histogram(hist_like)
    if len(hist_obj.axes) != 1:
        msg = "Only 1D histograms are supported."
        raise ValueError(msg)

    axis = hist_obj.axes[0]

    edges = np.arange(len(axis) + 1).astype(float)
    if isinstance(axis[0], tuple):  # Regular axis
        edges[0] = axis[0][0]
        edges[1:] = [axis[i][1] for i in range(len(axis))]
    else:  # Categorical axis
        msg = "Categorical axis is not supported yet."
        raise NotImplementedError(msg)

    return EnhancedPlottableHistogram(
        np.array(hist_obj.values()),  # copy to avoid further modification
        edges=edges,
        variances=np.array(hist_obj.variances()),  # copy to avoid further modification
        kind=hist_obj.kind,
        **kwargs,
    )


def _stack(*plottables):
    baseline = np.nan_to_num(copy.deepcopy(plottables[0].values()), 0)
    baseline_variance = (
        np.nan_to_num(copy.deepcopy(plottables[0].variances()), 0)
        if plottables[0].variances() is not None
        else None
    )
    for i in range(1, len(plottables)):
        _mask = np.isnan(plottables[i].values())
        _baseline = copy.deepcopy(baseline)
        _baseline[_mask] = np.nan
        plottables[i].baseline = _baseline
        baseline += np.nan_to_num(plottables[i].values(), 0)

        # Update variances cumulatively for proper error calculation
        if baseline_variance is not None and plottables[i].variances() is not None:
            baseline_variance += np.nan_to_num(plottables[i].variances(), 0)
            plottables[i].set_variances(np.copy(baseline_variance))
        elif baseline_variance is None and plottables[i].variances() is not None:
            baseline_variance = np.nan_to_num(plottables[i].variances(), 0)
            plottables[i].set_variances(np.copy(baseline_variance))

        plottables[i].set_values(np.nansum([plottables[i].values(), _baseline], axis=0))
        plottables[i].set_values(np.where(_mask, np.nan, plottables[i].values()))
    return plottables


def _align_marker(
    marker,
    halign="center",
    valign="middle",
):
    # Taken from https://stackoverflow.com/a/26726237
    """
    From
    create markers with specified alignment.

    Parameters
    ----------

    marker : a valid marker specification.
      See mpl.markers

    halign : string, float {'left', 'center', 'right'}
      Specifies the horizontal alignment of the marker. *float* values
      specify the alignment in units of the markersize/2 (0 is 'center',
      -1 is 'right', 1 is 'left').

    valign : string, float {'top', 'middle', 'bottom'}
      Specifies the vertical alignment of the marker. *float* values
      specify the alignment in units of the markersize/2 (0 is 'middle',
      -1 is 'top', 1 is 'bottom').

    Returns
    -------

    marker_array : numpy.ndarray
      A Nx2 array that specifies the marker path relative to the
      plot target point at (0, 0).

    Notes
    -----
    The mark_array can be passed directly to ax.plot and ax.scatter, e.g.::

        ax.plot(1, 1, marker=align_marker('>', 'left'))

    """

    if isinstance(halign, (str)):
        halign = {
            "right": -1.0,
            "middle": 0.0,
            "center": 0.0,
            "left": 1.0,
        }[halign]

    if isinstance(valign, (str)):
        valign = {
            "top": -1.0,
            "middle": 0.0,
            "center": 0.0,
            "bottom": 1.0,
        }[valign]

    # Define the base marker
    bm = markers.MarkerStyle(marker)

    m_arr = bm.get_path().transformed(bm.get_transform()).vertices

    # Shift the marker vertices for the specified alignment.
    m_arr[:, 0] += halign / 2
    m_arr[:, 1] += valign / 2

    return Path(m_arr, bm.get_path().codes)


def _to_padded2d(h, variances=False):
    if np.array_equal(
        np.array(h.values().shape) + 2, np.array(h.values(flow=True).shape)
    ):
        padded = h.values(flow=True)
        padded_varis = h.variances(flow=True)
    else:
        vals_flow = h.values(flow=True)
        variances_flow = h.variances(flow=True)
        xpadlo, xpadhi = 1 - h.axes[0].traits.underflow, 1 - h.axes[0].traits.overflow
        ypadlo, ypadhi = 1 - h.axes[1].traits.underflow, 1 - h.axes[1].traits.overflow
        xpadhi_m, mypadhi_m = (-pad if pad != 0 else None for pad in [xpadhi, ypadhi])

        padded = np.zeros(
            (
                vals_flow.shape[0] + xpadlo + xpadhi,
                (vals_flow.shape[1] + ypadlo + ypadhi),
            )
        )
        padded_varis = padded.copy()
        padded[xpadlo:xpadhi_m, ypadlo:mypadhi_m] = vals_flow
        padded_varis[xpadlo:xpadhi_m, ypadlo:mypadhi_m] = variances_flow
    if variances:
        return padded, padded_varis
    return padded


class EnhancedPlottableHistogram(NumPyPlottableHistogram):
    """A container for histogram-like data, supporting error propagation and multiple plotting formats."""

    def __init__(
        self,
        values,
        *,
        edges=None,
        xoffsets=None,
        variances=None,
        yerr=None,
        w2method="poisson",
        kind=Kind.COUNT,
    ):
        """Initialize the EnhancedPlottableHistogram object with values, bin edges, optional variances, and error bars."""

        super().__init__(values.astype(float), edges, variances=variances, kind=kind)

        if isinstance(self._variances, np.ndarray) and self._variances.ndim == 0:
            self._variances = None

        self._binwnorm = False
        self._density = False

        self.baseline = np.zeros_like(self.values())
        self.centers = self.axes[0].edges.mean(axis=1)

        if xoffsets is not None:
            self.centers = self.edges_1d()[:-1] + xoffsets

        self.xerr_lo, self.xerr_hi = (
            self.centers - self.edges_1d()[:-1],
            self.edges_1d()[1:] - self.centers,
        )

        self.method = w2method
        self.yerr = yerr

        assert self.variances() is None or self.yerr is None
        if self.yerr is not None:
            self._errors_present = True
            self.yerr_lo, self.yerr_hi = yerr
        else:
            self._errors_present = False
            self.yerr_lo, self.yerr_hi = (
                np.zeros_like(self.values()),
                np.zeros_like(self.values()),
            )
        self._hash = None

    def __eq__(self, other):
        """Check equality between two EnhancedPlottableHistogram instances based on values(), variances(), and edges."""
        return np.all(
            [
                np.array_equal(self.values(), other.values()),
                np.array_equal(self.variances(), other.variances()),
                np.array_equal(self.edges_1d(), other.edges_1d()),
            ]
        )

    def __hash__(self):
        """Return a hash of the EnhancedPlottableHistogram object based on its values, variances, and edges."""
        if self._hash is None:
            self._hash = hash(
                (
                    tuple(self.values().flatten()),
                    tuple(
                        self.variances().flatten()
                        if self.variances() is not None
                        else []
                    ),
                    tuple(self.edges_1d().flatten()),
                )
            )
        return self._hash

    def __repr__(self):
        """Return string representation of the EnhancedPlottableHistogram object."""
        return f"EnhancedPlottableHistogram(values={self.values()}, edges={self.axes[0].edges}, variances={self.variances()})"

    def __add__(self, other):
        """
        Add two EnhancedPlottableHistograms.
        """
        if not isinstance(other, EnhancedPlottableHistogram):
            msg = (
                "Can only add EnhancedPlottableHistogram to EnhancedPlottableHistogram."
            )
            raise TypeError(msg)
        if len(self.axes) > 1:
            msg = "Addition of multi-dimensional histograms is not supported."
            raise NotImplementedError(msg)
        if self.axes != other.axes:
            msg = "Histograms must have the same axes to be added."
            raise ValueError(msg)
        if not np.allclose(self.centers, other.centers):
            msg = "Histograms must have the same bin centers to be added."
            raise ValueError(msg)
        if self.kind != Kind.COUNT or other.kind != Kind.COUNT:
            msg = "Histograms must be of kind COUNT to be added."
            raise TypeError(msg)
        if self.method != other.method:
            msg = f"Histograms must have the same w2method to be added. (got {self.method} and {other.method})"
            raise ValueError(msg)
        if self._errors_present or other._errors_present:
            msg = "Cannot add histograms with fixed errors."
            raise RuntimeError(msg)
        added_values = self.values() + other.values()
        added_variances = None
        if self._variances is not None and other._variances is not None:
            added_variances = self._variances + other._variances
        else:
            added_variances = None
        return EnhancedPlottableHistogram(
            added_values,
            edges=self.axes[0].edges,
            variances=added_variances,
            kind=self.kind,
            w2method=self.method,
        )

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            msg = "Factor must be a scalar (int or float)."
            raise TypeError(msg)
        if len(self.axes) > 1:
            msg = "Scaling of multi-dimensional histograms is not supported."
            raise NotImplementedError(msg)
        if self._errors_present:
            msg = "Cannot multiply a histogram with fixed errors."
            raise RuntimeError(msg)
        return EnhancedPlottableHistogram(
            self.values() * factor,
            edges=self.axes[0].edges,
            variances=(
                self.variances() * factor**2 if self.variances() is not None else None
            ),
            kind=self.kind,
            w2method=self.method,
        )

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def set_values(self, values: np.typing.NDArray[Any]) -> None:
        """Set the values of the histogram."""
        self._values = values

    def set_variances(self, variances: np.typing.NDArray[Any] | None) -> None:
        """Set the variances of the histogram."""
        self._variances = variances

    def edges_1d(self):
        """Return the edges of the first axis as a 1D array."""
        edges = np.empty(len(self.axes[0].edges) + 1, dtype=float)
        edges[0] = self.axes[0].edges[0][0]
        edges[1:] = [self.axes[0].edges[i][1] for i in range(len(self.axes[0]))]
        return edges

    def is_unweighted(self):
        """Check if the histogram is unweighted."""
        if self.variances() is None:
            msg = "Variances are not set, cannot determine if histogram is unweighted."
            raise RuntimeError(msg)
        return np.allclose(self.variances(), np.around(self.variances()))

    def errors(self, method=None, assume_variances_equal_values=False):
        """
        Calculate y-errors using a specified or inferred method ('poisson', 'sqrt', or callable).
        The method should have signature method(sumw, sumw2) -> (lower_abs_val, upper_abs_val).
        If variances is None and assume_variances_equal_values is True, the values will be used as variances.
        """
        if self._errors_present:
            return
        if assume_variances_equal_values and self.variances() is None:
            self._variances = self.values()
        if self.variances() is None:
            return
        if np.allclose(self.variances(), 0):
            self.yerr_lo = np.zeros_like(self.values())
            self.yerr_hi = np.zeros_like(self.values())
            self._errors_present = True
            return
        assert method in ["poisson", "sqrt", None] or callable(method)
        if method is None:
            method = self.method
            if method is None:
                method = "poisson" if self.is_unweighted() else "sqrt"

        def sqrt_method(values, variances):
            return values - np.sqrt(variances), values + np.sqrt(variances)

        def calculate_relative(method_fcn, variances):
            return np.abs(method_fcn(self.values(), variances) - self.values())

        if method == "sqrt":
            self.yerr_lo, self.yerr_hi = calculate_relative(
                sqrt_method, self.variances()
            )
        elif method == "poisson":
            try:
                from .error_estimation import poisson_interval  # noqa: PLC0415

                self.yerr_lo, self.yerr_hi = calculate_relative(
                    poisson_interval, self.variances()
                )
            except ImportError:
                warnings.warn(
                    "Integer weights indicate poissonian data. Will calculate "
                    "Garwood interval if ``scipy`` is installed. Otherwise errors "
                    "will be set to ``sqrt(w2)``.",
                    stacklevel=2,
                )
                self.yerr_lo, self.yerr_hi = calculate_relative(
                    sqrt_method, self.variances()
                )
        elif callable(method):
            self.yerr_lo, self.yerr_hi = calculate_relative(method, self.variances())
        else:
            msg = "``method'' needs to be a callable or 'poisson' or 'sqrt'."
            raise RuntimeError(msg)
        self.yerr_lo = np.nan_to_num(self.yerr_lo, 0)
        self.yerr_hi = np.nan_to_num(self.yerr_hi, 0)

    def fixed_errors(self, yerr_lo, yerr_hi):
        """Manually assign fixed lower and upper y-errors."""
        self.yerr_lo = yerr_lo
        self.yerr_hi = yerr_hi
        self._errors_present = True

    def scale(self, scale):
        """Apply a scaling factor to values and variances."""
        if self._errors_present:
            msg = "Cannot recompute errors when errors already present."
            raise RuntimeError(msg)
        self._values *= scale
        if self.variances() is not None:
            self._variances *= scale * scale
        return self

    def flat_scale(self, scale):
        """Multiply values and errors by a flat scalar."""
        self.errors()
        self._errors_present = True
        self._values *= scale
        self.yerr_lo *= scale
        self.yerr_hi *= scale
        return self

    def binwnorm(self):
        """Normalize values and errors by the bin widths."""
        if self._binwnorm:
            return self
        self._binwnorm = True
        return self.flat_scale(1 / np.diff(self.edges_1d()))

    def density(self):
        """Normalize values and errors by the area."""
        if self._density:
            return self
        self._density = True
        return self.flat_scale(1 / np.sum(np.diff(self.edges_1d()) * self.values()))

    def to_stairs(self):
        """Export data in a dictionary format suitable for stair plots (e.g., step histograms)."""
        return {
            "values": self.values(),
            "edges": self.edges_1d(),
            "baseline": self.baseline,
        }

    def to_stairband(self):
        """Export upper and lower stair-step error bands for uncertainty visualization."""
        self.errors()
        return {
            "values": self.values() + self.yerr_hi,
            "edges": self.edges_1d(),
            "baseline": self.values() - self.yerr_lo,
        }

    def to_errorbar(self):
        """Export data in a dictionary format for error bar plotting (e.g., matplotlib 'errorbar')."""
        self.errors()

        # Convert single-element arrays to scalars to avoid NumPy deprecation warnings
        def _maybe_scalar(arr):
            """Convert single-element arrays to scalars."""
            if isinstance(arr, np.ndarray) and arr.ndim > 0 and arr.size == 1:
                return arr.item()
            return arr

        # Handle yerr and xerr - ensure they're properly formatted for matplotlib
        yerr = [self.yerr_lo, self.yerr_hi]
        xerr = [self.xerr_lo, self.xerr_hi]

        # For single-element arrays, ensure error arrays are also scalars or proper shape
        if self.yerr_lo.size == 1 and self.yerr_hi.size == 1:
            # Convert to the shape matplotlib expects: [lower_errors, upper_errors]
            yerr = np.array(
                [[_maybe_scalar(self.yerr_lo)], [_maybe_scalar(self.yerr_hi)]]
            )

        if self.xerr_lo.size == 1 and self.xerr_hi.size == 1:
            xerr = np.array(
                [[_maybe_scalar(self.xerr_lo)], [_maybe_scalar(self.xerr_hi)]]
            )

        return {
            "x": _maybe_scalar(self.centers),
            "y": _maybe_scalar(self.values()),
            "yerr": yerr,
            "xerr": xerr,
        }


def _hist_legend(ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    handles, labels = ax.get_legend_handles_labels()
    new_handles = [
        Line2D([], [], c=h.get_edgecolor()) if isinstance(h, mpl.patches.Polygon) else h
        for h in handles
    ]
    ax.legend(handles=new_handles[::-1], labels=labels[::-1], **kwargs)

    return ax


def _is_debug_marker(artist):
    """Check if an artist is a debug marker that should be excluded from overlap detection."""
    DEBUG_LABELS = {"overlap vertices", "overlapping vertices", "overlap bbox"}
    return hasattr(artist, "get_label") and artist.get_label() in DEBUG_LABELS


def _overlap(ax, bboxes, get_vertices=False, exclude_texts=None):
    """
    Find overlap of bboxes (in display coordinates) with drawn elements on axes.

    Collects vertices from lines and patches, bounding boxes from rectangles and texts.
    Transforms everything to display coordinates for overlap checking.
    Logs summary in data coordinates for understandability.

    Returns number of overlapping points/bboxes.
    If get_vertices, also return vertices in data coordinates.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to check
    bboxes : Bbox or list of Bbox
        Bounding boxes to check for overlap
    get_vertices : bool, optional
        If True, also return vertices in data coordinates
    exclude_texts : list, optional
        List of Text objects to exclude from overlap detection (to avoid self-overlap)
    """
    if not isinstance(bboxes, list):
        bboxes = [bboxes]

    if exclude_texts is None:
        exclude_texts = []

    # Ensure canvas is drawn before collecting vertices
    fig = ax.figure
    if fig is not None:
        fig.canvas.draw()

    lines_display = []
    bboxes_display = []

    # Collect vertices from lines (Line2D)
    for handle in ax.lines:
        if isinstance(handle, Line2D) and not _is_debug_marker(handle):
            xdata, ydata = handle.get_xdata(), handle.get_ydata()
            data_points = np.column_stack((xdata, ydata))
            vertices_display = ax.transData.transform(data_points)
            lines_display.append(vertices_display)

    # Collect vertices from collections (e.g., scatter plots, fill_between)
    for handle in ax.collections:
        if _is_debug_marker(handle):
            continue

        if isinstance(handle, plt.matplotlib.collections.PathCollection):
            # Scatter plots: use offsets as data points
            vertices_display = ax.transData.transform(handle.get_offsets())
            lines_display.append(vertices_display)
        elif hasattr(handle, "get_paths"):
            # Poly collections like fill_between: use path vertices
            for path in handle.get_paths():
                vertices_display = ax.transData.transform(path.vertices)
                lines_display.append(vertices_display)
        elif hasattr(handle, "get_offsets"):
            # Fallback for other collections
            vertices_display = ax.transData.transform(handle.get_offsets())
            lines_display.append(vertices_display)

    # Collect bboxes from patches
    for handle in ax.patches:
        if _is_debug_marker(handle):
            continue
        if isinstance(handle, Patch):
            if hasattr(handle, "get_bbox") and isinstance(handle, Rectangle):
                # Rectangle bbox in display coords (for bar plots)
                bbox_patch = handle.get_bbox().transformed(handle.get_data_transform())
                bboxes_display.append(bbox_patch)
            # Get vertices from patch path
            path = handle.get_path()
            if len(path.vertices) > 0:
                vertices_display = ax.transData.transform(path.vertices)
                lines_display.append(vertices_display)

                # For step/line paths, also sample intermediate points along edges
                # This ensures we detect overlap with horizontal/vertical segments
                if len(path.vertices) > 1:
                    for i in range(len(path.vertices) - 1):
                        v1 = path.vertices[i]
                        v2 = path.vertices[i + 1]
                        # Sample 5 intermediate points along each edge
                        t = np.linspace(0, 1, 7)[
                            1:-1
                        ]  # Exclude endpoints (already in vertices)
                        interpolated = v1 + (v2 - v1) * t[:, np.newaxis]
                        interpolated_display = ax.transData.transform(interpolated)
                        lines_display.append(interpolated_display)

    # Collect bboxes from texts (excluding specified text objects to avoid self-overlap)
    for handle in ax.texts:
        if isinstance(handle, Text) and handle not in exclude_texts:
            bboxes_display.append(handle.get_window_extent())

    # Concatenate all vertices in display coordinates
    all_vertices_display = (
        np.concatenate(lines_display) if lines_display else np.empty((0, 2))
    )

    # Transform to data coordinates for logging
    all_vertices_data = ax.transData.inverted().transform(all_vertices_display)
    bboxes_data = [bbox.transformed(ax.transData.inverted()) for bbox in bboxes]

    logger.info(
        f"Found {len(all_vertices_data)} vertices from plot elements in data coordinates:"
    )
    if len(all_vertices_data) > 0:
        logger.debug(
            f"  Bounds: x=[{all_vertices_data[:, 0].min():.3f}, {all_vertices_data[:, 0].max():.3f}], "
            f"y=[{all_vertices_data[:, 1].min():.3f}, {all_vertices_data[:, 1].max():.3f}]"
        )
        logger.debug(
            f"  Shape: {all_vertices_data.shape}, x_min: {all_vertices_data[:, 0].min():.3f}, x_max: {all_vertices_data[:, 0].max():.3f}, y_min: {all_vertices_data[:, 1].min():.3f}, y_max: {all_vertices_data[:, 1].max():.3f}"
        )
    else:
        logger.debug("  No vertices found.")

    logger.info(
        f"Annotation bboxes extents in data coordinates: {[f'x=[{b.x0:.3f}, {b.x1:.3f}], y=[{b.y0:.3f}, {b.y1:.3f}]' for b in bboxes_data]}"
    )

    # Calculate overlap in display coordinates
    overlap_count = 0
    overlapping_vertices_data = []  # Track all vertices that contribute to overlap in data coordinates
    for bbox in bboxes:
        contained = bbox.count_contains(all_vertices_display)
        if contained > 0:
            # Find which vertices are contained
            contained_mask = np.array(
                [bbox.contains(x, y) for x, y in all_vertices_display]
            )
            overlapping_vertices_data.extend(all_vertices_data[contained_mask])
        overlap_count += contained + bbox.count_overlaps(bboxes_display)

    # Also check if data vertices are above the text bbox (occluding it)
    # This catches cases where the histogram bars cover the text
    for bbox in bboxes:
        if len(all_vertices_display) > 0:
            # Check if any vertices are in the same x-range but above the bbox
            in_x_range = (all_vertices_display[:, 0] >= bbox.x0) & (
                all_vertices_display[:, 0] <= bbox.x1
            )
            above_bbox = all_vertices_display[:, 1] > bbox.y1
            occluding = in_x_range & above_bbox
            if occluding.any():
                overlap_count += occluding.sum()
                # Collect occluding vertices in data coordinates
                overlapping_vertices_data.extend(all_vertices_data[occluding])

    logger.info(f"Overlap count: {overlap_count}")
    if overlapping_vertices_data:
        logger.warning(
            f"Total overlapping vertices: {len(overlapping_vertices_data)} in data coordinates: {overlapping_vertices_data}"
        )
    else:
        logger.warning("No overlapping vertices found")

    if _DEBUG_OVERLAP:
        # Save current axis limits to prevent debug markers from affecting them
        current_xlim, current_ylim = ax.get_xlim(), ax.get_ylim()

        # Remove existing debug markers
        for artist in ax.patches + ax.collections + ax.lines:
            if _is_debug_marker(artist):
                artist.remove()

        # Plot all vertices used in overlap detection
        if len(all_vertices_data) > 0:
            ax.scatter(
                all_vertices_data[:, 0],
                all_vertices_data[:, 1],
                color="red",
                s=20,
                alpha=0.3,
                label="overlap vertices",
            )

        # Plot annotation bboxes as rectangles
        for bbox in bboxes_data:
            rect = mpl.patches.Rectangle(
                (bbox.x0, bbox.y0),
                bbox.width,
                bbox.height,
                linewidth=1,
                edgecolor="blue",
                facecolor="none",
                alpha=0.3,
                label="overlap bbox",
            )
            ax.add_patch(rect)
        # Plot occluding vertices as fat blue pluses
        if overlapping_vertices_data:
            overlapping_array = np.array(overlapping_vertices_data)
            ax.scatter(
                overlapping_array[:, 0],
                overlapping_array[:, 1],
                color="blue",
                s=100,
                alpha=0.9,
                marker="+",
                linewidth=3,
                label="overlapping vertices",
                zorder=10,  # Plot on top
            )

        # Plot overlapping vertices with emphasis
        if overlapping_vertices_data:
            overlapping_array = np.array(overlapping_vertices_data)
            ax.scatter(
                overlapping_array[:, 0],
                overlapping_array[:, 1],
                color="blue",
                s=100,
                alpha=0.9,
                marker="+",
                linewidth=3,
                label="overlapping vertices",
                zorder=10,
            )

        # Restore original axis limits (don't let debug markers affect scaling)
        ax.set_xlim(current_xlim)
        ax.set_ylim(current_ylim)

    if get_vertices:
        return overlap_count, all_vertices_data
    return overlap_count


def _calculate_optimal_scaling(ax, bboxes, exclude_texts=None):
    """
    Calculate the optimal y-axis scaling factor to eliminate annotation overlaps.

    Uses display-based margins (inches) to ensure consistent visual spacing across
    different figure sizes and data ranges. Caps extreme scaling at 2x to prevent
    axis distortion in edge cases.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes containing the plot and annotations
    bboxes : list of matplotlib.transforms.Bbox
        Annotation bounding boxes in display coordinates
    exclude_texts : list, optional
        Text objects to exclude from overlap detection

    Returns
    -------
    float
        Scaling factor for y-axis (1.0 if no scaling needed, max 2.0)
    """
    if not isinstance(bboxes, list):
        bboxes = [bboxes]

    # Check for overlaps
    overlap_count, vertices = _overlap(
        ax, bboxes, get_vertices=True, exclude_texts=exclude_texts
    )
    if overlap_count == 0:
        return 1.0

    # Convert bboxes to data coordinates and filter degenerate ones
    bboxes_data = [bbox.transformed(ax.transData.inverted()) for bbox in bboxes]
    bboxes_data = [b for b in bboxes_data if b.y1 > b.y0]
    if not bboxes_data:
        return 1.0

    # Get annotation properties
    tallest_bbox = max(bboxes_data, key=lambda b: b.y1)
    annotation_height = tallest_bbox.y1 - tallest_bbox.y0
    lowest_bbox_y0 = min(b.y0 for b in bboxes_data)

    # Get axis properties
    current_ylim = ax.get_ylim()
    current_axis_height = current_ylim[1] - current_ylim[0]
    annotation_fraction = annotation_height / current_axis_height

    # Find maximum y-coordinate of data (including patches and collections)
    max_y = vertices[:, 1].max() if len(vertices) > 0 else current_ylim[0]

    # Check patches (e.g., histogram bars) - skip debug markers
    for handle in ax.patches:
        if isinstance(handle, Rectangle) and not _is_debug_marker(handle):
            max_y = max(max_y, handle.get_bbox().y1)

    # Check collections (e.g., fill_between) - skip debug markers
    for handle in ax.collections:
        if hasattr(handle, "get_datalim") and not _is_debug_marker(handle):
            max_y = max(max_y, handle.get_datalim(ax.transData).y1)

    logger.debug(
        f"Current ylim: {current_ylim}, annotation_fraction: {annotation_fraction:.3f}, "
        f"max_y: {max_y:.3f}, lowest_bbox_y0: {lowest_bbox_y0:.3f}"
    )

    # Calculate margin in display units (inches) based on annotation size
    fig = ax.figure
    if fig is None:
        # Fallback: use data-coordinate margin
        margin_data = (
            0.025 if annotation_fraction <= 0.15 else 0.05
        ) * current_axis_height
    else:
        fig.canvas.draw()
        axes_height_inches = ax.get_position().height * fig.get_figheight()
        margin_inches = (
            0.025 if annotation_fraction <= 0.15 else 0.05
        ) * axes_height_inches
        margin_data = margin_inches * (current_axis_height / axes_height_inches)
        logger.debug(
            f"margin: {margin_inches:.3f} inches = {margin_data:.3f} data units"
        )

    # Calculate required scaling
    # After scaling by s: bbox.y0_new = bbox.y0 * s
    # We need: bbox.y0_new >= max_y + margin_data
    # Therefore: s >= (max_y + margin_data) / bbox.y0

    if lowest_bbox_y0 <= 0:
        required_scaling = 1.01  # Edge case: bbox at or below zero
    elif lowest_bbox_y0 > max_y + margin_data:
        required_scaling = 1.0  # Already clear
    else:
        required_scaling = (max_y + margin_data) / lowest_bbox_y0
        # Cap at 2x to prevent extreme distortion (e.g., very short figures)
        if required_scaling > 2.0:
            required_scaling = 2.0
            logger.debug("Capping scaling at 2.0x to prevent extreme distortion")

    scaling = max(1.0, required_scaling)
    logger.debug(f"Required scaling: {scaling:.3f}")
    return scaling


def _draw_leg_bbox(ax):
    """
    Draw legend() and fetch its bbox
    """
    fig = ax.figure
    leg = ax.get_legend()
    if leg is None:
        leg = next(
            (
                c
                for c in ax.get_children()
                if isinstance(c, plt.matplotlib.legend.Legend)
            ),
            None,
        )
    if leg is None:
        return []

    fig.canvas.draw()
    return [leg.get_frame().get_bbox()]


def _draw_text_bbox(ax):
    """
    Draw text objects and fetch their bboxes

    Returns
    -------
    tuple
        (bboxes, text_objects) - List of bboxes and corresponding text objects
    """
    fig = ax.figure
    textboxes = [k for k in ax.get_children() if isinstance(k, (AnchoredText, Text))]
    logger.debug(f"_draw_text_bbox: Found {len(textboxes)} text objects")
    logger.debug(f"_draw_text_bbox: Found {textboxes}")
    if not textboxes:
        return [], []

    fig.canvas.draw()
    bboxes = []
    for box in textboxes:
        bboxes.append(box.get_tightbbox(fig.canvas.renderer))
    logger.debug(f"_draw_text_bbox: Returning {len(bboxes)} bboxes")
    return bboxes, textboxes
