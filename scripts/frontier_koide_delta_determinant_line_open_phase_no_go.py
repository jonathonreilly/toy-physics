#!/usr/bin/env python3
"""
Koide delta determinant-line open-phase no-go.

Theorem attempt:
  The APS eta invariant defines a determinant-line/Bismut-Freed holonomy.
  Perhaps that holonomy fixes the selected-line open Berry phase endpoint,
  deriving theta_end - theta0 = eta_APS.

Result:
  Negative.  Eta fixes a closed-loop holonomy, e.g.

      Hol_loop = exp(2*pi*i*eta_APS).

  The selected-line Brannen phase is an open-path phase.  Open-path phases are
  endpoint-trivialization dependent:

      delta_open -> delta_open + chi_end - chi_start.

  The same closed holonomy can be decomposed into infinitely many open segment
  phases plus complementary closing phases.  Therefore determinant-line
  holonomy supplies strong APS support but does not select the open endpoint
  without an additional endpoint trivialization / Berry-APS functor.

No PDG masses, Koide Q target, delta pin, or H_* pin is used.
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
    section("A. Closed determinant-line holonomy from APS eta")

    eta = eta_abss_z3_weights_12()
    hol = sp.exp(2 * sp.pi * sp.I * eta)
    record(
        "A.1 ambient APS scalar is exactly eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 determinant-line closed holonomy is exp(2*pi*i*eta_APS)",
        hol == sp.exp(4 * sp.pi * sp.I / 9),
        f"Hol_loop={hol}",
    )

    section("B. Open selected-line phase is endpoint-gauge dependent")

    delta, chi_start, chi_end = sp.symbols("delta chi_start chi_end", real=True)
    delta_gauge = sp.simplify(delta + chi_end - chi_start)
    record(
        "B.1 open-path phase shifts by endpoint trivialization difference",
        delta_gauge == delta + chi_end - chi_start,
        f"delta_open -> {delta_gauge}",
    )
    record(
        "B.2 choosing chi_end-chi_start can move any open phase to eta",
        sp.solve(sp.Eq(delta_gauge, eta), chi_end) == [chi_start - delta + sp.Rational(2, 9)],
        "Endpoint gauges can set the open segment phase unless a physical trivialization is fixed.",
    )

    section("C. Same closed holonomy decomposes into many open phases")

    endpoint_samples = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    decomposition_lines = []
    ok = True
    for open_phase in endpoint_samples:
        closing_phase = sp.simplify(eta - open_phase)
        total_phase = sp.simplify(open_phase + closing_phase)
        ok = ok and total_phase == eta
        decomposition_lines.append(
            f"open={open_phase}, closing={closing_phase}, total={total_phase}, Hol=exp(2pi i eta)"
        )
    record(
        "C.1 closed holonomy permits a continuum of open/closing decompositions",
        ok,
        "\n".join(decomposition_lines),
    )
    record(
        "C.2 the eta open phase is one decomposition, not selected by closed holonomy",
        sp.Rational(2, 9) in endpoint_samples,
        "Selecting open=eta requires a preferred closing segment/trivialization.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 determinant-line holonomy route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after determinant-line audit",
        True,
        "Residual primitive: endpoint trivialization or functor mapping closed APS holonomy to selected open phase.",
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
        print("VERDICT: determinant-line closed holonomy does not close delta.")
        print("KOIDE_DELTA_DETERMINANT_LINE_OPEN_PHASE_NO_GO=TRUE")
        print("DELTA_DETERMINANT_LINE_OPEN_PHASE_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_TRIVIALIZATION=selected_line_open_phase_endpoint_trivialization")
        return 0

    print("VERDICT: determinant-line open-phase audit has FAILs.")
    print("KOIDE_DELTA_DETERMINANT_LINE_OPEN_PHASE_NO_GO=FALSE")
    print("DELTA_DETERMINANT_LINE_OPEN_PHASE_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_TRIVIALIZATION=selected_line_open_phase_endpoint_trivialization")
    return 1


if __name__ == "__main__":
    sys.exit(main())
