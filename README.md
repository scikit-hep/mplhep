# cmsstyle
- offering mpl stylesheets to modify `matplotlib` defaults to look ROOT-like
- A set of helper functions for common labeling
- Works by copying styles and fonts to respective matplotlib data locations

# Installation 
```
pip install cmsstyle
```
Installation places optimized style sheets to your matplotlib `stylelib` folder and freely licensed fonts - TeX Gyre Heros, Firs Sans and Fira Math - into your `mpl-data` folder. `mpl` font cache is now also cleared to load new fonts properly.

# Basic use
- `plt.style.use(['ROOT'])`
- For examples see https://github.com/andrzejnovak/cmsstyle/blob/master/Examples.ipynb

<p float="center">
  <img src="Example1.png" width="400" />
  <img src="Example2.png" width="400" /> 
</p>

### Available styles:

- `plt.style.use(['ROOT'])` - Default (figure 10x10 inches, full column size)
- `plt.style.use(['ROOTlegacy'])` - Same as ROOT style above, but use ROOT fonts - Helvetica, fallback to Arial - instead of TeX Gyre Heros, requires font to be already available on the system
- `plt.style.use(['ROOTs'])` - Default (figure 6x6 inches, half column size)
- `plt.style.use(['fira'])` - use Fira Sans 

- `plt.style.use(['firamath'])` - use Fira Math

#### Styles can be chained:
- e.g. `plt.style.use(['ROOT', 'fira', 'firamath'])`

#### Styling with LaTeX
- `plt.style.use(['ROOTtex'])` - Use LaTeX to produce all text labels
- Requires having the full tex-live distro
- True Helvetica 
- Use sansmath as the math font
- Takes longer and not always better
- In general more possibilities, but a bit more difficult to get everything working properly


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
with pyplot.style.context(['ROOT']):
    plotting...
```    
- This syntax would be ideal, however, it doesn't work properly for fonts and there are no plans by mpl devs to fix this behaviour https://github.com/matplotlib/matplotlib/issues/11673

For now one has to set the style globally
```
plt.style.use(['ROOT'])
```