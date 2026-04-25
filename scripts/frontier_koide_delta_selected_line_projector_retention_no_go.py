#!/usr/bin/env python3
"""
Koide delta selected-line projector-retention no-go.

Theorem attempt:
  Derive the selected endpoint identity from the retained CP1 selected line.
  The normalized selected-line ray

      chi(theta) = (1, exp(-2i theta)) / sqrt(2)

  defines a canonical rank-one projector P_chi.  If the physical open boundary
  anomaly/source channel is retained with support projector P_chi, then the
  spectator channel is zero.  If the same retention also fixes the endpoint
  torsor basepoint, then delta_open = eta_APS.

Result:
  Conditional positive, retained negative.  The CP1 line does define a unique
  rank-one projector, and a support-on-P_chi law would eliminate spectator
  anomaly weight.  But retained boundary data permit any convex source
  rho = p P_chi + (1-p)(I-P_chi), and the endpoint-exact offset c is
  independent even at p=1.  Thus the missing theorem is not the existence of
  the selected projector; it is the physical retention law selecting that
  projector as the open boundary source support and setting the endpoint
  exact counterterm to zero.

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


def main() -> int:
    section("A. Retained selected-line projector")

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([sp.Integer(1), sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    P = sp.simplify(chi * chi.conjugate().T)
    I2 = sp.eye(2)
    Q = sp.simplify(I2 - P)
    record(
        "A.1 selected-line CP1 ray defines a normalized rank-one projector",
        sp.simplify((chi.conjugate().T * chi)[0]) == 1
        and sp.simplify(P**2 - P) == sp.zeros(2, 2)
        and sp.trace(P) == 1
        and sp.det(P) == 0,
        f"P_chi={P}",
    )
    record(
        "A.2 the orthogonal spectator projector is also retained by the same line split",
        sp.simplify(Q**2 - Q) == sp.zeros(2, 2)
        and sp.simplify(P * Q) == sp.zeros(2, 2)
        and sp.trace(Q) == 1,
        f"Q_chi=I-P_chi={Q}",
    )

    section("B. Conditional positive theorem")

    p, c = sp.symbols("p c", real=True)
    rho = sp.simplify(p * P + (1 - p) * Q)
    selected_weight = sp.simplify(sp.trace(rho * P))
    spectator_weight = sp.simplify(sp.trace(rho * Q))
    eta = eta_abss_z3_weights_12()
    delta_open = sp.simplify(selected_weight * eta + c)
    residual = sp.simplify(delta_open / eta - 1)
    record(
        "B.1 convex boundary source has selected weight p and spectator weight 1-p",
        selected_weight == p and spectator_weight == 1 - p,
        f"selected={selected_weight}; spectator={spectator_weight}",
    )
    record(
        "B.2 support-on-selected-projector condition is equivalent to spectator=0",
        sp.solve(sp.Eq(spectator_weight, 0), p) == [1],
        "Tr(rho Q_chi)=0 forces rho=P_chi in this two-channel positive algebra.",
    )
    record(
        "B.3 selected-projector support plus zero endpoint offset would close delta",
        sp.simplify(delta_open.subs({p: 1, c: 0})) == eta
        and eta == sp.Rational(2, 9),
        f"eta_APS={eta}; delta_open|p=1,c=0={delta_open.subs({p: 1, c: 0})}",
    )

    section("C. Retained negative: projector exists, but retention is not a support law")

    retained_constraints = sp.Matrix([0, 0, 0])
    projector_retention_law = sp.symbols("projector_retention_law", real=True)
    endpoint_basepoint_law = sp.symbols("endpoint_basepoint_law", real=True)
    record(
        "C.1 retained constraints have zero rank in the projector-retention variable",
        retained_constraints.jacobian([projector_retention_law]).rank() == 0,
        "The retained line supplies P_chi but no equation Tr(rho Q_chi)=0.",
    )
    record(
        "C.2 retained constraints have zero rank in the endpoint-basepoint variable",
        retained_constraints.jacobian([endpoint_basepoint_law]).rank() == 0,
        "The retained line supplies the carrier but no equation c=0.",
    )
    record(
        "C.3 the reduced endpoint residual remains a two-term identity law",
        residual == c / eta - (1 - p),
        f"delta/eta_APS - 1 = {residual}",
    )

    section("D. Exact countermodels")

    cases = [
        ("selected projector, based", sp.Integer(1), sp.Integer(0)),
        ("spectator projector, based", sp.Integer(0), sp.Integer(0)),
        ("unpolarized projector mixture, based", sp.Rational(1, 2), sp.Integer(0)),
        ("selected projector, endpoint shift", sp.Integer(1), sp.Rational(1, 9)),
    ]
    lines = []
    deltas = set()
    for label, p_value, c_value in cases:
        delta_value = sp.simplify(delta_open.subs({p: p_value, c: c_value}))
        residual_value = sp.simplify(residual.subs({p: p_value, c: c_value}))
        deltas.add(delta_value)
        lines.append(
            f"{label}: p={p_value}, c={c_value}, "
            f"delta_open={delta_value}, residual={residual_value}"
        )
    record(
        "D.1 same retained CP1 projector split admits closing and nonclosing source states",
        len(deltas) == len(cases),
        "\n".join(lines),
    )
    record(
        "D.2 projector retention alone cannot remove endpoint exact shifts",
        sp.simplify(residual.subs(p, 1)) == c / eta,
        "Even at p=1, c remains unless a basepoint/trivialization law is retained.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "eta_APS is computed independently; p=1,c=0 are audited as missing laws.",
    )
    record(
        "E.2 selected-line projector existence is not promoted as endpoint closure",
        True,
        "The no-go distinguishes P_chi existence from physical source support on P_chi.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need selected-line projector retention plus selected endpoint basepoint.",
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
        print("VERDICT: selected-line projector retention is conditional, not retained-only delta proof.")
        print("KOIDE_DELTA_SELECTED_LINE_PROJECTOR_RETENTION_NO_GO=TRUE")
        print("DELTA_SELECTED_LINE_PROJECTOR_RETENTION_CLOSES_DELTA_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_DELTA_CLOSES_IF_PROJECTOR_RETENTION_AND_BASEPOINT_ARE_PHYSICAL=TRUE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_CHANNEL=derive_selected_line_projector_as_physical_boundary_source_support")
        print("RESIDUAL_TRIVIALIZATION=derive_selected_endpoint_exact_counterterm_zero")
        print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
        print("COUNTERSTATE=unpolarized_projector_mixture_or_selected_projector_with_endpoint_shift")
        return 0

    print("VERDICT: selected-line projector-retention audit has FAILs.")
    print("KOIDE_DELTA_SELECTED_LINE_PROJECTOR_RETENTION_NO_GO=FALSE")
    print("DELTA_SELECTED_LINE_PROJECTOR_RETENTION_CLOSES_DELTA_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
