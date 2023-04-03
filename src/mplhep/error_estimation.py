from __future__ import annotations

import warnings

import numpy as np
import scipy.stats

_coverage1sd = scipy.stats.norm.cdf(1) - scipy.stats.norm.cdf(-1)


def poisson_interval(sumw, sumw2, coverage=_coverage1sd):
    """Frequentist coverage interval for Poisson-distributed observations
    Parameters
    ----------
        sumw : numpy.ndarray
            Sum of weights vector
        sumw2 : numpy.ndarray
            Sum weights squared vector
        coverage : float, optional
            Central coverage interval, defaults to 68%
    Calculates the so-called 'Garwood' interval,
    c.f. https://www.ine.pt/revstat/pdf/rs120203.pdf or
    http://ms.mcmaster.ca/peter/s743/poissonalpha.html
    For weighted data, this approximates the observed count by ``sumw**2/sumw2``, which
    effectively scales the unweighted poisson interval by the average weight.
    This may not be the optimal solution: see https://arxiv.org/pdf/1309.1287.pdf for a
    proper treatment. When a bin is zero, the scale of the nearest nonzero bin is
    substituted to scale the nominal upper bound.
    If all bins zero, a warning is generated and interval is set to ``sumw``.
    # Taken from Coffea
    """
    scale = np.empty_like(sumw)
    scale[sumw != 0] = sumw2[sumw != 0] / sumw[sumw != 0]
    if np.sum(sumw == 0) > 0:
        missing = np.where(sumw == 0)
        available = np.nonzero(sumw)
        if len(available[0]) == 0:
            warnings.warn(
                "All sumw are zero!  Cannot compute meaningful error bars",
                RuntimeWarning,
                stacklevel=2,
            )
            return np.vstack([sumw, sumw])
        nearest = np.sum(
            [np.subtract.outer(d, d0) ** 2 for d, d0 in zip(available, missing)]
        ).argmin(axis=0)
        argnearest = tuple(dim[nearest] for dim in available)
        scale[missing] = scale[argnearest]
    counts = sumw / scale
    lo = scale * scipy.stats.chi2.ppf((1 - coverage) / 2, 2 * counts) / 2.0
    hi = scale * scipy.stats.chi2.ppf((1 + coverage) / 2, 2 * (counts + 1)) / 2.0
    interval = np.array([lo, hi])
    interval[interval == np.nan] = 0.0  # chi2.ppf produces nan for counts=0
    return interval


def normal_interval(pw, tw, pw2, tw2, coverage=_coverage1sd):
    """Compute errors based on the expansion of pass/(pass + fail), possibly weighted
    Parameters
    ----------
    pw : np.ndarray
        Numerator, or number of (weighted) successes, vectorized
    tw : np.ndarray
        Denominator or number of (weighted) trials, vectorized
    pw2 : np.ndarray
        Numerator sum of weights squared, vectorized
    tw2 : np.ndarray
        Denominator sum of weights squared, vectorized
    coverage : float, optional
        Central coverage interval, defaults to 68%
    c.f. https://root.cern.ch/doc/master/TEfficiency_8cxx_source.html#l02515
    """

    eff = pw / tw

    variance = (pw2 * (1 - 2 * eff) + tw2 * eff**2) / (tw**2)
    sigma = np.sqrt(variance)

    prob = 0.5 * (1 - coverage)
    delta = np.zeros_like(sigma)
    delta[sigma != 0] = scipy.stats.norm.ppf(prob, scale=sigma[sigma != 0])

    lo = eff - np.minimum(eff + delta, np.ones_like(eff))
    hi = np.maximum(eff - delta, np.zeros_like(eff)) - eff

    return np.array([lo, hi])


def clopper_pearson_interval(num, denom, coverage=_coverage1sd):
    """Compute Clopper-Pearson coverage interval for a binomial distribution
    Parameters
    ----------
        num : numpy.ndarray
            Numerator, or number of successes, vectorized
        denom : numpy.ndarray
            Denominator or number of trials, vectorized
        coverage : float, optional
            Central coverage interval, defaults to 68%
    c.f. http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    """
    if np.any(num > denom):
        raise ValueError(
            "Found numerator larger than denominator while calculating binomial uncertainty"
        )
    lo = scipy.stats.beta.ppf((1 - coverage) / 2, num, denom - num + 1)
    hi = scipy.stats.beta.ppf((1 + coverage) / 2, num + 1, denom - num)
    interval = np.array([lo, hi])
    interval[:, num == 0.0] = 0.0
    interval[1, num == denom] = 1.0
    return interval
