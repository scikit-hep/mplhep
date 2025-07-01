"""Test suite for EnhancedPlottableHistogram covering functionality, edge cases, and error handling."""

import numpy as np
import pytest

from mplhep import EnhancedPlottableHistogram


@pytest.fixture
def basic_hist():
    edges = np.array([[0, 1], [1, 2], [2, 3]], dtype=float)
    values = np.array([1.0, 2.0, 3.0], dtype=float)
    variances = values
    return EnhancedPlottableHistogram(values, edges=edges, variances=variances)


# --- Representation and equality ---


def test_equality_and_repr(basic_hist):
    other = EnhancedPlottableHistogram(
        basic_hist.values(),
        edges=basic_hist.axes[0].edges,
        variances=basic_hist.variances(),
    )
    assert basic_hist == other
    other.set_values(np.array([1.0, 2.1, 3.0]))
    assert basic_hist != other
    rep = repr(basic_hist)
    assert "EnhancedPlottableHistogram" in rep
    assert str(basic_hist.values()) in rep


# --- Addition and related edge cases ---


def test_add_type_error(basic_hist):
    with pytest.raises(TypeError):
        _ = basic_hist + 5


def test_add_not_implemented_for_multidimensional(basic_hist):
    h = basic_hist
    h.axes = [h.axes[0], h.axes[0]]
    with pytest.raises(NotImplementedError):
        _ = h + h


def test_add_mismatched_axes(basic_hist):
    other = EnhancedPlottableHistogram(
        basic_hist.values(),
        edges=np.array([[0, 2], [2, 4], [4, 6]], dtype=float),
        variances=basic_hist.variances(),
    )
    with pytest.raises(ValueError, match="same axes"):
        _ = basic_hist + other


def test_add_mismatched_centers(basic_hist):
    shifted = EnhancedPlottableHistogram(
        basic_hist.values(), edges=basic_hist.axes[0].edges, xoffsets=0.1
    )
    with pytest.raises(ValueError, match="same bin centers"):
        _ = basic_hist + shifted


def test_add_wrong_kind(basic_hist):
    other = EnhancedPlottableHistogram(
        basic_hist.values(), edges=basic_hist.axes[0].edges, kind=None
    )
    with pytest.raises(TypeError):
        _ = basic_hist + other


def test_add_with_fixed_errors(basic_hist):
    h1 = basic_hist
    lo = np.array([0.1, 0.1, 0.1])
    hi = np.array([0.2, 0.2, 0.2])
    h1.fixed_errors(lo, hi)
    h2 = EnhancedPlottableHistogram(basic_hist.values(), edges=basic_hist.axes[0].edges)
    with pytest.raises(RuntimeError):
        _ = h1 + h2


def test_radd_with_zero(basic_hist):
    h1 = basic_hist
    h2 = EnhancedPlottableHistogram(
        np.zeros_like(h1.values()), edges=h1.axes[0].edges, variances=h1.variances()
    )
    result = sum([h1, h2])
    assert np.allclose(result.values(), h1.values())


def test_radd(basic_hist):
    h1 = basic_hist
    h2 = EnhancedPlottableHistogram(
        np.array([4.0, 5.0, 6.0], dtype=float), edges=h1.axes[0].edges
    )
    result = h2 + h1
    assert np.array_equal(result.values(), [5.0, 7.0, 9.0])
    assert result.variances() is None

    h2 = EnhancedPlottableHistogram(
        np.array([4.0, 5.0, 6.0], dtype=float),
        edges=h1.axes[0].edges,
        variances=np.array([4.0, 5.0, 6.0]),
    )
    result = h2 + h1
    assert np.array_equal(result.values(), [5.0, 7.0, 9.0])
    assert np.array_equal(result.variances(), [5.0, 7.0, 9.0])


# --- Multiplication and scaling ---


def test_mul_and_rmul_and_typeerror(basic_hist):
    h = basic_hist
    original_values = h.values().copy()
    original_variances = h.variances().copy()
    result = h * 3
    assert np.array_equal(result.values(), original_values * 3)
    assert np.array_equal(result.variances(), original_variances * 3**2)

    h_no_variances = EnhancedPlottableHistogram(
        original_values, edges=basic_hist.axes[0].edges
    )
    result = 4 * h_no_variances
    assert np.array_equal(result.values(), original_values * 4)
    assert result.variances() is None

    with pytest.raises(TypeError):
        _ = basic_hist * "a"


def test_mul_not_implemented_for_multidimensional(basic_hist):
    h = basic_hist
    h.axes = [h.axes[0], h.axes[0]]
    with pytest.raises(NotImplementedError):
        _ = h * 2


