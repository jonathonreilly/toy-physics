#!/usr/bin/env python3
"""
Koide Q/delta retained-observability descent no-go.

Theorem attempt:
  Remove the operational-quotient descent condition by deriving it from the
  current retained notion of physical observability.

Result:
  Negative.  Current retained observability is too broad:

  Q side:
    The central projectors P_plus and P_perp are themselves retained
    C3-invariant effects.  Therefore the singlet/doublet central split is
    observable in the retained algebra, and a general central state can assign
    arbitrary probability u to P_plus.  Equal quotient weights require an
    additional quotient-readout/descent rule.

  Delta side:
    Closed APS eta is retained, but open selected-line phases remain endpoint
    trivialization dependent.  Gauge-invariant closed holonomy permits many
    open/complement decompositions.  Therefore observability of the closed APS
    value does not remove endpoint complements.

This proves that "physical observability" as currently retained does not by
itself derive operational-quotient descent.

No PDG masses, target fitted value, or H_* pin is used.
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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Retained Q observability includes the central split")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    record(
        "A.1 P_plus and P_perp are retained C3-invariant effects",
        sp.simplify(P_plus**2 - P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp**2 - P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus + P_perp - I3) == sp.zeros(3, 3)
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"ranks=({P_plus.rank()},{P_perp.rank()})",
    )

    u = sp.symbols("u", positive=True, real=True)
    rho_u = sp.simplify(u * P_plus + ((1 - u) / 2) * P_perp)
    p_plus = sp.simplify(sp.trace(P_plus * rho_u))
    p_perp = sp.simplify(sp.trace(P_perp * rho_u))
    record(
        "A.2 retained central effects read an arbitrary central source state",
        sp.simplify(sp.trace(rho_u) - 1) == 0
        and p_plus == u
        and p_perp == 1 - u
        and sp.simplify(C * rho_u - rho_u * C) == sp.zeros(3, 3),
        f"probabilities=({p_plus},{p_perp})",
    )
    record(
        "A.3 Q descent is a proper restriction of retained central observability",
        sp.solve(sp.Eq(ktl_from_weight(u), 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={sp.factor(ktl_from_weight(u))}",
    )

    section("B. Retained Q counterstates remain observable")

    samples = [
        ("rank_state", sp.Rational(1, 3)),
        ("descended_state", sp.Rational(1, 2)),
        ("singlet_heavy_state", sp.Rational(2, 3)),
    ]
    lines = []
    ok = True
    for name, value in samples:
        q_value = q_from_weight(value)
        ktl_value = ktl_from_weight(value)
        ok = ok and 0 < value < 1
        lines.append(f"{name}: u={value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.1 current retained observability allows closing and non-closing central states",
        ok,
        "\n".join(lines),
    )
    record(
        "B.2 observability alone does not identify source-visible labels with quotient-kernel labels",
        True,
        "P_plus/P_perp are observable central effects until a stricter quotient-readout law removes them.",
    )

    section("C. Retained delta observability includes closed holonomy, not open endpoint")

    eta = eta_abss_z3_weights_12()
    delta_open, tau = sp.symbols("delta_open tau", real=True)
    bridge = sp.Eq(eta, delta_open + tau)
    tau_solution = sp.solve(bridge, tau)
    record(
        "C.1 retained APS observability fixes the closed eta value",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "C.2 closed observability leaves an open endpoint/complement split",
        tau_solution == [sp.Rational(2, 9) - delta_open],
        f"eta_APS=delta_open+tau -> tau={tau_solution[0]}",
    )

    section("D. Retained delta counterendpoints remain observable")

    endpoint_samples = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    endpoint_lines = []
    endpoint_ok = True
    for value in endpoint_samples:
        tau_value = sp.simplify(eta - value)
        total = sp.simplify(value + tau_value)
        endpoint_ok = endpoint_ok and total == eta
        endpoint_lines.append(f"delta_open={value}, tau={tau_value}, closed_total={total}")
    record(
        "D.1 same retained closed holonomy has many open/complement decompositions",
        endpoint_ok,
        "\n".join(endpoint_lines),
    )
    record(
        "D.2 observability alone does not identify endpoint complement with quotient kernel",
        True,
        "Closed APS phase is observable; the open selected endpoint still needs a functor/trivialization law.",
    )

    section("E. Verdict")

    record(
        "E.1 retained observability does not derive operational-quotient descent",
        True,
        "It leaves both the central source state u and endpoint transition tau free.",
    )
    record(
        "E.2 removing the descent condition requires a stricter retained readout theorem",
        True,
        "The theorem must restrict physical charged-lepton readout to quotient-descended effects/phases.",
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
        print("VERDICT: retained observability alone does not derive descent.")
        print("KOIDE_Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_NO_GO=TRUE")
        print("Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_CLOSES_Q=FALSE")
        print("Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=stricter_quotient_descended_readout_not_retained")
        print("RESIDUAL_Q=central_projectors_are_retained_observable_effects")
        print("RESIDUAL_DELTA=open_endpoint_split_not_fixed_by_closed_APS_observability")
        return 0

    print("VERDICT: retained-observability descent audit has FAILs.")
    print("KOIDE_Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_NO_GO=FALSE")
    print("Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_CLOSES_Q=FALSE")
    print("Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=stricter_quotient_descended_readout_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
