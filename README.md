<p float="left">
  <img src="https://raw.githubusercontent.com/scikit-hep/mplhep/master/docs/source/_static/mplhep.png" width="300"/>
</p>

[![DOI](https://zenodo.org/badge/184555939.svg)](https://zenodo.org/badge/latestdoi/184555939)
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)
[![Docs](https://readthedocs.org/projects/mplhep/badge/?version=latest)](https://mplhep.readthedocs.io/en/latest/?badge=latest)

[sk-badge]: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg

[![Actions Status][actions-badge]][actions-link]
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/scikit-hep/mplhep/main.svg)](https://results.pre-commit.ci/latest/github/scikit-hep/mplhep/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

[![PyPI version](https://badge.fury.io/py/mplhep.svg)](https://badge.fury.io/py/mplhep)
[![Conda-forge version](https://img.shields.io/conda/vn/conda-forge/mplhep.svg)](https://anaconda.org/conda-forge/mplhep)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/mplhep.svg)](https://pypi.org/project/mplhep/)

[![PyPI download week](https://img.shields.io/pypi/dw/mplhep?label=downloads%20%28incl%20CI%29)](https://img.shields.io/pypi/dw/mplhep?label=downloads%20%28incl%20CI%29)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scikit-hep/mplhep/master)

A set of helpers for `matplotlib` to more easily produce plots typically
needed in HEP as well as style them in way that's compatible with current
collaboration requirements (ROOT-like plots for CMS, ATLAS, LHCb, ALICE).


## Installation

```bash
pip install mplhep
```

## Documentation and Getting Started
A tutorial given at PyHEP 2020 is available as a binder [here](https://github.com/andrzejnovak/2020-07-17-pyhep2020-mplhep)
or you can watch the recording [here](https://www.youtube.com/watch?v=gUziXqCGe0o).

Documentation can be found at [scikit-hep.org/mplhep](https://scikit-hep.org/mplhep/).

<!---
# Notes

## Consistency \& Fonts
As it is ROOT does not come with any fonts and therefore relies on using system fonts. Therefore the font in a figure can be dependent on whether it was produced on OSX or PC. The default sans-serif font used is Helvetica, but it only comes with OSX, in Windows this will silently fallback to Arial.

### License
Both Helvetica and Arial are proprietary, which as far as fonts go means you can use it to create any text/graphics once you have the license, but you cannot redistribute the font files as part of other software. That means we cannot just package Helvetica with this to make sure everyone has the same font in plots.

Luckily for fonts it seems only the software is copyrighted, not the actual shapes, which means there are quite a few open alternatives with similar look. The most closely resembling Helvetica being Tex Gyre Heros

#### Tex Gyre Heros
http://www.gust.org.pl/projects/e-foundry/tex-gyre/heros

You can compare yourself if the differences are meanigful below.

<p float="center">
  <img src="img/FontComp.png" width="400" />
</p>

They are Tex Gyre Heros, Helvetica and Arial respectively.

### Math Fonts
- Math fonts are a separate set from regular fonts due to the amount of special characters
- It's not trivial to make sure you get a matching math font to your regular font
- Most math-fonts are serif fonts, but this is not ideal if one wants to use sans-serif font for normal text like Helvetica or Arial
- The number of sans-serif math-fonts is very limited
 	- The number of **open** sans-serif math-fonts is **extremely** limited
 	- Basically there's two, Fira Sans and GFS Neohellenic Math, of which I like Fira Sans better
 	- https://tex.stackexchange.com/questions/374250/are-there-opentype-sans-math-fonts-under-development

For consistent styling Fira Sans is included as well.
#### Default Fira Sans
https://github.com/mozilla/Fira
#### Math font extension
https://github.com/firamath/firamath

--->


## Notes

### Citation

If you've found this library helpful and are able to, please consider citing it. You can find us on [Zenodo](doi.org/10.5281/zenodo.3766157) as a permalink to the latest version.

BiBTeX:
```
@software{Novak_mplhep_2020,
  author = {Novak, Andrzej and Schreiner, Henry and Feickert, Matthew and Eschle, Jonas and Fillinger, Tristan and Praz, Cyrille},
  doi = {10.5281/zenodo.3766157},
  license = {MIT},
  month = apr,
  title = {{mplhep}},
  url = {https://github.com/scikit-hep/mplhep},
  year = {2020}
}
```

APA:
```
Novak, A., Schreiner, H., Feickert, M., Eschle, J., Fillinger, T., & Praz, C. (2020). mplhep [Computer software]. https://doi.org/10.5281/zenodo.3766157
```

### Use in publications

Updating list of citations and use cases of `mplhep` in publications:

- [Simultaneous Jet Energy and Mass Calibrations with Neural Networks](https://cds.cern.ch/record/2706189), ATLAS Collaboration, 2019
- [Integration and Performance of New Technologies in the CMS Simulation](https://arxiv.org/abs/2004.02327), Kevin Pedro, 2020 (Fig 5,6)
- [GeantV: Results from the prototype of concurrent vector particle transport simulation in HEP](https://arxiv.org/abs/2005.00949), Amadio et al, 2020 (Fig 25,26)
- [Search for the standard model Higgs boson decaying to charm quarks](https://cds.cern.ch/record/2682638), CMS Collaboration, 2019 (Fig 1)
- [Search for long-lived particles decaying to eμν](https://arxiv.org/abs/2012.02696), LHCb Collaboration, 2020
- [Measurement of the mass dependence of the transverse momentum of lepton pairs in Drell-Yan production in proton-proton collisions at √s = 13 TeV](http://arxiv.org/abs/2205.04897), CMS Collaboration, 2022 (Figs 3-)
- And many others by now...

[actions-badge]:            https://github.com/scikit-hep/mplhep/workflows/CI/badge.svg
[actions-link]:             https://github.com/scikit-hep/mplhep/actions
