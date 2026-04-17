#!/usr/bin/env python3
"""Sensitivity boundary for same-surface DM selector claims from the retained thermal kernel.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Test whether the apparent structural collapse clue

      sigma ~= 1 / (2 R_base) = 9/62

  is robust on the retained same-surface DM kernel, or whether it is an
  artifact of the current coarse thermal averaging implementation.

Answer:
  It is not robust enough to support a selector claim on the current branch.
  Refining the retained thermal quadrature shifts the admitted-family root by
  orders of magnitude more than the apparent 9/62 residual itself.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.optimize import brentq

from dm_full_closure_minimal_reduced_cycle_extension_map_common import R_BASE_EXACT, omega_b_from_eta
from dm_full_closure_same_surface_thermal_support_common import ALPHA_HI, ALPHA_LO, OMEGA_DM_OBS, coarse_sigma_root
from dm_leptogenesis_exact_common import ETA_OBS

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def sommerfeld(alpha_eff: float, v: float) -> float:
    zeta = alpha_eff / v
    if abs(zeta) < 1.0e-15:
        return 1.0
    arg = -np.pi * zeta
    if arg > 700.0:
        return 0.0
    return float((np.pi * zeta) / (1.0 - np.exp(arg)))


def thermal_avg(alpha_eff: float, x_f: float, attractive: bool, npts: int, vmin: float = 0.001, vmax: float = 2.0) -> float:
    v = np.linspace(vmin, vmax, npts)
    weight = v**2 * np.exp(-x_f * v**2 / 4.0)
    sign = 1.0 if attractive else -1.0
    vals = np.array([sommerfeld(sign * alpha_eff, float(v_i)) for v_i in v], dtype=float)
    return float(np.trapezoid(vals * weight, v) / np.trapezoid(weight, v))


def refined_ratio(alpha_s: float, npts: int, vmin: float = 0.001, vmax: float = 2.0) -> float:
    c2_su3 = 4.0 / 3.0
    alpha_1 = c2_su3 * alpha_s
    alpha_8 = (1.0 / 6.0) * alpha_s
    s_1 = thermal_avg(alpha_1, 25.0, attractive=True, npts=npts, vmin=vmin, vmax=vmax)
    s_8 = thermal_avg(alpha_8, 25.0, attractive=False, npts=npts, vmin=vmin, vmax=vmax)
    w_1 = (1.0 / 9.0) * c2_su3**2
    w_8 = (8.0 / 9.0) * (1.0 / 6.0) ** 2
    s_vis = (w_1 * s_1 + w_8 * s_8) / (w_1 + w_8)
    return float(R_BASE_EXACT * s_vis)


def alpha_sigma(sigma: float) -> float:
    return float(ALPHA_LO + sigma * (ALPHA_HI - ALPHA_LO))


def refined_sigma_root(npts: int, omega_b: float, vmin: float = 0.001, vmax: float = 2.0) -> float:
    r_target = OMEGA_DM_OBS / omega_b
    return float(brentq(lambda s: refined_ratio(alpha_sigma(s), npts, vmin=vmin, vmax=vmax) - r_target, 0.0, 1.0))


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE THERMAL SELECTOR SENSITIVITY BOUNDARY")
    print("=" * 88)

    omega_b = float(omega_b_from_eta(ETA_OBS))
    sigma_struct = float(1.0 / (2.0 * R_BASE_EXACT))
    sigma_base, _alpha_base, _r_base = coarse_sigma_root(omega_b)

    print("\n" + "=" * 88)
    print("PART 1: BASELINE APPARENT MATCH")
    print("=" * 88)
    check(
        "The coarse retained runner gives an apparent near-match to 9/62",
        abs(sigma_base - sigma_struct) < 2.0e-7,
        f"sigma_base={sigma_base:.15f}, sigma_struct={sigma_struct:.15f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: QUADRATURE REFINEMENT DESTROYS THE APPARENT MATCH")
    print("=" * 88)
    sigma_4000 = refined_sigma_root(4000, omega_b)
    sigma_8000 = refined_sigma_root(8000, omega_b)
    sigma_16000 = refined_sigma_root(16000, omega_b)

    check(
        "Refining the thermal quadrature shifts the selector root by far more than the apparent 9/62 residual",
        abs(sigma_4000 - sigma_base) > 1.0e-4 and abs(sigma_8000 - sigma_base) > 1.0e-4,
        f"sigma_2000={sigma_base:.15f}, sigma_4000={sigma_4000:.15f}, sigma_8000={sigma_8000:.15f}",
    )
    check(
        "The refined roots also move materially away from 9/62",
        abs(sigma_8000 - sigma_struct) > 1.0e-4 and abs(sigma_16000 - sigma_struct) > 1.0e-4,
        f"sigma_8000={sigma_8000:.15f}, sigma_16000={sigma_16000:.15f}, sigma_struct={sigma_struct:.15f}",
    )

    print()
    print(f"  sigma_2000  = {sigma_base:.15f}")
    print(f"  sigma_4000  = {sigma_4000:.15f}")
    print(f"  sigma_8000  = {sigma_8000:.15f}")
    print(f"  sigma_16000 = {sigma_16000:.15f}")
    print(f"  sigma_9/62  = {sigma_struct:.15f}")

    print("\n" + "=" * 88)
    print("BOTTOM LINE")
    print("=" * 88)
    print("  Honest status:")
    print("    - the apparent 9/62 match in the coarse retained thermal runner is not stable")
    print("    - the retained same-surface thermal kernel is not yet numerically converged enough")
    print("      to support a structural selector claim")
    print("    - so 9/62 must not be promoted as a DM selector law on the current branch")
    print("    - the correct next step is to replace the retained thermal average with a")
    print("      converged or exact thermal theorem before attempting further selector collapse")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
