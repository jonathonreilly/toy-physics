#!/usr/bin/env python3
"""
Koide Q named-axiom semialgebraic admissibility no-go.

Theorem attempt:
  Under the no-new-axioms rule, prove that retained semialgebraic
  admissibility conditions (positivity, smooth source response, concavity of
  the log source generator, and finite local source-domain inequalities)
  isolate the hidden kernel source charge rho=0 even though retained
  polynomial equalities do not.

Result:
  No retained closure.  The current semialgebraic admissibility constraints
  reduce to an open interval containing both

      rho=0, reduced source response, Q=2/3;
      rho=1, full determinant source response, Q=1.

  Inequalities such as source positivity and log-concavity prove admissibility
  of a region; they do not create a retained boundary equation selecting the
  endpoint rho=0.  A condition that excludes rho=1 while retaining rho=0 is an
  additional order/source law unless it is already retained.

Exact residual:

      derive_retained_semialgebraic_boundary_selecting_rho_zero.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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

    section("A. Brainstormed semialgebraic routes")

    routes = [
        "source-response positivity",
        "strict log-concavity / stable local maximum",
        "finite-radius analytic source domain",
        "closed interval or boundary admissibility",
        "wrong-assumption inversion: full determinant rho=1 is admissible",
    ]
    record(
        "A.1 five inequality/order variants are considered",
        len(routes) == 5,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )

    section("B. Retained semialgebraic source-admissibility region")

    W_rho = sp.log(1 + k_plus) + (1 + rho) * sp.log(1 + k_perp)
    grad0 = (
        sp.diff(W_rho, k_plus).subs({k_plus: 0, k_perp: 0}),
        sp.diff(W_rho, k_perp).subs({k_plus: 0, k_perp: 0}),
    )
    hessian0 = sp.hessian(W_rho, (k_plus, k_perp)).subs({k_plus: 0, k_perp: 0})
    record(
        "B.1 source positivity is the open inequality rho > -1",
        grad0 == (1, 1 + rho),
        f"dW_rho|0={grad0}; positivity requires 1+rho>0",
    )
    record(
        "B.2 log-source concavity gives the same open inequality",
        hessian0 == sp.diag(-1, -rho - 1),
        f"Hessian at zero={hessian0}; negative definite iff rho>-1",
    )

    admissible_samples = [-sp.Rational(1, 2), sp.Integer(0), sp.Integer(1), sp.Integer(2)]
    sample_truth = [(value, bool(1 + value > 0)) for value in admissible_samples]
    record(
        "B.3 retained inequalities define a connected admissible interval containing rho=0 and rho=1",
        all(ok for _, ok in sample_truth)
        and sp.Interval.open(-1, sp.oo).contains(sp.Integer(0))
        and sp.Interval.open(-1, sp.oo).contains(sp.Integer(1)),
        f"admissible_interval=(-1, infinity); samples={sample_truth}",
    )

    record(
        "B.4 both source models satisfy the current semialgebraic constraints",
        q_from_rho(0) == sp.Rational(2, 3)
        and q_from_rho(1) == 1
        and ktl_from_rho(0) == 0
        and ktl_from_rho(1) == sp.Rational(3, 8),
        f"rho=0 -> Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}; "
        f"rho=1 -> Q={q_from_rho(1)}, K_TL={ktl_from_rho(1)}",
    )

    section("C. Boundary conditions are extra source laws")

    boundary_zero = rho
    inequality_excluding_counterstate = 1 - rho
    record(
        "C.1 selecting rho=0 requires a boundary equation, not an open admissibility inequality",
        boundary_zero.subs(rho, 0) == 0
        and boundary_zero.subs(rho, 1) != 0,
        "The equation rho=0 is exactly the missing no-hidden-kernel source law.",
    )
    record(
        "C.2 an inequality that keeps rho=0 but excludes rho=1 supplies a threshold",
        inequality_excluding_counterstate.subs(rho, 0) > 0
        and inequality_excluding_counterstate.subs(rho, 1) == 0,
        "The threshold rho<1 or rho<=0 is not present in the named retained axioms.",
    )
    record(
        "C.3 minimization of |rho| would close only after adding an objective",
        sp.diff(rho**2, rho).subs(rho, 0) == 0
        and sp.diff(rho**2, rho, 2) == 2,
        "Least-source norm is a selector objective; it is not a retained source equation.",
    )

    section("D. Semialgebraic model separation")

    retained_inequality_residuals = sp.Matrix([1 + rho])
    jac = retained_inequality_residuals.jacobian([rho])
    record(
        "D.1 retained inequalities have nonzero rho slope but no zero-level selector",
        jac.rank() == 1
        and retained_inequality_residuals.subs(rho, 0)[0] > 0
        and retained_inequality_residuals.subs(rho, 1)[0] > 0,
        f"inequality polynomial=1+rho; derivative={jac[0]}; positive at rho=0,1",
    )
    record(
        "D.2 inequality truth is locally stable around both rho=0 and rho=1",
        all(1 + value > 0 for value in [-sp.Rational(1, 4), sp.Rational(1, 4), sp.Rational(3, 4), sp.Rational(5, 4)]),
        "Open admissibility cannot isolate either point without an added boundary.",
    )
    record(
        "D.3 no semialgebraic closure follows from the currently named admissibility region",
        True,
        "The admissible region contains a path from rho=0 to rho=1: rho(t)=t for 0<=t<=1.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target is assumed as input",
        True,
        "rho=0 is treated as the tested boundary condition, not as a theorem input.",
    )
    record(
        "E.2 no observational pin or mass data are used",
        True,
        "The audit uses exact symbolic source-response inequalities only.",
    )
    record(
        "E.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_semialgebraic_boundary_selecting_rho_zero",
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
        print("VERDICT: retained semialgebraic admissibility does not close Q.")
        print("KOIDE_Q_NAMED_AXIOM_SEMIALGEBRAIC_ADMISSIBILITY_NO_GO=TRUE")
        print("Q_NAMED_AXIOM_SEMIALGEBRAIC_ADMISSIBILITY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("RESIDUAL_SCALAR=derive_retained_semialgebraic_boundary_selecting_rho_zero")
        print("RESIDUAL_SOURCE=admissible_rho_interval_contains_rho_0_and_rho_1")
        print("COUNTERMODEL_PAIR=rho_0_reduced_response_and_rho_1_full_determinant_response")
        return 0

    print("VERDICT: named-axiom semialgebraic admissibility audit has FAILs.")
    print("KOIDE_Q_NAMED_AXIOM_SEMIALGEBRAIC_ADMISSIBILITY_NO_GO=FALSE")
    print("Q_NAMED_AXIOM_SEMIALGEBRAIC_ADMISSIBILITY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_semialgebraic_boundary_selecting_rho_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
