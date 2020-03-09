import mplhep.plot as hep

# To monkeyclass
from matplotlib.pyplot import Axes


# Add and overwrite axes methods
class MonkeyAxes(Axes):
    def histplot(self, *args, **kwargs):
        return hep.histplot(*args, ax=self, **kwargs)

    def hist2dplot(self, *args, **kwargs):
        return hep.hist2dplot(*args, ax=self, **kwargs)

    # def set_xlabel(self, *args, **kwargs):
    #     if 'x' not in kwargs:
    #         kwargs.update(x=1.0)
    #     if 'ha' not in kwargs or 'horizontalalignment' not in kwargs:
    #         kwargs.update(ha='right')
    #     return Axes.set_xlabel(self, *args, **kwargs)


# Add
Axes.histplot = MonkeyAxes.histplot
Axes.hist2dplot = MonkeyAxes.hist2dplot

# Overwrite
# Axes.set_xlabel = MonkeyAxes.set_xlabel

# Import rest of pyplot
from matplotlib.pyplot import * # noqa