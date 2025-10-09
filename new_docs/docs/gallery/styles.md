# Styles

This page provides a gallery of available styles in mplhep. The styles are sorted by the experiments they are associated with.

Styles can be used by calling `mplhep.style.use(style)` with `style` one of the available styles in `mplhep.style`. In this gallery, only the most used and actively maintained styles are shown.

The following plots are generated using `mplhep.histplot` and `plt.plot(...)` to plot the fit of a Gaussian distribution (for the signal peak) and an exponential distribution (for the background) on top of a histogram.

All plots have additionally a legend, axis labels, and a title as well as

- the text "Preliminary" at position 0 (see Labels for more positions), using the experiment specific function if available (or none otherwise),
- the year 2016
- a luminosity of 9 fb⁻¹
- `data=True` to show that it's not simulation

to illustrate the visual appearance of the styles.

## ATLAS

ATLAS has two recommended styles. The main recommendation, `ATLAS` (or `ATLAS2`, based on [this work](https://jfly.uni-koeln.de/color/)) provides 7 colors, with Vermilion, the first color in the palette, recommended for signal. In the case of large signals, white can also be used.

For plots that require large numbers of colors, the `ATLAS1` palette is provided with 10 colors [based on this paper](https://arxiv.org/pdf/2107.02270).

## CMS

## LHCb

LHCb has two styles, the older one, `LHCb1`, and the newer one, `LHCb2`.

### LHCb1 style (old)

### LHCb2 style

## ALICE

ALICE style

## DUNE

DUNE neutrino experiment style. DUNE points to the newest style, currently only DUNE1 is available. If you want to use the newest style, in case of updates, use `DUNE`, if you want to make sure that backwards compatibility is kept, use `DUNE1`.
