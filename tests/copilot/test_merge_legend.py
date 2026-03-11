"""Tests for mplhep.merge_legend_handles_labels() utility function.

This function was completely untested. These tests cover:
- Basic deduplication of handles/labels
- Preserving order
- No duplicates case
- Empty inputs
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt

os.environ['RUNNING_PYTEST'] = 'true'

import mplhep as mh

plt.switch_backend('Agg')


def test_merge_legend_no_duplicates():
    """Test merge with no duplicate labels - should pass through unchanged."""
    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 2], label='A')
    ax.plot([1, 2], [2, 3], label='B')
    handles, labels = ax.get_legend_handles_labels()

    merged_handles, merged_labels = mh.merge_legend_handles_labels(handles, labels)
    assert merged_labels == ['A', 'B']
    assert len(merged_handles) == 2
    # Each handle should be a tuple with one element
    assert all(isinstance(h, tuple) for h in merged_handles)
    assert all(len(h) == 1 for h in merged_handles)
    plt.close('all')


def test_merge_legend_with_duplicates():
    """Test merge with duplicate labels - should combine handles."""
    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 2], label='A')
    ax.plot([1, 2], [2, 3], label='A')
    ax.plot([1, 2], [3, 4], label='B')
    handles, labels = ax.get_legend_handles_labels()

    merged_handles, merged_labels = mh.merge_legend_handles_labels(handles, labels)
    assert merged_labels == ['A', 'B']
    assert len(merged_handles) == 2
    # 'A' should have 2 handles merged
    assert len(merged_handles[0]) == 2
    # 'B' should have 1 handle
    assert len(merged_handles[1]) == 1
    plt.close('all')


def test_merge_legend_empty():
    """Test merge with empty inputs."""
    merged_handles, merged_labels = mh.merge_legend_handles_labels([], [])
    assert merged_handles == []
    assert merged_labels == []


def test_merge_legend_preserves_order():
    """Test that merge preserves the first-seen order of labels."""
    fig, ax = plt.subplots()
    ax.plot([1], [1], label='C')
    ax.plot([1], [2], label='A')
    ax.plot([1], [3], label='B')
    ax.plot([1], [4], label='A')  # Duplicate
    handles, labels = ax.get_legend_handles_labels()

    merged_handles, merged_labels = mh.merge_legend_handles_labels(handles, labels)
    assert merged_labels == ['C', 'A', 'B']
    plt.close('all')