def test_mul_no_fixed_errors(basic_hist):
    basic_hist.fixed_errors(np.array([0.1, 0.1, 0.1]), np.array([0.2, 0.2, 0.2]))
    with pytest.raises(RuntimeError):
        _ = basic_hist * 2


def test_scale_and_scale_error(basic_hist):
    values = np.array([1.0, 2.0, 3.0])
    vars = np.array([1.0, 4.0, 9.0])
    edges = basic_hist.axes[0].edges
    h = EnhancedPlottableHistogram(values.copy(), edges=edges, variances=vars.copy())
    h2 = h.scale(2.0)
    assert np.allclose(h2.values(), values * 2)
    assert np.allclose(h2.variances(), vars * 4)
    h2.fixed_errors(np.zeros(3), np.zeros(3))
    with pytest.raises(RuntimeError):
        h2.scale(2.0)


def test_flat_scale(basic_hist):
    h = basic_hist
    original = h.values().copy()
    lo = np.array([0.1, 0.1, 0.1])
    hi = np.array([0.2, 0.2, 0.2])
    h.fixed_errors(lo.copy(), hi.copy())
    h2 = h.flat_scale(3.0)
    assert np.allclose(h2.values(), original * 3)
    assert np.allclose(h2.yerr_lo, lo * 3)
    assert np.allclose(h2.yerr_hi, hi * 3)


# --- Value and variance setters ---


def test_set_values_and_set_variances(basic_hist):
    h = basic_hist
    new_vals = np.array([5.0, 5.0, 5.0])
    h.set_values(new_vals)
    assert np.array_equal(h.values(), new_vals)
    new_vars = np.array([1.0, 1.0, 1.0])
    h.set_variances(new_vars)
    assert np.array_equal(h.variances(), new_vars)


def test_is_unweighted(basic_hist):
    h = basic_hist
    assert h.is_unweighted()
    basic_hist.set_variances(h.values() / 2)
    assert not h.is_unweighted()


# --- Bin edges and structure ---


def test_edges_1d(basic_hist):
    expected = np.array([0.0, 1.0, 2.0, 3.0])
    assert np.array_equal(basic_hist.edges_1d(), expected)


def test_edges_1d_nonuniform():
    values = np.array([1.0, 2.0])
    edges = np.array([[0, 1.5], [1.5, 3.0]])
    h = EnhancedPlottableHistogram(values, edges=edges)
    assert np.allclose(h.edges_1d(), np.array([0.0, 1.5, 3.0]))


def test_scalar_variance_gets_ignored():
    values = np.array([1.0, 2.0])
    edges = np.array([[0, 1], [1, 2]])
    h = EnhancedPlottableHistogram(values, edges=edges, variances=np.array(1.0))
    assert h.variances() is None


# --- Error handling and propagation ---


def test_errors_no_variances(basic_hist):
    h = EnhancedPlottableHistogram(
        basic_hist.values(), edges=basic_hist.axes[0].edges, variances=None
    )
    h.errors()
    assert np.all(h.yerr_lo == 0)
    assert np.all(h.yerr_hi == 0)


def test_errors_assume_variances_equal_values():
    values = np.array([4.0, 9.0])
    edges = np.array([[0, 1], [1, 2]], dtype=float)
    h = EnhancedPlottableHistogram(values, edges=edges, variances=None)
    h.errors(assume_variances_equal_values=True)
    assert np.allclose(h.yerr_lo, np.array([1.91433919, 2.94346104]))
    assert np.allclose(h.yerr_hi, np.array([3.16275317, 4.11020414]))

    h.errors(method="sqrt", assume_variances_equal_values=True)
    expected = np.sqrt(values)
    assert np.allclose(h.yerr_lo, expected)
    assert np.allclose(h.yerr_hi, expected)


def test_errors_sqrt_behavior():
    values = np.array([1.0, 4.0])
    edges = np.array([[0, 1], [1, 2]], dtype=float)
    variances = np.array([1.0, 4.0])
    h = EnhancedPlottableHistogram(values, edges=edges, variances=variances)
    h.errors(method="sqrt")
    expected = np.sqrt(variances)
    assert np.allclose(h.yerr_lo, expected)
    assert np.allclose(h.yerr_hi, expected)


