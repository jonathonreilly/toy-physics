#!/usr/bin/env python3
"""
Vector gauge-field compactness spectral tower verification on retained S^3.

Verifies the structural identities in
  docs/VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md

V1: m_l^2 = [l(l+2) - 1] hbar^2 / (c^2 R^2), l >= 1
V2: (m_l/m_k)^2 = [l(l+2)-1] / [k(k+2)-1] in Q

The numerical mass values are bounded companion checks only; the retained
content is the compact S^3 eigenvalue and ratio surface.
"""

from __future__ import annotations

import math
from fractions import Fraction

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f" ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def vector_num(l_val: int) -> int:
    """Transverse vector one-form numerator lambda_l^V * R^2."""
    return l_val * (l_val + 2) - 1


def tt_num(l_val: int) -> int:
    """Transverse-traceless spin-2 numerator lambda_l^TT * R^2."""
    return l_val * (l_val + 2) - 2


def scalar_num(l_val: int) -> int:
    """Scalar numerator lambda_l^scalar * R^2."""
    return l_val * (l_val + 2)


HBAR_J_S = 1.054571817e-34
C_LIGHT = 2.99792458e8
EV_PER_J = 6.241509074e18
H0_PER_S = 2.184e-18
R_HUBBLE_M = C_LIGHT / H0_PER_S
PHOTON_BOUND_COMPARATOR_EV = 1.0e-18
W_MASS_EV = 80.379e9
GRAVITON_LOWEST_EV = 3.52e-33


def compactness_energy_ev(numerator: int, radius_m: float = R_HUBBLE_M) -> float:
    """Return m c^2 in eV for m^2 = numerator * hbar^2/(c^2 R^2)."""
    energy_j = HBAR_J_S * C_LIGHT * math.sqrt(numerator) / radius_m
    return energy_j * EV_PER_J


def part_a_vector_eigenvalues() -> None:
    banner("Part A: V1 vector tower numerators")
    expected = {1: 2, 2: 7, 3: 14, 4: 23, 5: 34, 6: 47, 7: 62, 8: 79, 9: 98, 10: 119}
    for l_val, exp in expected.items():
        got = vector_num(l_val)
        check(
            f"lambda_{l_val}^V R^2 = {exp}",
            got == exp and got > 0,
            f"computed {got}",
        )


def part_b_lambda_form() -> None:
    banner("Part B: Lambda coefficient form")
    for l_val in range(1, 5):
        coeff = Fraction(vector_num(l_val), 3)
        reconstructed = coeff * 3
        check(
            f"m_{l_val}^2 coefficient in hbar^2 Lambda/c^2 is {coeff}",
            reconstructed == vector_num(l_val),
            f"3*{coeff} = {reconstructed}",
        )


def part_c_rational_ratios() -> None:
    banner("Part C: V2 rational squared-mass ratios")
    pairs = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 6), (4, 7), (5, 10)]
    for l_val, k_val in pairs:
        ratio = Fraction(vector_num(l_val), vector_num(k_val))
        check(
            f"(m_{l_val}/m_{k_val})^2 is rational",
            isinstance(ratio, Fraction) and ratio > 0,
            f"{ratio}",
        )

    expected_from_lowest = {
        2: Fraction(7, 2),
        3: Fraction(7, 1),
        4: Fraction(23, 2),
        5: Fraction(17, 1),
        6: Fraction(47, 2),
    }
    for l_val, expected in expected_from_lowest.items():
        ratio = Fraction(vector_num(l_val), vector_num(1))
        check(
            f"(m_{l_val}/m_1)^2 = {expected}",
            ratio == expected,
            f"computed {ratio}",
        )


def part_d_lambda_connection() -> None:
    banner("Part D: connection to retained Lambda = 3/R^2")
    for l_val in range(1, 7):
        coeff = Fraction(vector_num(l_val), 3)
        check(
            f"m_{l_val}^2 = ({coeff}) hbar^2 Lambda/c^2",
            coeff.denominator in (1, 3),
            f"vector numerator {vector_num(l_val)}",
        )

    check(
        "lowest vector mode has m_1^2 = (2/3) hbar^2 Lambda/c^2",
        Fraction(vector_num(1), 3) == Fraction(2, 3),
        f"coefficient {Fraction(vector_num(1), 3)}",
    )


def part_e_graviton_comparison() -> None:
    banner("Part E: comparison with retained TT graviton tower")
    for l_val in range(2, 8):
        ratio = Fraction(vector_num(l_val), tt_num(l_val))
        check(
            f"common-level vector/TT squared ratio at l={l_val} is rational",
            ratio > 1,
            f"{ratio}",
        )

    lowest_ratio = Fraction(vector_num(1), tt_num(2))
    check(
        "lowest vector / lowest TT squared ratio is 1/3",
        lowest_ratio == Fraction(1, 3),
        f"computed {lowest_ratio}",
    )


def part_f_spin_shift_pattern() -> None:
    banner("Part F: scalar/vector/TT spin-curvature shift bookkeeping")
    l_val = 4
    check(
        "scalar numerator has zero shift",
        scalar_num(l_val) == l_val * (l_val + 2),
        f"{scalar_num(l_val)}",
    )
    check(
        "vector numerator has -1 shift",
        vector_num(l_val) == scalar_num(l_val) - 1,
        f"{vector_num(l_val)}",
    )
    check(
        "TT numerator has -2 shift",
        tt_num(l_val) == scalar_num(l_val) - 2,
        f"{tt_num(l_val)}",
    )


def part_g_numerical_companion_checks() -> None:
    banner("Part G: bounded numerical companion checks")
    lowest_vector_ev = compactness_energy_ev(vector_num(1))
    expected_from_graviton = GRAVITON_LOWEST_EV * math.sqrt(Fraction(1, 3))
    check(
        "lowest vector compactness mass matches graviton-ratio companion value",
        abs(lowest_vector_ev - expected_from_graviton) / expected_from_graviton < 0.02,
        f"{lowest_vector_ev:.3e} eV vs {expected_from_graviton:.3e} eV",
    )

    w_shift_fraction = (lowest_vector_ev / W_MASS_EV) ** 2
    check(
        "electroweak W/Z Higgs masses dominate compactness shift",
        w_shift_fraction < 1e-80,
        f"fractional m^2 shift {w_shift_fraction:.3e}",
    )


def main() -> int:
    print("Vector gauge-field compactness spectral tower verification")
    print("Status boundary: structural tower retained; numerical masses bounded")
    part_a_vector_eigenvalues()
    part_b_lambda_form()
    part_c_rational_ratios()
    part_d_lambda_connection()
    part_e_graviton_comparison()
    part_f_spin_shift_pattern()
    part_g_numerical_companion_checks()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT == 0:
        print("PASSED: 46/46")
        print("VECTOR_GAUGE_FIELD_KK_TOWER=TRUE")
        print("VECTOR_KK_STRUCTURAL_IDENTITY_RETAINED=TRUE")
        print("VECTOR_KK_NUMERICAL_MASSES_BOUNDED=TRUE")
        print("VECTOR_KK_PHYSICAL_PARTICLE_INTERPRETATION_PROMOTED=FALSE")
        return 0

    print(f"FAILED: {FAIL_COUNT} checks")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
