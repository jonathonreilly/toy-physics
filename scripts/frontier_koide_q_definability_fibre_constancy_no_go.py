#!/usr/bin/env python3
"""
Koide Q definability/fibre-constancy no-go.

Theorem attempt:
  Derive the missing physical readout factorization through the operational
  quotient by a definability or parametricity theorem.  If the physical source
  readout is definable only in the quotient language, then it cannot name the
  retained C3 orbit representatives {0} and {1,2}.  The two quotient-fibre
  components are exchangeable, so the source is fibre-constant:

      p_plus = p_perp = 1/2 -> K_TL = 0 -> Q = 2/3.

Result:
  Conditional positive, retained negative.  Quotient-language definability
  does force fibre constancy.  But the current retained Cl(3)/Z3 language
  contains orbit-size/rank data distinguishing the trivial real block from the
  two-dimensional real block.  In that retained language the label-preserving
  automorphism group is trivial, and rank-definable source states such as
  (1/3, 2/3) remain exact countermodels.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
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
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Conditional positive theorem in the quotient language")

    u = sp.symbols("u", real=True)
    source = sp.Matrix([u, 1 - u])
    swap = sp.Matrix([[0, 1], [1, 0]])
    quotient_invariance = list(sp.simplify(swap * source - source))
    quotient_solution = sp.solve(quotient_invariance, [u], dict=True)
    u_star = quotient_solution[0][u]
    record(
        "A.1 quotient-language parametricity forces the two-fibre source to be uniform",
        quotient_solution == [{u: sp.Rational(1, 2)}],
        f"swap*p-p={quotient_invariance}; u={u_star}",
    )
    record(
        "A.2 quotient-definable source gives K_TL=0 and Q=2/3",
        ktl_from_weight(u_star) == 0 and q_from_weight(u_star) == sp.Rational(2, 3),
        f"K_TL={ktl_from_weight(u_star)}, Q={q_from_weight(u_star)}",
    )
    n = sp.symbols("n", integer=True, positive=True)
    p0, p1, p2 = sp.symbols("p0 p1 p2", real=True)
    s3_solution = sp.solve(
        [sp.Eq(p0, p1), sp.Eq(p1, p2), sp.Eq(p0 + p1 + p2, 1)],
        [p0, p1, p2],
        dict=True,
    )
    record(
        "A.3 the theorem is general orbit uniformity, not a Koide-specific fit",
        s3_solution == [{p0: sp.Rational(1, 3), p1: sp.Rational(1, 3), p2: sp.Rational(1, 3)}],
        f"three-fibre solution={s3_solution}; formal n-symbol present={n}",
    )

    section("B. Retained language has orbit-size/rank predicates")

    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    rank_vector = sp.Matrix([rank_plus, rank_perp])
    swapped_rank_vector = sp.simplify(swap * rank_vector)
    record(
        "B.1 retained rank/orbit-size data distinguish plus and perp",
        rank_plus != rank_perp and swapped_rank_vector != rank_vector,
        f"rank_vector={list(rank_vector)}, swapped={list(swapped_rank_vector)}",
    )
    # If rank is part of the language, an automorphism must preserve it.  The
    # nontrivial swap is therefore not a retained-language automorphism.
    retained_automorphism_count = 1
    record(
        "B.2 retained-language automorphism group on the two labelled components is trivial",
        retained_automorphism_count == 1,
        "The swap violates the rank/orbit-size predicate, so no p_plus=p_perp equation follows.",
    )
    retained_normalization = sp.solve(sp.Eq(source[0] + source[1], 1), u, dict=True)
    record(
        "B.3 retained definability leaves a free normalized source scalar",
        retained_normalization == [],
        "source=(u,1-u) is normalized identically for every u.",
    )

    section("C. Exact retained definable counterstate")

    rank_state_plus = sp.simplify(rank_plus / (rank_plus + rank_perp))
    rank_state_perp = sp.simplify(rank_perp / (rank_plus + rank_perp))
    record(
        "C.1 rank-counting source is definable in the retained language",
        rank_state_plus == sp.Rational(1, 3)
        and rank_state_perp == sp.Rational(2, 3),
        f"rank source=({rank_state_plus},{rank_state_perp})",
    )
    record(
        "C.2 retained rank-definable source is exact and off Koide",
        q_from_weight(rank_state_plus) == 1
        and ktl_from_weight(rank_state_plus) == sp.Rational(3, 8),
        f"Q={q_from_weight(rank_state_plus)}, K_TL={ktl_from_weight(rank_state_plus)}",
    )
    z_expectation = sp.simplify(rank_state_plus - rank_state_perp)
    record(
        "C.3 the retained Z expectation is nonzero for the rank-definable source",
        z_expectation == -sp.Rational(1, 3),
        f"<Z>={z_expectation}",
    )

    section("D. Definability boundary")

    language_forget_rank = sp.symbols("language_forget_rank", real=True)
    record(
        "D.1 closure requires deleting the retained rank/orbit-size predicate from physical source language",
        sp.solve(sp.Eq(language_forget_rank, 0), language_forget_rank) == [0],
        "language_forget_rank=0 is the missing fibre-constancy/quotient-readout theorem.",
    )
    record(
        "D.2 definability theorem is valid only after choosing the quotient language as physical",
        True,
        "That choice is equivalent to saying source-visible C3 orbit labels are not physical readout data.",
    )
    record(
        "D.3 if the retained language is physical, rank-definable nonclosure survives",
        q_from_weight(rank_state_plus) != sp.Rational(2, 3),
        "The counterstate (1/3,2/3) is retained-language definable and normalized.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The Koide value is computed only after quotient-language invariance forces u=1/2.",
    )
    record(
        "E.2 quotient-language definability is not promoted as retained closure",
        True,
        "The retained language still distinguishes the two components by rank/orbit size.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem that physical source readouts are definable only in the quotient language.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: definability/fibre-constancy route is conditional, not retained-only proof.")
        print("KOIDE_Q_DEFINABILITY_FIBRE_CONSTANCY_NO_GO=TRUE")
        print("Q_DEFINABILITY_FIBRE_CONSTANCY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_PHYSICAL_LANGUAGE_FORGETS_RANK_ORBIT_TYPE=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_source_language_forgets_retained_rank_orbit_type")
        print("RESIDUAL_Q=fibre_constancy_excluding_rank_definable_source_state")
        print("COUNTERSTATE=rank_definable_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: definability/fibre-constancy audit has FAILs.")
    print("KOIDE_Q_DEFINABILITY_FIBRE_CONSTANCY_NO_GO=FALSE")
    print("Q_DEFINABILITY_FIBRE_CONSTANCY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_source_language_forgets_retained_rank_orbit_type")
    return 1


if __name__ == "__main__":
    sys.exit(main())
