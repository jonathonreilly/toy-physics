#!/usr/bin/env python3
"""Conditional support audit for the Koide Q OP-locality / C3-fixed source route.

This runner intentionally does not certify retained Koide closure. It verifies
only the landable conditional algebra:

    strict onsite source + C3-fixed undeformed-source premise
      => J = sI
      => equal (P_+, P_perp) channel source
      => reduced trace-zero source coordinate z = 0
      => Q = 2/3 on the admitted criterion carrier.

The remaining physical source-selection theorem is checked as explicitly open
by closeout flags in the note.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTE = DOCS / "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md"

REFERENCE_DOCS = [
    "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md",
    "THREE_GENERATION_STRUCTURE_NOTE.md",
    "KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md",
    "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
]

PASS = 0
FAIL = 0

Matrix = tuple[tuple[Fraction, ...], ...]


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88)
    print(title)
    print("-" * 88)


def normalize(text: str) -> str:
    return " ".join(text.split())


def contains(text: str, phrase: str) -> bool:
    return normalize(phrase) in normalize(text)


def mat(rows: Iterable[Iterable[int | Fraction]]) -> Matrix:
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def identity(n: int) -> Matrix:
    return tuple(
        tuple(Fraction(1) if i == j else Fraction(0) for j in range(n))
        for i in range(n)
    )


def all_ones(n: int) -> Matrix:
    return tuple(tuple(Fraction(1) for _ in range(n)) for _ in range(n))


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


def transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a)))


def trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def diag3(a: Fraction, b: Fraction, c: Fraction) -> Matrix:
    return mat([[a, 0, 0], [0, b, 0], [0, 0, c]])


def is_scalar_identity(a: Matrix) -> bool:
    n = len(a)
    lam = a[0][0]
    return all(a[i][j] == (lam if i == j else 0) for i in range(n) for j in range(n))


def frob_inner(a: Matrix, b: Matrix) -> Fraction:
    return sum(a[i][j] * b[i][j] for i in range(len(a)) for j in range(len(a)))


def project_coeff(j: Matrix, p: Matrix) -> Fraction:
    return frob_inner(j, p) / frob_inner(p, p)


I3 = identity(3)
J3 = all_ones(3)
C = mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
P_PLUS = scale(Fraction(1, 3), J3)
P_PERP = sub(I3, P_PLUS)
Z3 = sub(P_PLUS, P_PERP)


def q_of_z(z: Fraction) -> Fraction:
    return Fraction(2, 1) / (3 * (1 + z))


def main() -> int:
    print("=" * 88)
    print("Koide Q OP-locality / C3-fixed source conditional support audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    note_text = NOTE.read_text(encoding="utf-8")

    section("Status boundary")
    check("support note exists", NOTE.exists(), str(NOTE.relative_to(ROOT)))
    for name in REFERENCE_DOCS:
        path = DOCS / name
        check(f"reference exists: {name}", path.exists())

    required_boundaries = [
        "conditional support note",
        "not retained Koide closure",
        "This note proves what follows from `P_SOURCE`; it does not prove `P_SOURCE`.",
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE",
        "KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE",
        "CD_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=FALSE",
        "CRIT_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=FALSE",
        "RESIDUAL_Q=derive_physical_charged_lepton_source_selection_strict_onsite_C3_fixed",
    ]
    for phrase in required_boundaries:
        check(f"note states boundary: {phrase}", contains(note_text, phrase))

    forbidden_overclaims = [
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=" + "TRUE",
        "CD_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=" + "TRUE",
        "CRIT_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=" + "TRUE",
        "retained native " + "closure",
    ]
    for phrase in forbidden_overclaims:
        check(f"note avoids overclaim: {phrase}", not contains(note_text, phrase))

    section("C3 projector algebra")
    C2 = mmul(C, C)
    C3 = mmul(C2, C)
    check("C^3 = I", C3 == I3)
    check("P_+ = (I + C + C^2)/3", P_PLUS == scale(Fraction(1, 3), add(add(I3, C), C2)))
    check("P_+ idempotent", mmul(P_PLUS, P_PLUS) == P_PLUS)
    check("P_perp idempotent", mmul(P_PERP, P_PERP) == P_PERP)
    check("P_+ + P_perp = I", add(P_PLUS, P_PERP) == I3)
    check("P_+ P_perp = 0", mmul(P_PLUS, P_PERP) == scale(Fraction(0), I3))
    check("Tr(P_+) = 1", trace(P_PLUS) == 1)
    check("Tr(P_perp) = 2", trace(P_PERP) == 2)
    check("Z = P_+ - P_perp", Z3 == sub(P_PLUS, P_PERP))
    check("Tr(Z) = -1", trace(Z3) == -1)

    section("Conditional C3-fixed onsite source")
    j1, j2, j3 = Fraction(2), Fraction(5), Fraction(7)
    j_nonuniform = diag3(j1, j2, j3)
    cjc = mmul(mmul(C, j_nonuniform), transpose(C))
    check("generic onsite source is not automatically C3-fixed", cjc != j_nonuniform)

    s = Fraction(11, 13)
    j_scalar = scale(s, I3)
    check("J = sI is C3-fixed", mmul(mmul(C, j_scalar), transpose(C)) == j_scalar)
    check("C3-fixed onsite source lands in span{I}", is_scalar_identity(j_scalar))

    # For a diagonal source, CJC^-1 = J iff the three diagonal entries are equal.
    samples = [
        diag3(Fraction(1), Fraction(1), Fraction(1)),
        diag3(Fraction(1), Fraction(2), Fraction(1)),
        diag3(Fraction(3), Fraction(3), Fraction(4)),
    ]
    fixed_flags = [mmul(mmul(C, x), transpose(C)) == x for x in samples]
    equal_flags = [x[0][0] == x[1][1] == x[2][2] for x in samples]
    check("on diagonal samples, C3-fixed iff j1=j2=j3", fixed_flags == equal_flags)

    section("Projection of J = sI into two C3 isotype channels")
    k_plus = project_coeff(j_scalar, P_PLUS)
    k_perp = project_coeff(j_scalar, P_PERP)
    z_reduced = (k_plus - k_perp) / 2
    check("Frobenius coefficient K_+ = s", k_plus == s, f"K_+={k_plus}")
    check("Frobenius coefficient K_perp = s", k_perp == s, f"K_perp={k_perp}")
    check("trace-zero reduced source coordinate z = 0", z_reduced == 0, f"z={z_reduced}")

    section("Canonical descent cross-check")
    s0 = Fraction(17, 19)
    z0 = Fraction(5, 23)
    k_comm = add(scale(s0, I3), scale(z0, Z3))
    e_loc = scale(trace(k_comm) / 3, I3)
    expected = scale(s0 - z0 / 3, I3)
    traceless_after_descent = sub(e_loc, scale(trace(e_loc) / 3, I3))
    check("E_loc(sI + zZ) = (s - z/3)I", e_loc == expected)
    check("E_loc target is strict onsite scalar", is_scalar_identity(e_loc))
    check("reduced traceless coordinate is killed by descent", traceless_after_descent == scale(Fraction(0), I3))

    section("Criterion-carrier Q consequence")
    check("Q(z=0) = 2/3", q_of_z(Fraction(0)) == Fraction(2, 3))
    for z in [Fraction(-1, 3), Fraction(1, 5), Fraction(2, 7)]:
        check(f"nonzero z={z} gives non-Koide Q", q_of_z(z) != Fraction(2, 3), f"Q={q_of_z(z)}")

    # Exact inverse: Q = 2/3 implies z = 0 under Q(z) = 2/(3(1+z)).
    q = Fraction(2, 3)
    z_from_q = Fraction(2, 1) / (3 * q) - 1
    check("inverse map z(Q=2/3) = 0", z_from_q == 0)

    section("Final support flags")
    support_flags_ok = all(
        contains(note_text, phrase)
        for phrase in [
            "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT=TRUE",
            "CONDITIONAL_C3_FIXED_ONSITE_SOURCE_IMPLIES_Z_ZERO=TRUE",
            "CONDITIONAL_Z_ZERO_IMPLIES_Q_TWO_THIRDS=TRUE",
        ]
    )
    closure_flags_ok = all(
        contains(note_text, phrase)
        for phrase in [
            "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE",
            "KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE",
            "CHARGED_LEPTON_MASS_RETENTION=FALSE",
        ]
    )
    check("positive support flags present", support_flags_ok)
    check("retained-closure flags remain false", closure_flags_ok)

    print(f"\nTOTAL: PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
