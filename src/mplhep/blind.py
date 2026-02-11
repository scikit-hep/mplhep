"""Utilities for blinding histogram regions."""

from __future__ import annotations

import numpy as np


class loc:
    """UHI-like value-based bin locator.

    Use ``loc(value)`` to create a locator for a single value, or
    ``loc[start:stop]`` to create a slice of locators.

    When both sides of the slice are plain numbers (no ``j`` suffix),
    they are treated as **value-based** (the purpose of ``loc``).
    When at least one side uses the complex-number ``j`` suffix (UHI
    convention), the ``j``-suffixed side is value-based and any plain-int
    side is **index-based**, enabling mixed specs like ``loc[5:10j]``.
    """

    def __init__(self, value):
        self.value = value

    def __class_getitem__(cls, key):
        if isinstance(key, slice):
            has_complex = isinstance(key.start, complex) or isinstance(
                key.stop, complex
            )
            if has_complex:
                # Mixed mode: complex → value-based (extract .imag),
                # plain int/float → pass through as-is (index-based).
                start = (
                    cls(key.start.imag) if isinstance(key.start, complex) else key.start
                )
                stop = cls(key.stop.imag) if isinstance(key.stop, complex) else key.stop
            else:
                # Pure loc mode: everything is value-based.
                start = cls(key.start) if key.start is not None else None
                stop = cls(key.stop) if key.stop is not None else None
            return slice(start, stop)
        return cls(key)


def _parse_blind_spec(spec):
    """Normalize a single blind specification into per-side type information.

    Parameters
    ----------
    spec : int, tuple, str, or slice
        A blind region specification:

        - ``int``: single bin index to blind.
        - Tuple ``(start, stop)``: always value-based.
        - String ``"start:stop"``: ``j`` suffix means value-based, plain int
          means index-based.  Mixing is allowed (e.g. ``"5:10j"``).
        - Slice: ``loc`` objects or complex numbers are value-based, integers
          are index-based.  Mixing is allowed (e.g. ``slice(5, 10j)``).

    Returns
    -------
    tuple
        ``(start, stop, start_is_vb, stop_is_vb)`` where start/stop may be
        ``None`` for open-ended ranges.
    """
    # --- single integer → blind one bin by index ---
    if isinstance(spec, int) and not isinstance(spec, bool):
        return (spec, spec + 1, False, False)

    # --- tuple → always value-based ---
    if isinstance(spec, tuple):
        if len(spec) != 2:
            msg = (
                'Tuple blind spec must be of the form (start, stop); '
                f'got {spec!r} with {len(spec)} elements'
            )
            raise ValueError(msg)
        return (spec[0], spec[1], True, True)

    # --- string → parse "start:stop" with optional j suffix ---
    if isinstance(spec, str):
        parts = spec.split(":")
        if len(parts) != 2:
            msg = f"Blind string spec must contain exactly one ':', got {spec!r}"
            raise ValueError(msg)
        raw_start, raw_stop = parts

        def _parse_part(s):
            s = s.strip()
            if s == "":
                return None, None
            if s.endswith("j"):
                return float(s[:-1]), True
            return int(s), False

        start, start_vb = _parse_part(raw_start)
        stop, stop_vb = _parse_part(raw_stop)

        # Infer unknown sides from the known side; default to index-based.
        if start_vb is None:
            start_vb = stop_vb if stop_vb is not None else False
        if stop_vb is None:
            stop_vb = start_vb

        return (start, stop, start_vb, stop_vb)

    # --- slice → inspect loc / complex / int ---
    if isinstance(spec, slice):

        def _resolve(val):
            if val is None:
                return None, None
            if isinstance(val, loc):
                return val.value, True
            if isinstance(val, complex):
                return val.imag, True
            return val, False

        start_val, start_vb = _resolve(spec.start)
        stop_val, stop_vb = _resolve(spec.stop)

        if start_vb is None:
            start_vb = stop_vb if stop_vb is not None else False
        if stop_vb is None:
            stop_vb = start_vb

        return (start_val, stop_val, start_vb, stop_vb)

    msg = (
        f"Blind spec must be an int, tuple, string, or slice, got {type(spec).__name__}"
    )
    raise TypeError(msg)


def _resolve_one_side(val, is_vb, edges, n_bins, *, is_start):
    """Resolve a single start/stop value to a bin index.

    Parameters
    ----------
    val : float, int, or None
        The raw value.
    is_vb : bool
        Whether *val* is value-based.
    edges : np.ndarray
        Histogram bin edges.
    n_bins : int
        Number of bins.
    is_start : bool
        ``True`` when resolving the start side (affects defaults and
        ``searchsorted`` convention).

    Returns
    -------
    int
        The resolved bin index.
    """
    if val is None:
        return 0 if is_start else n_bins

    if is_vb:
        if is_start:
            return int(np.searchsorted(edges[1:], val, side="right"))
        return int(np.searchsorted(edges[:-1], val, side="left"))
    return int(val)


def _resolve_blind_mask(blind, edges):
    """Convert blind spec(s) into a boolean mask over histogram bins.

    Parameters
    ----------
    blind : int, tuple, str, slice, or list thereof
        Blind region specification(s).  A list of plain integers (e.g.
        ``[2, 5, 7]``) blinds those individual bins by index.  Lists may
        freely mix integers, tuples, strings, and slices.
    edges : array-like
        Histogram bin edges (length = n_bins + 1).

    Returns
    -------
    np.ndarray
        Boolean mask of shape ``(n_bins,)``. ``True`` = visible,
        ``False`` = blinded.
    """
    edges = np.asarray(edges, dtype=float)
    n_bins = len(edges) - 1
    mask = np.ones(n_bins, dtype=bool)

    # Normalize to list of specs
    specs = blind if isinstance(blind, list) else [blind]

    for spec in specs:
        start, stop, start_vb, stop_vb = _parse_blind_spec(spec)

        start_idx = _resolve_one_side(start, start_vb, edges, n_bins, is_start=True)
        stop_idx = _resolve_one_side(stop, stop_vb, edges, n_bins, is_start=False)

        mask[start_idx:stop_idx] = False

    return mask
