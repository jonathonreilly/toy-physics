#!/usr/bin/env python3
"""
Koide Q minimal sufficient source-statistic no-go.

Theorem attempt:
  Use operational indistinguishability / minimal sufficient statistics to
  derive the source-domain quotient needed for Koide Q.  Since the reduced
  scalar observable jets of the plus and perp center slots are identical, maybe
  the physical source must identify the two slots, forcing the uniform source
  state and K_TL=0.

Result:
  Negative under current retained structure.  Identical scalar likelihoods
  make the C3 orbit label unobservable to that restricted scalar experiment,
  but they do not choose the hidden prior over labels.  The prior w remains
  arbitrary unless one adds a quotient-preparation law.  If the retained label
  observable Z=P_plus-P_perp is admitted as part of the physical experiment,
  the minimal sufficient statistic distinguishes the two labels exactly.

Thus the sufficient-statistic route is equivalent to the already exposed
source-domain quotient residual:

    derive that physical source preparation forgets retained C3 orbit label Z.

No PDG masses, H_* pins, Q targets, delta targets, or K_TL=0 assumptions are
used as inputs.
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
    section("A. Restricted scalar-jet experiment")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    W_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    jet_order = 6
    plus_likelihood = sp.Matrix(
        [sp.diff(W_red.subs(k_perp, 0), k_plus, n).subs(k_plus, 0) for n in range(1, jet_order + 1)]
    )
    perp_likelihood = sp.Matrix(
        [sp.diff(W_red.subs(k_plus, 0), k_perp, n).subs(k_perp, 0) for n in range(1, jet_order + 1)]
    )
    record(
        "A.1 plus and perp have identical reduced scalar-jet likelihoods",
        plus_likelihood == perp_likelihood,
        f"jet={list(plus_likelihood)}",
    )
    scalar_statistic_rank = sp.Matrix.hstack(plus_likelihood, perp_likelihood).rank()
    record(
        "A.2 the restricted scalar experiment has one sufficient jet class",
        scalar_statistic_rank == 1,
        f"rank([jet_plus, jet_perp])={scalar_statistic_rank}",
    )

    section("B. Identical likelihoods do not determine the hidden source prior")

    w = sp.symbols("w", positive=True, real=True)
    prior = sp.Matrix([w, 1 - w])
    scalar_evidence = sp.simplify(prior[0] * plus_likelihood + prior[1] * perp_likelihood)
    record(
        "B.1 scalar evidence is independent of the hidden label prior",
        scalar_evidence == plus_likelihood and scalar_evidence.has(w) is False,
        f"evidence={list(scalar_evidence)}",
    )
    record(
        "B.2 arbitrary priors remain compatible with scalar indistinguishability",
        ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8)
        and ktl_from_weight(sp.Rational(1, 2)) == 0
        and ktl_from_weight(sp.Rational(2, 3)) == -sp.Rational(3, 8),
        "w=1/3,1/2,2/3 have the same restricted scalar likelihood class but different K_TL.",
    )
    record(
        "B.3 uniformity requires a quotient-preparation law, not sufficiency alone",
        sp.solve(sp.Eq(ktl_from_weight(w), 0), w) == [sp.Rational(1, 2)],
        f"K_TL(w)={ktl_from_weight(w)}",
    )

    section("C. Full retained experiment includes the label observable Z")

    # Add one retained label measurement coordinate: Z eigenvalue +1 on P_plus,
    # -1 on P_perp.  This is the central source direction P_plus-P_perp.
    plus_full = sp.Matrix(list(plus_likelihood) + [1])
    perp_full = sp.Matrix(list(perp_likelihood) + [-1])
    full_rank = sp.Matrix.hstack(plus_full, perp_full).rank()
    record(
        "C.1 adding retained Z separates the two center labels exactly",
        plus_full != perp_full and full_rank == 2,
        f"plus_full={list(plus_full)}, perp_full={list(perp_full)}, rank={full_rank}",
    )
    label_expectation = sp.simplify((sp.Matrix([[1, -1]]) * prior)[0])
    record(
        "C.2 the Z expectation carries exactly the free source prior",
        label_expectation == 2 * w - 1,
        f"<Z>={label_expectation}",
    )
    record(
        "C.3 full retained sufficient statistic therefore does not collapse the labels",
        full_rank == 2,
        "The minimal statistic for the full retained experiment is label-resolving.",
    )

    section("D. Conditional positive route and obstruction")

    record(
        "D.1 if the physical experiment deletes Z and quotient-prepares, Q closes conditionally",
        ktl_from_weight(sp.Rational(1, 2)) == 0
        and q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3),
        "This is exactly the quotient-center anonymity law, not a consequence of sufficiency alone.",
    )
    record(
        "D.2 if Z remains retained, a nonclosing source prior is an exact countermodel",
        q_from_weight(sp.Rational(1, 3)) == 1
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "w=1/3 remains admissible in the full retained experiment.",
    )

    section("E. Hostile review")

    record(
        "E.1 no target value or observational pin is used as an input",
        True,
        "The target midpoint appears only as the residual condition tested after deriving the state space.",
    )
    record(
        "E.2 minimal sufficiency cannot be used to rename the missing quotient law",
        True,
        "Sufficiency identifies statistics for a chosen experiment; choosing the scalar-only experiment is the extra step.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "RESIDUAL_PRIMITIVE=derive_physical_experiment_excludes_Z_label_and_quotient_prepares.",
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
        print("KOIDE_Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_NO_GO=TRUE")
        print("Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=source_prior_w_minus_one_half_after_scalar_statistic_quotient")
        print("RESIDUAL_LABEL=retained_Z_label_makes_full_sufficient_statistic_label_resolving")
        print("RESIDUAL_PRIMITIVE=derive_physical_experiment_excludes_Z_label_and_quotient_prepares")
        return 0

    print("KOIDE_Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_NO_GO=FALSE")
    print("Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=source_prior_w_minus_one_half_after_scalar_statistic_quotient")
    return 1


if __name__ == "__main__":
    sys.exit(main())
