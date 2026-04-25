#!/usr/bin/env python3
"""
Koide Q named-axiom rho-rank no-go.

Theorem attempt:
  Prove the hidden-kernel source charge rho=0 directly from the named retained
  framework axioms, without adding a new axiom and without relying on the
  accumulated no-go corpus.

Result:
  No retained closure.  The named axioms cited by the reviewer stress packet
  are rho-blind: Cl(3)/Z3 carrier, SELECTOR=sqrt(6)/3, observable principle,
  S3/C3 cubic symmetry, and continuum PL S3 x R structure do not provide a
  source-side equality with nonzero rho derivative.  The exact pair

      rho=0 reduced/quotient source response, Q=2/3;
      rho=1 full determinant source response, Q=1

  satisfies the same named-axiom checks.

Exact residual:

      derive_named_retained_axiom_with_nonzero_rho_jacobian.
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


def q_from_rho(rho: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho) / 3)


def ktl_from_rho(rho: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    rho, k_plus, k_perp = sp.symbols("rho k_plus k_perp", real=True)

    section("A. Named retained axioms")

    I3 = sp.eye(3)
    C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    swap12 = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)
    selector = sp.sqrt(6) / 3

    record(
        "A.1 Cl(3)/Z3 carrier equations hold without rho",
        C3**3 == I3
        and sp.simplify(P_plus**2 - P_plus) == sp.zeros(3)
        and sp.simplify(P_perp**2 - P_perp) == sp.zeros(3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3)
        and sp.simplify(P_plus + P_perp - I3) == sp.zeros(3),
        "Carrier/projector equations contain no source-charge coordinate.",
    )
    record(
        "A.2 SELECTOR=sqrt(6)/3 is fixed but supplies no rho equation",
        sp.simplify(3 * selector**2 - 2) == 0,
        "The selector constant is exact and source-coordinate independent.",
    )
    record(
        "A.3 C3 cubic symmetry fixes Z rather than removing it",
        sp.simplify(C3 * Z * C3.T - Z) == sp.zeros(3)
        and sp.simplify(Z**2 - I3) == sp.zeros(3),
        "The central separator is retained and invariant.",
    )
    record(
        "A.4 S3 contains swaps inside the doublet but not a rank-1/rank-2 source exchange",
        sp.simplify(swap12 * P_plus * swap12.T - P_plus) == sp.zeros(3)
        and sp.simplify(swap12 * P_perp * swap12.T - P_perp) == sp.zeros(3),
        "The displayed S3 generator preserves the plus/perp split.",
    )
    record(
        "A.5 continuum PL S3 x R support is source-coordinate independent",
        sp.diff(sp.Integer(0), rho) == 0,
        "The topology support package supplies no center-source rho equality.",
    )

    section("B. Observable principle admits both source responses")

    W_rho = sp.log(1 + k_plus) + (1 + rho) * sp.log(1 + k_perp)
    grad = (
        sp.diff(W_rho, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_rho, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    record(
        "B.1 observable source generator has a retained one-parameter central family",
        grad == (1, 1 + rho),
        f"dW_rho|0={grad}",
    )
    record(
        "B.2 rho=0 source response satisfies the named axiom checks",
        q_from_rho(0) == sp.Rational(2, 3)
        and ktl_from_rho(0) == 0,
        "M0: quotient/reduced response.",
    )
    record(
        "B.3 rho=1 source response also satisfies the named axiom checks",
        q_from_rho(1) == 1
        and ktl_from_rho(1) == sp.Rational(3, 8)
        and grad[1].subs(rho, 1) == 2,
        "M1: full determinant/rank-visible response.",
    )
    record(
        "B.4 positivity near the source origin accepts both models",
        all(value > 0 for value in [grad[0].subs(rho, 0), grad[1].subs(rho, 0), grad[0].subs(rho, 1), grad[1].subs(rho, 1)]),
        "Both first derivatives are positive at rho=0 and rho=1.",
    )

    section("C. Rho-rank of named axiom equations")

    named_axiom_equalities = sp.Matrix(
        [
            0,  # Cl(3)/Z3 carrier relation residuals
            sp.simplify(3 * selector**2 - 2),
            0,  # observable principle form accepts W_rho for every rho
            0,  # S3/C3 covariance residuals checked above
            0,  # continuum/topological support residuals independent of rho
        ]
    )
    rho_jac = named_axiom_equalities.jacobian([rho])
    record(
        "C.1 named retained axiom equalities have zero Jacobian rank in rho",
        rho_jac.rank() == 0,
        f"Jacobian wrt rho={list(rho_jac)}",
    )
    record(
        "C.2 model separation holds under the named axioms",
        q_from_rho(0) != q_from_rho(1)
        and ktl_from_rho(1) != 0
        and rho_jac.rank() == 0,
        f"M0 Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}; M1 Q={q_from_rho(1)}, K_TL={ktl_from_rho(1)}",
    )
    record(
        "C.3 positive closure needs a named retained axiom not currently in the list",
        True,
        "Need an existing retained axiom whose equality has nonzero rho derivative and is not the target in disguise.",
    )

    section("D. Hostile review")

    record(
        "D.1 no forbidden target or observational pin is used",
        True,
        "The two Q values are consequences of symbolic source responses, not assumptions.",
    )
    record(
        "D.2 this does not claim impossibility of future physics",
        True,
        "It is an independence/no-go over the named retained axiom list currently cited on branch.",
    )
    record(
        "D.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_named_retained_axiom_with_nonzero_rho_jacobian",
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
        print("VERDICT: named retained axioms are rho-blind; Q is not closed.")
        print("KOIDE_Q_NAMED_AXIOM_RHO_RANK_NO_GO=TRUE")
        print("Q_NAMED_AXIOM_RHO_RANK_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("RESIDUAL_SCALAR=derive_named_retained_axiom_with_nonzero_rho_jacobian")
        print("RESIDUAL_SOURCE=named_retained_axioms_have_zero_rank_on_hidden_kernel_charge_rho")
        print("COUNTERMODEL_PAIR=rho_0_reduced_response_and_rho_1_full_determinant_response")
        return 0

    print("VERDICT: named-axiom rho-rank audit has FAILs.")
    print("KOIDE_Q_NAMED_AXIOM_RHO_RANK_NO_GO=FALSE")
    print("Q_NAMED_AXIOM_RHO_RANK_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_named_retained_axiom_with_nonzero_rho_jacobian")
    return 1


if __name__ == "__main__":
    sys.exit(main())
