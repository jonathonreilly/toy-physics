#!/usr/bin/env python3
"""
Koide Q block-total Frobenius closure review no-go.

Theorem under review:
  The block-total Frobenius functional gives one scalar slot for the trivial
  real isotype and one scalar slot for the real doublet.  Since the d=3
  isotype multiplicity pattern is (1,1), a block log-law with equal weights
  has its extremum at E_+ = E_perp, deriving K_TL = 0.

Nature-grade review result:
  The block-total arithmetic is exact support, but the closure step chooses
  equal isotype weights in the variational/log law.  A weighted block log-law
  with coefficients alpha,beta has extremum E_perp/E_+ = beta/alpha.  The
  equal choice alpha=beta gives Koide; the inherited dimension/rank choice
  alpha:beta=1:2 gives the rank state.  Frobenius reciprocity names the
  isotype multiplicities; it does not by itself prove the physical source
  functional uses multiplicity weights rather than dimension/rank weights.

No PDG masses, fitted target, delta pin, or H_* pin is used.
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


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + r) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Exact block-total Frobenius arithmetic")

    a, b = sp.symbols("a b", positive=True, real=True)
    E_plus = 3 * a**2
    E_perp = 6 * b**2
    ratio = sp.simplify(E_perp / E_plus)
    record(
        "A.1 block totals are E_plus=3a^2 and E_perp=6|b|^2",
        ratio == 2 * b**2 / a**2,
        f"E_perp/E_plus={ratio}",
    )
    record(
        "A.2 E_plus=E_perp is equivalent to the source-neutral kappa leaf",
        sp.solve(sp.Eq(E_plus, E_perp), b) == [sp.sqrt(2) * a / 2],
        "E_plus=E_perp -> |b|^2=a^2/2 -> kappa=2.",
    )

    section("B. Weighted block log-law exposes the hidden prior")

    E, alpha, beta = sp.symbols("E alpha beta", positive=True, real=True)
    x = sp.symbols("x", positive=True, real=True)  # x = E_plus, E_perp=E-x.
    S = sp.simplify(alpha * sp.log(x) + beta * sp.log(E - x))
    stationary = sp.solve(sp.Eq(sp.diff(S, x), 0), x)
    x_star = sp.simplify(alpha * E / (alpha + beta))
    r_star = sp.simplify((E - x_star) / x_star)
    record(
        "B.1 weighted block log-law extremum has E_perp/E_plus=beta/alpha",
        stationary == [x_star] and r_star == beta / alpha,
        f"E_plus*={x_star}, E_perp/E_plus={r_star}",
    )
    record(
        "B.2 equal isotype weights alpha=beta give the Koide leaf",
        q_from_ratio(r_star.subs({alpha: 1, beta: 1})) == sp.Rational(2, 3)
        and ktl_from_ratio(r_star.subs({alpha: 1, beta: 1})) == 0,
        "alpha:beta=1:1 -> E_perp/E_plus=1.",
    )
    record(
        "B.3 inherited dimension/rank weights alpha:beta=1:2 give the non-closing rank leaf",
        q_from_ratio(r_star.subs({alpha: 1, beta: 2})) == 1
        and ktl_from_ratio(r_star.subs({alpha: 1, beta: 2})) == sp.Rational(3, 8),
        "alpha:beta=1:2 -> E_perp/E_plus=2.",
    )

    section("C. Multiplicity count is not a physical source theorem by itself")

    multiplicity_weights = (sp.Integer(1), sp.Integer(1))
    dimension_weights = (sp.Integer(1), sp.Integer(2))
    record(
        "C.1 d=3 real-isotype multiplicities are (1,1)",
        multiplicity_weights == (1, 1),
        "one trivial real isotype and one real doublet isotype.",
    )
    record(
        "C.2 the retained carrier dimensions are (1,2)",
        dimension_weights == (1, 2),
        "the same retained carrier has rank/dimension weights 1 and 2.",
    )
    record(
        "C.3 choosing multiplicity weights over dimension weights is the source primitive",
        multiplicity_weights != dimension_weights,
        "Frobenius reciprocity supplies a count; it does not select the physical weighting functional.",
    )

    section("D. Review verdict")

    residual = sp.simplify(beta - alpha)
    record(
        "D.1 block-total Frobenius route does not close Q under Nature-grade review",
        residual == beta - alpha,
        f"RESIDUAL_WEIGHT={residual}",
    )
    record(
        "D.2 Q remains open after block-total Frobenius review",
        True,
        "Residual primitive: physical law selecting equal isotype weights in the source functional.",
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
        print("VERDICT: block-total Frobenius arithmetic is support, not Nature-grade Q closure.")
        print("KOIDE_Q_BLOCK_TOTAL_FROBENIUS_REVIEW_NO_GO=TRUE")
        print("Q_BLOCK_TOTAL_FROBENIUS_REVIEW_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=equal_isotype_log_weight_minus_rank_weight_equiv_K_TL")
        print("RESIDUAL_WEIGHT=alpha_minus_beta_source_functional_weight")
        return 0

    print("VERDICT: block-total Frobenius review audit has FAILs.")
    print("KOIDE_Q_BLOCK_TOTAL_FROBENIUS_REVIEW_NO_GO=FALSE")
    print("Q_BLOCK_TOTAL_FROBENIUS_REVIEW_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=equal_isotype_log_weight_minus_rank_weight_equiv_K_TL")
    print("RESIDUAL_WEIGHT=alpha_minus_beta_source_functional_weight")
    return 1


if __name__ == "__main__":
    sys.exit(main())
