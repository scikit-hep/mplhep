from typing import Optional, TYPE_CHECKING, Iterable, cast, Any, Sequence, Tuple

import numpy as np
import enum

if TYPE_CHECKING:
    from uhi.typing.plottable import (
        PlottableHistogram,
        PlottableAxisGeneric,
        PlottableAxis,
        PlottableTraits,
    )

    # Only added in NumPy 1.20
    ArrayLike = Any


class Kind(str, enum.Enum):
    COUNT = "COUNT"
    MEAN = "MEAN"


class Traits:
    __slots__ = ("circular", "discrete")

    def __init__(self, circular: bool = False, discrete: bool = False) -> None:
        self.circular = circular
        self.discrete = discrete


if TYPE_CHECKING:
    _traits: PlottableTraits = cast(Traits, None)


class NumPyPlottableAxis:
    def __init__(self, vals: np.ndarray) -> None:
        self.traits: "PlottableTraits" = Traits()
        self.vals = vals

    def __getitem__(self, index: int) -> Tuple[float, float]:
        """
        Get the pair of edges (not discrete) or bin label (discrete).
        """

        return tuple(self.vals[index])  # type: ignore

    def __len__(self) -> int:
        """
        Return the number of bins (not counting flow bins, which are ignored
        for this Protocol currently).
        """
        return self.vals.shape[0]

    def __eq__(self, other: Any) -> bool:
        return np.allclose(self.vals, other.vals)


if TYPE_CHECKING:
    _axis: PlottableAxisGeneric[Tuple[float, float]] = cast(NumPyPlottableAxis, None)


def _bin_helper(shape: int, bins: "np.ndarray | None") -> NumPyPlottableAxis:
    if bins is None:
        return NumPyPlottableAxis(
            np.array([np.arange(0, shape), np.arange(1, shape + 1)]).T
        )
    elif bins.ndim == 2:
        return NumPyPlottableAxis(bins)
    elif bins.ndim == 1:
        return NumPyPlottableAxis(np.array([bins[:-1], bins[1:]]).T)
    else:
        raise ValueError(
            "Bins not understood, should be 2d array of min/max edges or 1D array of edges or None"
        )


# TODO: Support bins for ND histograms
class NumPyPlottableProtocol:
    def __init__(
        self,
        hist: np.ndarray,
        *bins: "np.ndarray | None",
        variances: Optional[np.ndarray] = None,
        kind: str = Kind.COUNT,
    ) -> None:

        self._values = hist
        self._variances = variances
        self.kind = kind

        self.axes: "Sequence[PlottableAxis]" = [
            _bin_helper(shape, b) for shape, b in zip(hist.shape, bins)
        ]

    def values(self) -> np.ndarray:
        return self._values

    def counts(self) -> np.ndarray:
        return self._values

    def variances(self) -> Optional[np.ndarray]:
        return self._variances


if TYPE_CHECKING:
    # Verfiy that the above class is a valid PlottableHistogram
    _: PlottableHistogram = cast(NumPyPlottableProtocol, None)


def get_plottable_protocol_bins(axis: "PlottableAxis") -> np.ndarray:
    out = np.empty(len(axis) + 1)
    assert isinstance(
        axis[0], tuple
    ), f"Currently only support non-discrete axes {axis}"
    # TODO: Support discreete axes
    out[0] = axis[0][0]
    out[1:] = [axis[i][1] for i in range(len(axis))]  # type: ignore
    return out


def hist_object_handler(
    hist: "ArrayLike | PlottableHistogram", *bins: "Sequence[float] | None"
) -> "PlottableHistogram":
    if hasattr(hist, "values") and hasattr(hist, "axes") and hasattr(hist, "variances"):
        # Protocol
        if len(hist.axes) not in {1, 2}:
            raise ValueError("Must have only 1 or 2 axes")
        if not all(b is None for b in bins):
            raise ValueError("Must not specify bins with a PlottableHistogram object")
        return hist

    elif hasattr(hist, "to_numpy"):
        # Generic (possibly Uproot 4)
        if not all(b is None for b in bins):
            raise ValueError("Must not specify bins with a hist.to_numpy() object")
        _tup = hist.to_numpy(flow=False)  # type: ignore
        if len(_tup) not in {2, 3}:
            raise ValueError("to_numpy() method not understood")
        else:
            return NumPyPlottableProtocol(*_tup)

    elif hasattr(hist, "numpy"):
        # uproot/TH1
        if not all(b is None for b in bins):
            raise ValueError("Must not specify bins with a hist.numpy() object")
        _tup = hist.numpy()  # type: ignore
        if len(_tup) not in {2, 3}:
            raise ValueError("numpy() method not understood")
        else:
            return NumPyPlottableProtocol(*_tup)

    elif isinstance(hist, tuple):
        # Numpy histogram tuple
        if not all(b is None for b in bins):
            raise ValueError("Must not specify bins with a NumPy tuple object")
        if len(hist) not in {2, 3}:
            raise ValueError("numpy() method not understood")
        return NumPyPlottableProtocol(*hist)

    else:
        return NumPyPlottableProtocol(
            np.asarray(hist),
            *(np.asarray(b, dtype=float) for b in bins if b is not None),
        )


def process_histogram_parts(
    H: "ArrayLike | PlottableHistogram | Iterable[ArrayLike] | Iterable[PlottableHistogram]",
    *bins: "Sequence[float] | None",
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

        *bins : Sequence[float], optional
            Histogram bins, if not part of ``h``. One iterable per histogram dimension.

    Returns
    -------
        values, bins: Iterator[Tuple[np.ndarray, np.ndarray]]

    """

    # Try to understand input
    if not isinstance(H, list) or isinstance(H[0], (float, int)):
        return _process_histogram_parts_iter((H,), *bins)
    else:
        return _process_histogram_parts_iter(H, *bins)


def _process_histogram_parts_iter(
    hists: "Iterable[ArrayLike] | Iterable[PlottableHistogram]",
    *bins: "Sequence[float] | None",
) -> "Iterable[PlottableHistogram]":
    original_bins: Tuple[Sequence[float], ...] = bins  # type: ignore

    for hist in hists:
        h = hist_object_handler(hist, *bins)
        current_bins: Tuple[Sequence[float], ...] = tuple(get_plottable_protocol_bins(a) for a in h.axes)  # type: ignore
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
