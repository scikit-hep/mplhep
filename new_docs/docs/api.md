---
search:
  boost: 10
---

# API reference

## Top Level

::: mplhep
    options:
      members:
        - histplot
        - hist2dplot
        - funcplot
        - hist
        - add_text
        - append_text
      show_root_heading: true
      show_source: false

## Plotting

::: mplhep.plot
    options:
      members:
        - histplot
        - hist2dplot
        - model
        - funcplot
        - hist
      show_root_heading: true
      show_source: false

::: mplhep.comp
    heading_level: 2
    options:
      show_root_heading: true
      show_source: false

## Labeling

::: mplhep.label
    options:
      filters:
        - "mplhep._compat.filter_deprecated"
    heading_level: 2
    options:
      show_root_heading: true
      show_source: false

## Utilities

::: mplhep.utils
    options:
      show_root_heading: true
      show_source: false

## Experiment styling

::: mplhep.style
    heading_level: 2
    options:
      show_root_heading: true
      show_source: false

::: mplhep.atlas
    options:
      heading_level: 2
      members:
        - label
        - text
      filters:
        - "mplhep._compat.filter_deprecated"
      show_root_heading: true
      show_source: false

::: mplhep.cms
    options:
      heading_level: 2
      members:
        - label
        - text
      show_root_heading: true
      show_source: false

::: mplhep.lhcb
    options:
      heading_level: 2
      members:
        - label
        - text
      show_root_heading: true
      show_source: false

::: mplhep.alice
    options:
      heading_level: 2
      members:
        - label
        - text
      show_root_heading: true
      show_source: false

::: mplhep.dune
    options:
      heading_level: 2
      members:
        - label
        - text
      show_root_heading: true
      show_source: false
