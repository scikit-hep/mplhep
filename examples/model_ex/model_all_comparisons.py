"""
Data/model comparisons
======================

All supported comparisons between data and model.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import numpy as np
import seaborn as sns

import mplhep as mh

np.random.seed(42)
# --8<-- [end:imports]

# --8<-- [start:setup]
# Create data histogram with mixed components
data_hist = hist.new.Regular(50, -8, 8).Weight()
data_hist.fill(
    np.concatenate(
        [
            np.random.normal(0, 2, 3000),
            np.random.normal(-3, 0.8, 1500),
            np.random.normal(-2, 1.5, 1200),
            np.random.normal(0, 0.5, 300),
        ]
    )
)

# Create background component histograms
background_hists = [
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(0, 2, 3500)),
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-3, 0.8, 1800)),
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-2, 1.5, 1400)),
]

# Scale backgrounds to match data
scale = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [scale * h for h in background_hists]
# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, axes = mh.subplots(nrows=6, hspace=0.3)

mh.comp.data_model(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=["c0", "c1", "c2"],
    stacked_colors=sns.color_palette("cubehelix", 3),
    xlabel="",
    ylabel="Entries",
    comparison="ratio",
    fig=fig,
    ax_main=axes[0],
    ax_comparison=axes[1],
)

mh.add_text(
    r"Multiple data-model comparisons, $\mathbf{with}$ model uncertainty",
    ax=axes[0],
    loc="over left",
    fontsize="small",
)
mh.add_text(
    r'  $\mathbf{→}$ comparison = "ratio"', ax=axes[1], loc="over left", fontsize=13
)

# Add remaining comparison types
for k, comp in enumerate(
    ["split_ratio", "pull", "relative_difference", "difference"], start=2
):
    mh.comp.comparison(
        data_hist,
        sum(background_hists),
        ax=axes[k],
        comparison=comp,
        xlabel="",
        h1_label="Data",
        h2_label="MC",
        h1_w2method="poisson",
    )
    mh.add_text(
        rf'  $\mathbf{{→}}$ comparison = "{comp}"',
        ax=axes[k],
        fontsize=13,
        loc="over left",
    )
    mh.set_fitting_ylabel_fontsize(axes[k])

axes[-1].set_xlabel("Observable")
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig("model_all_comparisons.svg", bbox_inches="tight")
