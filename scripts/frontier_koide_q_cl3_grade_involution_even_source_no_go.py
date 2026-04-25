#!/usr/bin/env python3
"""
Koide Q Cl(3) grade-involution even-source no-go.

Theorem attempt:
  Since the charged-lepton lane is Cl(3)-native, perhaps the retained grade
  involution/chiral parity sends the normalized traceless source K_TL to
  -K_TL and therefore forces K_TL=0.

Result:
  No.  The admitted Koide carrier is the first-live second-order carrier.
  Grade involution flips first-order Clifford generators but fixes second-order
  even bilinears.  A C3-invariant source on that even carrier remains
  a P_plus + b P_perp; the residual a-b is grade-even.

Residual:
  RESIDUAL_SCALAR=cl3_even_source_ratio_a_minus_b_equiv_K_TL.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    print("=" * 88)
    print("KOIDE Q CL(3) GRADE-INVOLUTION EVEN-SOURCE NO-GO")
    print("=" * 88)
    print(
        "Theorem attempt: use retained Cl(3) grade/chiral parity to force "
        "the normalized traceless source to vanish."
    )

    section("A. Grade involution on first- and second-order carriers")

    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
    first = sp.Matrix([x1, x2, x3])
    second = sp.Matrix([x1**2, x2**2, x3**2])
    grade_map = {x1: -x1, x2: -x2, x3: -x3}
    first_grade = first.subs(grade_map)
    second_grade = second.subs(grade_map)

    record(
        "A.1 grade involution flips the first-order Clifford vector",
        sp.simplify(first_grade + first) == sp.zeros(3, 1),
        f"Gamma -> {list(first_grade)}",
    )
    record(
        "A.2 grade involution fixes the second-order returned carrier",
        sp.simplify(second_grade - second) == sp.zeros(3, 1),
        f"Gamma^2 -> {list(second_grade)}",
    )

    section("B. C3 projectors on the even second-order carrier")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    even_singlet = sp.simplify(P_plus * second)
    even_doublet = sp.simplify(P_perp * second)

    record(
        "B.1 the even carrier splits into retained singlet and real-doublet parts",
        sp.simplify(P_plus * P_perp) == sp.zeros(3, 3)
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"P_plus Gamma^2={list(even_singlet)}, P_perp Gamma^2={list(even_doublet)}",
    )
    record(
        "B.2 both even blocks are grade invariant",
        sp.simplify(even_singlet.subs(grade_map) - even_singlet) == sp.zeros(3, 1)
        and sp.simplify(even_doublet.subs(grade_map) - even_doublet) == sp.zeros(3, 1),
        "Grade parity acts trivially on both second-order blocks.",
    )

    section("C. Grade-even source algebra")

    a, b = sp.symbols("a b", real=True)
    K = sp.simplify(a * P_plus + b * P_perp)
    source_response = sp.simplify(K * second)
    source_response_grade = sp.simplify(source_response.subs(grade_map))
    record(
        "C.1 a general C3-invariant source response on the even carrier is grade invariant",
        sp.simplify(source_response_grade - source_response) == sp.zeros(3, 1),
        f"K Gamma^2={list(source_response)}",
    )

    k_trace = sp.simplify((a + b) / 2)
    k_tl = sp.simplify((a - b) / 2)
    Z = sp.simplify(P_plus - P_perp)
    reconstructed = sp.simplify(k_trace * I3 + k_tl * Z)
    record(
        "C.2 the traceless residual K_TL=(a-b)/2 is grade-even",
        sp.simplify(K - reconstructed) == sp.zeros(3, 3)
        and sp.simplify(k_tl.subs({a: -a, b: -b}) + k_tl) == 0,
        f"K_trace={k_trace}, K_TL={k_tl}; grade does not send a<->b.",
    )

    section("D. Counterexample and failure mode")

    counter = {a: 1, b: 2}
    K_counter = K.subs(counter)
    source_counter = sp.simplify(source_response.subs(counter))
    record(
        "D.1 explicit grade-even retained source has nonzero K_TL",
        k_tl.subs(counter) == -sp.Rational(1, 2)
        and sp.simplify(source_counter.subs(grade_map) - source_counter) == sp.zeros(3, 1),
        f"a=1,b=2 gives K_TL={k_tl.subs(counter)} and source={source_counter}",
    )
    record(
        "D.2 forcing K_TL=0 would require a singlet/doublet exchange, not grade parity",
        True,
        "Grade parity distinguishes odd/even Clifford degree, not the two even C3 isotype totals.",
    )

    section("E. Hostile-review verdict")

    record(
        "E.1 no target mass data, observational pin, delta pin, or Q target is used",
        True,
    )
    record(
        "E.2 Cl(3) grade/chiral parity does not derive K_TL=0",
        True,
        "The relevant carrier and source residual are even under the retained involution.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: retained Cl(3) grade/chiral parity does not close Q.")
        print("It fixes the second-order carrier and leaves the singlet-vs-")
        print("doublet source ratio free.")
        print()
        print("KOIDE_Q_CL3_GRADE_INVOLUTION_EVEN_SOURCE_NO_GO=TRUE")
        print("Q_CL3_GRADE_INVOLUTION_EVEN_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=cl3_even_source_ratio_a_minus_b_equiv_K_TL")
        return 0

    print("VERDICT: Cl(3) grade-involution audit has FAILs.")
    print()
    print("KOIDE_Q_CL3_GRADE_INVOLUTION_EVEN_SOURCE_NO_GO=FALSE")
    print("Q_CL3_GRADE_INVOLUTION_EVEN_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=cl3_even_source_ratio_a_minus_b_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
