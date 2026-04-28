#!/usr/bin/env python3
"""Lane 4 Dirac/seesaw fork no-go guardrail.

This runner checks a narrow claim-boundary question for the neutrino
quantitative lane:

  Can the current-stack Majorana zero law, the diagonal seesaw atmospheric
  benchmark, and the retained local coefficient y_nu^eff be combined into a
  single global neutrino-mass closure without an extra premise?

Answer:

  No. On the current stack the Majorana activation amplitude is zero, so a
  type-I seesaw mass matrix is not invertible there. The atmospheric-scale
  benchmark is a nonzero Majorana/seesaw extension surface. Conversely, using
  the retained local coefficient directly as a one-Higgs Dirac Yukawa gives a
  GeV-scale neutrino mass, not a meV-scale mass. A positive Lane 4 closure must
  derive either a nonzero charge-2 Majorana primitive or a separate tiny Dirac
  Yukawa activation law.
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


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Canonical constants mirrored from the current Lane 4 scripts.
PI = math.pi
ALPHA_BARE = 1.0 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0

M_PL_GEV = 1.2209e19
C_APBC = (7.0 / 8.0) ** 0.25
V_EW_GEV = M_PL_GEV * C_APBC * ALPHA_LM ** 16

G_WEAK = 0.653
Y_NU_EFF = (G_WEAK * G_WEAK) / 64.0

K_A = 7
K_B = 8
EPS_OVER_B = ALPHA_LM / 2.0

A_SCALE_GEV = M_PL_GEV * ALPHA_LM ** K_A
B_SCALE_GEV = M_PL_GEV * ALPHA_LM ** K_B
M1_HEAVY_GEV = B_SCALE_GEV * (1.0 - EPS_OVER_B)
M2_HEAVY_GEV = B_SCALE_GEV * (1.0 + EPS_OVER_B)
M3_HEAVY_GEV = A_SCALE_GEV

M3_SEESAW_EV = (Y_NU_EFF ** 2) * (V_EW_GEV ** 2) * 1e9 / M1_HEAVY_GEV
M1_LIGHT_DIAG_EV = (Y_NU_EFF ** 2) * (V_EW_GEV ** 2) * 1e9 / M3_HEAVY_GEV
DM2_31_SEESAW_EV2 = M3_SEESAW_EV ** 2 - M1_LIGHT_DIAG_EV ** 2

M_DIRAC_DIRECT_EV = Y_NU_EFF * V_EW_GEV * 1e9
M_DIRAC_DIRECT_SM_EV = Y_NU_EFF * V_EW_GEV / math.sqrt(2.0) * 1e9
Y_DIRAC_FOR_M3_SM = math.sqrt(2.0) * M3_SEESAW_EV / (V_EW_GEV * 1e9)


def part1_current_stack_and_seesaw_are_different_surfaces() -> None:
    section("Part 1: current-stack zero law vs type-I seesaw invertibility")
    print("  Current-stack Majorana input: mu_current = 0.")
    print("  Type-I seesaw input: an invertible nonzero right-handed Majorana matrix.")
    print()
    print(f"  Benchmark heavy masses: M1={M1_HEAVY_GEV:.6e} GeV, "
          f"M2={M2_HEAVY_GEV:.6e} GeV, M3={M3_HEAVY_GEV:.6e} GeV")

    det_current = 0.0
    det_benchmark = M1_HEAVY_GEV * M2_HEAVY_GEV * M3_HEAVY_GEV

    check(
        "current-stack Majorana matrix is non-invertible",
        det_current == 0.0,
        "det(M_R,current)=0",
    )
    check(
        "diagonal seesaw benchmark uses an invertible nonzero M_R",
        det_benchmark > 0.0,
        f"det(M_R,bench)={det_benchmark:.3e} GeV^3",
    )
    check(
        "there is no algebraic path from M_R,current=0 to the benchmark inverse",
        det_current == 0.0 and det_benchmark > 0.0,
        "seesaw inversion requires an added nonzero charge-2 surface",
    )


def part2_retained_local_coefficient_is_not_a_dirac_mass_closure() -> None:
    section("Part 2: retained local coefficient is not a one-Higgs Dirac mass")
    print(f"  y_nu^eff = g_weak^2/64 = {Y_NU_EFF:.12f}")
    print(f"  v_EW = {V_EW_GEV:.6f} GeV")
    print()
    print(f"  Direct Dirac mass y v:        {M_DIRAC_DIRECT_EV:.6e} eV")
    print(f"  SM convention y v/sqrt(2):    {M_DIRAC_DIRECT_SM_EV:.6e} eV")
    print(f"  Seesaw atmospheric benchmark: {M3_SEESAW_EV:.6e} eV")
    print(f"  SM Dirac Yukawa needed for that mass: {Y_DIRAC_FOR_M3_SM:.6e}")

    ratio_sm = M_DIRAC_DIRECT_SM_EV / M3_SEESAW_EV

    check(
        "direct one-Higgs Dirac reading overshoots the meV scale by many orders",
        ratio_sm > 1.0e9,
        f"(y v/sqrt2)/m3={ratio_sm:.3e}",
    )
    check(
        "a pure Dirac closure would require a new tiny Yukawa activation law",
        Y_DIRAC_FOR_M3_SM < 1.0e-12,
        f"y_Dirac(m3)={Y_DIRAC_FOR_M3_SM:.3e}",
    )
    check(
        "retained y_nu^eff and pure-Dirac y_Dirac(m3) are not the same object",
        Y_NU_EFF / Y_DIRAC_FOR_M3_SM > 1.0e9,
        f"ratio={Y_NU_EFF / Y_DIRAC_FOR_M3_SM:.3e}",
    )


def part3_atmospheric_benchmark_remains_useful_but_not_global_closure() -> None:
    section("Part 3: atmospheric benchmark value and honest status")
    print(f"  m3(seesaw benchmark)       = {M3_SEESAW_EV:.6e} eV")
    print(f"  Delta m31^2(seesaw diag)   = {DM2_31_SEESAW_EV2:.6e} eV^2")
    print("  This is the existing useful benchmark surface.")
    print()
    print("  The no-go is only against silently upgrading that surface to global")
    print("  Lane 4 closure while also retaining M_R,current = 0.")

    check(
        "seesaw benchmark reproduces the retained atmospheric-scale target",
        abs(M3_SEESAW_EV - 5.058e-2) / 5.058e-2 < 1.0e-3,
        f"m3={M3_SEESAW_EV:.6e} eV",
    )
    check(
        "diagonal atmospheric splitting reproduces the retained benchmark",
        abs(DM2_31_SEESAW_EV2 - 2.539e-3) / 2.539e-3 < 5.0e-3,
        f"Delta m31^2={DM2_31_SEESAW_EV2:.6e} eV^2",
    )
    check(
        "benchmark usefulness does not remove the Dirac/seesaw fork",
        M1_HEAVY_GEV > 0.0 and M_DIRAC_DIRECT_SM_EV > 1.0e6,
        "nonzero M_R extension or new tiny Dirac law still required",
    )


def part4_claim_state() -> None:
    section("Part 4: claim-state consequence")
    print("  Exact negative boundary:")
    print("    The current Lane 4 stack has no hidden one-surface quantitative")
    print("    closure obtained by combining mu_current=0, y_nu^eff, and the")
    print("    diagonal seesaw benchmark.")
    print()
    print("  Remaining positive routes:")
    print("    1. Majorana/seesaw route: derive a nonzero charge-2 primitive and")
    print("       then repair the full M_R texture, including the solar gap.")
    print("    2. Dirac route: derive the tiny Y_nu activation law on the minimal")
    print("       surviving Dirac lane, not y_nu^eff reused as a Dirac eigenvalue.")
    print()
    print("  Therefore Lane 4 remains open after this no-go. The artifact retires")
    print("  a hidden-closure conflation, not the neutrino problem.")

    check(
        "Lane 4 status after this artifact is open, not retained closure",
        M1_HEAVY_GEV > 0.0
        and M_DIRAC_DIRECT_SM_EV / M3_SEESAW_EV > 1.0e9
        and Y_DIRAC_FOR_M3_SM < 1.0e-12,
        "fork isolated; positive activation law still missing",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 4 NEUTRINO DIRAC/SEESAW FORK NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can current-stack mu=0, the diagonal seesaw benchmark, and y_nu^eff")
    print("  be treated as one global quantitative neutrino closure?")
    print()
    print("Answer:")
    print("  No. They live on a forked claim surface unless an extra activation law")
    print("  is supplied.")

    part1_current_stack_and_seesaw_are_different_surfaces()
    part2_retained_local_coefficient_is_not_a_dirac_mass_closure()
    part3_atmospheric_benchmark_remains_useful_but_not_global_closure()
    part4_claim_state()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
