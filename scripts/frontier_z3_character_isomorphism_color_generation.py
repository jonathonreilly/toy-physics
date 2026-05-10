#!/usr/bin/env python3
"""Z_3 character-isomorphism open-gate diagnostic.

This runner verifies only the finite algebra used by
docs/Z3_CHARACTER_ISOMORPHISM_COLOR_GENERATION_OPEN_GATE_NOTE_2026-05-10.md.

It proves two narrow facts:

1. Two abstract three-label spaces with the same imposed cyclic permutation
   action carry the regular Z_3 character (3, 0, 0), hence are isomorphic as
   representations of that imposed T_3.
2. The SU(3)_c center Z_3 is not that bridge. On the color fundamental, the
   center character is (3, 3 omega, 3 omega^2), not the regular character.

The runner does not assert that the physical color labels or generation labels
are derived from a common axis-cycle action. That bridge remains open.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cycle_matrix() -> sp.Matrix:
    """The order-three cyclic permutation on three labels."""
    return sp.Matrix(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ]
    )


def regular_character() -> dict[str, sp.Expr]:
    P = cycle_matrix()
    return {
        "e": sp.trace(sp.eye(3)),
        "c": sp.trace(P),
        "c^2": sp.trace(P * P),
    }


def center_character() -> dict[str, sp.Expr]:
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    return {
        "e": sp.Integer(3),
        "c": 3 * omega,
        "c^2": 3 * omega**2,
    }


def part1_cycle_generator() -> None:
    print()
    print("=" * 78)
    print("PART 1: ORDER-THREE PERMUTATION GENERATOR")
    print("=" * 78)

    P = cycle_matrix()
    I3 = sp.eye(3)
    print(f"  P = {P.tolist()}")

    check(
        "P has determinant 1",
        sp.simplify(P.det() - 1) == 0,
        f"det(P) = {P.det()}",
    )
    check(
        "P is orthogonal",
        sp.simplify(P * P.T - I3) == sp.zeros(3, 3),
        "P P^T = I_3",
    )
    check(
        "P^3 = I_3",
        sp.simplify(P**3 - I3) == sp.zeros(3, 3),
        "order divides three",
    )
    check(
        "P is not the identity",
        sp.simplify(P - I3) != sp.zeros(3, 3),
        "nontrivial cycle",
    )


def part2_cube_roots() -> None:
    print()
    print("=" * 78)
    print("PART 2: EIGENVALUES ARE CUBE ROOTS OF UNITY")
    print("=" * 78)

    P = cycle_matrix()
    x = sp.Symbol("x")
    char_poly = P.charpoly(x).as_expr()
    expected = x**3 - 1
    check(
        "Characteristic polynomial is x^3 - 1",
        sp.simplify(char_poly - expected) == 0,
        f"char_poly = {char_poly}",
    )

    eigenvalues = []
    for eigenvalue, multiplicity in P.eigenvals().items():
        eigenvalues.extend([eigenvalue] * multiplicity)

    for eigenvalue in eigenvalues:
        cubed = sp.simplify(eigenvalue**3)
        check(
            f"Eigenvalue {sp.sstr(eigenvalue)} satisfies lambda^3 = 1",
            sp.simplify(cubed - 1) == 0,
            f"lambda^3 = {sp.sstr(cubed)}",
        )

    numeric_sum = sum(complex(ev.evalf()) for ev in eigenvalues)
    check(
        "Numerical eigenvalue sum is zero",
        math.isclose(numeric_sum.real, 0.0, abs_tol=1e-10)
        and math.isclose(numeric_sum.imag, 0.0, abs_tol=1e-10),
        f"sum = {numeric_sum:.6f}",
    )


def part3_regular_character_equality() -> None:
    print()
    print("=" * 78)
    print("PART 3: COMMON IMPOSED PERMUTATION ACTION")
    print("=" * 78)

    color_label_char = regular_character()
    generation_label_char = regular_character()
    print(
        "  chi_label: "
        f"e={color_label_char['e']}, "
        f"c={color_label_char['c']}, "
        f"c^2={color_label_char['c^2']}"
    )

    check(
        "Permutation label character is (3, 0, 0)",
        color_label_char == {"e": 3, "c": 0, "c^2": 0},
        str(color_label_char),
    )
    chars_equal = all(
        sp.simplify(color_label_char[key] - generation_label_char[key]) == 0
        for key in ("e", "c", "c^2")
    )
    check(
        "Two spaces with the same imposed cycle have equal characters",
        chars_equal,
        "both use the same permutation matrix P",
    )


def part4_decomposition() -> None:
    print()
    print("=" * 78)
    print("PART 4: REGULAR Z_3 DECOMPOSITION")
    print("=" * 78)

    omega = sp.exp(2 * sp.pi * sp.I / 3)
    irreducibles = {
        "chi_0": {"e": 1, "c": 1, "c^2": 1},
        "chi_omega": {"e": 1, "c": omega, "c^2": omega**2},
        "chi_omega^2": {"e": 1, "c": omega**2, "c^2": omega**4},
    }
    char = regular_character()

    for name, irrep in irreducibles.items():
        norm = sp.Rational(1, 3) * sum(
            irrep[key] * sp.conjugate(irrep[key]) for key in ("e", "c", "c^2")
        )
        check(
            f"{name} has unit character norm",
            sp.simplify(norm - 1) == 0,
            f"norm = {sp.sstr(sp.simplify(norm))}",
        )

    multiplicities = {}
    for name, irrep in irreducibles.items():
        multiplicity = sp.Rational(1, 3) * sum(
            char[key] * sp.conjugate(irrep[key]) for key in ("e", "c", "c^2")
        )
        multiplicities[name] = sp.simplify(multiplicity)

    for name, multiplicity in multiplicities.items():
        check(
            f"Regular label representation contains {name} once",
            sp.simplify(multiplicity - 1) == 0,
            f"multiplicity = {sp.sstr(multiplicity)}",
        )

    check(
        "All three irreducibles occur with multiplicity one",
        all(sp.simplify(value - 1) == 0 for value in multiplicities.values()),
        str({key: sp.sstr(value) for key, value in multiplicities.items()}),
    )


def part5_center_boundary() -> None:
    print()
    print("=" * 78)
    print("PART 5: SU(3)_c CENTER Z_3 IS NOT THE REGULAR-LABEL BRIDGE")
    print("=" * 78)

    regular = regular_character()
    center = center_character()
    omega = sp.exp(2 * sp.pi * sp.I / 3)

    print(
        "  regular label character: "
        f"({regular['e']}, {regular['c']}, {regular['c^2']})"
    )
    print(
        "  center color character:  "
        f"({center['e']}, {sp.sstr(center['c'])}, {sp.sstr(center['c^2'])})"
    )

    check(
        "Center generator trace is nonzero",
        sp.simplify(center["c"]) != 0,
        f"trace(z) = {sp.sstr(center['c'])}",
    )
    check(
        "Permutation generator trace is zero",
        sp.simplify(regular["c"]) == 0,
        f"trace(c) = {regular['c']}",
    )
    check(
        "Center character differs from regular permutation character",
        any(sp.simplify(center[key] - regular[key]) != 0 for key in ("e", "c", "c^2")),
        "center=(3, 3 omega, 3 omega^2), regular=(3, 0, 0)",
    )
    check(
        "Center character is three copies of one nontrivial scalar character",
        sp.simplify(center["c"] - 3 * omega) == 0
        and sp.simplify(center["c^2"] - 3 * omega**2) == 0,
        "not chi_0 + chi_omega + chi_omega^2",
    )


def main() -> int:
    print("=" * 78)
    print("Z_3 CHARACTER-ISOMORPHISM OPEN-GATE DIAGNOSTIC")
    print("=" * 78)
    print()
    print("This verifies finite Z_3 representation algebra only.")
    print("It does not derive a physical color/generation bridge.")

    part1_cycle_generator()
    part2_cube_roots()
    part3_regular_character_equality()
    part4_decomposition()
    part5_center_boundary()

    print()
    print("=" * 78)
    print("SUMMARY CLASS-A ASSERTIONS")
    print("=" * 78)

    P = cycle_matrix()
    assert sp.simplify(P**3 - sp.eye(3)) == sp.zeros(3, 3), "P^3 != I"
    print("  [PASS] P^3 = I verified")

    char = regular_character()
    assert char == {"e": 3, "c": 0, "c^2": 0}, "regular character mismatch"
    print("  [PASS] regular permutation character is (3, 0, 0)")

    center = center_character()
    assert any(sp.simplify(center[key] - char[key]) != 0 for key in ("e", "c", "c^2"))
    print("  [PASS] SU(3)_c center character is not the regular character")

    print()
    print("=" * 78)
    print(f"Z_3 CHARACTER OPEN-GATE DIAGNOSTIC: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
