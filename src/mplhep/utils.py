from __future__ import annotations

import copy
import warnings
from numbers import Real
from typing import TYPE_CHECKING, Any, Iterable, Sequence

import numpy as np
from uhi.numpy_plottable import ensure_plottable_histogram
from uhi.typing.plottable import PlottableAxis, PlottableHistogram
from matplotlib import markers
from matplotlib.path import Path

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
        raise TypeError("Cannot give bins with existing histogram")
    else:
        hist_obj = ensure_plottable_histogram((hist, *bins))

    if len(hist_obj.axes) not in {1, 2}:
        raise ValueError("Must have only 1 or 2 axes")

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
    if (isinstance(H, list) or isinstance(H, np.ndarray)) and not isinstance(
        H[0], (Real)
    ):
        return _process_histogram_parts_iter(H, *bins)
    else:
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
    elif hasattr(axis, "title"):
        return axis.title
    elif hasattr(axis, "name"):
        return axis.name

    # No axis title found
    return ""


class Plottable:
    def __init__(self, values, *, edges=None, variances=None, yerr=None):
        self._values = np.array(values).astype(float)
        self.variances = None
        self._variances = None
        if variances is not None:
            self._variances = np.array(variances).astype(float)
            self.variances = np.array(variances).astype(float)
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
            raise RuntimeError(
                "``method'' needs to be a callable or 'poisson' or 'sqrt'."
            )
        self.yerr_lo = np.nan_to_num(self.yerr_lo, 0)
        self.yerr_hi = np.nan_to_num(self.yerr_hi, 0)

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
        xpadhi_m, mypadhi_m = [-pad if pad != 0 else None for pad in [xpadhi, ypadhi]]

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
    else:
        return padded
