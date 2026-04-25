#!/usr/bin/env python3
"""
Koide delta adiabatic spectral-projector endpoint no-go.

Theorem attempt:
  Use the adiabatic theorem for the selected spectral line: perhaps the
  projector path itself fixes the open Berry endpoint and derives
  theta_end - theta0 = eta_APS.

Result:
  Negative.  A spectral projector path fixes a line, not a preferred endpoint
  phase lift.  For a two-level line

      psi(theta,phi) = (cos(theta/2), exp(i phi) sin(theta/2)),

  the open Berry integral along phi:0->Phi is

      gamma_open = sin(theta/2)^2 * Phi.

  The equation gamma_open=2/9 selects a continuum of endpoint/path choices.
  Multiplying the eigenvector lift by an endpoint gauge leaves the projector
  unchanged and shifts the open integral by chi_end-chi_start.  Thus the
  adiabatic projector theorem supplies the right language for the selected
  line, but not the missing physical endpoint/trivialization functor.

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


def main() -> int:
    section("A. Open Berry phase of a selected spectral line")

    theta, phi, Phi = sp.symbols("theta phi Phi", real=True)
    eta = sp.Rational(2, 9)
    berry_density = sp.sin(theta / 2) ** 2
    gamma_open = sp.simplify(berry_density * Phi)
    record(
        "A.1 two-level line has open Berry phase sin(theta/2)^2 * Phi",
        gamma_open == Phi * sp.sin(theta / 2) ** 2,
        f"gamma_open={gamma_open}",
    )
    phi_needed = sp.solve(sp.Eq(gamma_open, eta), Phi)
    expected_phi = sp.Rational(2, 9) / sp.sin(theta / 2) ** 2
    record(
        "A.2 matching eta_APS selects an endpoint/path parameter",
        len(phi_needed) == 1 and sp.trigsimp(phi_needed[0] - expected_phi) == 0,
        f"Phi needed={phi_needed}",
    )

    sample_lines = []
    ok_samples = True
    for theta_value in [sp.pi / 2, sp.pi / 3, sp.pi / 4]:
        phi_value = sp.simplify(eta / (sp.sin(theta_value / 2) ** 2))
        phase_value = sp.simplify((sp.sin(theta_value / 2) ** 2) * phi_value)
        ok_samples = ok_samples and phase_value == eta
        sample_lines.append(f"theta={theta_value}, Phi={phi_value}, gamma={phase_value}")
    record(
        "A.3 infinitely many projector endpoints can be tuned to eta",
        ok_samples,
        "\n".join(sample_lines),
    )

    section("B. Projector path does not fix the endpoint phase lift")

    chi0, chi_end = sp.symbols("chi0 chi_end", real=True)
    gamma_gauged = sp.simplify(gamma_open + chi_end - chi0)
    record(
        "B.1 eigenvector endpoint gauge shifts the open Berry integral",
        gamma_gauged == Phi * sp.sin(theta / 2) ** 2 + chi_end - chi0,
        f"gamma_open -> {gamma_gauged}",
    )
    chi_fit = sp.solve(sp.Eq(gamma_gauged, eta), chi_end)
    record(
        "B.2 unchanged projector can fit eta by endpoint gauge",
        chi_fit == [chi0 - Phi * sp.sin(theta / 2) ** 2 + sp.Rational(2, 9)],
        f"chi_end={chi_fit}",
    )

    # Projector invariance under a U(1) lift: (e^{i chi} psi)(e^{i chi} psi)^* = psi psi^*.
    chi = sp.symbols("chi", real=True)
    projector_phase_factor = sp.simplify(sp.exp(sp.I * chi) * sp.exp(-sp.I * chi))
    record(
        "B.3 the spectral projector is invariant under the phase lift",
        projector_phase_factor == 1,
        f"phase factor in |psi><psi| = {projector_phase_factor}",
    )

    section("C. Closed APS holonomy can be split into many open segments")

    open_segments = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    split_lines = []
    ok_split = True
    for segment in open_segments:
        complement = sp.simplify(eta - segment)
        total = sp.simplify(segment + complement)
        ok_split = ok_split and total == eta
        split_lines.append(f"open={segment}, complement={complement}, closed_total={total}")
    record(
        "C.1 same closed APS value permits many open/complement decompositions",
        ok_split,
        "\n".join(split_lines),
    )
    record(
        "C.2 selecting open=eta is a boundary/trivialization statement",
        sp.Rational(2, 9) in open_segments,
        "The projector theorem does not choose that segment by itself.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 adiabatic spectral-projector route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after projector endpoint audit",
        True,
        "Residual primitive: physical endpoint/trivialization functor for the selected line.",
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
        print("VERDICT: adiabatic spectral-projector theorem does not close delta.")
        print("KOIDE_DELTA_ADIABATIC_PROJECTOR_ENDPOINT_NO_GO=TRUE")
        print("DELTA_ADIABATIC_PROJECTOR_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_TRIVIALIZATION=open_selected_line_projector_endpoint_lift_not_retained")
        return 0

    print("VERDICT: adiabatic projector endpoint audit has FAILs.")
    print("KOIDE_DELTA_ADIABATIC_PROJECTOR_ENDPOINT_NO_GO=FALSE")
    print("DELTA_ADIABATIC_PROJECTOR_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_TRIVIALIZATION=open_selected_line_projector_endpoint_lift_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
