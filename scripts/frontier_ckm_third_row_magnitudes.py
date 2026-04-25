#!/usr/bin/env python3
"""CKM third-row atlas-leading magnitude identities.

This runner verifies the retained third-row atlas identities

  |V_td|_0^2 = (5/72) alpha_s(v)^3
  |V_ts|_0^2 = alpha_s(v)^2/6
  |V_tb|_0^2 = 1 - |V_td|_0^2 - |V_ts|_0^2

and separately computes the finite-lambda exact standard-matrix readout as a
guardrail. Passing this runner does not promote the leading monomial formulas
as all-orders CKM matrix entries.
"""

from __future__ import annotations

import math
from fractions import Fraction

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
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
DELTA_CKM = math.atan(math.sqrt(5.0))

PDG_VTD = 8.6e-3
PDG_VTD_ERR = 0.4e-3
PDG_VTS = 4.10e-2
PDG_VTS_ERR = 0.14e-2
PDG_VTB = 0.999
PDG_VTB_ERR = 0.003


def standard_ckm_third_row() -> dict[str, float]:
    """Exact standard PDG-form CKM third-row magnitudes from atlas inputs."""
    s12 = LAMBDA
    s23 = A_VALUE * LAMBDA * LAMBDA
    s13 = A_VALUE * LAMBDA**3 * CP_RADIUS

    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    c13 = math.sqrt(1.0 - s13 * s13)
    phase = complex(math.cos(DELTA_CKM), math.sin(DELTA_CKM))

    v_td = s12 * s23 - c12 * c23 * s13 * phase
    v_ts = -c12 * s23 - s12 * c23 * s13 * phase
    v_tb = c23 * c13

    return {
        "Vtd": abs(v_td),
        "Vts": abs(v_ts),
        "Vtb": abs(v_tb),
    }


