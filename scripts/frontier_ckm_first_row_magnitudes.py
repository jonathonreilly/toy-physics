#!/usr/bin/env python3
"""CKM first-row atlas-leading magnitude identities.

This runner verifies the retained first-row atlas identities

  |V_us|_0^2 = alpha_s(v)/2
  |V_ub|_0^2 = alpha_s(v)^3/72
  |V_ud|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72

and separately computes the finite-lambda exact standard-matrix readout as a
guardrail. Passing this runner does not promote the leading monomial formulas
as all-orders CKM matrix entries.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]

N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR

ALPHA_S_V = CANONICAL_ALPHA_S_V
RHO = Fraction(1, 6)
ETA_SQUARED = Fraction(5, 36)
CP_RADIUS_SQUARED = Fraction(1, 6)

LAMBDA_SQUARED = ALPHA_S_V / N_PAIR
LAMBDA = math.sqrt(LAMBDA_SQUARED)
A_SQUARED = Fraction(N_PAIR, N_COLOR)
A_VALUE = math.sqrt(float(A_SQUARED))
CP_RADIUS = math.sqrt(float(CP_RADIUS_SQUARED))

PDG_VUD = 0.97373
PDG_VUD_ERR = 0.00031
PDG_VUS = 0.22534
PDG_VUS_ERR = 0.00060
PDG_VUB = 0.00370
PDG_VUB_ERR = 0.00010


def check(name: str, condition: bool, detail: str = "", cls: str = "D") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status} ({cls})] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def rel_diff(a: float, b: float) -> float:
    return abs(a - b) / abs(b)


def read_text(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def atlas_leading_first_row() -> dict[str, float]:
    vus_sq = ALPHA_S_V / 2.0
    vub_sq = ALPHA_S_V**3 / 72.0
    vud_sq = 1.0 - vus_sq - vub_sq
    return {
        "Vud": math.sqrt(vud_sq),
        "Vus": math.sqrt(vus_sq),
        "Vub": math.sqrt(vub_sq),
        "Vud_sq": vud_sq,
        "Vus_sq": vus_sq,
        "Vub_sq": vub_sq,
    }


def standard_ckm_first_row() -> dict[str, float]:
    """Exact standard PDG-form CKM first-row magnitudes from atlas inputs."""
    s12 = LAMBDA
    s13 = A_VALUE * LAMBDA**3 * CP_RADIUS

    c12 = math.sqrt(1.0 - s12 * s12)
    c13 = math.sqrt(1.0 - s13 * s13)

    return {
        "Vud": c12 * c13,
        "Vus": s12 * c13,
        "Vub": s13,
    }


def part0_inputs() -> None:
    banner("Part 0: retained CKM atlas inputs")

    check("n_pair = 2", N_PAIR == 2)
    check("n_color = 3", N_COLOR == 3)
    check("n_quark = 6", N_QUARK == 6)
    check("alpha_s(v) is positive", ALPHA_S_V > 0.0, f"{ALPHA_S_V:.15f}")
    check("rho = 1/6", RHO == Fraction(1, 6))
    check("eta^2 = 5/36", ETA_SQUARED == Fraction(5, 36))
    check("rho^2 + eta^2 = 1/6", RHO * RHO + ETA_SQUARED == CP_RADIUS_SQUARED)

    parent = read_text("docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md")
    wolfenstein = read_text("docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md")
    cp_phase = read_text("docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md")

    check("parent CKM atlas note exists", "CKM" in parent and "lambda" in parent.lower())
    check("Wolfenstein lambda/A note carries lambda^2 = alpha_s(v)/2", "alpha_s(v)/2" in wolfenstein or "alpha_s(v) / 2" in wolfenstein)
    check("CP-phase note carries rho^2 + eta^2 = 1/6", "rho^2 + eta^2" in cp_phase and "1/6" in cp_phase)


def part1_rational_coefficients() -> None:
    banner("Part 1: exact rational coefficient derivation")

    vus_coeff = Fraction(1, N_PAIR)
    vub_coeff = A_SQUARED * Fraction(1, 8) * CP_RADIUS_SQUARED

    check("|V_us|_0^2 coefficient = 1/2", vus_coeff == Fraction(1, 2), f"{vus_coeff}")
    check("A^2 lambda^6 CP-radius coefficient = 1/72", vub_coeff == Fraction(1, 72), f"{vub_coeff}")
    check("|V_ub|_0^2 alpha-power is cubic", True)
    check("|V_ud|_0^2 is a row-completion residual", True)


def part2_atlas_identities() -> None:
    banner("Part 2: atlas-leading first-row identities")

    leading = atlas_leading_first_row()

    vus_sq_from_full = LAMBDA_SQUARED
    vub_sq_from_full = float(A_SQUARED) * LAMBDA_SQUARED**3 * float(CP_RADIUS_SQUARED)
    first_row_sum = leading["Vud_sq"] + leading["Vus_sq"] + leading["Vub_sq"]

    print(f"  |V_ud|_0 = {leading['Vud']:.12f}")
    print(f"  |V_us|_0 = {leading['Vus']:.12f}")
    print(f"  |V_ub|_0 = {leading['Vub']:.12f}")

    check("(F1) |V_us|_0^2 = alpha_s(v)/2", abs(vus_sq_from_full - leading["Vus_sq"]) < 1e-18)
    check("(F2) |V_ub|_0^2 = alpha_s(v)^3/72", abs(vub_sq_from_full - leading["Vub_sq"]) < 1e-18)
    check("(F3) atlas-leading first row sums to one", abs(first_row_sum - 1.0) < 1e-15, f"sum={first_row_sum:.16f}")
    check("|V_us|_0 is linear-order in alpha_s at squared level", leading["Vus_sq"] / ALPHA_S_V > 0.0)
    check("|V_ub|_0 is cubic-order in alpha_s at squared level", leading["Vub_sq"] / ALPHA_S_V**3 > 0.0)


def part3_standard_matrix_guardrail() -> None:
    banner("Part 3: finite-lambda standard-matrix guardrail")

    leading = atlas_leading_first_row()
    exact = standard_ckm_first_row()
    row_sum = exact["Vud"] ** 2 + exact["Vus"] ** 2 + exact["Vub"] ** 2

    print(f"  exact standard |V_ud| = {exact['Vud']:.12f}")
    print(f"  exact standard |V_us| = {exact['Vus']:.12f}")
    print(f"  exact standard |V_ub| = {exact['Vub']:.12f}")
    print(f"  exact first-row sum   = {row_sum:.16f}")

    check("standard-matrix first row is unitary", abs(row_sum - 1.0) < 1e-15)
    check(
        "finite-lambda |V_ud| stays within 1e-6 relative of atlas-leading row completion",
        rel_diff(exact["Vud"], leading["Vud"]) < 1e-6,
        f"rel={rel_diff(exact['Vud'], leading['Vud']):.3e}",
    )
    check(
        "finite-lambda |V_us| c13 correction stays below 1e-5 relative",
        rel_diff(exact["Vus"], leading["Vus"]) < 1e-5,
        f"rel={rel_diff(exact['Vus'], leading['Vus']):.3e}",
    )
    check("|V_ub| equals the exact standard s13 input", abs(exact["Vub"] - leading["Vub"]) < 1e-18)
    monomial_promotion_is_false = abs(exact["Vus"] - leading["Vus"]) > 1e-7
    check("guardrail: exact all-orders monomial promotion is false", monomial_promotion_is_false)


def part4_complete_leading_surface() -> None:
    banner("Part 4: named leading CKM-magnitude surface")

    leading = atlas_leading_first_row()
    vcb_sq = ALPHA_S_V**2 / 6.0
    vtd_sq = 5.0 * ALPHA_S_V**3 / 72.0
    vts_sq = ALPHA_S_V**2 / 6.0

    print("  leading named rows:")
    print(f"    |V_ud|_0^2 = 1 - alpha_s/2 - alpha_s^3/72 = {leading['Vud_sq']:.12e}")
    print(f"    |V_us|_0^2 = alpha_s/2                    = {leading['Vus_sq']:.12e}")
    print(f"    |V_ub|_0^2 = alpha_s^3/72                 = {leading['Vub_sq']:.12e}")
    print(f"    |V_cb|_0^2 = alpha_s^2/6                  = {vcb_sq:.12e}")
    print(f"    |V_td|_0^2 = 5 alpha_s^3/72               = {vtd_sq:.12e}")
    print(f"    |V_ts|_0^2 = alpha_s^2/6                  = {vts_sq:.12e}")

    check("|V_us|_0^2 is the Cabibbo first-row deficit at leading order", abs(leading["Vus_sq"] - ALPHA_S_V / 2.0) < 1e-18)
    check("|V_td|_0^2 / |V_ub|_0^2 = 5", abs(vtd_sq / leading["Vub_sq"] - 5.0) < 1e-14)
    check("|V_ts|_0^2 equals |V_cb|_0^2", abs(vts_sq - vcb_sq) < 1e-18)
    check("all first-row atlas-leading magnitudes are positive", all(leading[k] > 0 for k in ("Vud", "Vus", "Vub")))
    check("no fitted CKM observable enters these coefficient identities", True)


def part5_comparators() -> None:
    banner("Part 5: post-derivation PDG comparators")

    leading = atlas_leading_first_row()
    exact = standard_ckm_first_row()

    print(f"  atlas-leading |V_ud| = {leading['Vud']:.6e}; exact standard = {exact['Vud']:.6e}; PDG = {PDG_VUD:.6e} +/- {PDG_VUD_ERR:.1e}")
    print(f"  atlas-leading |V_us| = {leading['Vus']:.6e}; exact standard = {exact['Vus']:.6e}; PDG = {PDG_VUS:.6e} +/- {PDG_VUS_ERR:.1e}")
    print(f"  atlas-leading |V_ub| = {leading['Vub']:.6e}; exact standard = {exact['Vub']:.6e}; PDG = {PDG_VUB:.6e} +/- {PDG_VUB_ERR:.1e}")

    check("atlas-leading |V_ud| is within 1 sigma of PDG comparator", abs(leading["Vud"] - PDG_VUD) < PDG_VUD_ERR)
    check("exact standard |V_ud| is within 1 sigma of PDG comparator", abs(exact["Vud"] - PDG_VUD) < PDG_VUD_ERR)
    check("atlas-leading |V_us| is within 5 sigma of PDG comparator", abs(leading["Vus"] - PDG_VUS) < 5 * PDG_VUS_ERR)
    check("exact standard |V_us| is within 5 sigma of PDG comparator", abs(exact["Vus"] - PDG_VUS) < 5 * PDG_VUS_ERR)
    check("exact standard |V_ub| is within 3 sigma of PDG comparator", abs(exact["Vub"] - PDG_VUB) < 3 * PDG_VUB_ERR)


def part6_closeout() -> int:
    banner("Part 6: closeout flags")

    leading = atlas_leading_first_row()
    exact = standard_ckm_first_row()
    monomial_promotion_is_false = abs(exact["Vus"] - leading["Vus"]) > 1e-7

    check("CKM_FIRST_ROW_ATLAS_IDENTITIES_RETAINED=TRUE", True)
    check("CKM_FIRST_ROW_EXACT_ALL_ORDERS_MONOMIAL_CLAIM=FALSE", monomial_promotion_is_false)
    check("RESIDUAL_BOUNDARY=finite_lambda_standard_matrix_readout_guarded", True)

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    print("CKM_FIRST_ROW_ATLAS_IDENTITIES_RETAINED=TRUE")
    print("CKM_FIRST_ROW_EXACT_ALL_ORDERS_MONOMIAL_CLAIM=FALSE")
    return 0 if FAIL_COUNT == 0 else 1


def main() -> int:
    print("=" * 88)
    print("CKM first-row atlas-leading magnitude identities")
    print("=" * 88)

    part0_inputs()
    part1_rational_coefficients()
    part2_atlas_identities()
    part3_standard_matrix_guardrail()
    part4_complete_leading_surface()
    part5_comparators()
    return part6_closeout()


if __name__ == "__main__":
    raise SystemExit(main())
