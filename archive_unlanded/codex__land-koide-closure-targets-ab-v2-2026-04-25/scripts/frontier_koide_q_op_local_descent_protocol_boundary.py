#!/usr/bin/env python3
"""Audit the Koide Q OP local-descent protocol boundary note.

This runner verifies the exact algebra salvaged from the AB-v2 branch and
guards against promoting it to retained Koide closure.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "KOIDE_Q_OP_LOCAL_DESCENT_PROTOCOL_BOUNDARY_NOTE_2026-04-25.md"

AUTHORITY_FILES = [
    ROOT / "docs" / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md",
    ROOT / "docs" / "KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md",
    ROOT / "docs" / "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
    ROOT / "docs" / "KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md",
]

Matrix = tuple[tuple[Fraction, ...], ...]

passes = 0
fails = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global passes, fails
    if condition:
        passes += 1
        print(f"  [PASS] {label}")
    else:
        fails += 1
        print(f"  [FAIL] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"         {line}")


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


def identity(n: int) -> Matrix:
    return tuple(
        tuple(Fraction(1) if i == j else Fraction(0) for j in range(n))
        for i in range(n)
    )


def all_ones(n: int) -> Matrix:
    return tuple(tuple(Fraction(1) for _ in range(n)) for _ in range(n))


def trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def diag(a: Matrix) -> Matrix:
    n = len(a)
    return tuple(
        tuple(a[i][i] if i == j else Fraction(0) for j in range(n))
        for i in range(n)
    )


def is_scalar(a: Matrix) -> bool:
    n = len(a)
    lam = a[0][0]
    return all(a[i][j] == (lam if i == j else 0) for i in range(n) for j in range(n))


def has_offdiag(a: Matrix) -> bool:
    return any(a[i][j] != 0 for i in range(len(a)) for j in range(len(a)) if i != j)


def e_loc(x: Matrix) -> Matrix:
    return scale(trace(x) / 3, I3)


def q_of_z(z: Fraction) -> Fraction:
    return Fraction(2, 1) / (3 * (1 + z))


def contains_normalized(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()) in " ".join(text.split())


I3 = identity(3)
C = mat(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ]
)
P_PLUS = scale(Fraction(1, 3), all_ones(3))
P_PERP = sub(I3, P_PLUS)
Z = sub(P_PLUS, P_PERP)


def main() -> int:
    print("=" * 88)
    print("Koide Q OP local-descent protocol boundary audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    note_text = NOTE.read_text()

    section("Authority and boundary checks")
    check("note exists", NOTE.exists())
    for path in AUTHORITY_FILES:
        check(f"authority/reference exists: {path.relative_to(ROOT)}", path.exists())

    required_boundaries = [
        "not retained Koide closure",
        "The physical inference is not yet retained.",
        "Q_RETAINED_NATIVE_CLOSURE=FALSE",
        "DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE",
        "FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE",
        "RESIDUAL_Q=derive_physical_charged_lepton_dimensionless_readout_uses_canonical_onsite_descent_or_excludes_Z",
    ]
    for phrase in required_boundaries:
        check(f"note states boundary: {phrase}", contains_normalized(note_text, phrase))

    forbidden_promotions = [
        "Q_RETAINED_NATIVE_CLOSURE=TRUE",
        "KOIDE_BRANNEN_DELTA_2_OVER_9_RAD_RETAINED_FULL_CLOSURE=TRUE",
        "retained full closure",
        "therefore retained native Koide closure",
    ]
    for phrase in forbidden_promotions:
        check(f"note avoids promotion: {phrase}", not contains_normalized(note_text, phrase))

    section("C3 commutant algebra")
    check("C^3 = I", mmul(mmul(C, C), C) == I3)
    check("P_plus + P_perp = I", add(P_PLUS, P_PERP) == I3)
    check("P_plus P_perp = 0", mmul(P_PLUS, P_PERP) == scale(Fraction(0), I3))
    check("Z = P_plus - P_perp", Z == sub(P_PLUS, P_PERP))
    check("Z = -I/3 + (2/3)C + (2/3)C^2",
          Z == add(scale(Fraction(-1, 3), I3), add(scale(Fraction(2, 3), C), scale(Fraction(2, 3), mmul(C, C)))))
    check("Tr(Z) = -1", trace(Z) == Fraction(-1))
    check("Z has off-diagonal entries, so Z is not onsite", has_offdiag(Z))

    section("Canonical local descent")
    check("Diag(Z) = -I/3", diag(Z) == scale(Fraction(-1, 3), I3))
    check("E_loc(Z) = -I/3", e_loc(Z) == scale(Fraction(-1, 3), I3))
    check("E_loc(I) = I", e_loc(I3) == I3)

    s = Fraction(7, 11)
    z = Fraction(5, 13)
    k = add(scale(s, I3), scale(z, Z))
    descended = e_loc(k)
    check("K=sI+zZ is non-scalar when z != 0", not is_scalar(k))
    check("E_loc(sI+zZ) is scalar onsite", is_scalar(descended))
    check("E_loc(sI+zZ) = (s-z/3)I", descended == scale(s - z / 3, I3))
    check("descended source has zero reduced traceless coordinate",
          sub(descended, scale(descended[0][0], I3)) == scale(Fraction(0), I3))

    section("Conditional implication and counterdomain")
    check("if descent is imposed, z_eff=0 gives Q=2/3", q_of_z(Fraction(0)) == Fraction(2, 3))
    check("direct commutant readout at z=1/3 gives Q=1/2", q_of_z(Fraction(1, 3)) == Fraction(1, 2))
    check("direct commutant readout at z=-1/3 gives Q=1", q_of_z(Fraction(-1, 3)) == Fraction(1))
    check("descent is load-bearing because direct z != 0 differs from 2/3",
          q_of_z(Fraction(1, 3)) != Fraction(2, 3) and q_of_z(Fraction(-1, 3)) != Fraction(2, 3))

    section("Verdict")
    print("  Certified:")
    print("    OP local-descent algebra is exact, and canonical descent erases Z.")
    print("    Conditional route: if physical Q readout uses E_loc first, Q=2/3.")
    print()
    print("  Not certified:")
    print("    the physical readout protocol Q[K]=Q[E_loc(K)], retained Q closure,")
    print("    delta=2/9 rad closure, or full charged-lepton Koide closure.")

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={passes}, FAIL={fails}")
    print(f"PASSED: {passes}/{passes + fails}")
    print("=" * 88)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
