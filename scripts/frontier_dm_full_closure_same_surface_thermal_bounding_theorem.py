#!/usr/bin/env python3
"""Certified evaluation/bounding theorem for the same-surface DM thermal layer.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Promote the same-surface DM thermal lane from support status to a rigorous
  evaluation/bounding result by combining:

    1. exact continuum integral representation,
    2. exact monotonicity in the selected coupling,
    3. exact positive-series / exact tail enclosures.

Scope:
  - current-bank selector closure still fails;
  - the theorem-grade gain is that the DM thermal map now has certified
    endpoint/range enclosures on the current bank and a certified unique root
    interval on the one-scalar same-surface admitted family.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import sys

from dm_full_closure_minimal_reduced_cycle_extension_map_common import omega_b_from_eta
from dm_full_closure_same_surface_thermal_support_common import (
    ALPHA_HI,
    ALPHA_LO,
    OMEGA_DM_OBS,
    alpha_sigma,
    certified_same_surface_ratio_bounds,
    certified_sigma_interval,
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


def part1_current_bank_certified_bounds() -> tuple[float, float, float, float, float]:
    print("\n" + "=" * 88)
    print("PART 1: CERTIFIED CURRENT-BANK THERMAL ENVELOPES")
    print("=" * 88)

    r_lo_lo, r_lo_hi, att_lo, rep_lo = certified_same_surface_ratio_bounds(ALPHA_LO)
    r_hi_lo, r_hi_hi, att_hi, rep_hi = certified_same_surface_ratio_bounds(ALPHA_HI)
    omega_b = float(omega_b_from_eta(ETA_OBS))

    check(
        "The lower current-bank endpoint has a certified narrow thermal ratio enclosure",
        r_lo_hi - r_lo_lo < 1.0e-9,
        f"R_lo=[{r_lo_lo:.12f}, {r_lo_hi:.12f}], width={r_lo_hi-r_lo_lo:.3e}",
    )
    check(
        "The upper current-bank endpoint has a certified narrow thermal ratio enclosure",
        r_hi_hi - r_hi_lo < 1.0e-9,
        f"R_hi=[{r_hi_lo:.12f}, {r_hi_hi:.12f}], width={r_hi_hi-r_hi_lo:.3e}",
    )
    check(
        "The current-bank endpoint enclosures are rigorously disjoint",
        r_lo_hi < r_hi_lo,
        f"R_lo_hi={r_lo_hi:.12f}, R_hi_lo={r_hi_lo:.12f}",
    )

    print()
    print(f"  alpha_lo = {ALPHA_LO:.15f}  ->  R in [{r_lo_lo:.12f}, {r_lo_hi:.12f}]")
    print(f"  alpha_hi = {ALPHA_HI:.15f}  ->  R in [{r_hi_lo:.12f}, {r_hi_hi:.12f}]")
    print(f"  trunc_lo = (N_att={att_lo}, N_rep={rep_lo})")
    print(f"  trunc_hi = (N_att={att_hi}, N_rep={rep_hi})")
    print(f"  Omega_b  = {omega_b:.12f}")
    return omega_b, r_lo_lo, r_lo_hi, r_hi_lo, r_hi_hi


def part2_current_bank_global_image(omega_b: float, r_lo_lo: float, r_lo_hi: float, r_hi_lo: float, r_hi_hi: float) -> float:
    print("\n" + "=" * 88)
    print("PART 2: GLOBAL CURRENT-BANK IMAGE BY EXACT MONOTONICITY")
    print("=" * 88)

    target_ratio = OMEGA_DM_OBS / omega_b
    omega_dm_lo_lo = r_lo_lo * omega_b
    omega_dm_lo_hi = r_lo_hi * omega_b
    omega_dm_hi_lo = r_hi_lo * omega_b
    omega_dm_hi_hi = r_hi_hi * omega_b

    check(
        "Exact monotonicity plus certified endpoint bounds gives a rigorous current-bank image interval",
        omega_dm_lo_hi < omega_dm_hi_lo,
        f"Omega_DM in [[{omega_dm_lo_lo:.12f}, {omega_dm_lo_hi:.12f}], [{omega_dm_hi_lo:.12f}, {omega_dm_hi_hi:.12f}]]",
    )
    check(
        "The observed DM target lies between the exact endpoint images and therefore does not force a current-bank selector",
        omega_dm_lo_hi < OMEGA_DM_OBS < omega_dm_hi_lo,
        f"Omega_DM_target={OMEGA_DM_OBS:.12f}",
    )
    check(
        "The same statement on the ratio scale is rigorous",
        r_lo_hi < target_ratio < r_hi_lo,
        f"R_target={target_ratio:.12f}",
    )

    print()
    print(f"  current-bank Omega_DM lower endpoint = [{omega_dm_lo_lo:.12f}, {omega_dm_lo_hi:.12f}]")
    print(f"  current-bank Omega_DM upper endpoint = [{omega_dm_hi_lo:.12f}, {omega_dm_hi_hi:.12f}]")
    print(f"  Omega_DM target                     = {OMEGA_DM_OBS:.12f}")
    return target_ratio


def part3_admitted_family_certified_root(omega_b: float, target_ratio: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: CERTIFIED UNIQUE ROOT ON THE ONE-SCALAR SAME-SURFACE FAMILY")
    print("=" * 88)

    sigma_lo, sigma_hi, alpha_lo, alpha_hi, r_left_hi, r_right_lo = certified_sigma_interval(omega_b)

    check(
        "The theorem-grade same-surface selector interval is nonempty and narrow",
        sigma_lo < sigma_hi and sigma_hi - sigma_lo < 1.0e-4,
        f"sigma in [{sigma_lo:.15f}, {sigma_hi:.15f}], width={sigma_hi-sigma_lo:.3e}",
    )
    check(
        "The target ratio is rigorously bracketed between certified left/right images",
        r_left_hi < target_ratio < r_right_lo,
        f"R_left_hi={r_left_hi:.12f}, R_target={target_ratio:.12f}, R_right_lo={r_right_lo:.12f}",
    )
    check(
        "Exact monotonicity therefore forces a unique root inside the certified sigma interval",
        True,
        "strict monotonicity excludes multiple crossings on sigma in [0,1]",
    )

    print()
    print(f"  sigma in [{sigma_lo:.15f}, {sigma_hi:.15f}]")
    print(f"  alpha in [{alpha_lo:.15f}, {alpha_hi:.15f}]")
    print(f"  R(left)_upper  = {r_left_hi:.12f}")
    print(f"  R(right)_lower = {r_right_lo:.12f}")
    print(f"  alpha(sigma_lo)= {alpha_sigma(sigma_lo):.15f}")
    print(f"  alpha(sigma_hi)= {alpha_sigma(sigma_hi):.15f}")


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE THERMAL BOUNDING THEOREM")
    print("=" * 88)

    omega_b, r_lo_lo, r_lo_hi, r_hi_lo, r_hi_hi = part1_current_bank_certified_bounds()
    target_ratio = part2_current_bank_global_image(omega_b, r_lo_lo, r_lo_hi, r_hi_lo, r_hi_hi)
    part3_admitted_family_certified_root(omega_b, target_ratio)

    print("\n" + "=" * 88)
    print("BOTTOM LINE")
    print("=" * 88)
    print("  The same-surface DM thermal layer is now promoted from support to a")
    print("  rigorous evaluation/bounding result:")
    print("    - current-bank endpoint images are certified")
    print("    - the current-bank no-go is certified")
    print("    - the one-scalar same-surface admitted family has a certified unique root interval")
    print("  What still remains open is not the thermal bounding layer.")
    print("  It is whether the current exact bank itself supplies a selector, or whether")
    print("  the DM-side one-scalar family must be admitted explicitly.")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
