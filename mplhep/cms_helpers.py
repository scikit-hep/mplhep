def cms_annot(ax, paper=False, supplementary=False, data=False, year=2017, lumi=None, llabel=None, rlabel=None):
    from matplotlib import rcParams
    _font_size = rcParams['font.size']
    # CMS label    
    cms = ax.annotate('CMS', xy=(0.001, 1.015), xycoords='axes fraction', fontsize=_font_size*1.3, fontname='Arial',
                ha='left', fontweight='bold', annotation_clip=False)
    
    # Right label
    if rlabel != None:
        _lumi = rlabel
    else:
        if lumi != None:
            _lumi = r'{lumi}, {year} (13 TeV)'.format(lumi=str(lumi)+' $\mathrm{fb^{-1}}$', year=str(year))
        else: 
            _lumi = '{} (13 TeV)'.format(str(year))

    ax.annotate(_lumi, xy=(1, 1.015), xycoords='axes fraction', fontsize=_font_size, fontweight='normal', fontname='Arial',
            ha='right', annotation_clip=False)
    
    # Left label 
    if llabel != None:
        _label = llabel
    else:
        _label = ""
        if not data:
            _label = " ".join(["Simulation", _label])
        if not paper:
            _label = " ".join([_label, "Preliminary"])
        if supplementary:
            _label = " ".join([_label, "Supplementary"])    
        
        _label = " ".join(_label.split())            
    
    ax.annotate(_label, xy=(0.001, 1.015), xycoords='axes fraction', fontsize=_font_size, fontname='Arial', 
                xytext=(cms.get_window_extent(renderer=f.canvas.get_renderer()).width, 0), textcoords='offset points',
                fontstyle='italic', ha='left', annotation_clip=False)
    return ax

def cms_ticks(ax):
    import matplotlib.ticker as plticker
    xl = ax.get_xlim()
    ax.xaxis.set_major_locator(plticker.MultipleLocator(base=(xl[-1]-xl[0])/5))
    ax.xaxis.set_minor_locator(plticker.MultipleLocator(base=(xl[-1]-xl[0])/40))
    yl = ax.get_ylim()
    ax.yaxis.set_major_locator(plticker.MultipleLocator(base=(yl[-1]-yl[0])/5))
    ax.yaxis.set_minor_locator(plticker.MultipleLocator(base=(yl[-1]-yl[0])/40))

    return ax
    