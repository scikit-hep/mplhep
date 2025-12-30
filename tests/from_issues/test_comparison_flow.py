import hist
import matplotlib.pyplot as plt
import numpy as np
import pytest

import mplhep as hep


@pytest.mark.filterwarnings("ignore:divide by zero:RuntimeWarning")
@pytest.mark.mpl_image_compare(remove_text=False, style="default", tolerance=20)
def test_comparison_flow():
    """Test all flow options with comparison plotters (data_model)."""
    np.random.seed(42)

    # Create histograms with underflow and overflow
    h_data = hist.Hist(
        hist.axis.Regular(10, 0, 10, name="x", underflow=True, overflow=True)
    )
    h_data.fill(np.random.normal(5, 2, 1000))

    h_model = hist.Hist(
        hist.axis.Regular(10, 0, 10, name="x", underflow=True, overflow=True)
    )
    h_model.fill(np.random.normal(5, 2, 1000))

    # Create 2x2 grid for different flow options
    fig = plt.figure(figsize=(14, 10))

    # Define grid layout - 2 rows per subplot (main + comparison)
    gs = fig.add_gridspec(4, 2, height_ratios=[3, 1, 3, 1], hspace=0.3, wspace=0.3)

    flow_options = ["hint", "show", "sum", "none"]
    titles = ["Default(hint)", "Show", "Sum", "None"]

    for idx, (flow_opt, title) in enumerate(zip(flow_options, titles)):
        row_offset = (idx // 2) * 2  # 0 for first two, 2 for last two
        col = idx % 2

        ax_main = fig.add_subplot(gs[row_offset, col])
        ax_comparison = fig.add_subplot(gs[row_offset + 1, col], sharex=ax_main)

        # Create comparison plot with the specific flow option
        _, _, _ = hep.comparison_plotters.data_model(
            h_data,
            unstacked_components=[h_model],
            unstacked_labels=["Model"],
            data_label="Data",
            xlabel="x",
            flow=flow_opt,
            fig=fig,
            ax_main=ax_main,
            ax_comparison=ax_comparison,
        )

        ax_main.set_title(title, fontsize=14)

    return fig
