from __future__ import annotations

from types import SimpleNamespace

import matplotlib.lines
import matplotlib.pyplot  # noqa: ICN001
import numpy as np
import pytest
from pytest import approx

import mplhep as mh


@pytest.fixture
def mock_matplotlib(mocker):
    fig = mocker.Mock(spec=matplotlib.pyplot.Figure)
    ax = mocker.Mock(spec=matplotlib.pyplot.Axes)
    ax.figure = mocker.MagicMock(spec=matplotlib.pyplot.Figure)
    ax.figure.dpi_scale_trans = mocker.MagicMock()
    ax.get_window_extent.return_value = mocker.MagicMock()
    line2d = mocker.Mock(name="step", spec=matplotlib.lines.Line2D)
    line2d.get_color.return_value = "current-color"
    # errorbar_cont = mocker.Mock(name="err_cont", spec=matplotlib.container.ErrorbarContainer)
    # errorbar_cont.sticky_edges =  mocker.Mock(name="edges")
    ax.step.return_value = (line2d,)
    ax.plot.return_value = (line2d,)
    ax.errorbar.return_value = (line2d,)

    # Mock the _get_lines attribute
    _get_lines = mocker.Mock()
    _get_lines.get_next_color.return_value = "next-color"
    ax._get_lines = _get_lines

    mpl = mocker.patch("matplotlib.pyplot", autospec=True)
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig, ax))

    return SimpleNamespace(fig=fig, ax=ax, line2d=line2d, mpl=mpl)


def test_simple(mock_matplotlib):
    ax = mock_matplotlib.ax

    h = [1, 3, 2]
    bins = [0, 1, 2, 3]
    mh.histplot(h, bins, yerr=True, label="X", ax=ax)

    assert len(ax.mock_calls) == 13

    ax.stairs.assert_called_once_with(
        values=approx([1.0, 3.0, 2.0]),
        edges=approx([0.0, 1.0, 2.0, 3.0]),
        baseline=0,
        label=None,
        linewidth=1.5,
        color="next-color",
    )

    assert ax.errorbar.call_count == 2
    ax.errorbar.assert_any_call(
        approx([]),
        approx([]),
        yerr=1,
        xerr=None,
        linestyle="-",
        color=ax.stairs().get_edgecolor(),
        label="X",
    )

    ax.errorbar.assert_any_call(
        x=approx([0.5, 1.5, 2.5]),
        y=approx([1, 3, 2]),
        yerr=[
            approx([0.82724622, 1.63270469, 1.29181456]),
            approx([2.29952656, 2.91818583, 2.63785962]),
        ],
        color="next-color",
        linestyle="none",
        linewidth=1.5,
    )


def test_histplot_real(mock_matplotlib):
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 1000), bins=10)

    ax = mock_matplotlib.ax
    a, b, c = h, h * 2, np.random.poisson(h * 3)

    mh.histplot([a, b, c], bins=bins, ax=ax, yerr=True, label=["MC1", "MC2", "Data"])
    ax.legend()
    ax.set_title("Raw")
    assert len(ax.mock_calls) == 27

    ax.reset_mock()

    mh.histplot([a, b], bins=bins, ax=ax, stack=True, label=["MC1", "MC2"])
    mh.histplot([c], bins=bins, ax=ax, yerr=True, histtype="errorbar", label="Data")
    ax.legend()
    ax.set_title("Data/MC")
    assert len(ax.mock_calls) == 20
    ax.reset_mock()

    mh.histplot(
        [a, b], bins=bins, ax=ax, stack=True, label=["MC1", "MC2"], binwnorm=[2, 1]
    )
    mh.histplot(
        c,
        bins=bins,
        ax=ax,
        yerr=True,
        histtype="errorbar",
        label="Data",
        binwnorm=1,
    )
    ax.legend()
    ax.set_title("Data/MC binwnorm")
    assert len(ax.mock_calls) == 20
    ax.reset_mock()

    mh.histplot(
        [a, b], bins=bins, ax=ax, stack=True, label=["MC1", "MC2"], density=True
    )
    mh.histplot(
        c,
        bins=bins,
        ax=ax,
        yerr=True,
        histtype="errorbar",
        label="Data",
        density=True,
    )
    ax.legend()
    ax.set_title("Data/MC Density")
    assert len(ax.mock_calls) == 20
