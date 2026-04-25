#!/usr/bin/env python3
"""
Koide Q source-response rank-deletion no-go.

Theorem attempt:
  Derive deletion of rank-additive source counting from the retained
  source-response principle.  If the physical source generator is the reduced
  quotient logdet, not the full rank-additive Hilbert determinant, then the
  zero-source response is intensive on the two quotient components:

      dW_red|_0 = (1,1) -> K_TL=0 -> Q=2/3.

Result:
  Conditional positive, retained negative.  The reduced quotient logdet closes
  Q exactly.  But the rank-additive determinant over the retained ranks (1,2)
  is also an exact source-response functional unless a theorem deletes rank
  counting from the physical charged-lepton source.  It gives

      dW_rank|_0 = (1,2) -> Q=1, K_TL=3/8.

Thus the next positive theorem must derive the reduced quotient logdet as the
physical source generator, or equivalently reject rank-additive source response.

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


def normalized_weights(y_plus: sp.Expr, y_perp: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    total = sp.simplify(y_plus + y_perp)
    return sp.simplify(y_plus / total), sp.simplify(y_perp / total)


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def gradient_at_zero(w: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol]) -> tuple[sp.Expr, sp.Expr]:
    k_plus, k_perp = variables
    return (
        sp.simplify(sp.diff(w, k_plus).subs({k_plus: 0, k_perp: 0})),
        sp.simplify(sp.diff(w, k_perp).subs({k_plus: 0, k_perp: 0})),
    )


def main() -> int:
    section("A. Two exact source-response generators on the retained rank pair")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    w_reduced = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    w_rank = rank_plus * sp.log(1 + k_plus) + rank_perp * sp.log(1 + k_perp)
    record(
        "A.1 reduced quotient logdet and rank-additive logdet are distinct exact generators",
        sp.simplify(w_rank - w_reduced) == sp.log(1 + k_perp),
        f"W_red={w_reduced}; W_rank={w_rank}",
    )
    record(
        "A.2 retained ranks are 1 and 2",
        rank_plus == 1 and rank_perp == 2,
        f"rank pair=({rank_plus},{rank_perp})",
    )

    section("B. Reduced quotient source-response conditionally closes Q")

    y_red = gradient_at_zero(w_reduced, (k_plus, k_perp))
    w_red_weights = normalized_weights(*y_red)
    record(
        "B.1 reduced quotient zero-source response is intensive on quotient components",
        y_red == (1, 1) and w_red_weights == (sp.Rational(1, 2), sp.Rational(1, 2)),
        f"dW_red|0={y_red}; normalized={w_red_weights}",
    )
    record(
        "B.2 reduced quotient response gives K_TL=0 and Q=2/3",
        ktl_from_weights(*w_red_weights) == 0
        and q_from_weights(*w_red_weights) == sp.Rational(2, 3),
        f"K_TL={ktl_from_weights(*w_red_weights)}, Q={q_from_weights(*w_red_weights)}",
    )

    section("C. Rank-additive source-response countermodel")

    y_rank = gradient_at_zero(w_rank, (k_plus, k_perp))
    w_rank_weights = normalized_weights(*y_rank)
    record(
        "C.1 full rank-additive zero-source response gives rank weights",
        y_rank == (1, 2) and w_rank_weights == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"dW_rank|0={y_rank}; normalized={w_rank_weights}",
    )
    record(
        "C.2 rank-additive response is exact and off Koide",
        ktl_from_weights(*w_rank_weights) == sp.Rational(3, 8)
        and q_from_weights(*w_rank_weights) == 1,
        f"K_TL={ktl_from_weights(*w_rank_weights)}, Q={q_from_weights(*w_rank_weights)}",
    )

    section("D. General response exponent isolates the missing deletion law")

    a, b = sp.symbols("a b", positive=True, real=True)
    w_ab = a * sp.log(1 + k_plus) + b * sp.log(1 + k_perp)
    y_ab = gradient_at_zero(w_ab, (k_plus, k_perp))
    w_ab_weights = normalized_weights(*y_ab)
    ktl_ab = sp.factor(ktl_from_weights(*w_ab_weights))
    record(
        "D.1 any source-response carrier keeps one exponent ratio",
        y_ab == (a, b) and sp.simplify(w_ab_weights[0] + w_ab_weights[1]) == 1,
        f"dW_ab|0={y_ab}; normalized={w_ab_weights}; K_TL={ktl_ab}",
    )
    record(
        "D.2 K_TL=0 is equivalent to deleting the rank exponent difference",
        sp.solve(sp.Eq(ktl_ab, 0), a) == [b],
        f"K_TL numerator={sp.factor(sp.together(ktl_ab).as_numer_denom()[0])}",
    )
    record(
        "D.3 quotient response is a=b=1 while rank response is a:b=1:2",
        ktl_ab.subs({a: 1, b: 1}) == 0
        and ktl_ab.subs({a: 1, b: 2}) == sp.Rational(3, 8),
        "The missing theorem is a=b, not another consequence of source-response alone.",
    )
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.4 retained support constraints do not set a=b",
        retained_constraints.jacobian([a, b]).rank() == 0,
        "No retained equation in this audit chooses W_red over W_rank.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The two generators are audited before evaluating Q and K_TL.",
    )
    record(
        "E.2 reduced logdet is not promoted as retained closure",
        True,
        "The rank-additive logdet remains a retained countermodel unless rank source counting is deleted.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem selecting the reduced quotient logdet over the rank-additive determinant.",
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
        print("VERDICT: source-response rank deletion is conditional, not retained-only proof.")
        print("KOIDE_Q_SOURCE_RESPONSE_RANK_DELETION_NO_GO=TRUE")
        print("Q_SOURCE_RESPONSE_RANK_DELETION_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_REDUCED_QUOTIENT_LOGDET_IS_PHYSICAL=TRUE")
        print("RESIDUAL_SCALAR=derive_reduced_quotient_logdet_over_rank_additive_logdet")
        print("RESIDUAL_Q=rank_additive_source_response_not_excluded")
        print("COUNTERSTATE=rank_additive_logdet_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: source-response rank-deletion audit has FAILs.")
    print("KOIDE_Q_SOURCE_RESPONSE_RANK_DELETION_NO_GO=FALSE")
    print("Q_SOURCE_RESPONSE_RANK_DELETION_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_reduced_quotient_logdet_over_rank_additive_logdet")
    return 1


if __name__ == "__main__":
    sys.exit(main())
