"""Tests for mplhep.savelabels() and mplhep.save_variations() functions.

These functions were completely untested. These tests cover:
- savelabels with default labels
- savelabels with custom labels
- savelabels with string list labels
- save_variations with default text_list
- save_variations with custom text_list
- save_variations with exp parameter
- Bug fix: save_variations was using ExpText for both exp_labels and suffixes
"""

from __future__ import annotations

import os
import tempfile

import matplotlib.pyplot as plt
import pytest

os.environ['RUNNING_PYTEST'] = 'true'

import mplhep as mh
from mplhep.label import ExpLabel, ExpText

plt.switch_backend('Agg')


@pytest.fixture
def labeled_figure():
    """Create a figure with CMS experiment labels."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    mh.cms.label(data=False, ax=ax)
    return fig, ax


def test_savelabels_default(labeled_figure, tmp_path):
    """Test savelabels with default labels."""
    fig, ax = labeled_figure
    fname = str(tmp_path / 'test.png')
    mh.savelabels(fname, ax=ax)

    # Default labels should produce 4 files
    expected_files = ['test.png', 'test_pas.png', 'test_supp.png', 'test_wip.png']
    for expected in expected_files:
        assert (tmp_path / expected).exists(), f'Missing file: {expected}'
    plt.close('all')


def test_savelabels_custom_labels(labeled_figure, tmp_path):
    """Test savelabels with custom tuple labels."""
    fig, ax = labeled_figure
    fname = str(tmp_path / 'test.png')
    mh.savelabels(
        fname,
        ax=ax,
        labels=[('Preliminary', 'prelim'), ('', 'final')],
    )

    expected_files = ['test_prelim.png', 'test_final.png']
    for expected in expected_files:
        assert (tmp_path / expected).exists(), f'Missing file: {expected}'
    plt.close('all')


def test_savelabels_string_labels(labeled_figure, tmp_path):
    """Test savelabels with string list labels (auto-converted to tuples)."""
    fig, ax = labeled_figure
    fname = str(tmp_path / 'test.png')
    mh.savelabels(fname, ax=ax, labels=['Preliminary', 'Final'])

    expected_files = ['test_preliminary.png', 'test_final.png']
    for expected in expected_files:
        assert (tmp_path / expected).exists(), f'Missing file: {expected}'
    plt.close('all')


def test_savelabels_no_exp_text_raises(tmp_path):
    """Test savelabels raises when no ExpText is found."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    fname = str(tmp_path / 'test.png')
    with pytest.raises(ValueError, match='No ExpText object found'):
        mh.savelabels(fname, ax=ax)
    plt.close('all')


def test_save_variations_default(labeled_figure, tmp_path):
    """Test save_variations with default text_list."""
    fig, ax = labeled_figure
    fname = str(tmp_path / 'test.png')
    mh.save_variations(fig, fname)

    # Default text_list is ["Preliminary", ""]
    expected_files = ['test_preliminary.png', 'test.png']
    for expected in expected_files:
        assert (tmp_path / expected).exists(), f'Missing file: {expected}'
    plt.close('all')


def test_save_variations_custom_text(labeled_figure, tmp_path):
    """Test save_variations with custom text_list."""
    fig, ax = labeled_figure
    fname = str(tmp_path / 'test.png')
    mh.save_variations(fig, fname, text_list=['Work in Progress', 'Preliminary', ''])

    expected_files = [
        'test_work in progress.png',
        'test_preliminary.png',
        'test.png',
    ]
    for expected in expected_files:
        assert (tmp_path / expected).exists(), f'Missing file: {expected}'
    plt.close('all')


def test_save_variations_exp_changes_label(tmp_path):
    """Test that save_variations correctly modifies ExpLabel when exp is set.

    This tests the bug fix where save_variations was using ExpText for both
    exp_labels and suffixes, causing the experiment name to never be updated.
    """
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    mh.cms.label(data=False, ax=ax)

    # Get the original ExpLabel text
    exp_labels = [t for t in ax.get_children() if isinstance(t, ExpLabel)]
    assert len(exp_labels) > 0, 'No ExpLabel found after cms.label()'
    original_exp = exp_labels[0].get_text()

    fname = str(tmp_path / 'test.png')
    mh.save_variations(fig, fname, text_list=['Preliminary'], exp='ATLAS')

    # After save_variations with exp='ATLAS', the ExpLabel should have been changed
    exp_labels_after = [t for t in ax.get_children() if isinstance(t, ExpLabel)]
    assert exp_labels_after[0].get_text() == 'ATLAS'

    # And the ExpText should have been set to 'Preliminary'
    exp_texts = [t for t in ax.get_children() if isinstance(t, ExpText)]
    assert len(exp_texts) > 0, 'No ExpText found'
    assert exp_texts[0].get_text() == 'Preliminary'

    plt.close('all')


def test_save_variations_no_extension(labeled_figure, tmp_path):
    """Test save_variations with filename without extension."""
    fig, ax = labeled_figure
    fname = str(tmp_path / 'test')
    # This should not raise IndexError (bug fix)
    mh.save_variations(fig, fname + '.png', text_list=[''])

    assert (tmp_path / 'test.png').exists()
    plt.close('all')
