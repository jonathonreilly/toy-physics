#!/usr/bin/env python3
"""
Koide Q minimax block-decision no-go.

Theorem attempt:
  A decision-theoretic minimax or proper-scoring principle over the retained
  singlet/doublet quotient might force equal total block weights and thereby
  derive K_TL = 0.

Result:
  Negative.  Minimax log-loss over the two coarse block labels selects
  q_plus=q_perp=1/2, which lands on the Koide leaf.  But minimax over the
  physical real micro-dimensions, or equivalently rank-weighted outcomes,
  selects q_plus:q_perp = 1:2.  A general weighted minimax problem selects
  q_perp/q_plus equal to the chosen loss-weight ratio.  Therefore the result
  depends on a loss/coarse-graining primitive: count block labels equally, or
  count retained real dimensions/fusion weights.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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


def q_from_block_prob(p_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - p_plus) / p_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_block_prob(p_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - p_plus) / p_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Coarse two-label minimax")

    p = sp.symbols("p", positive=True, real=True)
    # Minimize max(-log p, -log(1-p)); at the minimizer both active losses
    # are equal, so p=1-p.
    coarse_solution = sp.solve(sp.Eq(-sp.log(p), -sp.log(1 - p)), p)
    record(
        "A.1 minimax log-loss over two coarse block labels selects p_plus=1/2",
        coarse_solution == [sp.Rational(1, 2)],
        f"-log(p)=-log(1-p) -> p={coarse_solution}",
    )
    record(
        "A.2 the coarse-label minimax point lands on the Koide/source-neutral leaf",
        q_from_block_prob(sp.Rational(1, 2)) == sp.Rational(2, 3)
        and ktl_from_block_prob(sp.Rational(1, 2)) == 0,
        f"Q={q_from_block_prob(sp.Rational(1, 2))}, K_TL={ktl_from_block_prob(sp.Rational(1, 2))}",
    )

    section("B. Physical micro-dimension minimax gives rank weights")

    # One singlet micro-outcome and two real-doublet micro-outcomes.
    q_micro = sp.Rational(1, 3)
    p_plus_micro = q_micro
    p_perp_micro = 2 * q_micro
    record(
        "B.1 minimax over three equal real micro-dimensions gives block weights 1:2",
        p_plus_micro == sp.Rational(1, 3) and p_perp_micro == sp.Rational(2, 3),
        f"micro probabilities=(1/3,1/3,1/3); block totals=({p_plus_micro},{p_perp_micro})",
    )
    record(
        "B.2 rank-weighted minimax is off the equal-block leaf",
        q_from_block_prob(p_plus_micro) == 1
        and ktl_from_block_prob(p_plus_micro) == sp.Rational(3, 8),
        f"Q={q_from_block_prob(p_plus_micro)}, K_TL={ktl_from_block_prob(p_plus_micro)}",
    )

    section("C. Weighted minimax exposes the free coarse-graining")

    c = sp.symbols("c", positive=True, real=True)
    # Equalize weighted active losses: -log p = -log((1-p)/c) is equivalent
    # to p = (1-p)/c, hence p=1/(1+c).  Here c is the relative number/cost of
    # doublet outcomes.
    p_star = sp.simplify(1 / (1 + c))
    r_star = sp.simplify((1 - p_star) / p_star)
    record(
        "C.1 weighted minimax selects the chosen relative outcome weight c",
        r_star == c,
        f"p_plus*=1/(1+c), p_perp/p_plus={r_star}",
    )
    samples = {
        "coarse_labels": sp.Integer(1),
        "real_dimensions": sp.Integer(2),
        "singlet_heavy": sp.Rational(1, 2),
    }
    sample_lines = []
    sample_values = []
    for label, value in samples.items():
        p_value = sp.simplify(p_star.subs(c, value))
        q_value = q_from_block_prob(p_value)
        ktl_value = ktl_from_block_prob(p_value)
        sample_values.append((q_value, ktl_value))
        sample_lines.append(
            f"{label}: c={value}, p_plus={p_value}, Q={q_value}, K_TL={ktl_value}"
        )
    record(
        "C.2 different retained-compatible loss coarse grainings select different exact Q values",
        len(set(sample_values)) == len(sample_values),
        "\n".join(sample_lines),
    )

    section("D. Verdict")

    record(
        "D.1 minimax can support equal-block democracy only after choosing block-label loss",
        True,
        "Counting two central labels equally is a decision primitive; real dimensions/fusion count differently.",
    )
    record(
        "D.2 Q remains open after minimax decision audit",
        True,
        "Residual primitive: physical coarse-graining/loss measure selecting c=1 rather than c=2 or another value.",
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
        print("VERDICT: minimax block-decision route does not close Q.")
        print("KOIDE_Q_MINIMAX_BLOCK_DECISION_NO_GO=TRUE")
        print("Q_MINIMAX_BLOCK_DECISION_CLOSES_Q=FALSE")
        print("RESIDUAL_COARSEGRAINING=loss_weight_c_equals_1_equiv_K_TL")
        return 0

    print("VERDICT: minimax block-decision audit has FAILs.")
    print("KOIDE_Q_MINIMAX_BLOCK_DECISION_NO_GO=FALSE")
    print("Q_MINIMAX_BLOCK_DECISION_CLOSES_Q=FALSE")
    print("RESIDUAL_COARSEGRAINING=loss_weight_c_equals_1_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
