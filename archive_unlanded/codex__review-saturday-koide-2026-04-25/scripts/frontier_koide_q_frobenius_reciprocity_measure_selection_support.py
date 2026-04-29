#!/usr/bin/env python3
"""Koide Q Frobenius-reciprocity measure-selection support audit.

This runner verifies the support-grade content in
docs/KOIDE_Q_FROBENIUS_RECIPROCITY_MEASURE_SELECTION_SUPPORT_NOTE_2026-04-25.md.

It deliberately does not certify retained Koide closure.  The positive claim is
conditional:

    Frobenius reciprocity selects the (1,1) block-total multiplicity measure;
    if that measure is selected as the physical charged-lepton extremal
    convention, the admitted AM-GM chain gives kappa=2 and Q=2/3.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "KOIDE_Q_FROBENIUS_RECIPROCITY_MEASURE_SELECTION_SUPPORT_NOTE_2026-04-25.md"

AUTHORITY_FILES = [
    ROOT / "docs" / "KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md",
    ROOT / "docs" / "KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md",
    ROOT / "docs" / "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
]

PASS_COUNT = 0
FAIL_COUNT = 0


def normalized(text: str) -> str:
    return re.sub(r"[\s`*_]+", " ", text.lower())


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    haystack = normalized(text)
    return all(normalized(phrase) in haystack for phrase in phrases)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frob_norm_sq(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.H * matrix))


def schur_inner(chi_a: list[sp.Expr], chi_b: list[sp.Expr]) -> sp.Expr:
    value = sum(chi_a[i] * sp.conjugate(chi_b[i]) for i in range(3)) / 3
    return sp.nsimplify(sp.simplify(value))


def main() -> int:
    print("=" * 88)
    print("Koide Q Frobenius-reciprocity measure-selection support audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    section("Authority and status boundary")
    note_text = read(NOTE)
    for path in AUTHORITY_FILES:
        check(f"authority exists: {path.relative_to(ROOT)}", path.exists())

    kappa_text = read(AUTHORITY_FILES[0])
    frob_text = read(AUTHORITY_FILES[1])
    crit_text = read(AUTHORITY_FILES[2])

    check(
        "KAPPA identifies Frobenius reciprocity multiplicity count",
        has_all(kappa_text, ("Frobenius reciprocity", "multiplicity count", "kappa = 2")),
    )
    check(
        "FROB SPLIT retains Frobenius inner-product canonicality inside admitted route",
        has_all(frob_text, ("Frobenius", "canonical inner product", "Herm(3)")),
    )
    check(
        "CRIT keeps Q closure support-grade, not retained native closure",
        has_all(crit_text, ("Q = 2/3", "not retained native Koide closure")),
    )

    required_boundaries = [
        "exact support / criterion theorem only",
        "not retained native Koide closure",
        "CONDITIONAL_Q_EQ_2_OVER_3_IF_FR_BLOCK_TOTAL_PHYSICAL=TRUE",
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE",
        "KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE",
        "KOIDE_FULL_DIMENSIONLESS_CLOSURE=FALSE",
        "RESIDUAL_Q=derive_physical_source_domain_and_source_free_reduced_carrier_selection",
    ]
    for phrase in required_boundaries:
        check(f"note states boundary: {phrase}", normalized(phrase) in normalized(note_text))

    forbidden_promotions = [
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE",
        "KOIDE_FULL_DIMENSIONLESS_CLOSURE=TRUE",
        "Q_l = 2/3 retained closure",
        "therefore proves charged-lepton Koide",
    ]
    for phrase in forbidden_promotions:
        check(f"note avoids overpromotion: {phrase}", phrase not in note_text)

    section("Herm_circ(3) Frobenius energy algebra")
    a, x, y = sp.symbols("a x y", real=True)
    c3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    eye3 = sp.eye(3)
    h_plus = a * eye3
    h_perp = (x + sp.I * y) * c3 + (x - sp.I * y) * (c3**2)

    e_plus = frob_norm_sq(h_plus)
    e_perp = frob_norm_sq(h_perp)

    check("E_plus = ||a I||_F^2 = 3a^2", sp.simplify(e_plus - 3 * a**2) == 0, f"E_plus={e_plus}")
    check(
        "E_perp = ||b C + bbar C^2||_F^2 = 6|b|^2",
        sp.simplify(e_perp - 6 * (x**2 + y**2)) == 0,
        f"E_perp={e_perp}",
    )
    check("Frobenius orthogonality: <H_plus,H_perp> = 0", sp.simplify(sp.trace(h_plus.H * h_perp)) == 0)

    section("AM-GM conditional chain")
    ep, eq, n = sp.symbols("E_plus E_perp N", positive=True)
    product = ep * (n - ep)
    derivative = sp.diff(product, ep)
    critical = sp.solve(sp.Eq(derivative, 0), ep)
    second_derivative = sp.diff(product, ep, 2)
    check("E_plus*E_perp at fixed total has unique critical point E_plus=N/2", critical == [n / 2])
    check("critical point is a strict maximum", second_derivative == -2)

    kappa = sp.symbols("kappa", positive=True)
    kappa_from_equal_energy = sp.simplify(2 * (ep / eq)).subs(ep, eq)
    check("E_plus=E_perp implies kappa=2", kappa_from_equal_energy == 2, f"kappa={kappa_from_equal_energy}")

    c_sq = 4 / kappa
    q_of_kappa = sp.simplify((c_sq + 2) / 6)
    check("at kappa=2, c^2=2", sp.simplify(c_sq.subs(kappa, 2) - 2) == 0)
    check("at kappa=2, Q=2/3", sp.simplify(q_of_kappa.subs(kappa, 2) - sp.Rational(2, 3)) == 0)

    mu, nu = sp.symbols("mu nu", positive=True)
    kappa_weighted = 2 * mu / nu
    check("block-total weights (1,1) give kappa=2", sp.simplify(kappa_weighted.subs({mu: 1, nu: 1}) - 2) == 0)
    check("det/rank weights (1,2) give kappa=1", sp.simplify(kappa_weighted.subs({mu: 1, nu: 2}) - 1) == 0)
    check("det/rank kappa=1 gives Q=1, not Q=2/3", q_of_kappa.subs(kappa, 1) == 1)

    section("C3 Schur orthogonality / multiplicity count")
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    chi_triv = [sp.Integer(1), sp.Integer(1), sp.Integer(1)]
    chi_omega = [sp.Integer(1), omega, sp.conjugate(omega)]
    chi_omega_bar = [sp.Integer(1), sp.conjugate(omega), omega]

    check("<trivial,trivial>_C3 = 1", schur_inner(chi_triv, chi_triv) == 1)
    check("<omega,omega>_C3 = 1", schur_inner(chi_omega, chi_omega) == 1)
    check("<omega,omega_bar>_C3 = 0", schur_inner(chi_omega, chi_omega_bar) == 0)
    check("<trivial,omega>_C3 = 0", schur_inner(chi_triv, chi_omega) == 0)

    multiplicities = []
    for d in range(2, 9):
        trivial = 1
        doublets = (d - 1) // 2
        sign = 1 if d % 2 == 0 else 0
        multiplicities.append((d, trivial, doublets, sign))

    check("d=3 has exactly (trivial,doublet,sign)=(1,1,0)", (3, 1, 1, 0) in multiplicities)
    check(
        "among d=2..8, d=3 is the only no-sign single-doublet carrier",
        [d for d, trivial, doublets, sign in multiplicities if (trivial, doublets, sign) == (1, 1, 0)] == [3],
        f"multiplicities={multiplicities}",
    )

    section("Summary")
    total = PASS_COUNT + FAIL_COUNT
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}, CHECKS={total}")
    if FAIL_COUNT:
        print("VERDICT: failed support audit.")
        return 1

    print("VERDICT: support theorem verified.")
    print("  Frobenius reciprocity selects the (1,1) block-total measure.")
    print("  Conditional on selecting that measure physically, kappa=2 and Q=2/3.")
    print("  Retained Koide Q/delta/full dimensionless closure remains explicitly false.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
