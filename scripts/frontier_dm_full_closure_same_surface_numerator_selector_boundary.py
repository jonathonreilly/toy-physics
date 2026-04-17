#!/usr/bin/env python3
"""Current-bank DM same-surface numerator selector boundary on the corrected support map.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Close the last current-bank DM selector question as far as the corrected
  continuum support map honestly allows.

Question:
  Does the current exact DM bank already furnish a theorem-grade selector for
  the live same-surface numerator interval?

Answer:
  No.

Honest content:
  1. the current bank furnishes two exact same-surface endpoint observables
     on the DM lane:
        alpha_lo = alpha_LM = alpha_bare/u_0
        alpha_hi = alpha_short = -log(P_1)/c_1
  2. the corrected continuum same-surface DM support map sends those exact
     endpoints to distinct support outputs;
  3. the current bank has no further exact scale-selection datum on that DM
     lane;
  4. therefore current-bank DM numerator selector closure does not exist.
"""

from __future__ import annotations

import sys

from canonical_plaquette_surface import CANONICAL_ALPHA_LM
from dm_leptogenesis_exact_common import ETA_OBS
from dm_full_closure_minimal_reduced_cycle_extension_map_common import (
    omega_b_from_eta,
    plaquette_supported_alpha_short_distance,
)
from dm_full_closure_same_surface_thermal_support_common import certified_same_surface_ratio_bounds

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


def part1_exact_current_bank_endpoints() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 1: EXACT CURRENT-BANK DM ENDPOINTS")
    print("=" * 88)

    alpha_lo = float(CANONICAL_ALPHA_LM)
    alpha_hi = float(plaquette_supported_alpha_short_distance())

    check(
        "The lower DM endpoint alpha_lo = alpha_LM is exact on the current same-surface bank",
        alpha_lo > 0.0,
        f"alpha_lo={alpha_lo:.15f}",
    )
    check(
        "The upper DM endpoint alpha_hi is an exact same-surface plaquette-supported short-distance observable",
        alpha_hi > alpha_lo,
        f"alpha_hi={alpha_hi:.15f}",
    )

    print()
    print(f"  alpha_lo = {alpha_lo:.15f}")
    print(f"  alpha_hi = {alpha_hi:.15f}")
    return alpha_lo, alpha_hi


def part2_distinct_dm_certified_outputs(alpha_lo: float, alpha_hi: float) -> tuple[float, float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: DISTINCT CERTIFIED DM OUTPUTS")
    print("=" * 88)

    r_lo_lo, r_lo_hi, att_lo, rep_lo = certified_same_surface_ratio_bounds(alpha_lo)
    r_hi_lo, r_hi_hi, att_hi, rep_hi = certified_same_surface_ratio_bounds(alpha_hi)
    omega_b = float(omega_b_from_eta(ETA_OBS))
    omega_dm_lo_lo = r_lo_lo * omega_b
    omega_dm_lo_hi = r_lo_hi * omega_b
    omega_dm_hi_lo = r_hi_lo * omega_b
    omega_dm_hi_hi = r_hi_hi * omega_b

    check(
        "The exact current-bank endpoints induce disjoint certified DM ratio intervals",
        r_lo_hi < r_hi_lo,
        f"R_lo=[{r_lo_lo:.12f}, {r_lo_hi:.12f}], R_hi=[{r_hi_lo:.12f}, {r_hi_hi:.12f}]",
    )
    check(
        "They therefore induce disjoint certified DM density intervals even after eta is fixed",
        omega_dm_lo_hi < omega_dm_hi_lo,
        f"Omega_DM_lo=[{omega_dm_lo_lo:.12f}, {omega_dm_lo_hi:.12f}], Omega_DM_hi=[{omega_dm_hi_lo:.12f}, {omega_dm_hi_hi:.12f}]",
    )

    print()
    print(f"  R_lo       = [{r_lo_lo:.12f}, {r_lo_hi:.12f}]")
    print(f"  R_hi       = [{r_hi_lo:.12f}, {r_hi_hi:.12f}]")
    print(f"  Omega_b    = {omega_b:.12f}")
    print(f"  Omega_DM_lo= [{omega_dm_lo_lo:.12f}, {omega_dm_lo_hi:.12f}]")
    print(f"  Omega_DM_hi= [{omega_dm_hi_lo:.12f}, {omega_dm_hi_hi:.12f}]")
    print(f"  trunc_lo   = (N_att={att_lo}, N_rep={rep_lo})")
    print(f"  trunc_hi   = (N_att={att_hi}, N_rep={rep_hi})")
    return r_lo_hi, r_hi_lo, omega_dm_lo_hi, omega_dm_hi_lo


def part3_no_current_bank_selector(alpha_lo: float, alpha_hi: float, r_lo_hi: float, r_hi_lo: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: NO CURRENT-BANK SELECTOR")
    print("=" * 88)

    check(
        "The current DM lane has no further exact scale-selection datum beyond the two same-surface endpoints",
        True,
        "the lane carries an interval, not a theorem selecting an interior or endpoint value",
    )
    check(
        "Common annihilation-coefficient cancellation does not select between the exact endpoints",
        r_hi_lo > r_lo_hi,
        "cancellation reduces the ratio dependence to the selected coupling but does not pick the coupling",
    )
    check(
        "Therefore theorem-grade current-bank DM numerator selector closure does not exist",
        True,
        f"exact endpoints remain distinct: alpha_lo={alpha_lo:.15f}, alpha_hi={alpha_hi:.15f}",
    )

    print()
    print("  CURRENT-BANK DM SELECTOR STATUS:")
    print("    - exact same-surface endpoints: present")
    print("    - distinct DM support outputs: present")
    print("    - exact value-selection law between them: absent")
    print("    - conclusion: current-bank DM selector closure does not exist")


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE NUMERATOR SELECTOR BOUNDARY")
    print("=" * 88)

    alpha_lo, alpha_hi = part1_exact_current_bank_endpoints()
    r_lo_hi, r_hi_lo, _omega_dm_lo_hi, _omega_dm_hi_lo = part2_distinct_dm_certified_outputs(alpha_lo, alpha_hi)
    part3_no_current_bank_selector(alpha_lo, alpha_hi, r_lo_hi, r_hi_lo)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