def test_errors_poisson_behavior():
    values = np.array([1.0, 4.0])
    edges = np.array([[0, 1], [1, 2]], dtype=float)
    variances = np.array([1.0, 4.0])
    h = EnhancedPlottableHistogram(values, edges=edges, variances=variances)
    h.errors(method="poisson")
    assert np.allclose(h.yerr_lo, np.array([0.82724622, 1.91433919]))
    assert np.allclose(h.yerr_hi, np.array([2.29952656, 3.16275317]))


def test_errors_callable_method():
    def custom(sumw, _):
        return sumw * 0.5, sumw * 1.5

    values = np.array([2.0, 4.0])
    edges = np.array([[0, 1], [1, 2]], dtype=float)
    h = EnhancedPlottableHistogram(values, edges=edges, variances=np.array([1.0, 4.0]))
    h.errors(method=custom)
    expected_lo = values * 0.5
    expected_hi = values * 0.5
    assert np.allclose(h.yerr_lo, expected_lo)
    assert np.allclose(h.yerr_hi, expected_hi)


def test_errors_invalid_method_raises(basic_hist):
    h = basic_hist
    h.set_variances(np.array([1.0, 1.0, 1.0]))
    with pytest.raises(AssertionError):
        h.errors(method="invalid")


def test_errors_invalid_callable_method(basic_hist):
    h = basic_hist
    h.set_variances(np.array([1.0, 1.0, 1.0]))
    with pytest.raises(AssertionError):
        h.errors(method=42)


# --- Manual error specification ---


def test_fixed_errors(basic_hist):
    h = basic_hist
    lo = np.array([0.2, 0.2, 0.2])
    hi = np.array([0.3, 0.3, 0.3])
    h.fixed_errors(lo, hi)
    assert h._errors_present is True
    assert np.array_equal(h.yerr_lo, lo)
    assert np.array_equal(h.yerr_hi, hi)


# --- Normalizations ---


def test_binwnorm_idempotence(basic_hist):
    # The basic histogram has unitary bin widths,
    # so binwnorm should not change the values.
    h = basic_hist
    before = h.values().copy()
    h1 = h.binwnorm()
    assert h1 is h
    assert np.allclose(h1.values(), before)
    h2 = h1.binwnorm()
    assert np.allclose(h2.values(), before)


def test_binwnorm_non_unitary_bin_widths():
    edges = np.array([[0, 1], [1, 3]], dtype=float)
    values = np.array([1.0, 4.0], dtype=float)
    variances = values
    h = EnhancedPlottableHistogram(
        values, edges=edges, variances=variances, w2method="sqrt"
    )
    # The first bin is normalized by 1, the second by 2.
    h.binwnorm()
    assert np.allclose(h.values(), [1.0, 2.0])
    assert np.allclose([h.yerr_lo], [1.0, 1.0])
    assert np.allclose([h.yerr_hi], [1.0, 1.0])

    # Another normalization should not change the values
    h.binwnorm()
    assert np.allclose(h.values(), [1.0, 2.0])
    assert np.allclose([h.yerr_lo], [1.0, 1.0])
    assert np.allclose([h.yerr_hi], [1.0, 1.0])


def test_density_normalization(basic_hist):
    h = basic_hist
    h1 = h.density()
    assert np.isclose(np.sum(h1.values()), 1.0)


def test_binwnorm_then_density(basic_hist):
    h = basic_hist
    h.set_variances(np.array([1.0, 1.0, 1.0]))
    h.binwnorm()
    h.density()
    area = np.sum(np.diff(h.edges_1d()) * h.values())
    assert np.isclose(area, 1.0)


# --- Output formats ---


def test_to_stairs_and_to_stairband_and_to_errorbar(basic_hist):
    h = basic_hist
    vars = np.array([1.0, 1.0, 1.0])
    h.set_variances(vars)
    stairs = h.to_stairs()
    assert set(stairs) == {"values", "edges", "baseline"}
    stairband = h.to_stairband()
    assert set(stairband) == {"values", "edges", "baseline"}
    errbar = h.to_errorbar()
    assert set(errbar) == {"x", "y", "xerr", "yerr"}
    n = len(basic_hist.values())
    assert len(errbar["x"]) == n
    assert len(errbar["y"]) == n
    assert len(errbar["xerr"][0]) == n
    assert len(errbar["yerr"][0]) == n


# --- Constructor validation ---


def test_constructor_variances_and_yerr_conflict():
    values = np.array([1.0, 2.0])
    edges = np.array([[0, 1], [1, 2]])
    variances = np.array([1.0, 1.0])
    yerr = (np.array([0.1, 0.1]), np.array([0.2, 0.2]))
    with pytest.raises(AssertionError):
        EnhancedPlottableHistogram(values, edges=edges, variances=variances, yerr=yerr)
