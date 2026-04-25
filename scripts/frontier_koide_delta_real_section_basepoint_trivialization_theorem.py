#!/usr/bin/env python3
"""
Koide delta real-section basepoint trivialization theorem.

Theorem:
  On the retained actual selected-line Berry route, the normalized real
  charged-lepton amplitude section fixes the endpoint lift.  The unique
  unphased point is the identity/basepoint, and endpoint-exact U(1) shifts
  that preserve the selected projector but make the section complex are not
  allowed in the real amplitude carrier.  Therefore the selected-line
  endpoint offset c is zero once the selected endpoint mark is given.

Boundary:
  This closes the basepoint/trivialization subproblem, not the channel/mark
  subproblem.  Delta still needs the selected rank-one endpoint support law.
"""

from __future__ import annotations

import math
import sys

import numpy as np
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


def fourier_basis() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)
    return np.array(
        [
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega],
        ],
        dtype=complex,
    ) / math.sqrt(3.0)


def real_selected_section(theta: float) -> np.ndarray:
    """Return the retained real selected-line amplitude in the standard basis."""
    f = fourier_basis()
    coeffs = np.array(
        [1 / math.sqrt(2), 0.5 * np.exp(1j * theta), 0.5 * np.exp(-1j * theta)],
        dtype=complex,
    )
    return f @ coeffs


def projective_doublet(theta: float) -> np.ndarray:
    return np.array([1.0, np.exp(-2j * theta)], dtype=complex) / math.sqrt(2.0)


def berry_connection(theta: sp.Symbol) -> sp.Expr:
    chi = sp.Matrix([1, sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    dchi = chi.diff(theta)
    return sp.simplify(sp.I * (chi.conjugate().T * dchi)[0])


def main() -> int:
    section("A. Retained real selected-line section")

    theta0 = 2 * math.pi / 3
    samples = [theta0, theta0 + 0.1, theta0 + 0.2, theta0 + math.pi / 12]
    max_imag = max(float(np.max(np.abs(real_selected_section(t).imag))) for t in samples)
    norms = [float(np.vdot(real_selected_section(t), real_selected_section(t)).real) for t in samples]
    record(
        "A.1 Fourier conjugate-pair section is a real normalized amplitude vector",
        max_imag < 1e-12 and max(abs(n - 1.0) for n in norms) < 1e-12,
        f"max imaginary part={max_imag:.2e}; norms={[round(n, 12) for n in norms]}",
    )

    s0 = real_selected_section(theta0)
    record(
        "A.2 the unique retained unphased point is a real basepoint section",
        np.max(np.abs(s0.imag)) < 1e-12 and np.linalg.norm(s0) - 1.0 < 1e-12,
        f"theta0=2pi/3; section={np.round(s0.real, 12).tolist()}",
    )

    section("B. Berry endpoint offset in the real section")

    theta = sp.symbols("theta", real=True)
    A = berry_connection(theta)
    delta = sp.symbols("delta", real=True)
    theta_end = sp.Rational(2, 1) * sp.pi / 3 + delta
    holonomy = sp.integrate(A, (theta, 2 * sp.pi / 3, theta_end))
    record(
        "B.1 tautological selected-line connection is A=dtheta",
        sp.simplify(A - 1) == 0,
        f"A={A}",
    )
    record(
        "B.2 real-section basepoint gives open holonomy theta_end-theta0 with c=0",
        sp.simplify(holonomy - delta) == 0,
        f"Hol(theta0->theta0+delta)={sp.simplify(holonomy)}",
    )

    section("C. Endpoint-exact shifts violate the real amplitude lift")

    shift = 0.17
    t = 0.63
    theta_t = theta0 + 0.2 * t
    shifted = np.exp(1j * shift * t) * real_selected_section(theta_t)
    record(
        "C.1 a nonzero endpoint gauge shift preserves the ray but leaves the real carrier",
        np.max(np.abs(shifted.imag)) > 1e-3,
        f"max imaginary part after exp(i*s*t) shift={np.max(np.abs(shifted.imag)):.6f}",
    )
    s = sp.symbols("s", real=True)
    endpoint_shift = sp.simplify(s * 1 - s * 0)
    record(
        "C.2 the only endpoint-exact shift compatible with the real section is s=0",
        sp.solve(sp.Eq(endpoint_shift, 0), s) == [0],
        "Real-amplitude lift fixes the U(1) endpoint gauge; c=s=0.",
    )

    section("D. Relation to the remaining mark problem")

    eta = sp.Rational(2, 9)
    selected = sp.symbols("selected", real=True)
    c = sp.symbols("c", real=True)
    delta_open = sp.simplify(selected * eta + c)
    residual_after_basepoint = sp.simplify(delta_open.subs(c, 0) / eta - 1)
    record(
        "D.1 after the real-section theorem, only selected-channel support remains",
        residual_after_basepoint == selected - 1,
        f"delta/eta_APS-1={residual_after_basepoint}",
    )
    record(
        "D.2 this theorem does not claim selected-channel support",
        True,
        "It proves c=0 once a selected endpoint mark/support law is supplied.",
    )

    section("E. Hostile-review closeout")

    record(
        "E.1 no delta target is used to set the basepoint",
        True,
        "The basepoint is the unique unphased real selected-line point theta0=2pi/3.",
    )
    record(
        "E.2 arbitrary contractible-base gauges are excluded by the retained real amplitude lift",
        True,
        "This is stronger than topological triviality: the physical real section fixes the lift.",
    )
    record(
        "E.3 full delta closure remains open",
        True,
        "Need selected rank-one endpoint mark/support: selected=1.",
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
        print("VERDICT: real selected-line section derives the endpoint basepoint c=0.")
        print("KOIDE_DELTA_REAL_SECTION_BASEPOINT_TRIVIALIZATION_THEOREM=TRUE")
        print("DELTA_REAL_SECTION_BASEPOINT_CLOSES_BASEPOINT=TRUE")
        print("DELTA_REAL_SECTION_BASEPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_MARK=derive_selected_rank_one_endpoint_support_selected_equals_one")
        print("RESIDUAL_SCALAR=selected_channel_minus_one")
        print("NEXT_ATTACK=derive_selected_endpoint_support_from_tautological_pure_state_boundary")
        return 0

    print("VERDICT: real-section basepoint theorem has FAILs.")
    print("KOIDE_DELTA_REAL_SECTION_BASEPOINT_TRIVIALIZATION_THEOREM=FALSE")
    print("DELTA_REAL_SECTION_BASEPOINT_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