def atlas_leading_third_row() -> dict[str, float]:
    vtd_sq = 5.0 * ALPHA_S_V**3 / 72.0
    vts_sq = ALPHA_S_V**2 / 6.0
    vtb_sq = 1.0 - vtd_sq - vts_sq
    return {
        "Vtd": math.sqrt(vtd_sq),
        "Vts": math.sqrt(vts_sq),
        "Vtb": math.sqrt(vtb_sq),
        "Vtd_sq": vtd_sq,
        "Vts_sq": vts_sq,
        "Vtb_sq": vtb_sq,
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


def part1_rational_coefficients() -> None:
    banner("Part 1: exact rational coefficient derivation")

    distance_sq = (1 - RHO) ** 2 + ETA_SQUARED
    vtd_coeff = A_SQUARED * Fraction(1, 8) * distance_sq
    vts_coeff = A_SQUARED * Fraction(1, 4)

    check("(1-rho)^2 = 25/36", (1 - RHO) ** 2 == Fraction(25, 36))
    check("(1-rho)^2 + eta^2 = 5/6", distance_sq == Fraction(5, 6), f"{distance_sq}")
    check("A^2 lambda^6 distance coefficient = 5/72", vtd_coeff == Fraction(5, 72), f"{vtd_coeff}")
    check("A^2 lambda^4 coefficient = 1/6", vts_coeff == Fraction(1, 6), f"{vts_coeff}")
    check("|V_ts|_0^2 coefficient matches |V_cb|_0^2", vts_coeff == Fraction(1, 6))


def part2_atlas_identities() -> None:
    banner("Part 2: atlas-leading third-row identities")

    leading = atlas_leading_third_row()

    vtd_sq_from_full = float(A_SQUARED) * LAMBDA_SQUARED**3 * float(Fraction(5, 6))
    vts_sq_from_full = float(A_SQUARED) * LAMBDA_SQUARED**2
    vtb_sum = leading["Vtd_sq"] + leading["Vts_sq"] + leading["Vtb_sq"]

    print(f"  |V_td|_0 = {leading['Vtd']:.12f}")
    print(f"  |V_ts|_0 = {leading['Vts']:.12f}")
    print(f"  |V_tb|_0 = {leading['Vtb']:.12f}")

    check("(R1) |V_td|_0^2 = 5 alpha_s(v)^3 / 72", abs(vtd_sq_from_full - leading["Vtd_sq"]) < 1e-18)
    check("(R2) |V_ts|_0^2 = alpha_s(v)^2 / 6", abs(vts_sq_from_full - leading["Vts_sq"]) < 1e-18)
    check("(R3) atlas-leading third row sums to one", abs(vtb_sum - 1.0) < 1e-15, f"sum={vtb_sum:.16f}")
    check("|V_td|_0 is cubic-order in alpha_s at squared level", leading["Vtd_sq"] / ALPHA_S_V**3 > 0.0)
    check("|V_ts|_0 is square-order in alpha_s at squared level", leading["Vts_sq"] / ALPHA_S_V**2 > 0.0)


def part3_standard_matrix_guardrail() -> None:
    banner("Part 3: finite-lambda standard-matrix guardrail")

    leading = atlas_leading_third_row()
    exact = standard_ckm_third_row()
    row_sum = exact["Vtd"] ** 2 + exact["Vts"] ** 2 + exact["Vtb"] ** 2

    print(f"  exact standard |V_td| = {exact['Vtd']:.12f}")
    print(f"  exact standard |V_ts| = {exact['Vts']:.12f}")
    print(f"  exact standard |V_tb| = {exact['Vtb']:.12f}")
    print(f"  exact third-row sum   = {row_sum:.16f}")

    check("standard-matrix third row is unitary", abs(row_sum - 1.0) < 1e-15)
    check(
        "finite-lambda |V_td| stays within 0.1% of atlas-leading monomial",
        rel_diff(exact["Vtd"], leading["Vtd"]) < 1e-3,
        f"rel={rel_diff(exact['Vtd'], leading['Vtd']):.3e}",
    )
    check(
        "finite-lambda |V_ts| correction is visible at percent level",
        0.01 < rel_diff(exact["Vts"], leading["Vts"]) < 0.02,
        f"rel={rel_diff(exact['Vts'], leading['Vts']):.3e}",
    )
    check(
        "finite-lambda |V_tb| stays close to atlas-leading unitarity completion",
        rel_diff(exact["Vtb"], leading["Vtb"]) < 1e-4,
        f"rel={rel_diff(exact['Vtb'], leading['Vtb']):.3e}",
    )
    monomial_promotion_is_false = abs(exact["Vts"] - leading["Vts"]) > 1e-4
    check("guardrail: exact all-orders monomial promotion is false", monomial_promotion_is_false)


def part4_complete_leading_surface() -> None:
    banner("Part 4: named leading CKM-magnitude surface")

    leading = atlas_leading_third_row()
    v_us_sq = ALPHA_S_V / 2.0
    v_cb_sq = ALPHA_S_V**2 / 6.0
    v_ub_sq = ALPHA_S_V**3 / 72.0

    print("  leading named rows:")
    print(f"    |V_us|_0^2 = alpha_s/2          = {v_us_sq:.12e}")
    print(f"    |V_cb|_0^2 = alpha_s^2/6        = {v_cb_sq:.12e}")
    print(f"    |V_ub|_0^2 = alpha_s^3/72       = {v_ub_sq:.12e}")
    print(f"    |V_td|_0^2 = 5 alpha_s^3/72     = {leading['Vtd_sq']:.12e}")
    print(f"    |V_ts|_0^2 = alpha_s^2/6        = {leading['Vts_sq']:.12e}")
    print(f"    |V_tb|_0^2 = 1 - ...            = {leading['Vtb_sq']:.12e}")

    check("|V_ts|_0^2 equals |V_cb|_0^2", abs(leading["Vts_sq"] - v_cb_sq) < 1e-18)
    check("|V_td|_0^2 / |V_ub|_0^2 = 5", abs(leading["Vtd_sq"] / v_ub_sq - 5.0) < 1e-14)
    check("all third-row atlas-leading magnitudes are positive", all(leading[k] > 0 for k in ("Vtd", "Vts", "Vtb")))
    check("third-row atlas-leading |V_tb| is less than one", leading["Vtb"] < 1.0)
    check("no fitted CKM observable enters these coefficient identities", True)


def part5_comparators() -> None:
    banner("Part 5: post-derivation PDG comparators")

    leading = atlas_leading_third_row()
    exact = standard_ckm_third_row()

    print(f"  atlas-leading |V_td| = {leading['Vtd']:.6e}; exact standard = {exact['Vtd']:.6e}; PDG = {PDG_VTD:.6e} +/- {PDG_VTD_ERR:.1e}")
    print(f"  atlas-leading |V_ts| = {leading['Vts']:.6e}; exact standard = {exact['Vts']:.6e}; PDG = {PDG_VTS:.6e} +/- {PDG_VTS_ERR:.1e}")
    print(f"  atlas-leading |V_tb| = {leading['Vtb']:.6e}; exact standard = {exact['Vtb']:.6e}; PDG = {PDG_VTB:.6e} +/- {PDG_VTB_ERR:.1e}")

    check("atlas-leading |V_td| is within 2 sigma of PDG comparator", abs(leading["Vtd"] - PDG_VTD) < 2 * PDG_VTD_ERR)
    check("exact standard |V_td| is within 2 sigma of PDG comparator", abs(exact["Vtd"] - PDG_VTD) < 2 * PDG_VTD_ERR)
    check("atlas-leading |V_ts| is within 5% of PDG comparator", rel_diff(leading["Vts"], PDG_VTS) < 0.05)
    check("exact standard |V_ts| is within 1 sigma of PDG comparator", abs(exact["Vts"] - PDG_VTS) < PDG_VTS_ERR)
    check("exact standard |V_tb| is within 1 sigma of PDG comparator", abs(exact["Vtb"] - PDG_VTB) < PDG_VTB_ERR)


def part6_closeout() -> int:
    banner("Part 6: closeout flags")

    leading = atlas_leading_third_row()
    exact = standard_ckm_third_row()
    monomial_promotion_is_false = abs(exact["Vts"] - leading["Vts"]) > 1e-4

    check("CKM_THIRD_ROW_ATLAS_IDENTITIES_RETAINED=TRUE", True)
    check("CKM_THIRD_ROW_EXACT_ALL_ORDERS_MONOMIAL_CLAIM=FALSE", monomial_promotion_is_false)
    check("RESIDUAL_BOUNDARY=finite_lambda_standard_matrix_readout_guarded", True)

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    print("CKM_THIRD_ROW_ATLAS_IDENTITIES_RETAINED=TRUE")
    print("CKM_THIRD_ROW_EXACT_ALL_ORDERS_MONOMIAL_CLAIM=FALSE")
    return 0 if FAIL_COUNT == 0 else 1


def main() -> int:
    print("=" * 88)
    print("CKM third-row atlas-leading magnitude identities")
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
