#!/usr/bin/env python3
"""Shared higher-fidelity same-surface thermal support helpers for the DM lane.

Scope:
  - ``omega_b_from_eta`` and ``R_BASE_EXACT`` stay in the existing map common.
  - this module owns the corrected continuum thermal support layer on the
    retained same-surface DM interval
  - it also exposes exact series/tail support objects used to harden the
    thermal analysis around the remaining DM selector gate

Honest status:
  The functions here are stronger than the old coarse or SciPy-grid support,
  but they are still support helpers, not theorem-grade current-bank closure.
"""

from __future__ import annotations

import math
from functools import lru_cache

import mpmath as mp

from canonical_plaquette_surface import CANONICAL_ALPHA_LM
from dm_full_closure_minimal_reduced_cycle_extension_map_common import (
    R_BASE_EXACT,
    omega_b_from_eta,
    plaquette_supported_alpha_short_distance,
)
from dm_leptogenesis_exact_common import ETA_OBS

mp.mp.dps = 80

X_F = mp.mpf(25)
A = X_F / 4
R_BASE_MP = mp.mpf(31) / 9
SQRT_PI = mp.sqrt(mp.pi)

ALPHA_LO = float(CANONICAL_ALPHA_LM)
ALPHA_HI = float(plaquette_supported_alpha_short_distance())
OMEGA_DM_OBS = 0.268


def alpha_sigma(sigma: float) -> float:
    return float(ALPHA_LO + sigma * (ALPHA_HI - ALPHA_LO))


def stable_sommerfeld(alpha_eff: float | mp.mpf, v: float | mp.mpf) -> mp.mpf:
    alpha_eff_mp = mp.mpf(alpha_eff)
    v_mp = mp.mpf(v)
    zeta = alpha_eff_mp / v_mp
    if abs(zeta) < mp.mpf("1.0e-40"):
        return mp.mpf(1)
    return (mp.pi * zeta) / (1 - mp.e ** (-mp.pi * zeta))


@lru_cache(maxsize=None)
def converged_thermal_avg(alpha_eff: float, x_f: float, attractive: bool) -> float:
    sign = mp.mpf(1) if attractive else mp.mpf(-1)
    alpha_eff_mp = mp.mpf(alpha_eff)
    a_mp = mp.mpf(x_f) / 4

    def numerator(v: mp.mpf) -> mp.mpf:
        return stable_sommerfeld(sign * alpha_eff_mp, v) * v * v * mp.e ** (-a_mp * v * v)

    def denominator(v: mp.mpf) -> mp.mpf:
        return v * v * mp.e ** (-a_mp * v * v)

    num = mp.quad(numerator, [0, 1, mp.inf])
    den = mp.quad(denominator, [0, 1, mp.inf])
    return float(num / den)


@lru_cache(maxsize=None)
def converged_same_surface_ratio(alpha_s: float) -> float:
    alpha_s_mp = mp.mpf(alpha_s)
    alpha_1 = (mp.mpf(4) / 3) * alpha_s_mp
    alpha_8 = alpha_s_mp / 6
    s_1 = mp.mpf(converged_thermal_avg(float(alpha_1), 25.0, attractive=True))
    s_8 = mp.mpf(converged_thermal_avg(float(alpha_8), 25.0, attractive=False))
    s_vis = (8 * s_1 + s_8) / 9
    return float(R_BASE_MP * s_vis)


def _ratio_delta(sigma: mp.mpf, r_target: mp.mpf) -> mp.mpf:
    return mp.mpf(converged_same_surface_ratio(alpha_sigma(float(sigma)))) - r_target


