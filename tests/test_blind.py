"""Tests for the blind module."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pytest

import mplhep as mh
from mplhep._utils import EnhancedPlottableHistogram
from mplhep.blind import _parse_blind_spec, _resolve_blind_mask, loc


class TestLoc:
    def test_loc_init(self):
        locator = loc(100)
        assert locator.value == 100

    def test_loc_class_getitem_slice(self):
        result = loc[100:200]
        assert isinstance(result, slice)
        assert isinstance(result.start, loc)
        assert isinstance(result.stop, loc)
        assert result.start.value == 100
        assert result.stop.value == 200

    def test_loc_class_getitem_open_ended(self):
        result = loc[100:]
        assert isinstance(result, slice)
        assert isinstance(result.start, loc)
        assert result.stop is None
        assert result.start.value == 100

        result = loc[:200]
        assert isinstance(result, slice)
        assert result.start is None
        assert isinstance(result.stop, loc)
        assert result.stop.value == 200

    def test_loc_class_getitem_scalar(self):
        result = loc[100]
        assert isinstance(result, loc)
        assert result.value == 100

    def test_loc_exported(self):
        assert mh.loc is loc

    def test_loc_mixed_int_complex(self):
        """loc[5:10j] → mixed: start is plain int 5, stop is loc(10.0)."""
        result = loc[5:10j]
        assert isinstance(result, slice)
        assert result.start == 5  # plain int, index-based
        assert isinstance(result.stop, loc)
        assert result.stop.value == 10.0

    def test_loc_mixed_complex_int(self):
        """loc[5j:10] → mixed: start is loc(5.0), stop is plain int 10."""
        result = loc[5j:10]
        assert isinstance(result, slice)
        assert isinstance(result.start, loc)
        assert result.start.value == 5.0
        assert result.stop == 10  # plain int, index-based

    def test_loc_both_complex(self):
        """loc[5j:10j] → both value-based."""
        result = loc[5j:10j]
        assert isinstance(result, slice)
        assert isinstance(result.start, loc)
        assert isinstance(result.stop, loc)
        assert result.start.value == 5.0
        assert result.stop.value == 10.0


class TestParseBlindSpec:
    def test_tuple(self):
        assert _parse_blind_spec((100, 200)) == (100, 200, True, True)

    def test_tuple_with_none(self):
        assert _parse_blind_spec((100, None)) == (100, None, True, True)
        assert _parse_blind_spec((None, 200)) == (None, 200, True, True)

    def test_string_value_based(self):
        assert _parse_blind_spec("100j:200j") == (100.0, 200.0, True, True)

    def test_string_index_based(self):
        assert _parse_blind_spec("3:7") == (3, 7, False, False)

    def test_string_open_ended_value(self):
        start, stop, s_vb, e_vb = _parse_blind_spec("100j:")
        assert start == 100.0
        assert stop is None
        assert s_vb is True
        assert e_vb is True  # inferred from start

    def test_string_open_ended_index(self):
        start, stop, s_vb, e_vb = _parse_blind_spec(":7")
        assert start is None
        assert stop == 7
        assert s_vb is False  # inferred from stop
        assert e_vb is False

    def test_string_mixed_allowed(self):
        """Mixed j / plain-int in a string spec is now allowed."""
        start, stop, s_vb, e_vb = _parse_blind_spec("5:10j")
        assert start == 5
        assert stop == 10.0
        assert s_vb is False
        assert e_vb is True

    def test_string_mixed_reverse(self):
        start, stop, s_vb, e_vb = _parse_blind_spec("5j:10")
        assert start == 5.0
        assert stop == 10
        assert s_vb is True
        assert e_vb is False

    def test_slice_loc(self):
        spec = slice(loc(100), loc(200))
        assert _parse_blind_spec(spec) == (100, 200, True, True)

    def test_slice_complex(self):
        spec = slice(100j, 200j)
        assert _parse_blind_spec(spec) == (100.0, 200.0, True, True)

    def test_slice_int(self):
        spec = slice(3, 7)
        assert _parse_blind_spec(spec) == (3, 7, False, False)

    def test_slice_open_ended(self):
        spec = slice(loc(100), None)
        start, stop, s_vb, e_vb = _parse_blind_spec(spec)
        assert start == 100
        assert stop is None
        assert s_vb is True
        assert e_vb is True  # inferred from start

    def test_slice_mixed_int_complex(self):
        """slice(5, 10j) → index 5, value 10 — mixed, now allowed."""
        start, stop, s_vb, e_vb = _parse_blind_spec(slice(5, 10j))
        assert start == 5
        assert stop == 10.0
        assert s_vb is False
        assert e_vb is True

    def test_slice_mixed_complex_int(self):
        start, stop, s_vb, e_vb = _parse_blind_spec(slice(5j, 10))
        assert start == 5.0
        assert stop == 10
        assert s_vb is True
        assert e_vb is False

    def test_slice_mixed_loc_int(self):
        """slice(loc(25), 7) → value 25, index 7 — mixed."""
        start, stop, s_vb, e_vb = _parse_blind_spec(slice(loc(25), 7))
        assert start == 25
        assert stop == 7
        assert s_vb is True
        assert e_vb is False

    def test_single_int(self):
        """A bare integer blinds one bin by index."""
        assert _parse_blind_spec(3) == (3, 4, False, False)

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            _parse_blind_spec(3.14)

    def test_bool_rejected(self):
        with pytest.raises(TypeError):
            _parse_blind_spec(True)  # noqa: FBT003


class TestResolveBlindMask:
    """Test _resolve_blind_mask with various specs."""

    def setup_method(self):
        # 10 bins: [0, 10, 20, ..., 100]
        self.edges = np.linspace(0, 100, 11)

    def test_value_based_tuple(self):
        mask = _resolve_blind_mask((25, 75), self.edges)
        expected = np.array(
            [True, True, False, False, False, False, False, False, True, True]
        )
        np.testing.assert_array_equal(mask, expected)

    def test_value_based_exact_edges(self):
        mask = _resolve_blind_mask((20, 50), self.edges)
        expected = np.array(
            [True, True, False, False, False, True, True, True, True, True]
        )
        np.testing.assert_array_equal(mask, expected)

    def test_index_based_string(self):
        mask = _resolve_blind_mask("3:7", self.edges)
        expected = np.ones(10, dtype=bool)
        expected[3:7] = False
        np.testing.assert_array_equal(mask, expected)

    def test_open_ended_start_none(self):
        mask = _resolve_blind_mask(":5", self.edges)
        expected = np.ones(10, dtype=bool)
        expected[:5] = False
        np.testing.assert_array_equal(mask, expected)

    def test_open_ended_stop_none(self):
        mask = _resolve_blind_mask((50, None), self.edges)
        expected = np.array(
            [True, True, True, True, True, False, False, False, False, False]
        )
        np.testing.assert_array_equal(mask, expected)

    def test_multiple_regions(self):
        mask = _resolve_blind_mask([(10, 30), (70, 90)], self.edges)
        expected = np.array(
            [True, False, False, True, True, True, True, False, False, True]
        )
        np.testing.assert_array_equal(mask, expected)

    def test_loc_slice(self):
        mask = _resolve_blind_mask(loc[25:75], self.edges)
        expected = np.array(
            [True, True, False, False, False, False, False, False, True, True]
        )
        np.testing.assert_array_equal(mask, expected)

    def test_complex_slice(self):
        mask = _resolve_blind_mask(slice(25j, 75j), self.edges)
        expected = np.array(
            [True, True, False, False, False, False, False, False, True, True]
        )
        np.testing.assert_array_equal(mask, expected)

    # --- NEW: single-int and list-of-ints ---

    def test_single_int(self):
        """A bare integer blinds exactly one bin."""
        mask = _resolve_blind_mask(3, self.edges)
        expected = np.ones(10, dtype=bool)
        expected[3] = False
        np.testing.assert_array_equal(mask, expected)

    def test_list_of_ints(self):
        """A list of ints blinds those specific bins."""
        mask = _resolve_blind_mask([2, 5, 7], self.edges)
        expected = np.ones(10, dtype=bool)
        expected[[2, 5, 7]] = False
        np.testing.assert_array_equal(mask, expected)

    def test_mixed_list(self):
        """A list mixing ints, tuples, and strings."""
        mask = _resolve_blind_mask([0, (50, 70), "8:10"], self.edges)
        expected = np.ones(10, dtype=bool)
        expected[0] = False  # int
        expected[5:7] = False  # value-based tuple (50, 70)
        expected[8:10] = False  # index-based string
        np.testing.assert_array_equal(mask, expected)

    def test_mixed_string_index_start_value_stop(self):
        """'3:70j' → start at index 3, stop at value 70."""
        mask = _resolve_blind_mask("3:70j", self.edges)
        expected = np.ones(10, dtype=bool)
        # index 3 to value 70 → bins 3..6 blinded
        expected[3:7] = False
        np.testing.assert_array_equal(mask, expected)

    def test_mixed_string_value_start_index_stop(self):
        """'30j:7' → start at value 30, stop at index 7."""
        mask = _resolve_blind_mask("30j:7", self.edges)
        expected = np.ones(10, dtype=bool)
        expected[3:7] = False
        np.testing.assert_array_equal(mask, expected)

    def test_mixed_slice_int_complex(self):
        """slice(3, 70j) → index 3, value 70."""
        mask = _resolve_blind_mask(slice(3, 70j), self.edges)
        expected = np.ones(10, dtype=bool)
        expected[3:7] = False
        np.testing.assert_array_equal(mask, expected)

    def test_mixed_loc_getitem(self):
        """loc[3:70j] → index 3, value 70."""
        mask = _resolve_blind_mask(loc[3:70j], self.edges)
        expected = np.ones(10, dtype=bool)
        expected[3:7] = False
        np.testing.assert_array_equal(mask, expected)


class TestHistplotBlind:
    """Test histplot with blind parameter."""

    def setup_method(self):
        self.values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.edges = np.linspace(0, 100, 11)

    def test_blind_none_no_effect(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=None)
        plt.close(fig)

    def test_blind_tuple_step(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=(25, 75), histtype="step")
        plt.close(fig)

    def test_blind_tuple_fill(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=(25, 75), histtype="fill")
        plt.close(fig)

    def test_blind_tuple_errorbar(self):
        fig, ax = plt.subplots()
        mh.histplot(
            self.values,
            self.edges,
            ax=ax,
            blind=(25, 75),
            histtype="errorbar",
            yerr=True,
        )
        plt.close(fig)

    def test_blind_tuple_band(self):
        fig, ax = plt.subplots()
        mh.histplot(
            self.values,
            self.edges,
            ax=ax,
            blind=(25, 75),
            histtype="band",
            yerr=True,
        )
        plt.close(fig)

    def test_blind_string(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind="25j:75j")
        plt.close(fig)

    def test_blind_index_string(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind="3:7")
        plt.close(fig)

    def test_blind_loc(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=loc[25:75])
        plt.close(fig)

    def test_blind_multiple(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=[(10, 30), (70, 90)])
        plt.close(fig)

    def test_blind_single_int(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=3)
        plt.close(fig)

    def test_blind_list_of_ints(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=[2, 5, 7])
        plt.close(fig)

    def test_blind_mixed_string(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind="3:70j")
        plt.close(fig)

    def test_blind_mixed_loc(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=loc[3:70j])
        plt.close(fig)

    def test_blind_mixed_list(self):
        fig, ax = plt.subplots()
        mh.histplot(self.values, self.edges, ax=ax, blind=[0, (50, 70), "8:10"])
        plt.close(fig)


class TestComparisonBlind:
    """Test that blind passes through to comparison plotters."""

    def setup_method(self):
        self.h1_vals = np.array([10, 20, 30, 40, 50], dtype=float)
        self.h2_vals = np.array([12, 18, 32, 38, 52], dtype=float)
        self.edges = np.linspace(0, 50, 6)

        self.h1 = EnhancedPlottableHistogram(
            self.h1_vals, edges=self.edges, variances=self.h1_vals
        )
        self.h2 = EnhancedPlottableHistogram(
            self.h2_vals, edges=self.edges, variances=self.h2_vals
        )

    def test_hists_blind(self):
        fig, ax_main, ax_comp = mh.comp.hists(self.h1, self.h2, blind=(10, 30))
        plt.close(fig)

    def test_data_model_blind(self):
        fig, ax_main, ax_comp = mh.comp.data_model(
            self.h1, stacked_components=[self.h2], blind=(10, 30)
        )
        plt.close(fig)
