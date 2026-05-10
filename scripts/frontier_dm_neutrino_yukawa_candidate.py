#!/usr/bin/env python3
"""
Neutrino Yukawa Cascade Candidate
=================================

STATUS: HISTORICAL BOUNDED PRECURSOR (SUPERSEDED)
SUPERSEDED BY: docs/DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md
               scripts/frontier_dm_neutrino_schur_suppression_theorem.py

This runner is preserved as a historical-reference numerical match. It is no
longer the live authority for the Dirac coefficient on the DM neutrino lane;
the local Schur identity `y_nu^eff = g_weak^2 / 64` (giving
`k_eff ~ 8.01`) is the downstream successor surface in the Schur
suppression theorem runner. That theorem is currently conditional on its
declared upstream inputs. Cite this artifact only as a bounded numerical
candidate that anticipated the correct scale, never as a closed positive
theorem for the `k_B = 8` Dirac Yukawa.

Purpose:
  Quantify the strongest currently defensible mechanism behind the
  `k_B = 8` leptogenesis candidate:

    1. the exact staircase/seesaw target for `y_nu`
    2. the bounded EWSB cascade suppression already used elsewhere on branch
    3. the resulting effective staircase level `k_B`

  The point is not to claim closure. The point is to preserve the historical
  pre-theorem intuition that replaced the bare "alpha_LM^2 looks nice"
  statement with a controlled candidate:

    second-order EWSB cascade + O(0.5-0.65) sector base Yukawa
      => y_nu ~ few x 10^-3
      => k_B ~ 8

  This explains why `k_B = 8` is structurally attractive.

  Historical note:
    the local Schur coefficient is now the downstream successor surface in
    `frontier_dm_neutrino_schur_suppression_theorem.py`. So this script is no
    longer the live authority for the Dirac coefficient; it is the bounded
    precursor that anticipated the correct scale.

Self-contained: stdlib only.
"""

from __future__ import annotations

import math
import sys

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


PI = math.pi

# Framework constants inherited from the DM / hierarchy runners.
G_BARE = 1.0
ALPHA_BARE = G_BARE**2 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0
M_PL = 1.2209e19  # GeV
C_APBC = (7.0 / 8.0) ** 0.25
V_EW = M_PL * C_APBC * ALPHA_LM**16

# Neutrino / leptogenesis benchmark surface already used on branch.
EPS_OVER_B = 0.041
DM2_31 = 2.453e-3  # eV^2
M3_NU = math.sqrt(DM2_31)  # eV
M3_GEV = M3_NU * 1.0e-9

# Existing bounded Yukawa / gauge surfaces.
ALPHA_S_PLANCK = 0.092
G_S_PLANCK = math.sqrt(4.0 * PI * ALPHA_S_PLANCK)
Y_TOP_PLANCK = G_S_PLANCK / math.sqrt(6.0)
G_WEAK = 0.653
Y_WEAK_FULLSPACE = G_WEAK / math.sqrt(2.0)
Y_WEAK_ACTIVE = G_WEAK

# EWSB cascade factor from existing branch scripts.
EPS_WEAK = G_WEAK**2 / (16.0 * PI**2)
LOG_HIERARCHY = math.log(M_PL / V_EW)
CASCADE_STEP = EPS_WEAK * LOG_HIERARCHY
CASCADE_TWO_STEP = CASCADE_STEP**2


def target_yukawa(k_b: float) -> float:
    """Seesaw-required Dirac Yukawa for staircase level k_B."""
    m_r = M_PL * ALPHA_LM**k_b * (1.0 - EPS_OVER_B)
    return math.sqrt(M3_GEV * m_r / V_EW**2)


def k_from_yukawa(y_nu: float) -> float:
    """Effective staircase level implied by a Dirac Yukawa."""
    m_r = y_nu**2 * V_EW**2 / M3_GEV
    return math.log(m_r / M_PL) / math.log(ALPHA_LM)


def ratio(a: float, b: float) -> float:
    if b == 0.0:
        return float("inf")
    return a / b


def print_candidate(label: str, y_nu: float, y_target: float) -> tuple[float, float]:
    k_eff = k_from_yukawa(y_nu)
    rel = ratio(y_nu, y_target)
    print(
        f"  {label:<24s} y_nu = {y_nu:.6e}, "
        f"k_eff = {k_eff:.3f}, y/y_k8 = {rel:.3f}"
    )
    return k_eff, rel


