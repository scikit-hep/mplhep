![mplhep]("img/mplhep.png")
# mplhep

![Hits](https://countimports.pythonanywhere.com/nocount/tag.svg?url=count_mplhep_imports)

- offering mpl stylesheets to modify `matplotlib` defaults to look ROOT-like
- A set of helper functions for common labeling and formating

# Installation
```
pip install mplhep
```
Fonts and styles are now served dynamically through the package. The fonts are made available to matplotlib by `import mplhep`, however as a backup solution, functions are provided to hard copy fonts and styles to their respective `mpl` locations
```
mplhep.tools.hardcopy_fonts()
mplhep.tools.hardcopy_styles()
```
These only need to be called once. Styles are then accessible direclty by name i.e. `plt.style.use("ROOT") as opposed to the package call.

# Basic use

## Styles
```
import matplotlib.pyplot as plt
import mplhep.style as sty
plt.style.use(sty.ROOT)
```
Styles are also included in experiment specific helpers
```
import mplhep as hep
plt.style.use(hep.cms.style.ROOT)
plt.style.use(hep.atlas.style.ATLAS)
```

#### Minimal Example
```diff
+ import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt

x = np.random.uniform(0, 10, 240)
y = np.random.normal(512, 112, 240)
z = np.random.normal(0.5, 0.1, 240)

+ plt.style.use(hep.style.ROOT)
f, ax = plt.subplots()
ax.scatter(x,y, c=z);

```

<p float="center">
  <img src="img/style0.png" width="400" />
  <img src="img/style1.png" width="400" />
</p>

- For more examples see https://github.com/andrzejnovak/mplhep/blob/master/Examples.ipynb

### Available styles:

- `plt.style.use(sty.ROOT)` - Default (figure 10x10 inches, full column size)
- `plt.style.use(sty.ROOTlegacy)` - Same as ROOT style above, but use ROOT fonts - Helvetica, fallback to Arial - instead of TeX Gyre Heros, requires font to be already available on the system
- `plt.style.use(sty.ROOTs)` - Default (figure 6x6 inches, half column size)
- `plt.style.use(sty.fira)` - use Fira Sans

- `plt.style.use(sty.firamath)` - use Fira Math

- `plt.style.use(sty.ATLAS)` - use default ATLAS style from https://github.com/kratsg/ATLASstylempl, note it defaults to Helvetica, which is not supplied in this package as explained below, and will only work properly if already available on the system

#### Styles can be chained:
- e.g. `plt.style.use([sty.ROOT, sty.fira, sty.firamath])`
- reappearing rcParams get overwritten silently

#### Styles can be modified on the fly
- Since styles are dictionaries and they can be chained/overwritten they can be easiely modified on the fly. e.g.
```
plt.style.use(sty.ROOT)
plt.style.use({"font.sans-serif":'Comic Sans MS'})
```

#### Styling with LaTeX
- `plt.style.use(sty.ROOTtex)` - Use LaTeX to produce all text labels
- Requires having the full tex-live distro
- True Helvetica
- Use sansmath as the math font
- Takes longer and not always better
- In general more possibilities, but a bit more difficult to get everything working properly

## Experiment annotations
```diff
+ plt.style.use(hep.cms.style.ROOT)
+ ax = hep.cms.cmslabel(ax, data=False, paper=False, year='2017')
```
<p float="center">
  <img src="img/style1.png" width="400" />
  <img src="img/style2.png" width="400" />
</p>


## Plot helper functions

#### Box (or other) aspect

#### Square plot with subplot (works with `tight_layout()`)

#### Append a new axes, without modifying the original

# Notes

## Consistency \& Fonts
As it is ROOT does not come with any fonts and therefore relies on using system fonts. Therfore the font in a figure can be dependent on whether it was produced on OSX or PC. The default sans-serif font used is Helvetica, but it only comes with OSX, in Windows this will silently fallback to Arial.

### License
Both Helvetica and Arial are proprietary, which as far as fonts go means you can use it to create any text/graphics once you have the license, but you cannot redistribute the font files as part of other software. That means we cannot just package Helvetica with this to make sure everyone has the same font in plots.

Luckily for fonts it seems only the software is copyrighted, not the actual shapes, which means there are quite a few open alternatives with similar look. The most closely resembling Helvetica being Tex Gyre Heros

#### Tex Gyre Heros
http://www.gust.org.pl/projects/e-foundry/tex-gyre/heros

You can compare yourself if the differences are meanigful below.

<p float="center">
  <img src="FontComp.png" width="400" />
</p>

They are Tex Gyre Heros, Helvetica and Arial respecively.

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

## What doesn't work

### Context styles and fonts
```
with pyplot.style.context(sty.ROOT):
    plotting...
```
- This syntax would be ideal, however, it doesn't work properly for fonts and there are no plans by mpl devs to fix this behaviour https://github.com/matplotlib/matplotlib/issues/11673

For now one has to set the style globally
```
plt.style.use(sty.ROOT)
```
