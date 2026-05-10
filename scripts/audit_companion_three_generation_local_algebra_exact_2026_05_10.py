#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`THREE_GENERATION_LOCAL_ALGEBRA_NARROW_THEOREM_NOTE_2026-05-10`.

The narrow theorem's load-bearing content is:

  (N1) Total corner count on {0, 1}^d is 2^d.
  (N2) Corner count at Hamming weight w is binomial(d, w).
  (N3) Binomial sum: sum_{w=0}^{d} binomial(d, w) = 2^d.

specialized at d = 3 to:

  (R1)-(R6): 8 = 1 + 3 + 3 + 1, with binomial(3, 1) = 3.

The runner verifies (N1)-(N3) by direct enumeration plus sympy
binomial-identity check across d in {1, 2, 3, 4, 5, 6}, then
specializes to the framework d = 3 instance.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow note's
load-bearing combinatorial class-A counts hold at exact precision.
"""

from itertools import product
from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, binomial, simplify, summation, symbols
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def enumerate_hypercube(d: int) -> list:
    """Return all 2^d corners of {0, 1}^d as tuples."""
    return list(product([0, 1], repeat=d))


def count_by_weight(corners: list) -> dict:
    """Return a dict mapping Hamming weight -> count."""
    counts: dict = {}
    for c in corners:
        w = sum(c)
        counts[w] = counts.get(w, 0) + 1
    return counts


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("THREE_GENERATION_LOCAL_ALGEBRA_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: combinatorial verification of (N1)-(N3) and (R1)-(R6)")
    print("by direct enumeration plus sympy binomial-identity check")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 1: (N1) total corner count |{0,1}^d| = 2^d (direct enumeration)")
    # ---------------------------------------------------------------------
    for d in [1, 2, 3, 4, 5, 6]:
        corners = enumerate_hypercube(d)
        check(
            f"(N1) at d = {d}: |{{0,1}}^d| = 2^d = {2**d}",
            len(corners) == 2**d,
            detail=f"enumerated count = {len(corners)}",
        )

    # ---------------------------------------------------------------------
    section("Part 2: (N2) corner count at Hamming weight w = binomial(d, w)")
    # ---------------------------------------------------------------------
    for d in [1, 2, 3, 4, 5, 6]:
        corners = enumerate_hypercube(d)
        by_weight = count_by_weight(corners)
        for w in range(d + 1):
            expected = int(binomial(d, w))
            got = by_weight.get(w, 0)
            check(
                f"(N2) at d = {d}, w = {w}: count = binomial({d}, {w}) = {expected}",
                got == expected,
                detail=f"enumerated count = {got}",
            )

    # ---------------------------------------------------------------------
    section("Part 3: (N3) binomial sum identity sum_w binomial(d, w) = 2^d")
    # ---------------------------------------------------------------------
    # Numerical check at small d.
    for d in [1, 2, 3, 4, 5, 6]:
        total = sum(int(binomial(d, w)) for w in range(d + 1))
        check(
            f"(N3) at d = {d}: sum_w binomial({d}, w) = 2^d = {2**d}",
            total == 2**d,
            detail=f"sum = {total}",
        )

    # Symbolic sympy identity check (binomial theorem, (1+1)^d = sum_w bin(d,w)):
    d_sym, w_sym = symbols("d w", positive=True, integer=True)
    # At a specific d the summation simplifies; verify for d = 3 and d = 4.
    sum_at_d3 = summation(binomial(3, w_sym), (w_sym, 0, 3))
    check(
        "(N3) sympy summation at d=3: sum_{w=0}^{3} binomial(3, w) = 8",
        sum_at_d3 == 8,
        detail=f"sympy summation = {sum_at_d3}",
    )
    sum_at_d4 = summation(binomial(4, w_sym), (w_sym, 0, 4))
    check(
        "(N3) sympy summation at d=4: sum_{w=0}^{4} binomial(4, w) = 16",
        sum_at_d4 == 16,
        detail=f"sympy summation = {sum_at_d4}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (R1)-(R6) framework specialization d = 3")
    # ---------------------------------------------------------------------
    corners_3 = enumerate_hypercube(3)
    by_weight_3 = count_by_weight(corners_3)

    check(
        "(R1) total corner count at d=3 = 2^3 = 8",
        len(corners_3) == 8,
        detail=f"got {len(corners_3)}",
    )
    check(
        "(R2) weight-0 count at d=3 = binomial(3, 0) = 1",
        by_weight_3.get(0, 0) == 1,
        detail=f"got {by_weight_3.get(0, 0)}",
    )
    check(
        "(R3) weight-1 count at d=3 = binomial(3, 1) = 3",
        by_weight_3.get(1, 0) == 3,
        detail=f"got {by_weight_3.get(1, 0)}",
    )
    check(
        "(R4) weight-2 count at d=3 = binomial(3, 2) = 3",
        by_weight_3.get(2, 0) == 3,
        detail=f"got {by_weight_3.get(2, 0)}",
    )
    check(
        "(R5) weight-3 count at d=3 = binomial(3, 3) = 1",
        by_weight_3.get(3, 0) == 1,
        detail=f"got {by_weight_3.get(3, 0)}",
    )
    check(
        "(R6) partition: 8 = 1 + 3 + 3 + 1",
        sum(by_weight_3.values()) == 8
        and by_weight_3[0] + by_weight_3[1] + by_weight_3[2] + by_weight_3[3] == 8
        and by_weight_3[0] == 1
        and by_weight_3[1] == 3
        and by_weight_3[2] == 3
        and by_weight_3[3] == 1,
        detail=f"partition = {[by_weight_3[w] for w in range(4)]}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (C1) binomial symmetry binomial(3, 1) = binomial(3, 2)")
    # ---------------------------------------------------------------------
    check(
        "(C1) binomial(3, 1) == binomial(3, 2) == 3",
        binomial(3, 1) == binomial(3, 2) == 3,
        detail="binomial symmetry k <-> d-k specializes at d=3",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (C2) extremal singletons binomial(3, 0) + binomial(3, 3) = 2")
    # ---------------------------------------------------------------------
    check(
        "(C2) binomial(3, 0) + binomial(3, 3) = 1 + 1 = 2",
        binomial(3, 0) + binomial(3, 3) == 2,
        detail="extremal singletons add to 2",
    )

    # ---------------------------------------------------------------------
    section("Part 7: (C3) corner-count factorization 8 = 2 * (1 + 3)")
    # ---------------------------------------------------------------------
    factorization_lhs = 8
    factorization_rhs = 2 * (1 + 3)
    check(
        "(C3) 8 == 2 * (1 + 3) == 2 * 4",
        factorization_lhs == factorization_rhs == 8,
        detail=f"lhs = {factorization_lhs}, rhs = {factorization_rhs}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: counterfactual at d = 4 (16 = 1 + 4 + 6 + 4 + 1)")
    # ---------------------------------------------------------------------
    corners_4 = enumerate_hypercube(4)
    by_weight_4 = count_by_weight(corners_4)
    expected_4 = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
    check(
        "counterfactual at d=4: 16 = 1 + 4 + 6 + 4 + 1 (NOT 8 = 1 + 3 + 3 + 1)",
        by_weight_4 == expected_4 and len(corners_4) == 16,
        detail=f"d=4 partition = {[by_weight_4[w] for w in range(5)]}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: counterfactual at d = 2 (4 = 1 + 2 + 1)")
    # ---------------------------------------------------------------------
    corners_2 = enumerate_hypercube(2)
    by_weight_2 = count_by_weight(corners_2)
    expected_2 = {0: 1, 1: 2, 2: 1}
    check(
        "counterfactual at d=2: 4 = 1 + 2 + 1 (NOT 8 = 1 + 3 + 3 + 1)",
        by_weight_2 == expected_2 and len(corners_2) == 4,
        detail=f"d=2 partition = {[by_weight_2[w] for w in range(3)]}",
    )

    # ---------------------------------------------------------------------
    section("Part 10: parametric sympy binomial identity")
    # ---------------------------------------------------------------------
    # Pascal: binomial(d+1, k) = binomial(d, k-1) + binomial(d, k).
    d_test = 3
    for k in range(1, d_test + 1):
        lhs = binomial(d_test + 1, k)
        rhs = binomial(d_test, k - 1) + binomial(d_test, k)
        check(
            f"Pascal: binomial({d_test+1}, {k}) = binomial({d_test}, {k-1}) + binomial({d_test}, {k})",
            lhs == rhs,
            detail=f"lhs = {lhs}, rhs = {rhs}",
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact precision:")
    print("    (N1) total corner count = 2^d for d in {1, 2, 3, 4, 5, 6}")
    print("    (N2) per-weight count = binomial(d, w) by enumeration")
    print("    (N3) binomial sum = 2^d both numerically and via sympy summation")
    print("    (R1)-(R6) framework specialization at d=3: 8 = 1 + 3 + 3 + 1")
    print("    (C1) binomial symmetry at d=3: binomial(3, 1) = binomial(3, 2) = 3")
    print("    (C2) extremal singletons add to 2")
    print("    (C3) factorization 8 = 2 * (1 + 3)")
    print("    Counterfactual at d=4: 16 = 1 + 4 + 6 + 4 + 1")
    print("    Counterfactual at d=2: 4 = 1 + 2 + 1")
    print("    Pascal identity at d = 3")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
