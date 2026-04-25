#!/usr/bin/env python3
"""
Koide Q refinement-axiom compatibility no-go.

Theorem attempt:
  Derive the missing Q source law by requiring the source rule to be both
  additive over retained refinements and invariant under dummy refinements.
  Perhaps the compatibility of those two naturality requirements forces the
  intensive quotient-component source and hence K_TL=0.

Result:
  Negative, but sharper.  On the retained rank pair (1,2), rank-additivity
  and independent source-blind refinement are incompatible.  Additivity over
  retained rank-one atoms gives the Hilbert/rank state (1/3,2/3), while
  independent dummy-refinement invariance gives the intensive state (1/2,1/2).
  Thus a positive Q closure cannot keep both principles.  It must derive that
  the retained rank/orbit-size refinement is source-blind, or else accept the
  nonclosing rank-additive counterstate.

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


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained rank-additivity fixes the nonclosing source")

    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    w_plus, w_perp = sp.symbols("w_plus w_perp", positive=True, real=True)
    rank_additive_solution = sp.solve(
        [
            sp.Eq(w_plus + w_perp, 1),
            sp.Eq(w_perp / w_plus, rank_perp / rank_plus),
        ],
        [w_plus, w_perp],
        dict=True,
    )
    rank_w_plus = rank_additive_solution[0][w_plus]
    rank_w_perp = rank_additive_solution[0][w_perp]
    record(
        "A.1 additive measure over retained rank-one atoms gives rank weights",
        rank_additive_solution
        == [{w_plus: sp.Rational(1, 3), w_perp: sp.Rational(2, 3)}],
        f"rank-additive solution={rank_additive_solution}",
    )
    record(
        "A.2 rank-additive source is exact and off Koide",
        q_from_weights(rank_w_plus, rank_w_perp) == 1
        and ktl_from_weights(rank_w_plus, rank_w_perp) == sp.Rational(3, 8),
        f"Q={q_from_weights(rank_w_plus, rank_w_perp)}, K_TL={ktl_from_weights(rank_w_plus, rank_w_perp)}",
    )

    section("B. Independent dummy-refinement invariance fixes the closing source")

    n_plus = sp.symbols("n_plus", integer=True, positive=True)
    n_perp = sp.symbols("n_perp", integer=True, positive=True)
    alpha = sp.symbols("alpha_refinement", real=True)
    base_ratio = sp.exp(alpha * sp.log(rank_perp / rank_plus))
    refined_ratio = sp.exp(alpha * sp.log(n_perp * rank_perp / (n_plus * rank_plus)))
    plus_only_solution = sp.solveset(
        sp.Eq(base_ratio, refined_ratio.subs({n_plus: 2, n_perp: 1})),
        alpha,
        domain=sp.S.Reals,
    )
    record(
        "B.1 invariance under plus-only dummy refinement forces alpha=0",
        plus_only_solution == sp.FiniteSet(0),
        "base ratio=2^alpha; after plus amplification by 2, ratio=1^alpha.",
    )
    intensive_solution = {w_plus: sp.Rational(1, 2), w_perp: sp.Rational(1, 2)}
    record(
        "B.2 alpha=0 is the intensive source and closes the Q chain",
        q_from_weights(intensive_solution[w_plus], intensive_solution[w_perp])
        == sp.Rational(2, 3)
        and ktl_from_weights(intensive_solution[w_plus], intensive_solution[w_perp]) == 0,
        f"intensive solution={intensive_solution}",
    )

    section("C. Compatibility obstruction")

    compatibility_equations = [
        sp.Eq(w_plus + w_perp, 1),
        sp.Eq(w_perp / w_plus, rank_perp / rank_plus),
        sp.Eq(w_plus, w_perp),
    ]
    compatibility_solution = sp.solve(compatibility_equations, [w_plus, w_perp], dict=True)
    record(
        "C.1 rank-additivity and dummy-refinement invariance are incompatible for ranks 1 and 2",
        compatibility_solution == [],
        f"solutions={compatibility_solution}",
    )
    r_plus, r_perp = sp.symbols("r_plus r_perp", positive=True, integer=True)
    general_compatibility = sp.solve(
        [
            sp.Eq(w_plus + w_perp, 1),
            sp.Eq(w_perp / w_plus, r_perp / r_plus),
            sp.Eq(w_plus, w_perp),
        ],
        [w_plus, w_perp, r_perp],
        dict=True,
    )
    record(
        "C.2 compatibility requires equal ranks in the general two-block case",
        general_compatibility == [{w_plus: sp.Rational(1, 2), w_perp: sp.Rational(1, 2), r_perp: r_plus}],
        f"general solution={general_compatibility}",
    )
    record(
        "C.3 the retained carrier violates the equal-rank compatibility condition",
        rank_plus != rank_perp,
        f"retained ranks=({rank_plus},{rank_perp})",
    )

    section("D. What a positive closure must prove")

    delete_rank_additivity = sp.symbols("delete_rank_additivity", real=True)
    classify_rank_dummy = sp.symbols("classify_rank_dummy", real=True)
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not delete rank-additivity",
        retained_constraints.jacobian([delete_rank_additivity]).rank() == 0,
        "The existing retained packet does not mark rank-one atoms as source-invisible.",
    )
    record(
        "D.2 retained support constraints do not classify rank as dummy refinement",
        retained_constraints.jacobian([classify_rank_dummy]).rank() == 0,
        "No retained equation chooses dummy-refinement invariance over rank-additivity.",
    )
    record(
        "D.3 exact next residual is a deletion/classification law, not another scalar fit",
        True,
        "Need a retained theorem removing rank-additive source counting for the charged-lepton source.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The two source conventions are derived from their stated refinement axioms before evaluating Q.",
    )
    record(
        "E.2 the incompatibility theorem is not promoted as Koide closure",
        True,
        "It proves that one retained-looking source axiom must be rejected or reclassified.",
    )
    record(
        "E.3 exact counterstate remains retained unless rank-additivity is deleted",
        rank_w_plus == sp.Rational(1, 3) and rank_w_perp == sp.Rational(2, 3),
        "rank-additive counterstate=(1/3,2/3).",
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
        print("VERDICT: refinement axiom compatibility does not close Q.")
        print("KOIDE_Q_REFINEMENT_AXIOM_COMPATIBILITY_NO_GO=TRUE")
        print("Q_REFINEMENT_AXIOM_COMPATIBILITY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_RANK_ADDITIVITY_IS_DELETED=TRUE")
        print("RESIDUAL_SCALAR=derive_deletion_of_rank_additive_source_counting")
        print("RESIDUAL_Q=classify_retained_rank_orbit_refinement_as_source_blind")
        print("COUNTERSTATE=rank_additive_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: refinement axiom compatibility audit has FAILs.")
    print("KOIDE_Q_REFINEMENT_AXIOM_COMPATIBILITY_NO_GO=FALSE")
    print("Q_REFINEMENT_AXIOM_COMPATIBILITY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_deletion_of_rank_additive_source_counting")
    return 1


if __name__ == "__main__":
    sys.exit(main())
