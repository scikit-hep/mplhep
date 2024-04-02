from __future__ import annotations

import os

import hist
import matplotlib.pyplot as plt
import numpy as np
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep  # noqa: E402

"""
To test run:
pytest --mpl

When adding new tests, run:
pytest --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_simple():
    fig, ax = plt.subplots(figsize=(10, 10))
    h = [1, 3, 2]
    bins = [0, 1, 2, 3]
    hep.histplot(h, bins, yerr=True, label="X")
    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_simple_xerr():
    fig, ax = plt.subplots(figsize=(10, 10))
    h = np.array([1, 3, 2])
    bins = [0, 1, 2, 4]
    hep.histplot(h, bins, yerr=True, histtype="errorbar")
    hep.histplot(h * 2, bins, yerr=True, histtype="errorbar", xerr=0.1)
    hep.histplot(h * 3, bins, yerr=True, histtype="errorbar", xerr=True)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_simple2d():
    fig, ax = plt.subplots()
    h = [[1, 3, 2], [1, 3, 2]]
    hep.hist2dplot(h)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_log():
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for ax in axs[0]:
        hep.histplot([1, 2, 3, 2], range(5), ax=ax)
    ax.semilogy()
    for ax in axs[1]:
        hep.histplot([1, 2, 3, 2], range(5), ax=ax, edges=False)
    ax.semilogy()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_onebin_hist():
    import hist

    fig, axs = plt.subplots()
    h = hist.Hist(hist.axis.Regular(1, 0, 1))
    h.fill([-1, 0.5])
    hep.histplot(h, ax=axs)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot(h, bins, ax=axs[0])

    axs[1].set_title("Plot No Edges", fontsize=18)
    hep.histplot(h, bins, edges=False, ax=axs[1])

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(h, bins, yerr=np.sqrt(h), ax=axs[2])

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot(h, bins, histtype="fill", ax=axs[3])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_density():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot(h, bins, ax=axs[0], density=True)

    axs[1].set_title("Plot No Edges", fontsize=18)
    hep.histplot(h, bins, edges=False, ax=axs[1], density=True)

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(h, bins, yerr=np.sqrt(h), ax=axs[2], density=True)

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot(h, bins, histtype="fill", ax=axs[3], density=True)

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_histplot_flow():
    np.random.seed(0)
    h = hist.new.Reg(20, 5, 15, name="x").Weight()
    h.fill(np.random.normal(10, 3, 400))
    fig, axs = plt.subplots(2, 2, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    hep.histplot(h, ax=axs[0], flow="hint")
    hep.histplot(h, ax=axs[1], flow="show")
    hep.histplot(h, ax=axs[2], flow="sum")
    hep.histplot(h, ax=axs[3], flow=None)

    axs[0].set_title("Default(hint)", fontsize=18)
    axs[1].set_title("Show", fontsize=18)
    axs[2].set_title("Sum", fontsize=18)
    axs[3].set_title("None", fontsize=18)
    return fig


@pytest.mark.parametrize("variances", [True, False], ids=["variances", "no_variances"])
@pytest.mark.mpl_image_compare(style="default")
def test_histplot_hist_flow(variances):
    np.random.seed(0)
    entries = np.random.normal(10, 3, 400)
    hist_constr = [
        hist.new.Reg(20, 5, 15, name="x", flow=True),
        hist.new.Reg(20, 5, 15, name="x", underflow=True, overflow=False),
        hist.new.Reg(20, 5, 15, name="x", underflow=False, overflow=True),
        hist.new.Reg(20, 5, 15, name="x", flow=False),
    ]
    if variances:
        hists = [h.Weight() for h in hist_constr]
    else:
        hists = [h.Double() for h in hist_constr]
    for h in hists:
        h.fill(entries, weight=np.ones_like(entries))

    fig, axs = plt.subplots(2, 2, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    for i, h in enumerate(hists):
        hep.histplot(h, ax=axs[i], flow="show", yerr=variances)

    axs[0].set_title("Two-side overflow", fontsize=18)
    axs[1].set_title("Left-side overflow", fontsize=18)
    axs[2].set_title("Right-side overflow", fontsize=18)
    axs[3].set_title("No overflow", fontsize=18)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    axs[0].legend()
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_histplot_uproot_flow():
    np.random.seed(0)
    entries = np.random.normal(10, 3, 400)
    h = hist.new.Reg(20, 5, 15, name="x", flow=True).Weight()
    h2 = hist.new.Reg(20, 5, 15, name="x", flow=True).Weight()
    h3 = hist.new.Reg(20, 5, 15, name="x", flow=True).Weight()
    h4 = hist.new.Reg(20, 5, 15, name="x", flow=True).Weight()

    h.fill(entries)
    h2.fill(entries[entries < 15])
    h3.fill(entries[entries > 5])
    h4.fill(entries[(entries > 5) & (entries < 15)])
    import uproot

    with uproot.recreate("flow_th1.root") as f:
        f["h"] = h
        f["h2"] = h2
        f["h3"] = h3
        f["h4"] = h4

    with uproot.open("flow_th1.root") as f:
        h = f["h"]
        h2 = f["h2"]
        h3 = f["h3"]
        h4 = f["h4"]

    fig, axs = plt.subplots(2, 2, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    hep.histplot(h, ax=axs[0], flow="show")
    hep.histplot(h2, ax=axs[1], flow="show")
    hep.histplot(h3, ax=axs[2], flow="show")
    hep.histplot(h4, ax=axs[3], flow="show")

    axs[0].set_title("Two-side overflow", fontsize=18)
    axs[1].set_title("Left-side overflow", fontsize=18)
    axs[2].set_title("Right-side overflow", fontsize=18)
    axs[3].set_title("No overflow", fontsize=18)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    axs[0].legend()
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_histplot_type_flow():
    np.random.seed(0)
    entries = np.random.normal(10, 3, 400)

    histh = hist.new.Reg(20, 5, 15, name="x", flow=False).Weight()
    nph, bins = np.histogram(entries, bins=20, range=(5, 15))
    histh.fill(entries)

    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10, 5))
    axs = axs.flatten()

    hep.histplot(histh, ax=axs[0], flow="hint", yerr=False)
    hep.histplot(nph, bins, ax=axs[1], flow="hint")

    axs[0].set_title("hist, noflow bin", fontsize=18)
    axs[1].set_title("numpy hist", fontsize=18)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_hist2dplot_hist_all_flow_show():
    flow_opts = []
    for ufl1 in [True, False]:
        for ofl1 in [True, False]:
            for ufl2 in [True, False]:
                for ofl2 in [True, False]:
                    flow_opts.append([ufl1, ofl1, ufl2, ofl2])

    np.random.seed(0)
    _fill = np.random.normal(2.5, 2, 10000).reshape(-1, 2).T
    fig, axs = plt.subplots(4, 4)
    axs = axs.flatten()
    for i, opt in enumerate(flow_opts):
        h = (
            hist.new.Reg(5, 0, 5, overflow=opt[0], underflow=opt[1])
            .Reg(5, 0, 5, overflow=opt[2], underflow=opt[3])
            .Weight()
            .fill(*_fill)
        )
        hep.hist2dplot(h, ax=axs[i], flow="show", cbar=False)
        axs[i].set_xticks([])
        axs[i].set_yticks([])
        axs[i].set_xlabel("")
        axs[i].set_ylabel("")
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_hist2dplot_hist_all_flow_hint():
    flow_opts = []
    for ufl1 in [True, False]:
        for ofl1 in [True, False]:
            for ufl2 in [True, False]:
                for ofl2 in [True, False]:
                    flow_opts.append([ufl1, ofl1, ufl2, ofl2])

    np.random.seed(0)
    _fill = np.random.normal(2.5, 2, 10000).reshape(-1, 2).T
    fig, axs = plt.subplots(4, 4)
    axs = axs.flatten()
    for i, opt in enumerate(flow_opts):
        h = (
            hist.new.Reg(5, 0, 5, overflow=opt[0], underflow=opt[1])
            .Reg(5, 0, 5, overflow=opt[2], underflow=opt[3])
            .Weight()
            .fill(*_fill)
        )
        hep.hist2dplot(h, ax=axs[i], flow="hint", cbar=False)
        axs[i].set_xticks([])
        axs[i].set_yticks([])
        axs[i].set_xlabel("")
        axs[i].set_ylabel("")
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_multiple():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default Overlay", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, ax=axs[0])

    axs[1].set_title("Default Overlay w/ Errorbars", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=[np.sqrt(h), np.sqrt(1.5 * h)], ax=axs[1])

    axs[2].set_title("Automatic Errorbars", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=True, ax=axs[2])

    axs[3].set_title("With Labels", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=True, ax=axs[3], label=["First", "Second"])
    axs[3].legend(fontsize=16, prop={"family": "Tex Gyre Heros"})

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_stack():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, stack=True, ax=axs[0])

    axs[1].set_title("Plot No Edges", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, edges=False, stack=True, ax=axs[1])

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(
        [h, 1.5 * h], bins, yerr=[np.sqrt(h), np.sqrt(h)], stack=True, ax=axs[2]
    )

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot([1.5 * h, h], bins, histtype="fill", stack=True, ax=axs[3])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots()
    hep.hist2dplot(H, xedges, yedges, labels=True)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_hist2dplot_flow():
    np.random.seed(0)
    h = hist.Hist(
        hist.axis.Regular(20, 5, 15, name="x"),
        hist.axis.Regular(20, -5, 5, name="y"),
        hist.storage.Weight(),
    )
    h.fill(np.random.normal(10, 3, 400), np.random.normal(0, 4, 400))
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()

    hep.hist2dplot(h, ax=axs[0], flow="hint", cmin=0, cmax=10)
    hep.hist2dplot(h, ax=axs[1], flow="show", cmin=0, cmax=10)
    hep.hist2dplot(h, ax=axs[2], flow="sum", cmin=0, cmax=10)
    hep.hist2dplot(h, ax=axs[3], flow=None, cmin=0, cmax=10)

    axs[0].set_title("Default(hint)", fontsize=18)
    axs[1].set_title("Show", fontsize=18)
    axs[2].set_title("Sum", fontsize=18)
    axs[3].set_title("None", fontsize=18)
    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_inputs_nobin():
    np.random.seed(0)
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()
    hep.hist2dplot([[1, 2, 3]], ax=axs[0])
    hep.hist2dplot(np.array([[1, 2, 3]]), ax=axs[1])
    hep.hist2dplot([[1, 2, 3], [3, 4, 1]], ax=axs[2])
    hep.hist2dplot(np.array([[1, 2, 3], [3, 4, 1]]), ax=axs[3])
    return fig


@pytest.mark.parametrize("cbarextend", [False, True])
@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_cbar(cbarextend):
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots()
    hep.hist2dplot(H, xedges, yedges, labels=True, cbar=True, cbarextend=cbarextend)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_cbar_subplots():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    hep.hist2dplot(H, xedges, yedges, labels=True, cbar=True, ax=ax1)
    hep.hist2dplot(H * 2, xedges, yedges, labels=True, cbar=True, ax=ax2)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_custom_labels():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots()

    @np.vectorize
    def _fmt(x):
        return f"${x:.2f}$"

    hep.hist2dplot(H, xedges, yedges, labels=_fmt(H))
    return fig


def test_hist2dplot_labels_option():
    """
    Test the functionality of hist2dplot's label options.
    """
    np.random.seed(0)

    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    assert hep.hist2dplot(H, xedges, yedges, labels=True)

    assert hep.hist2dplot(H, xedges, yedges, labels=False)

    label_array = np.chararray(H.shape, itemsize=2)
    label_array[:] = "hi"
    assert hep.hist2dplot(H, xedges, yedges, labels=label_array)

    label_array = np.chararray(H.shape[0], itemsize=2)
    label_array[:] = "hi"
    # Label array shape invalid
    with pytest.raises(ValueError):
        hep.hist2dplot(H, xedges, yedges, labels=label_array)

    # Invalid label type
    with pytest.raises(ValueError):
        hep.hist2dplot(H, xedges, yedges, labels=5)


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_kwargs():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 1000), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    hep.histplot(
        [h * 2, h * 1, h * 0.5],
        bins,
        label=["1", "2", "3"],
        stack=True,
        histtype="step",
        linestyle="--",
        color=["green", "black", (1, 0, 0, 0.4)],
        ax=axs[0],
    )
    axs[0].legend()

    hep.histplot(
        [h, h, h],
        bins,
        label=["1", "2", "3"],
        stack=True,
        histtype="step",
        linestyle=["--", ":", "-."],
        color=(1, 0, 0, 0.8),
        ax=axs[1],
    )
    axs[1].legend()

    hep.histplot(
        [h, h, h],
        bins,
        label=["1", "2", "3"],
        histtype="step",
        binwnorm=[0.5, 3, 6],
        linestyle=["--", ":", "-."],
        color=(1, 0, 0, 0.8),
        ax=axs[2],
    )
    axs[2].legend()

    hep.histplot(
        [h, h, h],
        bins,
        label=["1", "2", "3"],
        histtype="fill",
        binwnorm=[0.5, 3, 6],
        color=["green", "darkorange", "red"],
        alpha=[0.4, 0.7, 0.2],
        ax=axs[3],
    )
    axs[3].legend()

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_histplot_real():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 1000), bins=np.geomspace(1, 20, 10))

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()
    a, b, c = h, h * 2, np.random.poisson(h * 3)

    hep.histplot(
        [a, b, c], bins=bins, ax=axs[0], yerr=True, label=["MC1", "MC2", "Data"]
    )
    hep.histplot([a, b], bins=bins, ax=axs[1], stack=True, label=["MC1", "MC2"])
    hep.histplot(
        [c], bins=bins, ax=axs[1], yerr=True, histtype="errorbar", label="Data"
    )

    hep.histplot(
        [a, b], bins=bins, ax=axs[2], stack=True, label=["MC1", "MC2"], binwnorm=[1, 1]
    )
    hep.histplot(
        c,
        bins=bins,
        ax=axs[2],
        yerr=True,
        histtype="errorbar",
        label="Data",
        binwnorm=1,
    )
    hep.histplot(
        [a, b], bins=bins, ax=axs[3], stack=True, label=["MC1", "MC2"], density=True
    )
    hep.histplot(
        c,
        bins=bins,
        ax=axs[3],
        yerr=True,
        histtype="errorbar",
        label="Data",
        density=True,
    )
    for ax in axs:
        ax.legend()
    axs[0].set_title("Raw")
    axs[1].set_title("Data/MC")
    axs[2].set_title("Data/MC binwnorm")
    axs[3].set_title("Data/MC Density")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_w2():
    fig, ax = plt.subplots()
    hep.histplot([0, 3, 0], range(4), w2=np.array([0, 3, 0]))
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_types():
    hs, bins = [[2, 3, 4], [5, 4, 3]], [0, 1, 2, 3]
    fig, axs = plt.subplots(3, 2, figsize=(8, 12))
    axs = axs.flatten()

    for i, htype in enumerate(["step", "fill", "errorbar"]):
        hep.histplot(hs[0], bins, yerr=True, histtype=htype, ax=axs[i * 2], alpha=0.7)
        hep.histplot(hs, bins, yerr=True, histtype=htype, ax=axs[i * 2 + 1], alpha=0.7)

    return fig


h = np.geomspace(1, 10, 10)


@pytest.mark.parametrize("h", [h, [h, h], [h]])
@pytest.mark.parametrize("yerr", [h / 4, [h / 4, h / 4], 4])
@pytest.mark.parametrize("htype", ["step", "fill", "errorbar"])
def test_histplot_inputs_pass(h, yerr, htype):
    bins = np.linspace(1, 10, 11)

    fig, ax = plt.subplots()
    hep.histplot(h, bins, yerr=yerr, histtype=htype)
    plt.close(fig)
