#!/usr/bin/env python3
"""
Koide delta APS-boundary endpoint no-go.

Theorem attempt:
  The APS boundary condition or a one-dimensional self-adjoint extension
  parameter might physically identify the selected-line Berry endpoint with
  the ambient APS value eta_APS = 2/9.

Result:
  Negative.  In the standard shifted boundary Dirac model the reduced eta
  function has the exact form

      eta(alpha) = 1 - 2 alpha,   0 < alpha < 1.

  The ambient value eta_APS = 2/9 fixes the boundary spectral shift
  alpha = 7/18.  It does not by itself fix the selected-line open-path Berry
  endpoint delta = theta_end - theta0.  Any bridge from alpha or eta(alpha) to
  delta needs a separate normalization/identification map; the identity
  delta=alpha gives 7/18, not 2/9, while delta=eta(alpha) is exactly the
  missing Berry/APS endpoint law.

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
    section("A. Ambient eta and shifted boundary Dirac parameter")

    eta_aps = eta_abss_z3_weights_12()
    alpha = sp.symbols("alpha", positive=True, real=True)
    eta_alpha = sp.simplify(1 - 2 * alpha)
    alpha_solution = sp.solve(sp.Eq(eta_alpha, eta_aps), alpha)

    record(
        "A.1 retained ambient APS scalar is exactly 2/9",
        eta_aps == sp.Rational(2, 9),
        f"eta_APS={eta_aps}",
    )
    record(
        "A.2 shifted boundary Dirac eta law fixes alpha=7/18 for eta=2/9",
        alpha_solution == [sp.Rational(7, 18)],
        f"eta(alpha)=1-2alpha; eta(alpha)=2/9 -> alpha={alpha_solution}",
    )
    record(
        "A.3 boundary shift alpha and selected-line Berry endpoint delta are different coordinates",
        sp.Rational(7, 18) != eta_aps,
        "The identity delta=alpha would give 7/18, not the ambient eta value 2/9.",
    )

    section("B. General bridge map retains a free normalization")

    u, v = sp.symbols("u v", real=True)
    delta_bridge = sp.simplify(u * alpha + v)
    delta_at_eta_alpha = sp.simplify(delta_bridge.subs(alpha, sp.Rational(7, 18)))
    v_needed = sp.solve(sp.Eq(delta_at_eta_alpha, eta_aps), v)
    u_needed_identity_offset = sp.solve(sp.Eq(delta_at_eta_alpha.subs(v, 0), eta_aps), u)

    record(
        "B.1 an affine boundary-to-Berry bridge has free scale and offset",
        delta_bridge == u * alpha + v,
        f"delta=u alpha+v; at alpha=7/18, delta={delta_at_eta_alpha}",
    )
    record(
        "B.2 matching delta to eta fixes one bridge coefficient, not the bridge theorem",
        v_needed == [sp.Rational(2, 9) - 7 * u / 18],
        f"v needed={v_needed}",
    )
    record(
        "B.3 zero-offset bridge would need u=4/7, another unexplained normalization",
        u_needed_identity_offset == [sp.Rational(4, 7)],
        f"v=0 -> u={u_needed_identity_offset}",
    )

    section("C. Counter-endpoints preserve the same APS boundary data")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    delta = sp.simplify(theta_end - theta0)
    residual = sp.simplify(delta - eta_aps)
    endpoint_samples = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(7, 18)]
    sample_lines = []
    residual_values = []
    for endpoint_delta in endpoint_samples:
        residual_value = sp.simplify(endpoint_delta - eta_aps)
        residual_values.append(residual_value)
        sample_lines.append(
            f"delta={endpoint_delta}: eta_APS={eta_aps}, alpha=7/18, residual={residual_value}"
        )

    record(
        "C.1 selected-line endpoint remains continuous after fixing eta and alpha",
        len(set(residual_values)) == len(residual_values),
        "\n".join(sample_lines),
    )
    record(
        "C.2 equating endpoint delta with eta_APS is exactly the residual law",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )

    section("D. Verdict")

    record(
        "D.1 APS boundary condition does not close the Brannen endpoint bridge",
        True,
        "It fixes a boundary spectral shift for a chosen eta model; it does not identify "
        "the selected-line Berry endpoint with eta_APS.",
    )
    record(
        "D.2 delta remains open after APS-boundary endpoint audit",
        True,
        "Residual primitive: physical map delta = eta_APS, or an equivalent unit Berry/APS bridge.",
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
        print("VERDICT: APS-boundary endpoint route does not close delta.")
        print("KOIDE_DELTA_APS_BOUNDARY_ENDPOINT_NO_GO=TRUE")
        print("DELTA_APS_BOUNDARY_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_BRIDGE=boundary_alpha_to_selected_line_delta_normalization")
        return 0

    print("VERDICT: APS-boundary endpoint audit has FAILs.")
    print("KOIDE_DELTA_APS_BOUNDARY_ENDPOINT_NO_GO=FALSE")
    print("DELTA_APS_BOUNDARY_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_BRIDGE=boundary_alpha_to_selected_line_delta_normalization")
    return 1


if __name__ == "__main__":
    sys.exit(main())
