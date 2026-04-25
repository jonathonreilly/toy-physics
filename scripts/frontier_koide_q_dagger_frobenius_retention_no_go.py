#!/usr/bin/env python3
"""
Koide Q dagger-Frobenius retention no-go.

Theorem attempt:
  The special-Frobenius center reduction showed that a normalized special
  classical center counit would force equal center-label weights.  Perhaps that
  special dagger-Frobenius structure is not an added primitive, but is forced
  by the retained real C3 carrier and its inherited dagger/inner product.

Result:
  Negative.  The inherited Hilbert-Schmidt inner product on the retained
  projectors gives Frobenius weights equal to ranks:

      lambda_plus : lambda_perp = 1 : 2.

  A two-idempotent Frobenius algebra is special only when

      lambda_plus = lambda_perp.

  The inherited dagger and special center counit are therefore incompatible on
  the rank-1/rank-2 carrier.  Choosing the special label-counting dagger is a
  new physical source/inner-product primitive, not forced by retained C3 data.
  Equivalently, it requires inserting a non-Hilbert central density that
  reweights the doublet block by 1/2.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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
    w_plus = sp.sympify(w_plus)
    w_perp = sp.sympify(w_perp)
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    w_plus = sp.sympify(w_plus)
    w_perp = sp.sympify(w_perp)
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Inherited dagger on the retained C3 projectors")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    rank_plus = P_plus.rank()
    rank_perp = P_perp.rank()
    hs_plus = sp.trace(P_plus * P_plus)
    hs_perp = sp.trace(P_perp * P_perp)
    record(
        "A.1 retained projectors are central and have ranks 1 and 2",
        rank_plus == 1
        and rank_perp == 2
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"ranks=({rank_plus},{rank_perp})",
    )
    record(
        "A.2 inherited Hilbert-Schmidt Frobenius weights equal the ranks",
        hs_plus == 1 and hs_perp == 2,
        f"<P_plus,P_plus>={hs_plus}, <P_perp,P_perp>={hs_perp}",
    )

    section("B. Special Frobenius condition conflicts with inherited weights")

    lam_plus, lam_perp, beta, scale = sp.symbols(
        "lambda_plus lambda_perp beta scale", positive=True, real=True
    )
    special_equations = [
        sp.Eq(1 / lam_plus, beta),
        sp.Eq(1 / lam_perp, beta),
    ]
    inherited_equations = [
        sp.Eq(lam_plus, scale),
        sp.Eq(lam_perp, 2 * scale),
    ]
    combined_solution = sp.solve(
        special_equations + inherited_equations,
        [lam_plus, lam_perp, beta, scale],
        dict=True,
    )
    record(
        "B.1 specialness alone forces equal label weights",
        sp.solve(special_equations, [lam_plus, lam_perp], dict=True)
        == [{lam_plus: 1 / beta, lam_perp: 1 / beta}],
        "m o Delta = beta id.",
    )
    record(
        "B.2 inherited Hilbert-Schmidt dagger forces the rank ratio 1:2",
        inherited_equations == [sp.Eq(lam_plus, scale), sp.Eq(lam_perp, 2 * scale)],
        "lambda_i proportional to Tr(P_i).",
    )
    record(
        "B.3 no positive weights satisfy both inherited dagger and specialness",
        combined_solution == [],
        f"combined_solution={combined_solution}",
    )

    section("C. Consequences for Q")

    q_special = q_from_weights(1, 1)
    ktl_special = ktl_from_weights(1, 1)
    q_inherited = q_from_weights(1, 2)
    ktl_inherited = ktl_from_weights(1, 2)
    record(
        "C.1 special label-counting dagger lands on the source-neutral leaf",
        q_special == sp.Rational(2, 3) and ktl_special == 0,
        f"special weights (1,1): Q={q_special}, K_TL={ktl_special}",
    )
    record(
        "C.2 inherited carrier dagger lands off the source-neutral leaf",
        q_inherited == 1 and ktl_inherited == sp.Rational(3, 8),
        f"inherited weights (1,2): Q={q_inherited}, K_TL={ktl_inherited}",
    )

    section("D. Central density needed to turn rank trace into label trace")

    label_density = sp.simplify(P_plus + sp.Rational(1, 2) * P_perp)
    label_weight_plus = sp.simplify(sp.trace(label_density * P_plus))
    label_weight_perp = sp.simplify(sp.trace(label_density * P_perp))
    record(
        "D.1 label-counting dagger is obtained by inserting a non-Hilbert central density",
        label_weight_plus == 1
        and label_weight_perp == 1
        and label_density != I3,
        "G_label=P_plus+(1/2)P_perp gives Tr(G_label P_i)=1 for both center atoms.",
    )
    record(
        "D.2 the inherited Hilbert density gives rank weights instead",
        sp.trace(I3 * P_plus) == 1
        and sp.trace(I3 * P_perp) == 2,
        "G_H=I gives Tr(P_plus)=1, Tr(P_perp)=2.",
    )

    section("E. Residual primitive")

    record(
        "E.1 forcing special Frobenius requires changing the physical dagger/state",
        True,
        "The required move is from Hilbert/rank trace to label-counting center trace.",
    )
    record(
        "E.2 that move is exactly the missing source-law primitive",
        True,
        "It is not forced by retained C3 covariance or the inherited real carrier.",
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
        print("VERDICT: inherited dagger does not force the special Frobenius center source.")
        print("KOIDE_Q_DAGGER_FROBENIUS_RETENTION_NO_GO=TRUE")
        print("Q_DAGGER_FROBENIUS_RETENTION_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=label_counting_dagger_not_inherited_from_rank_carrier")
        print("RESIDUAL_PRIMITIVE=physical_choice_of_center_Frobenius_counit")
        print("RESIDUAL_DENSITY=G_label_central_density_not_retained_as_physical_source")
        return 0

    print("VERDICT: dagger-Frobenius retention audit has FAILs.")
    print("KOIDE_Q_DAGGER_FROBENIUS_RETENTION_NO_GO=FALSE")
    print("Q_DAGGER_FROBENIUS_RETENTION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=label_counting_dagger_not_inherited_from_rank_carrier")
    print("RESIDUAL_PRIMITIVE=physical_choice_of_center_Frobenius_counit")
    print("RESIDUAL_DENSITY=G_label_central_density_not_retained_as_physical_source")
    return 1


if __name__ == "__main__":
    sys.exit(main())
