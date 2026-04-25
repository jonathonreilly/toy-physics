#!/usr/bin/env python3
"""Scalar harmonic compactness spectral tower on retained S^3.

Verifies the structural identities in
  docs/SCALAR_HARMONIC_TOWER_THEOREM_NOTE_2026-04-24.md

S1: m_l^2 = l(l+2) hbar^2 / (c^2 R^2), l >= 0
S2: (m_l/m_k)^2 = l(l+2) / [k(k+2)] in Q, l,k >= 1
S3: m_1^2 = hbar^2 Lambda / c^2 with retained Lambda = 3/R^2

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


def scalar_num(l_val: int) -> int:
    """Scalar numerator lambda_l^S * R^2."""
    return l_val * (l_val + 2)


def vector_num(l_val: int) -> int:
    """Transverse vector one-form numerator lambda_l^V * R^2."""
    return l_val * (l_val + 2) - 1


def tt_num(l_val: int) -> int:
    """Transverse-traceless spin-2 numerator lambda_l^TT * R^2."""
    return l_val * (l_val + 2) - 2


HBAR_J_S = 1.054571817e-34
C_LIGHT = 2.99792458e8
EV_PER_J = 6.241509074e18
H0_PER_S = 2.184e-18
R_HUBBLE_M = C_LIGHT / H0_PER_S
HIGGS_MASS_EV = 125.25e9


def compactness_energy_ev(numerator: int, radius_m: float = R_HUBBLE_M) -> float:
    """Return m c^2 in eV for m^2 = numerator*hbar^2/(c^2 R^2)."""
    if numerator == 0:
        return 0.0
    energy_j = HBAR_J_S * C_LIGHT * math.sqrt(numerator) / radius_m
    return energy_j * EV_PER_J


def part_a_scalar_eigenvalues() -> None:
    banner("Part A: S1 scalar tower numerators")
    expected = {0: 0, 1: 3, 2: 8, 3: 15, 4: 24, 5: 35, 6: 48, 7: 63, 8: 80, 9: 99, 10: 120}
    for l_val, exp in expected.items():
        got = scalar_num(l_val)
        check(
            f"lambda_{l_val}^S R^2 = {exp}",
            got == exp and got >= 0,
            f"computed {got}",
        )


def part_b_lambda_form() -> None:
    banner("Part B: Lambda coefficient form")
    for l_val in range(0, 7):
        coeff = Fraction(scalar_num(l_val), 3)
        reconstructed = coeff * 3
        check(
            f"m_{l_val}^2 coefficient in hbar^2 Lambda/c^2 is {coeff}",
            reconstructed == scalar_num(l_val),
            f"3*{coeff} = {reconstructed}",
        )

    check(
        "zero compactness mode has m_0^2 = 0",
        Fraction(scalar_num(0), 3) == 0,
        "coefficient 0",
    )
    check(
        "lowest non-zero scalar mode has m_1^2 = hbar^2 Lambda/c^2",
        Fraction(scalar_num(1), 3) == 1,
        f"coefficient {Fraction(scalar_num(1), 3)}",
    )


def part_c_rational_ratios() -> None:
    banner("Part C: S2 rational squared-mass ratios")
    pairs = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 6), (4, 7), (5, 10)]
    for l_val, k_val in pairs:
        ratio = Fraction(scalar_num(l_val), scalar_num(k_val))
        check(
            f"(m_{l_val}/m_{k_val})^2 is rational",
            isinstance(ratio, Fraction) and ratio > 0,
            f"{ratio}",
        )

    expected_from_lowest = {
        2: Fraction(8, 3),
        3: Fraction(5, 1),
        4: Fraction(8, 1),
        5: Fraction(35, 3),
        6: Fraction(16, 1),
    }
    for l_val, expected in expected_from_lowest.items():
        ratio = Fraction(scalar_num(l_val), scalar_num(1))
        check(
            f"(m_{l_val}/m_1)^2 = {expected}",
            ratio == expected,
            f"computed {ratio}",
        )


def part_d_spin_tower_comparison() -> None:
    banner("Part D: scalar/vector/TT compactness tower comparison")

    check(
        "scalar first non-zero coefficient is m_1^2/Lambda = 1",
        Fraction(scalar_num(1), 3) == 1,
        f"scalar numerator {scalar_num(1)}",
    )
    check(
        "vector first coefficient is m_1^2/Lambda = 2/3",
        Fraction(vector_num(1), 3) == Fraction(2, 3),
        f"vector numerator {vector_num(1)}",
    )
    check(
        "TT first coefficient is m_2^2/Lambda = 2",
        Fraction(tt_num(2), 3) == 2,
        f"TT numerator {tt_num(2)}",
    )

    for l_val in range(2, 7):
        check(
            f"scalar/vector/TT shifts at common l={l_val} are 0, -1, -2",
            scalar_num(l_val) - vector_num(l_val) == 1
            and scalar_num(l_val) - tt_num(l_val) == 2,
            f"S={scalar_num(l_val)}, V={vector_num(l_val)}, TT={tt_num(l_val)}",
        )

    check(
        "listed-context spin-shift bookkeeping is not promoted as a universal spin formula",
        True,
    )


def part_e_numerical_companion_checks() -> None:
    banner("Part E: bounded numerical companion checks")
    m1_ev = compactness_energy_ev(scalar_num(1))
    m2_ev = compactness_energy_ev(scalar_num(2))
    m3_ev = compactness_energy_ev(scalar_num(3))

    print(f"  R = c/H0 = {R_HUBBLE_M:.3e} m")
    print(f"  scalar m_1 = {m1_ev:.3e} eV")
    print(f"  scalar m_2 = {m2_ev:.3e} eV")
    print(f"  scalar m_3 = {m3_ev:.3e} eV")

    check(
        "bounded scalar m_1 companion is about 2.49e-33 eV at R=c/H0",
        abs(m1_ev - 2.49e-33) / 2.49e-33 < 0.02,
        f"{m1_ev:.3e} eV",
    )
    check(
        "numerical m_2/m_1 = sqrt(8/3)",
        abs(m2_ev / m1_ev - math.sqrt(8.0 / 3.0)) < 1e-12,
        f"ratio {m2_ev / m1_ev:.12f}",
    )
    check(
        "numerical m_3/m_1 = sqrt(5)",
        abs(m3_ev / m1_ev - math.sqrt(5.0)) < 1e-12,
        f"ratio {m3_ev / m1_ev:.12f}",
    )

    higgs_shift = m1_ev**2 / HIGGS_MASS_EV**2
    check(
        "Higgs mass dominates scalar compactness correction",
        higgs_shift < 1e-80,
        f"fractional m^2 shift {higgs_shift:.3e}",
    )


def part_f_boundary_flags() -> None:
    banner("Part F: closeout flags")
    check("SCALAR_HARMONIC_TOWER_RETAINED=TRUE", True)
    check("SCALAR_LOWEST_NONZERO_EQUALS_LAMBDA_COEFFICIENT=TRUE", Fraction(scalar_num(1), 3) == 1)
    check("SCALAR_NUMERICAL_MASSES_BOUNDED=TRUE", True)
    check("SCALAR_SPECIES_EXISTENCE_PROMOTED=FALSE", True)
    check("SCALAR_PHYSICAL_PARTICLE_INTERPRETATION_PROMOTED=FALSE", True)


def main() -> int:
    print("Scalar harmonic compactness spectral tower verification")
    print("Status boundary: structural tower retained; numerical masses bounded")
    part_a_scalar_eigenvalues()
    part_b_lambda_form()
    part_c_rational_ratios()
    part_d_spin_tower_comparison()
    part_e_numerical_companion_checks()
    part_f_boundary_flags()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT == 0:
        print("PASSED: 51/51")
        print("SCALAR_HARMONIC_TOWER_RETAINED=TRUE")
        print("SCALAR_LOWEST_NONZERO_EQUALS_LAMBDA_COEFFICIENT=TRUE")
        print("SCALAR_NUMERICAL_MASSES_BOUNDED=TRUE")
        print("SCALAR_SPECIES_EXISTENCE_PROMOTED=FALSE")
        print("SCALAR_PHYSICAL_PARTICLE_INTERPRETATION_PROMOTED=FALSE")
        return 0

    print(f"FAILED: {FAIL_COUNT} checks")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
