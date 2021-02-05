import pytest
from pytest import approx
import matplotlib.pyplot
import mplhep as hep


@pytest.fixture(autouse=True)
def mock_matplotlib(mocker):
    fig = mocker.Mock(spec=matplotlib.pyplot.Figure)
    ax = mocker.Mock(spec=matplotlib.pyplot.Axes)
    step = mocker.Mock(name="step")
    step.get_color.return_value = "current-color"
    ax.configure_mock(**{"step.return_value": (step,)})

    mocker.patch("matplotlib.pyplot", autospec=True)
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig, ax))


def test_simple():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 10))
    h = [1, 3, 2]
    bins = [0, 1, 2, 3]
    hep.histplot(h, bins, yerr=True, label="X", ax=ax)

    assert not plt.mock_calls
    assert not fig.mock_calls

    assert len(ax.mock_calls) == 3

    ax.step.assert_called_once_with(
        approx([0.0, 0.0, 1.0, 2.0, 3.0, 3.0]),
        approx([0, 1.0, 3.0, 2.0, 2.0, 0]),
        where="post",
        label=None,
        marker="",
    )

    assert ax.errorbar.call_count == 2
    ax.errorbar.assert_any_call(
        approx([]), approx([]), yerr=1, xerr=1, color="current-color", label="X"
    )
    ax.errorbar.assert_any_call(
        approx([0.5, 1.5, 2.5]),
        approx([1, 3, 2]),
        yerr=[
            approx([1.0, 1.73205081, 1.41421356]),
            approx([1.0, 1.73205081, 1.41421356]),
        ],
        color="current-color",
        linestyle="none",
    )