@lru_cache(maxsize=None)
def converged_sigma_root(omega_b: float | None = None) -> tuple[float, float, float]:
    if omega_b is None:
        omega_b = float(omega_b_from_eta(ETA_OBS))
    omega_b_mp = mp.mpf(omega_b)
    r_target = mp.mpf(OMEGA_DM_OBS) / omega_b_mp

    lo = mp.mpf(0)
    hi = mp.mpf(1)
    flo = _ratio_delta(lo, r_target)
    fhi = _ratio_delta(hi, r_target)
    if not (flo < 0 < fhi):
        raise ValueError("same-surface support root is not bracketed on sigma in [0,1]")

    sigma_guess = (r_target - mp.mpf(converged_same_surface_ratio(ALPHA_LO))) / (
        mp.mpf(converged_same_surface_ratio(ALPHA_HI)) - mp.mpf(converged_same_surface_ratio(ALPHA_LO))
    )
    s0 = max(lo, sigma_guess - mp.mpf("0.05"))
    s1 = min(hi, sigma_guess + mp.mpf("0.05"))
    sigma = mp.findroot(lambda s: _ratio_delta(s, r_target), (s0, s1), tol=mp.mpf("1.0e-30"), maxsteps=30)
    alpha = mp.mpf(alpha_sigma(float(sigma)))
    ratio = mp.mpf(converged_same_surface_ratio(float(alpha)))
    return float(sigma), float(alpha), float(ratio)


def coarse_sigma_root(omega_b: float | None = None) -> tuple[float, float, float]:
    if omega_b is None:
        omega_b = float(omega_b_from_eta(ETA_OBS))
    r_target = OMEGA_DM_OBS / omega_b
    from dm_full_closure_minimal_reduced_cycle_extension_map_common import retained_structural_dm_ratio

    lo = 0.0
    hi = 1.0
    flo = retained_structural_dm_ratio(alpha_sigma(lo)) - r_target
    fhi = retained_structural_dm_ratio(alpha_sigma(hi)) - r_target
    if not (flo < 0.0 < fhi):
        raise ValueError("coarse support root is not bracketed on sigma in [0,1]")

    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fmid = retained_structural_dm_ratio(alpha_sigma(mid)) - r_target
        if fmid > 0.0:
            hi = mid
        else:
            lo = mid

    sigma = 0.5 * (lo + hi)
    alpha = alpha_sigma(sigma)
    ratio = retained_structural_dm_ratio(alpha)
    return float(sigma), float(alpha), float(ratio)


def exact_j1_meijerg(c: float | mp.mpf) -> mp.mpf:
    c_mp = mp.mpf(c)
    if c_mp == 0:
        return mp.mpf(1) / (2 * A)
    z = 4 / (A * c_mp * c_mp)
    return mp.meijerg(([0, mp.mpf("0.5"), 1], []), ([], []), z) / (2 * SQRT_PI * A)


def exact_j2_meijerg(c: float | mp.mpf) -> mp.mpf:
    c_mp = mp.mpf(c)
    if c_mp == 0:
        return SQRT_PI / (4 * A ** mp.mpf("1.5"))
    z = 4 / (A * c_mp * c_mp)
    return mp.meijerg(([-mp.mpf("0.5"), mp.mpf("0.5"), 1], []), ([], []), z) / (
        2 * SQRT_PI * A ** mp.mpf("1.5")
    )


def attractive_thermal_bounds(alpha_eff: float, terms: int = 60) -> tuple[float, float]:
    """Exact-series lower/upper support bounds for the attractive thermal factor."""
    b = mp.pi * mp.mpf(alpha_eff)
    pref = 4 * A ** mp.mpf("1.5") / SQRT_PI
    partial = mp.nsum(lambda n: b * exact_j1_meijerg(n * b), [0, terms - 1])
    upper = partial + exact_j2_meijerg(terms * b) + b * exact_j1_meijerg(terms * b)
    return float(pref * partial), float(pref * upper)


def repulsive_thermal_bounds(alpha_eff: float, terms: int = 600) -> tuple[float, float]:
    """Exact-series lower/upper support bounds for the repulsive thermal factor."""
    b = mp.pi * mp.mpf(alpha_eff)
    pref = 4 * A ** mp.mpf("1.5") / SQRT_PI
    partial = mp.nsum(lambda n: b * exact_j1_meijerg(n * b), [1, terms])
    upper = partial + exact_j2_meijerg((terms + 1) * b) + b * exact_j1_meijerg((terms + 1) * b)
    return float(pref * partial), float(pref * upper)


