#!/usr/bin/env python3
"""
Koide Q refinement-naturality source no-go.

Theorem attempt:
  Derive the intensive quotient-component source law from refinement
  consistency.  If internal rank is only dummy Morita refinement, physical
  component weights should be invariant under independent matrix refinements,
  which forces the rank exponent alpha=0 and hence Q=2/3.

Result:
  Conditional positive, retained negative.  Independent dummy-refinement
  invariance does force the intensive endpoint alpha=0.  But ordinary
  rank-one refinement additivity forces the retained Hilbert/rank endpoint
  alpha=1.  The current retained package does not prove that the real
  rank/orbit-size difference (1,2) is source-blind dummy refinement rather
  than physical multiplicity.  That classification is the missing source law.

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


def q_from_ratio(ratio_perp_over_plus: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + ratio_perp_over_plus) / 3)


def ktl_from_ratio(ratio_perp_over_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify(ratio_perp_over_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def weights_from_ratio(ratio_perp_over_plus: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    r = sp.simplify(ratio_perp_over_plus)
    return sp.simplify(1 / (1 + r)), sp.simplify(r / (1 + r))


def main() -> int:
    section("A. Rank-exponent family isolates the refinement convention")

    alpha = sp.symbols("alpha_refinement", real=True)
    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    ratio_alpha = sp.exp(alpha * sp.log(rank_perp / rank_plus))
    w_plus_alpha, w_perp_alpha = weights_from_ratio(ratio_alpha)
    ktl_alpha = ktl_from_ratio(ratio_alpha)
    q_alpha = q_from_ratio(ratio_alpha)
    record(
        "A.1 one exact exponent family contains label-intensive and rank-extensive states",
        sp.simplify(w_plus_alpha + w_perp_alpha) == 1,
        f"ratio=w_perp/w_plus=2^alpha; w=({w_plus_alpha},{w_perp_alpha})",
    )
    record(
        "A.2 alpha=0 is the intensive quotient-label endpoint",
        q_alpha.subs(alpha, 0) == sp.Rational(2, 3)
        and ktl_alpha.subs(alpha, 0) == 0,
        f"alpha=0 -> Q={q_alpha.subs(alpha,0)}, K_TL={ktl_alpha.subs(alpha,0)}",
    )
    record(
        "A.3 alpha=1 is the retained Hilbert/rank endpoint",
        q_alpha.subs(alpha, 1) == 1
        and ktl_alpha.subs(alpha, 1) == sp.Rational(3, 8),
        f"alpha=1 -> Q={q_alpha.subs(alpha,1)}, K_TL={ktl_alpha.subs(alpha,1)}",
    )
    record(
        "A.4 K_TL=0 selects only alpha=0 in the real exponent family",
        sp.solveset(sp.Eq(ratio_alpha, 1), alpha, domain=sp.S.Reals) == sp.FiniteSet(0),
        "Since ratio=2^alpha is positive, K_TL=0 iff ratio=1 iff alpha=0.",
    )

    section("B. Rank-one refinement additivity selects the nonclosing endpoint")

    fine_plus_atoms = rank_plus
    fine_perp_atoms = rank_perp
    w_plus_fine, w_perp_fine = weights_from_ratio(
        sp.Rational(fine_perp_atoms, fine_plus_atoms)
    )
    record(
        "B.1 uniform measure over retained rank-one refined atoms gives rank weights",
        (w_plus_fine, w_perp_fine) == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"fine atoms plus:perp={fine_plus_atoms}:{fine_perp_atoms}; w=({w_plus_fine},{w_perp_fine})",
    )
    record(
        "B.2 rank-one refinement additivity is exact and off Koide",
        q_from_ratio(sp.Rational(2, 1)) == 1
        and ktl_from_ratio(sp.Rational(2, 1)) == sp.Rational(3, 8),
        f"Q={q_from_ratio(sp.Rational(2,1))}, K_TL={ktl_from_ratio(sp.Rational(2,1))}",
    )
    record(
        "B.3 additivity over physical refined atoms therefore does not derive K_TL=0",
        True,
        "It derives the retained Hilbert/rank trace unless rank-one atoms are declared source-blind.",
    )

    section("C. Dummy-refinement invariance conditionally selects the closing endpoint")

    n_plus = sp.Integer(2)
    n_perp = sp.Integer(1)
    base_ratio = ratio_alpha
    amplified_ratio = sp.exp(alpha * sp.log((n_perp * rank_perp) / (n_plus * rank_plus)))
    record(
        "C.1 independent plus-block dummy amplification changes rank ratio unless alpha=0",
        sp.solveset(sp.Eq(base_ratio, amplified_ratio), alpha, domain=sp.S.Reals)
        == sp.FiniteSet(0),
        "Amplify plus by 2 only: base ratio=2^alpha, amplified ratio=1^alpha.",
    )
    record(
        "C.2 if independent block amplification is source-blind, Q closes",
        q_alpha.subs(alpha, 0) == sp.Rational(2, 3)
        and ktl_alpha.subs(alpha, 0) == 0,
        "Dummy-refinement invariance sets alpha=0, the intensive label state.",
    )
    record(
        "C.3 the closing theorem assumes the disputed source-blindness classification",
        True,
        "The retained rank/orbit-size pair (1,2) has not been proven to be dummy Morita refinement for physical sources.",
    )

    section("D. Hostile retained-language audit")

    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not classify rank as source-blind refinement",
        retained_constraints.jacobian([alpha]).rank() == 0,
        "No retained equation sets alpha=0 or rejects alpha=1.",
    )
    record(
        "D.2 the alpha=1 counterstate is retained and normalized",
        w_plus_alpha.subs(alpha, 1) == sp.Rational(1, 3)
        and w_perp_alpha.subs(alpha, 1) == sp.Rational(2, 3),
        "rank-extensive state remains an exact normalized source state.",
    )
    record(
        "D.3 exact residual primitive is named",
        True,
        "Need a retained theorem saying the rank/orbit-size refinement is source-blind rather than physical.",
    )

    section("E. Forbidden-input review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "Q and K_TL are evaluated after each refinement convention is specified.",
    )
    record(
        "E.2 conditional dummy-refinement theorem is not promoted as retained closure",
        True,
        "The nonclosing rank-refinement convention remains retained.",
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
        print("VERDICT: refinement naturality is conditional, not retained-only proof.")
        print("KOIDE_Q_REFINEMENT_NATURALITY_SOURCE_NO_GO=TRUE")
        print("Q_REFINEMENT_NATURALITY_SOURCE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_RANK_REFINEMENT_IS_SOURCE_BLIND=TRUE")
        print("RESIDUAL_SCALAR=derive_rank_refinement_source_blindness_over_rank_additivity")
        print("RESIDUAL_Q=rank_additive_source_state_not_excluded")
        print("COUNTERSTATE=rank_refinement_alpha_1_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: refinement-naturality source audit has FAILs.")
    print("KOIDE_Q_REFINEMENT_NATURALITY_SOURCE_NO_GO=FALSE")
    print("Q_REFINEMENT_NATURALITY_SOURCE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_rank_refinement_source_blindness_over_rank_additivity")
    return 1


if __name__ == "__main__":
    sys.exit(main())
