#!/usr/bin/env python3
"""Converged thermal selector support on the one-scalar same-surface DM family.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Replace the unstable coarse-grid retained thermal runner with a corrected
  high-precision continuum same-surface evaluation on the admitted DM-side
  family.

Scope:
  This is support, not theorem-grade closure. It stabilizes the admitted-family
  selector numerically and shows that the previous 9/62 clue was an artifact of
  the coarse thermal discretization.
"""

from __future__ import annotations

import sys

from dm_full_closure_minimal_reduced_cycle_extension_map_common import R_BASE_EXACT, omega_b_from_eta
from dm_full_closure_same_surface_thermal_support_common import (
    OMEGA_DM_OBS,
    converged_sigma_root,
    coarse_sigma_root,
)
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


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE CONVERGED THERMAL SELECTOR SUPPORT")
    print("=" * 88)

    omega_b = float(omega_b_from_eta(ETA_OBS))
    sigma_base, alpha_base, r_base = coarse_sigma_root(omega_b)
    sigma_conv, alpha_conv, r_conv = converged_sigma_root(omega_b)
    sigma_struct = float(1.0 / (2.0 * R_BASE_EXACT))

    print("\n" + "=" * 88)
    print("PART 1: THE ADMITTED DM FAMILY STILL HAS A UNIQUE CLOSURE CROSSING")
    print("=" * 88)
    check(
        "The converged same-surface kernel still gives a unique interior selector on the one-scalar DM family",
        0.0 < sigma_conv < 1.0 and abs(r_conv * omega_b - OMEGA_DM_OBS) < 1.0e-12,
        f"sigma_conv={sigma_conv:.15f}, alpha_conv={alpha_conv:.15f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE COARSE THERMAL ROOT IS NOT STABLE")
    print("=" * 88)
    check(
        "The converged selector differs materially from the coarse retained runner",
        abs(sigma_conv - sigma_base) > 1.0e-5,
        f"sigma_base={sigma_base:.15f}, sigma_conv={sigma_conv:.15f}",
    )
    check(
        "The converged selector also differs materially from the coarse 9/62 clue",
        abs(sigma_conv - sigma_struct) > 1.0e-5,
        f"sigma_conv={sigma_conv:.15f}, sigma_9/62={sigma_struct:.15f}",
    )

    print()
    print(f"  sigma_base   = {sigma_base:.15f}")
    print(f"  sigma_conv   = {sigma_conv:.15f}")
    print(f"  sigma_9/62   = {sigma_struct:.15f}")
    print(f"  alpha_conv   = {alpha_conv:.15f}")
    print(f"  R_conv       = {r_conv:.12f}")
    print(f"  Omega_DM     = {r_conv * omega_b:.12f}")

    print("\n" + "=" * 88)
    print("BOTTOM LINE")
    print("=" * 88)
    print("  Honest status:")
    print("    - the one-scalar same-surface DM family still closes positively")
    print("    - but the selector value must be read from a converged thermal evaluator,")
    print("      not from the coarse retained grid")
    print("    - the previous 9/62 clue does not survive as a stable selector law")
    print("    - current-bank selector closure is still open")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
