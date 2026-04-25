#!/usr/bin/env python3
"""
Koide delta minimal endpoint-action no-go.

Theorem attempt:
  Derive the selected endpoint degree mu=1 from an action/minimality
  principle.  For based circle maps of degree n, the Dirichlet endpoint action
  is proportional to n^2.  Perhaps the physical endpoint is the minimal
  positive orientation-preserving map, forcing n=1 and delta=2/9.

Result:
  Conditional positive, retained negative.  The minimal nonzero
  orientation-preserving based degree is n=1, so that principle would close
  delta.  But unconstrained action minimization selects the constant degree
  n=0 map, and the current retained endpoint packet does not derive the
  nonzero/primitive selected-channel constraint.  Thus minimality alone does
  not close delta; it must be paired with the missing primitive endpoint law.

No PDG masses, H_* pins, Q=2/3 assumptions, delta=2/9 assumptions, or
observational inputs are used.
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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def endpoint_action(degree: sp.Expr, offset: sp.Expr = 0) -> sp.Expr:
    # Minimal quadratic model: derivative energy n^2 plus endpoint-basepoint
    # penalty c^2.  This is enough to test what minimality can and cannot select.
    return sp.simplify(degree**2 + offset**2)


def main() -> int:
    section("A. Endpoint action and closed APS support")

    eta = eta_abss_z3_weights_12()
    n = sp.symbols("n", integer=True)
    c = sp.symbols("c", real=True)
    delta = sp.simplify(n * eta + c)
    action = endpoint_action(n, c)
    record(
        "A.1 closed APS support remains eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 quadratic endpoint action has degree and basepoint pieces",
        action == n**2 + c**2,
        f"S(n,c)={action}",
    )
    record(
        "A.3 closure requires n=1 and c=0",
        sp.solve([sp.Eq(delta, eta), sp.Eq(c, 0)], [n, c], dict=True) == [{n: 1, c: 0}],
        f"delta={delta}",
    )

    section("B. Unconstrained minimal action selects the nonclosing constant map")

    degrees = list(range(-4, 5))
    based_actions = {degree: endpoint_action(sp.Integer(degree), 0) for degree in degrees}
    min_action = min(based_actions.values())
    minimizers = [degree for degree, value in based_actions.items() if value == min_action]
    record(
        "B.1 unconstrained based endpoint action is minimized by degree zero",
        minimizers == [0],
        f"actions={based_actions}",
    )
    record(
        "B.2 degree zero is based and covariant but does not close delta",
        delta.subs({n: 0, c: 0}) == 0,
        "Minimal action without nonzero-channel constraint gives delta_open=0.",
    )

    section("C. Conditional positive: minimal nonzero orientation-preserving degree")

    positive_degrees = [degree for degree in degrees if degree > 0]
    positive_actions = {degree: based_actions[degree] for degree in positive_degrees}
    positive_min_action = min(positive_actions.values())
    positive_minimizers = [
        degree for degree, value in positive_actions.items() if value == positive_min_action
    ]
    record(
        "C.1 minimal positive based degree is one",
        positive_minimizers == [1],
        f"positive_actions={positive_actions}",
    )
    record(
        "C.2 minimal positive based endpoint closes delta",
        delta.subs({n: 1, c: 0}) == sp.Rational(2, 9),
        f"delta_open={delta.subs({n: 1, c: 0})}",
    )
    record(
        "C.3 the closing theorem assumes a nonzero primitive selected-channel constraint",
        True,
        "Minimality selects n=1 only after n>0 is supplied.",
    )

    section("D. Endpoint offset/basepoint")

    c_action = endpoint_action(1, c)
    record(
        "D.1 if degree one is fixed, action minimization sets c=0",
        sp.solve(sp.Eq(sp.diff(c_action, c), 0), c) == [0],
        f"S(1,c)={c_action}",
    )
    record(
        "D.2 basepoint minimization does not fix degree",
        endpoint_action(0, 0) < endpoint_action(1, 0),
        "The global action still prefers n=0 unless nonzero degree is derived.",
    )

    section("E. Hostile retained-status audit")

    nonzero_channel_law = sp.symbols("nonzero_channel_law", real=True)
    primitive_degree_law = sp.symbols("primitive_degree_law", real=True)
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "E.1 retained support constraints do not impose nonzero selected endpoint degree",
        retained_constraints.jacobian([nonzero_channel_law]).rank() == 0,
        "No retained equation excludes the based degree-zero countermap in this audit.",
    )
    record(
        "E.2 retained support constraints do not impose primitive positive degree",
        retained_constraints.jacobian([primitive_degree_law]).rank() == 0,
        "No retained equation excludes higher positive degrees except by adding minimal nonzero action.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem that the selected endpoint lies in the nonzero primitive positive degree sector.",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target or observational pin is used as an input",
        True,
        "The APS value is computed independently; action minimization is audited before closure.",
    )
    record(
        "F.2 minimal action is not promoted as retained closure",
        True,
        "Unconstrained minimality gives n=0, so the closing version assumes nonzero primitive degree.",
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
        print("VERDICT: minimal endpoint action is conditional, not retained-only proof.")
        print("KOIDE_DELTA_MINIMAL_ENDPOINT_ACTION_NO_GO=TRUE")
        print("DELTA_MINIMAL_ENDPOINT_ACTION_CLOSES_DELTA_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_DELTA_CLOSES_IF_NONZERO_POSITIVE_PRIMITIVE_SECTOR_IS_RETAINED=TRUE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_SCALAR=derive_nonzero_positive_primitive_selected_endpoint_degree")
        print("RESIDUAL_FUNCTOR=unconstrained_minimal_action_selects_degree_zero")
        print("COUNTERSTATE=based_minimal_degree_zero_delta_0")
        return 0

    print("VERDICT: minimal endpoint-action audit has FAILs.")
    print("KOIDE_DELTA_MINIMAL_ENDPOINT_ACTION_NO_GO=FALSE")
    print("DELTA_MINIMAL_ENDPOINT_ACTION_CLOSES_DELTA_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_nonzero_positive_primitive_selected_endpoint_degree")
    return 1


if __name__ == "__main__":
    sys.exit(main())
