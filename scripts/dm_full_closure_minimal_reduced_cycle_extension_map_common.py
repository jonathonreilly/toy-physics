#!/usr/bin/env python3
"""Shared helpers for the admitted-extension DM numerator/map lane.

Scope discipline:
  - ``omega_b_from_eta`` is the standard BBN conversion used once a closure
    theorem or admitted extension fixes ``eta``.
  - ``R_BASE_EXACT`` is the exact structural group/mass ratio on the current
    DM surface.
  - the Sommerfeld/Coulomb helper chain is the retained same-surface
    evaluation of the DM ratio kernel at a supplied exact coupling.

So these helpers do not select the coupling by themselves, but once the DM
lane fixes ``alpha_num`` they provide the canonical same-surface ratio/map
evaluation.
"""

from __future__ import annotations

import math

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_BARE

H_PARAM = 0.674
R_BASE_EXACT = 31.0 / 9.0


def omega_b_from_eta(eta: float) -> float:
    eta_10 = eta / 1.0e-10
    omega_b_h2 = 3.6515e-3 * eta_10
    return omega_b_h2 / (H_PARAM**2)


def sommerfeld_coulomb(alpha_eff: float, v: float) -> float:
    zeta = alpha_eff / v
    if abs(zeta) < 1.0e-12:
        return 1.0
    return (math.pi * zeta) / (1.0 - math.exp(-math.pi * zeta))


def thermal_avg_sommerfeld(alpha_eff: float, x_f: float, attractive: bool) -> float:
    """Retained thermal average from the audited lattice numerator lane."""
    v_arr = np.linspace(0.001, 2.0, 2000)
    dv = float(v_arr[1] - v_arr[0])
    weight = v_arr**2 * np.exp(-x_f * v_arr**2 / 4.0)
    sign = 1.0 if attractive else -1.0
    vals = np.zeros_like(v_arr)
    for i, v in enumerate(v_arr):
        vals[i] = sommerfeld_coulomb(sign * alpha_eff, float(v))
    return float(np.sum(vals * weight) * dv / (np.sum(weight) * dv))


def conditional_same_surface_dm_ratio(alpha_s: float) -> float:
    """Same-surface DM ratio evaluation at a supplied effective coupling.

    Exact content:
      - structural prefactor ``R_BASE_EXACT = 31/9``

    Retained content:
      - the thermal Coulomb/Sommerfeld evaluation used for the DM numerator
        readout at a supplied same-surface effective coupling ``alpha_s``
    """
    c2_su3 = 4.0 / 3.0
    c2_su2 = 3.0 / 4.0
    f_vis = c2_su3 * 8.0 + c2_su2 * 3.0
    f_dark = c2_su2 * 3.0
    r_base = (3.0 / 5.0) * f_vis / f_dark

    x_f = 25.0
    alpha_1 = c2_su3 * alpha_s
    alpha_8 = (1.0 / 6.0) * alpha_s
    s_1 = thermal_avg_sommerfeld(alpha_1, x_f, attractive=True)
    s_8 = thermal_avg_sommerfeld(alpha_8, x_f, attractive=False)
    w_1 = (1.0 / 9.0) * c2_su3**2
    w_8 = (8.0 / 9.0) * (1.0 / 6.0) ** 2
    s_vis = (w_1 * s_1 + w_8 * s_8) / (w_1 + w_8)
    return float(r_base * s_vis)


def retained_structural_dm_ratio(alpha_s: float) -> float:
    """Backward-compatible alias for the retained same-surface DM ratio."""
    return conditional_same_surface_dm_ratio(alpha_s)


def same_surface_dm_ratio_from_selected_alpha(alpha_s: float) -> float:
    """Canonical same-surface ratio readout once the DM lane selects ``alpha_s``."""
    return conditional_same_surface_dm_ratio(alpha_s)


def plaquette_supported_alpha_short_distance() -> float:
    """Short-distance plaquette-supported coupling on the same g=1 surface."""
    c_1 = math.pi**2 / 3.0
    p_1 = 1.0 - c_1 * CANONICAL_ALPHA_BARE
    return float(-math.log(p_1) / c_1)
