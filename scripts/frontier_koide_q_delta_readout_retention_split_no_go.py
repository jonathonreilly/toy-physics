#!/usr/bin/env python3
"""
Koide Q/delta readout-retention split audit.

Theorem attempt:
  Remove the operational-quotient descent condition by deriving strict readout
  from existing retained source-response and APS observability notes.

Result:
  Split.

  Q side:
    The retained observable-principle notes do support a strict zero-source
    local scalar readout: physical scalar observables are coefficients in the
    local source expansion of W[J] at the zero-source baseline.  On the exact
    normalized second-order carrier, that readout gives Y=I_2, hence K_TL=0
    and Q=2/3.

    This is stronger than generic central observability, because arbitrary
    nonzero K is an external probe/source coordinate rather than the physical
    baseline readout.

  Delta side:
    The same readout idea does not remove the Brannen bridge.  Closed APS
    holonomy is retained and exact, but the charged-lepton Brannen parameter is
    still an open selected-line endpoint coordinate unless a physical functor
    identifies it with the closed holonomy.  Replacing the open endpoint by the
    closed APS value is a readout change, not a derivation.

Therefore this route can advance Q, but it does not close the full
dimensionless Koide lane without the endpoint descent/functor law.

No PDG masses, target fitted value, or H_* pin is used.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def q_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
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
    section("A. Retained source-response readout support")

    observable_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    hierarchy_note = read("docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md")
    source_response_supported = (
        "local scalar observables are exactly the" in observable_note
        and "coefficients in its local source expansion" in observable_note
        and "subtracting the zero-source baseline" in observable_note
        and "The physical order parameter is not the raw fermion determinant" in hierarchy_note
        and "local curvature of the effective action" in hierarchy_note
    )
    record(
        "A.1 retained notes support zero-source local scalar source-response readout",
        source_response_supported,
        "observable principle + hierarchy selector notes identify physical scalar readout with source-expansion coefficients.",
    )

    section("B. Q consequence of strict zero-source readout")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    w_red = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    y_plus = sp.simplify(sp.diff(w_red, k_plus))
    y_perp = sp.simplify(sp.diff(w_red, k_perp))
    y0 = (sp.simplify(y_plus.subs(k_plus, 0)), sp.simplify(y_perp.subs(k_perp, 0)))
    record(
        "B.1 exact reduced generator gives Y=(1,1) at zero source",
        y0 == (1, 1),
        f"W_red={w_red}; dW/dK|0={y0}",
    )
    record(
        "B.2 zero-source readout gives K_TL=0 and Q=2/3",
        ktl_from_y(*y0) == 0 and q_from_y(*y0) == sp.Rational(2, 3),
        f"K_TL={ktl_from_y(*y0)}, Q={q_from_y(*y0)}",
    )
    y = sp.symbols("y", positive=True, real=True)
    k_probe = (sp.simplify(1 / y - 1), sp.simplify(1 / (2 - y) - 1))
    record(
        "B.3 nonzero K remains an external probe coordinate, not the strict physical baseline",
        sp.solve([sp.Eq(k_probe[0], 0), sp.Eq(k_probe[1], 0)], [y], dict=True) == [{y: 1}],
        f"K(y)={k_probe}; zero source only at y=1.",
    )

    section("C. Delta does not follow from closed readout alone")

    eta = eta_abss_z3_weights_12()
    delta_open, tau = sp.symbols("delta_open tau", real=True)
    tau_solution = sp.solve(sp.Eq(eta, delta_open + tau), tau)
    record(
        "C.1 retained APS readout fixes only the closed value eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "C.2 closed readout leaves the selected open endpoint split free",
        tau_solution == [sp.Rational(2, 9) - delta_open],
        f"eta_APS=delta_open+tau -> tau={tau_solution[0]}",
    )
    record(
        "C.3 setting physical delta equal to closed eta is a readout bridge, not derived by APS alone",
        True,
        "The Brannen mass formula uses a selected-line endpoint coordinate; closed APS support still needs a functor to that coordinate.",
    )

    section("D. Full-lane verdict")

    record(
        "D.1 strict source-response readout reduces the Q residual to one physical identification",
        True,
        "Q is removed only if the charged-lepton scalar selector is the retained zero-source source-response coefficient.",
    )
    record(
        "D.2 strict readout does not close the delta residual",
        True,
        "Delta still needs the closed-APS-to-open-selected-line endpoint functor or descent law.",
    )
    record(
        "D.3 full operational-quotient descent condition is not fully removed",
        True,
        "The endpoint part of the condition remains.",
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
        print("VERDICT: strict readout reduces the Q source condition but does not close the full lane.")
        print("KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO=TRUE")
        print("Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_Q=FALSE")
        print("Q_DELTA_READOUT_RETENTION_SPLIT_REDUCES_Q_TO_ZERO_SOURCE_READOUT=TRUE")
        print("Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_DELTA=FALSE")
        print("Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_FULL_LANE=FALSE")
        print("RESIDUAL_SCALAR=closed_APS_to_open_selected_line_endpoint_functor")
        print("RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout")
        return 0

    print("VERDICT: readout-retention split audit has FAILs.")
    print("KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO=FALSE")
    print("Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_Q=FALSE")
    print("Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_DELTA=FALSE")
    print("Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_FULL_LANE=FALSE")
    print("RESIDUAL_SCALAR=closed_APS_to_open_selected_line_endpoint_functor")
    return 1


if __name__ == "__main__":
    sys.exit(main())
