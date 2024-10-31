from __future__ import annotations

import copy
import inspect
import warnings
from numbers import Real
from typing import TYPE_CHECKING, Any, Iterable, Sequence

import numpy as np
from matplotlib import markers
from matplotlib.path import Path
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
        out[1:] = [axis[i][1] for i in range(len(axis))]  # type: ignore[index]
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
        hist_obj = hist
    else:
        hist_obj = ensure_plottable_histogram((hist, *bins))

    if len(hist_obj.axes) not in {1, 2}:
        msg = "Must have only 1 or 2 axes"
        raise ValueError(msg)

    return hist_obj


def process_histogram_parts(
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


def _process_histogram_parts_iter(
    hists: Iterable[ArrayLike] | Iterable[PlottableHistogram],
    *bins: Sequence[float | None],
) -> Iterable[PlottableHistogram]:
    original_bins: tuple[Sequence[float], ...] = bins  # type: ignore[assignment]

    for hist in hists:
        h = hist_object_handler(hist, *bins)
        current_bins: tuple[Sequence[float], ...] = tuple(
            get_plottable_protocol_bins(a)[0]  # type: ignore[misc]
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


def get_histogram_axes_title(axis: Any) -> str:
    if hasattr(axis, "label"):
        return axis.label
    # Classic support for older hist, deprecated
    if hasattr(axis, "title"):
        return axis.title
    if hasattr(axis, "name"):
        return axis.name

    # No axis title found
    return ""


def get_plottables(
    H,
    bins=None,
    yerr: ArrayLike | bool | None = None,
    w2=None,
    w2method=None,
    flow="hint",
    stack=False,
    density=False,
    binwnorm=None,
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

    Returns
    -------
    plottables : list of Plottable
        Processed histogram objects ready for plotting.
    (flow_bins, underflow, overflow) : tuple
        Flow bin information for handling underflow and overflow values.
    """
    plottables = []
    flow_bins = np.copy(bins)

    hists = list(process_histogram_parts(H, bins))
    final_bins, _ = get_plottable_protocol_bins(hists[0].axes[0])

    for h in hists:
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
            plottables.append(Plottable(value, edges=final_bins, variances=variance))
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
            plottables.append(Plottable(value, edges=flow_bins, variances=variance))
        elif flow == "sum":
            if underflow > 0:
                value[0] += underflow
                if has_variances:
                    variance[0] += underflowv
            if overflow > 0:
                value[-1] += overflow
                if has_variances:
                    variance[-1] += overflowv
            plottables.append(Plottable(value, edges=final_bins, variances=variance))
        else:
            plottables.append(Plottable(value, edges=final_bins, variances=variance))

    if w2 is not None:
        for _w2, _plottable in zip(
            w2.reshape(len(plottables), len(final_bins) - 1), plottables
        ):
            _plottable.variances = _w2
            _plottable.method = w2method

    if w2 is not None and yerr is not None:
        msg = "Can only supply errors or w2"
        raise ValueError(msg)

    yerr_plottables(plottables, final_bins, yerr)
    norm_stack_plottables(plottables, final_bins, stack, density, binwnorm)

    return plottables, (flow_bins, underflow, overflow)


def yerr_plottables(plottables, bins, yerr=None):
    """
    Calculate and format y-axis errors for Plottables.

    Parameters
    ----------
    plottables : list of Plottable
        List of Plottable objects.
    bins : iterable
        Plottable bins.
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
                _plottable.errors()
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


def norm_stack_plottables(plottables, bins, stack=False, density=False, binwnorm=None):
    """
    Normalize and stack histogram data with optional density or bin-width normalization.

    Parameters
    ----------
    plottables : list of Plottable
        List of Plottable objects.
    bins : iterable
        Plottable bins.
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
                np.array([plottable.values for plottable in plottables]), axis=0
            )
            for plottable in plottables:
                plottable.flat_scale(1.0 / np.sum(np.diff(bins) * _total))
        else:
            for plottable in plottables:
                plottable.density = True
    elif binwnorm is not None:
        for plottable, norm in zip(
            plottables, np.broadcast_to(binwnorm, (len(plottables),))
        ):
            plottable.flat_scale(norm)
            plottable.binwnorm()

    # Stack
    if stack and len(plottables) > 1:
        from .utils import stack as stack_fun

        plottables = stack_fun(*plottables)


class Plottable:
    def __init__(self, values, *, edges=None, variances=None, yerr=None):
        self._values = np.array(values).astype(float)
        self.variances = None
        self._variances = None
        self._has_variances = False
        if variances is not None:
            self._variances = np.array(variances).astype(float)
            self.variances = np.array(variances).astype(float)
            self._has_variances = True
        self._density = False

        self.values = np.array(values).astype(float)
        self.baseline = np.zeros_like(self.values)
        self.edges = np.array(edges)
        if self.edges is None:
            self.edges = np.arange(len(values) + 1)
        self.centers = self.edges[:-1] + np.diff(self.edges) / 2
        self.method = "poisson"

        self.yerr = yerr
        assert self.variances is None or self.yerr is None
        if self.yerr is not None:
            self._errors_present = True
            self.yerr_lo, self.yerr_hi = yerr
        else:
            self._errors_present = False
            self.yerr_lo, self.yerr_hi = (
                np.zeros_like(self.values),
                np.zeros_like(self.values),
            )

    def __eq__(self, other):
        return np.all(
            [
                np.array_equal(getattr(self, att), getattr(other, att))
                for att in ["values", "variances", "edges"]
            ]
        )

    def __repr__(self):
        return f"Plottable({self.values}, {self.edges}, {self.variances}"

    def errors(self, method=None):
        """Calculate errors with a provided method(w, w2) -> (lower_abs_val, upper_abs_val)"""
        assert method in ["poisson", "sqrt", None] or callable(method)
        variances = self.variances if self.variances is not None else self.values
        if method is None:
            method = self.method
            if method is None:
                if np.allclose(variances, np.around(variances)):
                    method = "poisson"
                else:
                    method = "sqrt"

        if self._errors_present:
            return

        def sqrt_method(values, _):
            return values - np.sqrt(values), values + np.sqrt(values)

        def calculate_relative(method_fcn, variances):
            return np.abs(method_fcn(self.values, variances) - self.values)

        if method == "sqrt":
            self.yerr_lo, self.yerr_hi = calculate_relative(sqrt_method, variances)
        elif method == "poisson":
            try:
                from .error_estimation import poisson_interval

                self.yerr_lo, self.yerr_hi = calculate_relative(
                    poisson_interval, variances
                )
            except ImportError:
                warnings.warn(
                    "Integer weights indicate poissonian data. Will calculate "
                    "Garwood interval if ``scipy`` is installed. Otherwise errors "
                    "will be set to ``sqrt(w2)``.",
                    stacklevel=2,
                )
                self.yerr_lo, self.yerr_hi = calculate_relative(sqrt_method, variances)
        elif callable(method):
            self.yerr_lo, self.yerr_hi = calculate_relative(method, variances)
        else:
            msg = "``method'' needs to be a callable or 'poisson' or 'sqrt'."
            raise RuntimeError(msg)
        self.yerr_lo = np.nan_to_num(self.yerr_lo, 0)
        self.yerr_hi = np.nan_to_num(self.yerr_hi, 0)
        self.variances = self.values if not self._has_variances else self.variances

    def fixed_errors(self, yerr_lo, yerr_hi):
        self.yerr_lo = yerr_lo
        self.yerr_hi = yerr_hi
        self._errors_present = True

    def scale(self, scale):
        """Scale values and variances to match, errors are recalculated"""
        self.values *= scale
        if self.variances is not None:
            self.variances *= scale * scale
        self.errors()
        return self

    def flat_scale(self, scale):
        """Scale values by a flat coefficient. Errors are scaled directly to match"""
        self.errors()
        self._errors_present = True
        self.values *= scale
        self.yerr_lo *= scale
        self.yerr_hi *= scale
        return self

    def binwnorm(self):
        """Scale values by a flat coefficient. Errors are scaled directly to match"""
        self.errors()
        self._errors_present = True
        self.values /= np.diff(self.edges)
        self.yerr_lo /= np.diff(self.edges)
        self.yerr_hi /= np.diff(self.edges)
        return self

    def reset(self):
        """Reset to original values"""
        self.values = copy.deepcopy(self._values)
        self.variances = copy.deepcopy(self._variances)
        self._density = False
        self.errors()
        return self

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, boolean: bool):
        if boolean and not self._density:
            self.flat_scale(1 / np.sum(np.diff(self.edges) * self.values))
        if not boolean:
            self.reset()
        self._density = boolean

    def to_stairs(self):
        return {"values": self.values, "edges": self.edges, "baseline": self.baseline}

    def to_stairband(self):
        self.errors()
        return {
            "values": self.values + self.yerr_hi,
            "edges": self.edges,
            "baseline": self.values - self.yerr_lo,
        }

    def to_errorbar(self):
        self.errors()
        return {
            "x": self.centers,
            "y": self.values,
            "yerr": [self.yerr_lo, self.yerr_hi],
        }


def stack(*plottables):
    baseline = np.nan_to_num(copy.deepcopy(plottables[0].values), 0)
    for i in range(1, len(plottables)):
        _mask = np.isnan(plottables[i].values)
        _baseline = copy.deepcopy(baseline)
        _baseline[_mask] = np.nan
        plottables[i].baseline = _baseline
        baseline += np.nan_to_num(plottables[i].values, 0)
        plottables[i].values = np.nansum([plottables[i].values, _baseline], axis=0)
        plottables[i].values[_mask] = np.nan
    return plottables


def align_marker(
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


def to_padded2d(h, variances=False):
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
