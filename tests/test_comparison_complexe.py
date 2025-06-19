import boost_histogram as bh
import numpy as np
import pytest

from mplhep import get_comparison


@pytest.fixture
def setup_histograms():
    """
    Fixture to create two histograms for testing.
    """
    rng = np.random.default_rng(8311311)
    h1 = bh.Histogram(
        bh.axis.Regular(10, -5, 5, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h1.fill(rng.normal(size=100000))
    h2 = bh.Histogram(
        bh.axis.Regular(10, -5, 5, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h2.fill(rng.normal(size=80000))
    return h1, h2


def test_difference_complex_values(setup_histograms):
    """
    Test difference with random values.
    """
    h1, h2 = setup_histograms

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="difference"
    )

    assert pytest.approx(values) == np.array(
        [-3.0, -47.0, -449.0, -2623.0, -6946.0, -6879.0, -2468.0, -575.0, -10.0, 0.0]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            2.6457513110645907,
            15.198684153570664,
            62.66578013557319,
            156.60459763365824,
            247.58029000710053,
            247.55807399476996,
            156.96496424361712,
            62.07253821135398,
            15.297058540778355,
            2.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="difference", h1_w2method="poisson"
    )

    assert pytest.approx(values) == np.array(
        [-3.0, -47.0, -449.0, -2623.0, -6946.0, -6879.0, -2468.0, -575.0, -10.0, 0.0]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            2.5823990507642316,
            15.187670343763216,
            62.66311771237798,
            156.60353291251036,
            247.5796166128547,
            247.55740054015223,
            156.96390196934192,
            62.069850261501465,
            15.28611912206896,
            1.9154072301701288,
        ]
    )
    assert pytest.approx(low_uncertainty) == np.array(
        [
            3.458077990673633,
            15.87202875900091,
            63.34102670156633,
            157.2767218220309,
            248.24860043264547,
            248.22678627397232,
            157.63960095483972,
            62.73478020967331,
            16.02801576337975,
            2.993042497122517,
        ]
    )


def test_ratio_complex_values(setup_histograms):
    """
    Test ratio with random values.
    """
    h1, h2 = setup_histograms

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio"
    )

    assert pytest.approx(values) == np.array(
        [
            0.4,
            0.6618705035971223,
            0.7947897623400365,
            0.8067629291292177,
            0.7964303508103514,
            0.7981632533302037,
            0.8179000959197226,
            0.7402890695573623,
            0.9180327868852459,
            1.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            0.3346640106136302,
            0.08895650327968395,
            0.02553343623433043,
            0.010362621371283012,
            0.006475424104450652,
            0.006489300534544608,
            0.01047411689978261,
            0.02412251340854011,
            0.1201371137656762,
            1.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="ratio", h1_w2method="poisson"
    )

    assert pytest.approx(values) == np.array(
        [
            0.4,
            0.6618705035971223,
            0.7947897623400365,
            0.8067629291292177,
            0.7964303508103514,
            0.7981632533302037,
            0.8179000959197226,
            0.7402890695573623,
            0.9180327868852459,
            1.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            0.31424734572549723,
            0.08885909032232045,
            0.025532071318029308,
            0.010362534042899352,
            0.006475401990114839,
            0.006489278416967618,
            0.010474030233249552,
            0.024121102346281367,
            0.12004352597513421,
            0.9577036150850644,
        ]
    )
    assert pytest.approx(low_uncertainty) == np.array(
        [
            0.5570746229934151,
            0.09484770051247897,
            0.025879130731868948,
            0.010417720738564722,
            0.006497363933563098,
            0.006511254880705368,
            0.010529131460053793,
            0.024469519001226153,
            0.12637764392827852,
            1.4965212485612585,
        ]
    )


def test_split_ratio_complex_values(setup_histograms):
    """
    Test split ratio with random values.
    """
    h1, h2 = setup_histograms

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="split_ratio"
    )

    assert pytest.approx(values) == np.array(
        [
            0.4,
            0.6618705035971223,
            0.7947897623400365,
            0.8067629291292177,
            0.7964303508103514,
            0.7981632533302037,
            0.8179000959197226,
            0.7402890695573623,
            0.9180327868852459,
            1.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            0.282842712474619,
            0.06900477011960747,
            0.019059103712973532,
            0.007709372753648256,
            0.004831289095230075,
            0.004839308721902339,
            0.007768414861135622,
            0.01828571136404441,
            0.08674594462506854,
            0.7071067811865476,
        ]
    )
    assert pytest.approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="split_ratio", h1_w2method="poisson"
    )

    assert pytest.approx(values) == np.array(
        [
            0.4,
            0.6618705035971223,
            0.7947897623400365,
            0.8067629291292177,
            0.7964303508103514,
            0.7981632533302037,
            0.8179000959197226,
            0.7402890695573623,
            0.9180327868852459,
            1.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            0.2583629119969045,
            0.06887914601983501,
            0.019057275098979868,
            0.007709255370032222,
            0.00483125945512883,
            0.004839279063162287,
            0.007768298008664885,
            0.018283849850174488,
            0.0866162856135678,
            0.6459072799922612,
        ]
    )
    assert pytest.approx(low_uncertainty) == np.array(
        [
            0.5275719245593493,
            0.07644923227878979,
            0.019519797023699485,
            0.007783277712946144,
            0.004860655827597242,
            0.00486870902804312,
            0.007842432908702224,
            0.01874110314510096,
            0.09520105928933346,
            1.3189298113983732,
        ]
    )