def same_surface_ratio_bounds(alpha_s: float, attractive_terms: int = 60, repulsive_terms: int = 600) -> tuple[float, float]:
    """Exact-series/tail support bounds for the same-surface DM ratio."""
    alpha_s_mp = mp.mpf(alpha_s)
    s1_lo, s1_hi = attractive_thermal_bounds(float((mp.mpf(4) / 3) * alpha_s_mp), terms=attractive_terms)
    s8_lo, s8_hi = repulsive_thermal_bounds(float(alpha_s_mp / 6), terms=repulsive_terms)
    r_lo = R_BASE_MP * ((8 * mp.mpf(s1_lo) + mp.mpf(s8_lo)) / 9)
    r_hi = R_BASE_MP * ((8 * mp.mpf(s1_hi) + mp.mpf(s8_hi)) / 9)
    return float(r_lo), float(r_hi)


@lru_cache(maxsize=None)
def certified_same_surface_ratio_bounds(
    alpha_s: float,
    tol: float = 1.0e-10,
    attractive_terms: int = 60,
    repulsive_terms: int = 600,
    max_terms: int = 76800,
) -> tuple[float, float, int, int]:
    """Rigorous same-surface ratio enclosure refined to a target width.

    The lower/upper bounds come from exact positive-series partial sums plus
    exact tail inequalities, so increasing the truncation only tightens the
    enclosure. This function doubles the truncation depths until the requested
    ratio-width target is met or the configured cap is reached.
    """

    att = int(attractive_terms)
    rep = int(repulsive_terms)
    lo, hi = same_surface_ratio_bounds(alpha_s, attractive_terms=att, repulsive_terms=rep)

    while hi - lo > tol and (att < max_terms or rep < max_terms):
        att = min(2 * att, max_terms)
        rep = min(2 * rep, max_terms)
        lo, hi = same_surface_ratio_bounds(alpha_s, attractive_terms=att, repulsive_terms=rep)

    return float(lo), float(hi), att, rep


def certified_sigma_interval(
    omega_b: float | None = None,
    ratio_tol: float = 1.0e-10,
    initial_radius: float = 1.0e-6,
    max_radius: float = 0.25,
) -> tuple[float, float, float, float, float, float]:
    """Rigorous enclosure of the unique same-surface admitted-family selector.

    Uses the exact monotonicity theorem plus certified ratio bounds at two
    enclosing sigma values. The converged support root is used only as a guide
    for where to start the bracket search; the returned interval is certified
    entirely by exact series/tail enclosures.
    """

    if omega_b is None:
        omega_b = float(omega_b_from_eta(ETA_OBS))

    target_ratio = float(OMEGA_DM_OBS / omega_b)
    sigma_guess, _alpha_guess, _ratio_guess = converged_sigma_root(omega_b)
    radius = float(initial_radius)

    while radius <= max_radius:
        sigma_lo = max(0.0, sigma_guess - radius)
        sigma_hi = min(1.0, sigma_guess + radius)
        alpha_lo = alpha_sigma(sigma_lo)
        alpha_hi = alpha_sigma(sigma_hi)
        r_lo_lo, r_lo_hi, _att_lo, _rep_lo = certified_same_surface_ratio_bounds(alpha_lo, tol=ratio_tol)
        r_hi_lo, r_hi_hi, _att_hi, _rep_hi = certified_same_surface_ratio_bounds(alpha_hi, tol=ratio_tol)
        if r_lo_hi < target_ratio < r_hi_lo:
            return (
                float(sigma_lo),
                float(sigma_hi),
                float(alpha_lo),
                float(alpha_hi),
                float(r_lo_hi),
                float(r_hi_lo),
            )
        radius *= 2.0

    raise ValueError("Could not certify a unique sigma interval on the admitted same-surface family")