def main() -> int:
    print("=" * 78)
    print("NEUTRINO YUKAWA CASCADE CANDIDATE")
    print("=" * 78)
    print()
    print("Framework inputs:")
    print(f"  alpha_LM               = {ALPHA_LM:.6f}")
    print(f"  v_EW                   = {V_EW:.3f} GeV")
    print(f"  epsilon_weak           = {EPS_WEAK:.6e}")
    print(f"  log(M_Pl / v)          = {LOG_HIERARCHY:.3f}")
    print(f"  1-step cascade factor  = {CASCADE_STEP:.6e}")
    print(f"  2-step cascade factor  = {CASCADE_TWO_STEP:.6e}")
    print()

    y_k7 = target_yukawa(7.0)
    y_k8 = target_yukawa(8.0)
    print("Seesaw targets from the staircase:")
    print(f"  y_nu(k_B=7)            = {y_k7:.6e}")
    print(f"  y_nu(k_B=8)            = {y_k8:.6e}")
    print(f"  alpha_LM^2             = {ALPHA_LM**2:.6e}")
    print()

    check(
        "k8 target near alpha_LM^2",
        0.5 < ratio(y_k8, ALPHA_LM**2) < 2.0,
        f"y_k8 / alpha_LM^2 = {ratio(y_k8, ALPHA_LM**2):.3f}",
    )

    print()
    print("One-step EWSB candidates:")
    k_one_top, _ = print_candidate("top-like base x step", Y_TOP_PLANCK * CASCADE_STEP, y_k8)
    k_one_weak_full, _ = print_candidate("weak full x step", Y_WEAK_FULLSPACE * CASCADE_STEP, y_k8)
    k_one_weak_active, _ = print_candidate("weak active x step", Y_WEAK_ACTIVE * CASCADE_STEP, y_k8)
    print_candidate("unit base x step", CASCADE_STEP, y_k8)

    print()
    print("Two-step EWSB candidates:")
    y_two_top = Y_TOP_PLANCK * CASCADE_TWO_STEP
    y_two_weak_full = Y_WEAK_FULLSPACE * CASCADE_TWO_STEP
    y_two_weak_active = Y_WEAK_ACTIVE * CASCADE_TWO_STEP
    y_two_unit = CASCADE_TWO_STEP
    k_two_top, r_two_top = print_candidate("top-like base x step^2", y_two_top, y_k8)
    k_two_weak_full, r_two_weak_full = print_candidate("weak full x step^2", y_two_weak_full, y_k8)
    k_two_weak_active, r_two_weak_active = print_candidate("weak active x step^2", y_two_weak_active, y_k8)
    print_candidate("unit base x step^2", y_two_unit, y_k8)

    print()
    check(
        "two-step closer than one-step (top-like)",
        abs(k_two_top - 8.0) < abs(k_one_top - 8.0),
        f"|k_2 - 8| = {abs(k_two_top - 8.0):.3f}, |k_1 - 8| = {abs(k_one_top - 8.0):.3f}",
    )
    check(
        "two-step closer than one-step (weak-like)",
        abs(k_two_weak_full - 8.0) < abs(k_one_weak_full - 8.0),
        f"|k_2 - 8| = {abs(k_two_weak_full - 8.0):.3f}, |k_1 - 8| = {abs(k_one_weak_full - 8.0):.3f}",
    )
    check(
        "two-step closer than one-step (weak-active)",
        abs(k_two_weak_active - 8.0) < abs(k_one_weak_active - 8.0),
        f"|k_2 - 8| = {abs(k_two_weak_active - 8.0):.3f}, |k_1 - 8| = {abs(k_one_weak_active - 8.0):.3f}",
    )
    check(
        "two-step top-like lands near k_B=8",
        abs(k_two_top - 8.0) < 0.5,
        f"k_eff = {k_two_top:.3f}",
    )
    check(
        "two-step weak-full lands near k_B=8",
        abs(k_two_weak_full - 8.0) < 0.5,
        f"k_eff = {k_two_weak_full:.3f}",
    )
    check(
        "two-step weak-active lands near k_B=8",
        abs(k_two_weak_active - 8.0) < 0.5,
        f"k_eff = {k_two_weak_active:.3f}",
    )
    check(
        "two-step top-like gives y in k8 ballpark",
        0.5 < r_two_top < 2.0,
        f"y / y_k8 = {r_two_top:.3f}",
    )
    check(
        "two-step weak-full gives y in k8 ballpark",
        0.5 < r_two_weak_full < 2.0,
        f"y / y_k8 = {r_two_weak_full:.3f}",
    )
    check(
        "two-step weak-active gives y in k8 ballpark",
        0.5 < r_two_weak_active < 2.0,
        f"y / y_k8 = {r_two_weak_active:.3f}",
    )

    print()
    print("Honest read:")
    print("  1. The staircase target for k_B=8 is a few x 10^-3 Dirac Yukawa.")
    print("  2. A second-order EWSB cascade naturally produces that scale from")
    print("     an O(0.5-0.65) sector base Yukawa already present as a bounded")
    print("     benchmark surface on branch.")
    print("  3. The retained observable-principle normalization now selects")
    print("     g_weak/sqrt(2) as the physical base surface; that selected")
    print("     benchmark lands near k_B=8, and even the rejected active-space")
    print("     comparator stays in the same ballpark.")
    print("  4. A one-step cascade points too low in k_B; the attraction to k_B=8")
    print("     is specifically a two-step effect.")
    print("  5. This script is no longer the live blocker surface: the local")
    print("     Schur coefficient is now the downstream successor surface.")
    print("     The live unresolved object is the")
    print("     Majorana / Z3 activation law.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
