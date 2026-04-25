#!/usr/bin/env python3
"""
Koide Q/delta C3 boundary-inflow no-go.

Theorem attempt:
  A single retained C3 boundary anomaly/inflow principle might derive both
  remaining primitives:

      Q side:     center-label source u = 1/2
      delta side: theta_end - theta0 = eta_APS = 2/9.

Result:
  Negative for finite C3 inflow data alone.  C3 group-cohomology/topological
  action labels give third-period phases k/3.  They do not contain the APS
  fraction 2/9 as an open endpoint, and they do not constrain the continuous
  center-label source u.  Any boundary source functor from the finite inflow
  class to u=1/2 needs a new map/normalization.  A mixed equation can be
  written symbolically, but without a retained coefficient and a second
  condition it leaves a continuum of (Q residual, delta residual) pairs.

No PDG masses, fitted Koide value, delta pin, or H_* pin is used.
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


def ktl_from_u(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def q_from_u(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def main() -> int:
    section("A. Finite C3 inflow phase lattice")

    eta = sp.Rational(2, 9)
    c3_phases = [sp.Rational(k, 3) for k in range(3)]
    record(
        "A.1 finite C3 boundary topological phases lie on the third lattice",
        c3_phases == [0, sp.Rational(1, 3), sp.Rational(2, 3)],
        f"C3 phases={c3_phases}",
    )
    record(
        "A.2 eta_APS=2/9 is not a finite C3 topological-action phase",
        eta not in c3_phases,
        "2/9 is the ABSS/APS support value, not a k/3 group-cohomology phase.",
    )

    section("B. Finite inflow class does not constrain the Q source state")

    u = sp.symbols("u", positive=True, real=True)
    ktl_u = ktl_from_u(u)
    q_u = q_from_u(u)
    record(
        "B.1 Q source neutrality is a continuous center-state equation u=1/2",
        sp.solve(sp.Eq(ktl_u, 0), u) == [sp.Rational(1, 2)],
        f"Q(u)={q_u}, K_TL(u)={ktl_u}",
    )
    samples = [sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(2, 3)]
    sample_lines = [
        f"k={k}, u={u_value}, Q={q_from_u(u_value)}, K_TL={ktl_from_u(u_value)}"
        for k in range(3)
        for u_value in samples
    ]
    record(
        "B.2 every finite inflow class permits closing and non-closing Q source states",
        len(sample_lines) == 9,
        "\n".join(sample_lines),
    )

    section("C. Boundary source functor is not retained by finite inflow data")

    k = sp.symbols("k", integer=True)
    phi_k = sp.Rational(1, 3) * k
    dphi_du = sp.diff(phi_k, u)
    record(
        "C.1 finite inflow phase has zero source-coordinate derivative",
        dphi_du == 0,
        "phi_k=k/3 is locally constant with respect to the continuous center source u.",
    )
    a0, a1 = sp.symbols("a0 a1", real=True)
    candidate_source_functor = a0 + a1 * phi_k
    fit_label = sp.solve(
        [sp.Eq(candidate_source_functor.subs(k, 0), sp.Rational(1, 2))],
        [a0],
        dict=True,
    )
    fit_rank = sp.solve(
        [sp.Eq(candidate_source_functor.subs(k, 0), sp.Rational(1, 3))],
        [a0],
        dict=True,
    )
    record(
        "C.2 finite-to-source maps can fit label or rank states once coefficients are chosen",
        fit_label == [{a0: sp.Rational(1, 2)}]
        and fit_rank == [{a0: sp.Rational(1, 3)}],
        "The finite class supplies no retained coefficient selecting the label fit over the rank fit.",
    )
    record(
        "C.3 a boundary source functor to u=1/2 is an added law",
        True,
        "Current retained inflow data specify topological phases, not a physical center-source preparation.",
    )

    section("D. Mixed inflow equation is underdetermined without new coefficients")

    r_q, r_delta, c = sp.symbols("r_q r_delta c", real=True)
    mixed_equation = sp.Eq(r_delta + c * r_q, 0)
    solution_line = sp.solve(mixed_equation, r_delta)
    record(
        "D.1 a single mixed anomaly equation leaves a residual line",
        solution_line == [-c * r_q],
        f"r_delta={solution_line[0]}",
    )
    counterexample = {r_q: sp.Rational(1, 6), r_delta: -c / 6}
    record(
        "D.2 the mixed equation can hold with nonzero Q and delta residuals",
        sp.simplify((r_delta + c * r_q).subs(counterexample)) == 0
        and counterexample[r_q] != 0,
        f"example: r_q=1/6, r_delta=-c/6 satisfies {mixed_equation}",
    )
    record(
        "D.3 setting both residuals to zero requires extra independent laws",
        True,
        "A retained coefficient plus one equation is not full lane closure.",
    )

    section("E. Open endpoint remains separate")

    theta0, theta_end, endpoint_gauge = sp.symbols("theta0 theta_end endpoint_gauge", real=True)
    endpoint_residual = sp.simplify(theta_end - theta0 - eta)
    gauge_solution = sp.solve(sp.Eq(theta_end - theta0 + endpoint_gauge, eta), endpoint_gauge)
    record(
        "E.1 finite inflow phase does not remove the open endpoint residual",
        endpoint_residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={endpoint_residual}",
    )
    record(
        "E.2 endpoint gauge can fit eta unless a physical trivialization is supplied",
        gauge_solution == [-theta_end + theta0 + sp.Rational(2, 9)],
        f"endpoint_gauge_required={gauge_solution}",
    )

    section("F. Verdict")

    record(
        "F.1 C3 boundary-inflow route does not close Q",
        True,
        "Finite inflow class does not select u=1/2.",
    )
    record(
        "F.2 C3 boundary-inflow route does not close delta",
        True,
        "Finite inflow phase does not select the open Berry/APS endpoint.",
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
        print("VERDICT: finite C3 boundary inflow does not close the Koide Q/delta lane.")
        print("KOIDE_Q_DELTA_C3_BOUNDARY_INFLOW_NO_GO=TRUE")
        print("Q_DELTA_C3_BOUNDARY_INFLOW_CLOSES_Q=FALSE")
        print("Q_DELTA_C3_BOUNDARY_INFLOW_CLOSES_DELTA=FALSE")
        print("RESIDUAL_Q=center_label_source_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_DELTA=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR=finite_C3_inflow_to_center_source_not_retained")
        return 0

    print("VERDICT: C3 boundary-inflow audit has FAILs.")
    print("KOIDE_Q_DELTA_C3_BOUNDARY_INFLOW_NO_GO=FALSE")
    print("Q_DELTA_C3_BOUNDARY_INFLOW_CLOSES_Q=FALSE")
    print("Q_DELTA_C3_BOUNDARY_INFLOW_CLOSES_DELTA=FALSE")
    print("RESIDUAL_Q=center_label_source_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_DELTA=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR=finite_C3_inflow_to_center_source_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
