# mplhep
Aims to simplify use of matplotlib for purposes of high energy physics community. In particular, the first step is to enable a simple replication of the styling of plots from ROOT. This is to be done in two steps:
- offering mpl stylesheets to modify the defaults to look ROOT-like
- A set of helper functions for common labeling sets

## Consistency \& Fonts
As it is ROOT uses system fonts and thus the font in a figure can be dependent on whether it was produced on OSX or PC (former serves Helvetica and latter Arial, which are similar but not the same).

For consistency a default sans-serif font - **Fira Sans** is served with this package (for now experimentally). 
#### Default Fira Sans
https://github.com/mozilla/Fira
#### Math font extension
https://github.com/firamath/firamath