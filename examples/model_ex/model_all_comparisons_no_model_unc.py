"""
Data/model comparisons, no model uncertainty
============================================

All supported comparisons between data and model, without model uncertainty.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import numpy as np
import seaborn as sns

import mplhep as mh

# --8<-- [end:imports]

# --8<-- [start:setup]
# Set seed for reproducible demo
np.random.seed(42)

# Create demo histograms directly
bins = np.linspace(-9, 12, 51)

# Background components with different shapes
bkg1_data = np.random.normal(0, 2.5, 4000)  # Broad background
bkg2_data = np.random.normal(3, 1.2, 2000)  # Narrower peak
bkg3_data = np.random.normal(-1, 1.8, 1500)  # Another component

# Data = backgrounds + signal peak + some deficit
data_data = np.concatenate(
    [
        np.random.normal(0, 2.5, 3500),  # Less background here
        np.random.normal(3, 1.2, 1800),  # Similar background
        np.random.normal(-1, 1.8, 1400),  # Similar background
        np.random.normal(0, 0.8, 500),  # Clear signal peak
        np.random.normal(-3, 0.5, 200),  # Some deficit here (under-predicted)
    ]
)

# Create histograms
data_hist = hist.new.Regular(50, -8, 8).Weight().fill(data_data)

background_hists = [
    hist.new.Regular(50, -8, 8).Weight().fill(bkg1_data),
    hist.new.Regular(50, -8, 8).Weight().fill(bkg2_data),
    hist.new.Regular(50, -8, 8).Weight().fill(bkg3_data),
]

# Scale backgrounds to match data
total_bkg = sum(background_hists).sum().value
data_total = data_hist.sum().value
scale_factor = data_total / total_bkg
background_hists = [scale_factor * h for h in background_hists]

# Labels and colors
background_labels = ["Broad BG", "Peak BG", "Offset BG"]
background_colors = sns.color_palette("cubehelix", 3)

# Scale backgrounds to match data
total_bkg = sum(background_hists).sum().value
data_total = data_hist.sum().value
scale_factor = data_total / total_bkg
background_hists = [scale_factor * h for h in background_hists]

# Labels and colors
background_labels = ["Background 1", "Background 2", "Background 3"]
background_colors = sns.color_palette("cubehelix", 3)
# --8<-- [end:setup]

# --8<-- [start:plot_body]
# Create comparison plots
fig, axes = mh.subplots(nrows=6, hspace=0.3)

background_sum = sum(background_hists)

mh.comp.data_model(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=background_labels,
    stacked_colors=background_colors,
    xlabel="",
    ylabel="Entries",
    model_uncertainty=False,  # <--
    comparison="ratio",
    fig=fig,
    ax_main=axes[0],
    ax_comparison=axes[1],
)

mh.add_text(
    r"Multiple data-model comparisons, $\mathbf{without}$ model uncertainty",
    ax=axes[0],
    loc="over left",
    fontsize="small",
)
mh.add_text(
    r'  $\mathbf{→}$ comparison = "ratio"', ax=axes[1], loc="over left", fontsize=13
)

for k_comp, comp in enumerate(
    ["split_ratio", "pull", "relative_difference", "difference"], start=2
):
    ax_comparison = axes[k_comp]

    # Copy the original histogram and set the uncertainties of the copy to 0.
    background_sum_copy = background_sum.copy()
    background_sum_copy[:] = np.c_[
        background_sum_copy.values(), np.zeros_like(background_sum_copy.values())
    ]

    mh.comp.comparison(
        data_hist,
        background_sum_copy,
        ax=ax_comparison,
        comparison=comp,
        xlabel="",
        h1_label="Data",
        h2_label="MC",
        h1_w2method="poisson",
    )
    if comp == "pull":
        # Since the uncertainties of the model are neglected, the pull label is "(Data - MC)/sigma_Data"
        ax_comparison.set_ylabel(r"$\frac{Data-MC}{\sigma_{Data}}$")
    mh.add_text(
        rf'  $\mathbf{{→}}$ comparison = "{comp}"',
        ax=ax_comparison,
        loc="over left",
        fontsize=13,
    )
    mh.set_fitting_ylabel_fontsize(ax_comparison)

axes[-1].set_xlabel("Observable")
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig("model_all_comparisons_no_model_unc.svg", bbox_inches="tight")