def test_pull_complex_values(setup_histograms):
    """
    Test pull with random values.
    """
    h1, h2 = setup_histograms

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="pull"
    )

    assert pytest.approx(values) == np.array(
        [
            -1.1338934190276817,
            -3.092372966310914,
            -7.164994978577123,
            -16.749188974233867,
            -28.055545131645136,
            -27.787419287101617,
            -15.723253987874301,
            -9.263355689470163,
            -0.6537204504606134,
            0.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array([1.0] * 10)
    assert pytest.approx(high_uncertainty) == low_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="pull", h1_w2method="poisson"
    )

    assert pytest.approx(values) == np.array(
        [
            -0.867533933037641,
            -2.9611841506616883,
            -7.088612600415852,
            -16.677611089631554,
            -27.980016756970926,
            -27.71256117543868,
            -15.655964523197618,
            -9.16556969002242,
            -0.6239075471118297,
            0.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array([1.0] * 10)
    assert pytest.approx(high_uncertainty) == low_uncertainty


def test_asymmetry_complex_values(setup_histograms):
    """
    Test asymmetry with random values.
    """
    h1, h2 = setup_histograms

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="asymmetry"
    )

    assert pytest.approx(values) == np.array(
        [
            -0.42857142857142855,
            -0.20346320346320346,
            -0.11433664374840845,
            -0.10695208970438329,
            -0.11331897676846776,
            -0.11224606347393326,
            -0.10017046838217387,
            -0.1492343628341552,
            -0.042735042735042736,
            0.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            0.41121309550224255,
            0.06714322983291869,
            0.016061640147033433,
            0.006421925838700013,
            0.004064944404444152,
            0.004064823476588014,
            0.0064027316127981,
            0.01628859006719069,
            0.06543171177234845,
            0.5,
        ]
    )
    assert pytest.approx(high_uncertainty) == low_uncertainty


def test_efficiency_complex_values():
    """
    Test efficiency with random values.
    """
    rng = np.random.default_rng(8311311)
    x1 = rng.normal(size=100000)
    x2 = rng.choice(x1, size=10000)
    h1 = bh.Histogram(
        bh.axis.Regular(10, -5, 5, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h1.fill(x1)
    h2 = bh.Histogram(
        bh.axis.Regular(10, -5, 5, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h2.fill(x2)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )

    assert pytest.approx(values) == np.array(
        [
            0.0,
            0.1079136690647482,
            0.09734917733089579,
            0.09864446736407839,
            0.10128659769643328,
            0.09779355671615515,
            0.10337194717036818,
            0.10388437217705511,
            0.10655737704918032,
            0.0,
        ]
    )
    assert pytest.approx(high_uncertainty) == np.array(
        [
            0.12371791482634838,
            0.02661654698726243,
            0.006343589231090674,
            0.0025597549707911415,
            0.0016334320872715157,
            0.0016090633836174837,
            0.002615474280842884,
            0.006489834814808297,
            0.02830633673352296,
            0.19364916731037085,
        ]
    )
    assert pytest.approx(high_uncertainty) == low_uncertainty
