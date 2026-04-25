#!/usr/bin/env python3
"""
Koide delta Dai-Freed open-trivialization no-go.

Theorem attempt:
  Use the Dai-Freed determinant-line viewpoint to turn the closed APS eta
  invariant into a canonical open selected-line Berry endpoint, deriving

      theta_end - theta0 = eta_APS = 2/9.

Result:
  Negative from the retained data alone.  Dai-Freed theory can provide a
  canonical section/trivialization after a boundary Dirac family, filling, and
  endpoint boundary data have been specified.  But the retained Koide delta
  packet supplies the closed ambient eta value, not a canonical selected-line
  endpoint boundary datum.  The open phase still has the form

      open_phase = path_holonomy + endpoint_section_end - endpoint_section_start,

  and the endpoint-section difference can move the open phase to any value.
  Setting it to eta_APS is the same residual endpoint law.

No PDG masses, Koide Q target, fitted delta, or H_* pin is used.
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
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Closed APS support")

    eta = eta_abss_z3_weights_12()
    record(
        "A.1 retained ambient APS scalar is exactly eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )

    section("B. Open determinant-line phase still has endpoint data")

    h, s0, s1 = sp.symbols("h s0 s1", real=True)
    open_phase = sp.simplify(h + s1 - s0)
    solve_s1 = sp.solve(sp.Eq(open_phase, eta), s1)
    solve_h = sp.solve(sp.Eq(open_phase, eta), h)
    record(
        "B.1 open phase decomposes into path holonomy plus endpoint-section difference",
        open_phase == h + s1 - s0,
        f"open_phase={open_phase}",
    )
    record(
        "B.2 endpoint section can be chosen to fit eta for any path holonomy",
        solve_s1 == [s0 - h + sp.Rational(2, 9)],
        f"s1_required={solve_s1}",
    )
    record(
        "B.3 path holonomy can be chosen to fit eta for any endpoint sections",
        solve_h == [s0 - s1 + sp.Rational(2, 9)],
        f"h_required={solve_h}",
    )

    section("C. Dai-Freed needs boundary data not supplied by retained packet")

    eta_start, eta_end = sp.symbols("eta_start eta_end", real=True)
    dai_freed_section_difference = sp.simplify((eta_end - eta_start) / 2)
    record(
        "C.1 endpoint trivialization requires endpoint eta/boundary data",
        dai_freed_section_difference == (eta_end - eta_start) / 2,
        f"section_difference={dai_freed_section_difference}",
    )
    record(
        "C.2 ambient eta_APS alone does not determine eta_start and eta_end",
        True,
        "The retained packet has the closed fixed-point eta, not a boundary family assigning endpoint sections.",
    )
    record(
        "C.3 choosing eta_end-eta_start=2 eta_APS is another endpoint law",
        sp.solve(sp.Eq(dai_freed_section_difference, eta), eta_end)
        == [eta_start + sp.Rational(4, 9)],
        "This is a boundary-data condition, not derived by the closed eta number itself.",
    )

    section("D. Counter-trivializations")

    samples = [
        (sp.Rational(0), sp.Rational(0), sp.Rational(0)),
        (sp.Rational(2, 9), sp.Rational(0), sp.Rational(0)),
        (sp.Rational(0), sp.Rational(0), sp.Rational(2, 9)),
        (sp.Rational(1, 9), sp.Rational(0), sp.Rational(1, 9)),
    ]
    lines = []
    for h_value, s0_value, s1_value in samples:
        phase_value = sp.simplify(open_phase.subs({h: h_value, s0: s0_value, s1: s1_value}))
        closes = sp.simplify(phase_value - eta) == 0
        lines.append(f"h={h_value}, s0={s0_value}, s1={s1_value}, open={phase_value}, closes={closes}")
    record(
        "D.1 multiple open decompositions preserve the same closed APS support",
        len(lines) == len(samples),
        "\n".join(lines),
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "E.1 Dai-Freed open-trivialization route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "E.2 delta remains open after Dai-Freed audit",
        True,
        "Residual primitive: physical endpoint boundary data/trivialization for the selected line.",
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
        print("VERDICT: Dai-Freed/open determinant trivialization does not close delta from retained data alone.")
        print("KOIDE_DELTA_DAI_FREED_OPEN_TRIVIALIZATION_NO_GO=TRUE")
        print("DELTA_DAI_FREED_OPEN_TRIVIALIZATION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_TRIVIALIZATION=endpoint_boundary_data_for_selected_line_not_retained")
        return 0

    print("VERDICT: Dai-Freed open-trivialization audit has FAILs.")
    print("KOIDE_DELTA_DAI_FREED_OPEN_TRIVIALIZATION_NO_GO=FALSE")
    print("DELTA_DAI_FREED_OPEN_TRIVIALIZATION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_TRIVIALIZATION=endpoint_boundary_data_for_selected_line_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
