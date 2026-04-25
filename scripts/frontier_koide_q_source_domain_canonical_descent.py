#!/usr/bin/env python3
"""Exact audit for the Koide Q source-domain canonical descent support theorem.

This verifies the algebra landed in
docs/KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md.
It deliberately does not certify retained Koide closure.  The only positive
claim audited here is the exact source-domain descent statement:

    A = span{P_plus, P_perp} -> D^C3 = span{I}
    E_loc(X) = Tr(X) I / 3

and the resulting erasure of the reduced traceless Z-coordinate modulo the
common scalar background.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md"

AUTHORITY_FILES = [
    ROOT / "docs" / "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
    ROOT / "docs" / "KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md",
    ROOT / "docs" / "KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md",
    ROOT / "docs" / "KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md",
]

Matrix = tuple[tuple[Fraction, ...], ...]

passes = 0
fails = 0


def check(name: str, condition: bool) -> None:
    global passes, fails
    if condition:
        passes += 1
        print(f"  [PASS] {name}")
    else:
        fails += 1
        print(f"  [FAIL] {name}")


def section(title: str) -> None:
    print("\n" + "-" * 88)
    print(title)
    print("-" * 88)


def mat(rows: Iterable[Iterable[int | Fraction]]) -> Matrix:
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x + y for x, y in zip(row_a, row_b)) for row_a, row_b in zip(a, b))


def sub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x - y for x, y in zip(row_a, row_b)) for row_a, row_b in zip(a, b))


def scale(c: Fraction, a: Matrix) -> Matrix:
    return tuple(tuple(c * x for x in row) for row in a)


def mmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def diag(a: Matrix) -> Matrix:
    n = len(a)
    return tuple(
        tuple(a[i][i] if i == j else Fraction(0) for j in range(n))
        for i in range(n)
    )


def identity(n: int) -> Matrix:
    return tuple(
        tuple(Fraction(1) if i == j else Fraction(0) for j in range(n))
        for i in range(n)
    )


def all_ones(n: int) -> Matrix:
    return tuple(tuple(Fraction(1) for _ in range(n)) for _ in range(n))


def is_scalar_identity(a: Matrix) -> bool:
    n = len(a)
    lam = a[0][0]
    return all(a[i][j] == (lam if i == j else 0) for i in range(n) for j in range(n))


def scalar_coefficient(a: Matrix) -> Fraction:
    assert is_scalar_identity(a)
    return a[0][0]


def e_loc(x: Matrix) -> Matrix:
    return scale(trace(x) / 3, I3)


def q_of_z(z: Fraction) -> Fraction:
    return Fraction(2, 1) / (3 * (1 + z))


def contains_normalized(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()) in " ".join(text.split())


I3 = identity(3)
J3 = all_ones(3)
R = mat(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ]
)
P_PLUS = scale(Fraction(1, 3), J3)
P_PERP = sub(I3, P_PLUS)
Z = sub(P_PLUS, P_PERP)


def main() -> int:
    print("=" * 88)
    print("Koide Q source-domain canonical descent support audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    section("Authority and status boundary")
    note_text = NOTE.read_text()
    for path in AUTHORITY_FILES:
        check(f"authority/reference exists: {path.relative_to(ROOT)}", path.exists())

    required_boundaries = [
        "not retained Koide closure",
        "This note does not prove that physical law.",
        "Q_RETAINED_NATIVE_CLOSURE=FALSE",
        "DELTA_RETAINED_NATIVE_CLOSURE=FALSE",
        "FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE",
        "RESIDUAL_Q=derive_physical_source_domain_uses_strict_onsite_descent_or_excludes_Z_as_undeformed_background",
    ]
    for phrase in required_boundaries:
        check(f"note states boundary: {phrase}", contains_normalized(note_text, phrase))

    forbidden_promotions = [
        "Q_RETAINED_NATIVE_CLOSURE=TRUE",
        "FULL_DIMENSIONLESS_KOIDE_CLOSURE=TRUE",
        "therefore retained native Koide closure",
        "therefore proves charged-lepton Koide",
    ]
    for phrase in forbidden_promotions:
        check(f"note avoids overclaim: {phrase}", not contains_normalized(note_text, phrase))

    section("C3 projector algebra")
    check("R^3 = I", mmul(mmul(R, R), R) == I3)
    check("P_plus is idempotent", mmul(P_PLUS, P_PLUS) == P_PLUS)
    check("P_perp is idempotent", mmul(P_PERP, P_PERP) == P_PERP)
    check("P_plus + P_perp = I", add(P_PLUS, P_PERP) == I3)
    check("P_plus P_perp = 0", mmul(P_PLUS, P_PERP) == scale(Fraction(0), I3))
    check("Z = P_plus - P_perp", Z == sub(P_PLUS, P_PERP))
    check("Tr(P_plus) = 1", trace(P_PLUS) == 1)
    check("Tr(P_perp) = 2", trace(P_PERP) == 2)
    check("Tr(Z) = -1", trace(Z) == -1)

    section("Site-local diagonal compression")
    check("Diag(P_plus) = I/3", diag(P_PLUS) == scale(Fraction(1, 3), I3))
    check("Diag(P_perp) = 2I/3", diag(P_PERP) == scale(Fraction(2, 3), I3))
    check("Diag(Z) = -I/3", diag(Z) == scale(Fraction(-1, 3), I3))
    check("Diag(P_plus) lands in D^C3", is_scalar_identity(diag(P_PLUS)))
    check("Diag(P_perp) lands in D^C3", is_scalar_identity(diag(P_PERP)))
    check("Diag(Z) lands in D^C3", is_scalar_identity(diag(Z)))

    section("Theorem 1: unique trace-preserving descent A -> D^C3")
    basis = [("I", I3), ("P_plus", P_PLUS), ("P_perp", P_PERP), ("Z", Z)]
    for name, x in basis:
        ex = e_loc(x)
        check(f"E_loc({name}) is scalar onsite", is_scalar_identity(ex))
        check(f"E_loc({name}) preserves trace", trace(ex) == trace(x))

    check("E_loc(I) = I", e_loc(I3) == I3)
    check("E_loc(P_plus) = I/3", e_loc(P_PLUS) == scale(Fraction(1, 3), I3))
    check("E_loc(P_perp) = 2I/3", e_loc(P_PERP) == scale(Fraction(2, 3), I3))
    check("E_loc(Z) = -I/3", e_loc(Z) == scale(Fraction(-1, 3), I3))

    alpha = Fraction(5, 7)
    beta = Fraction(-2, 5)
    x = add(scale(alpha, P_PLUS), scale(beta, P_PERP))
    expected_lam = (alpha + 2 * beta) / 3
    check("E_loc(alpha P_plus + beta P_perp) = (alpha+2 beta) I / 3",
          e_loc(x) == scale(expected_lam, I3))
    check("trace preservation fixes lambda uniquely",
          scalar_coefficient(e_loc(x)) == trace(x) / 3)

    section("Theorem 2: Diag restricted to A equals E_loc")
    for name, x0 in [
        ("P_plus", P_PLUS),
        ("P_perp", P_PERP),
        ("Z", Z),
        ("generic alpha/beta", x),
    ]:
        check(f"Diag({name}) = E_loc({name})", diag(x0) == e_loc(x0))

    section("Reduced Z-coordinate erasure modulo common scalar")
    s = Fraction(11, 13)
    z = Fraction(3, 8)
    k = add(scale(s, I3), scale(z, Z))
    descended = e_loc(k)
    check("E_loc(sI+zZ) is common scalar", is_scalar_identity(descended))
    check("E_loc(sI+zZ) = (s-z/3)I", descended == scale(s - z / 3, I3))
    check("reduced traceless quotient after descent is zero",
          sub(descended, scale(scalar_coefficient(descended), I3)) == scale(Fraction(0), I3))
    check("nonzero projected Z existed before descent", z != 0 and not is_scalar_identity(k))

    section("Conditional Q implication remains conditional")
    check("criterion Q(z=0) = 2/3", q_of_z(Fraction(0)) == Fraction(2, 3))
    check("nonzero z changes Q in the admitted reduced route", q_of_z(Fraction(-1, 3)) == 1)
    check("conditional closeout flag is true in note",
          "CONDITIONAL_Q_CLOSES_IF_PHYSICAL_SOURCE_DOMAIN_USES_ONSITE_DESCENT=TRUE" in note_text)
    check("physical source-domain law remains named residual",
          contains_normalized(note_text, "does not prove that physical law"))

    section("Summary")
    print("  Certified:")
    print("    exact unique trace-preserving local descent A -> D^C3,")
    print("    exact identification with diagonal compression, and exact")
    print("    erasure of the reduced Z coordinate modulo common scalar.")
    print()
    print("  Not certified:")
    print("    physical selection of onsite descent, retained Koide Q closure,")
    print("    delta=2/9 closure, or full dimensionless charged-lepton closure.")

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={passes}, FAIL={fails}")
    print(f"PASSED: {passes}/{passes + fails}")
    print("=" * 88)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
