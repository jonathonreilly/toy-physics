#!/usr/bin/env python3
"""
Koide selected-line / Brannen phase orbit bridge.

Companion to:
docs/KOIDE_SELECTED_LINE_BRANNEN_PHASE_ORBIT_BRIDGE_NOTE_2026-04-21.md

This runner proves that the current selected-line cyclic phase target is not a
new independent local phase variable. It is exactly the same C_3 Fourier phase
that appears in the Brannen/circulant parameterization, up to fixed orbit
bookkeeping:

  - on the current selected-line slot order (e, mu, tau),
      theta = -arg(b_sel),
  - on the standard Brannen order (tau, e, mu),
      delta = arg(b_std),
  - the two coefficient phases differ only by one exact C_3 shift,
      arg(b_sel) = delta + 2 pi / 3,
    so on the current selected-line convention
      theta = -(delta + 2 pi / 3)   (mod 2 pi).

Numerically, the current selected-line witness phase and the PDG fitted
Brannen phase satisfy that relation to high precision.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

from frontier_koide_selected_line_cyclic_phase_target_2026_04_20 import (
    physical_selected_point,
    selected_line_theta,
)

PASS_COUNT = 0
FAIL_COUNT = 0

OMEGA = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def wrap_to_pi(x: float) -> float:
    return (x + math.pi) % (2.0 * math.pi) - math.pi


def fourier_coeff_selected_order(amps: np.ndarray) -> complex:
    """Current selected-line / PDG slot order (e, mu, tau)."""
    w = np.exp(2j * np.pi / 3.0)
    u, v, wslot = [complex(x) for x in amps]
    return (u + np.conjugate(w) * v + w * wslot) / 3.0


def fourier_coeff_brannen_order(amps_tau_e_mu: np.ndarray) -> complex:
    """Standard Brannen order (tau, e, mu) = k=0,1,2."""
    w = np.exp(2j * np.pi / 3.0)
    lam0, lam1, lam2 = [complex(x) for x in amps_tau_e_mu]
    return (lam0 + np.conjugate(w) * lam1 + w * lam2) / 3.0


def part1_selected_line_phase_is_fourier_phase() -> None:
    print("=" * 88)
    print("PART 1: on the current selected-line slot order, theta is the cyclic Fourier phase")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", real=True)
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)
    b_sel = sp.simplify((u + sp.conjugate(OMEGA) * v + OMEGA * w) / 3)

    check(
        "On the current slot order, Re(b_sel) = r1 / 6 exactly",
        sp.simplify(sp.re(b_sel) - r1 / 6) == 0,
        detail=f"Re(b_sel)={sp.simplify(sp.re(b_sel))}",
    )
    check(
        "On the current slot order, Im(b_sel) = -r2 / 6 exactly",
        sp.simplify(sp.im(b_sel) + r2 / 6) == 0,
        detail=f"Im(b_sel)={sp.simplify(sp.im(b_sel))}",
    )
    check(
        "Therefore the selected-line circle phase is theta = -arg(b_sel) (mod 2 pi)",
        sp.simplify(r1**2 + r2**2 - 36 * sp.expand_complex(b_sel * sp.conjugate(b_sel))) == 0,
        detail="r1 = 6 Re(b_sel), r2 = -6 Im(b_sel)",
    )


def part2_brannen_standard_phase_and_c3_shift() -> None:
    print()
    print("=" * 88)
    print("PART 2: the standard Brannen phase and the selected-line phase differ by one fixed C_3 shift")
    print("=" * 88)

    a, delta = sp.symbols("a delta", positive=True, real=True)
    lam_tau = a * (1 + sp.sqrt(2) * sp.cos(delta))
    lam_e = a * (1 + sp.sqrt(2) * sp.cos(delta + 2 * sp.pi / 3))
    lam_mu = a * (1 + sp.sqrt(2) * sp.cos(delta + 4 * sp.pi / 3))

    b_std = sp.simplify((lam_tau + sp.conjugate(OMEGA) * lam_e + OMEGA * lam_mu) / 3)
    b_sel = sp.simplify((lam_e + sp.conjugate(OMEGA) * lam_mu + OMEGA * lam_tau) / 3)

    target_std = sp.simplify(a / sp.sqrt(2) * (sp.cos(delta) + sp.I * sp.sin(delta)))
    target_sel = sp.simplify(
        a
        / sp.sqrt(2)
        * (sp.cos(delta + 2 * sp.pi / 3) + sp.I * sp.sin(delta + 2 * sp.pi / 3))
    )

    check(
        "In the standard Brannen order (tau, e, mu), the Fourier phase is exactly delta",
        sp.simplify(sp.expand_complex(b_std - target_std)) == 0,
        detail="b_std = (a/sqrt(2)) exp(i delta)",
    )
    check(
        "In the current selected-line order (e, mu, tau), the same phase is shifted by +2 pi / 3",
        sp.simplify(sp.expand_complex(b_sel - target_sel)) == 0,
        detail="b_sel = (a/sqrt(2)) exp(i (delta + 2 pi / 3))",
    )

    r0 = 3 * a
    r1_sel = sp.simplify(6 * sp.re(target_sel))
    r2_sel = sp.simplify(-6 * sp.im(target_sel))
    check(
        "So the current selected-line phase obeys theta = -(delta + 2 pi / 3) on the same cyclic circle",
        sp.simplify(r1_sel - 3 * sp.sqrt(2) * a * sp.cos(delta + 2 * sp.pi / 3)) == 0
        and sp.simplify(r2_sel + 3 * sp.sqrt(2) * a * sp.sin(delta + 2 * sp.pi / 3)) == 0,
        detail="r1 = sqrt(2) r0 cos(delta+2pi/3), r2 = -sqrt(2) r0 sin(delta+2pi/3)",
    )


def part3_numeric_current_witness() -> None:
    print()
    print("=" * 88)
    print("PART 3: the current selected-line witness and the PDG Brannen fit satisfy the orbit relation")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps_selected = np.sqrt(masses)  # (e, mu, tau)
    amps_brannen = np.array([amps_selected[2], amps_selected[0], amps_selected[1]], dtype=float)  # (tau, e, mu)

    b_sel = fourier_coeff_selected_order(amps_selected)
    b_std = fourier_coeff_brannen_order(amps_brannen)
    theta_pdg = -math.atan2(b_sel.imag, b_sel.real)
    delta_fit = math.atan2(b_std.imag, b_std.real)

    m_star, _ = physical_selected_point()
    theta_star = float(selected_line_theta(m_star))
    theta_from_exact_delta = wrap_to_pi(-(2.0 / 9.0 + 2.0 * math.pi / 3.0))

    check(
        "The PDG amplitudes fit the standard Brannen phase near 2/9",
        abs(delta_fit - 2.0 / 9.0) < 1.0e-4,
        detail=f"delta_fit={delta_fit:.12f}",
        kind="NUMERIC",
    )
    check(
        "The PDG selected-order phase obeys theta = -(delta + 2 pi / 3)",
        abs(wrap_to_pi(theta_pdg + delta_fit + 2.0 * math.pi / 3.0)) < 1.0e-10,
        detail=f"theta_pdg={theta_pdg:.12f}, delta_fit={delta_fit:.12f}",
        kind="NUMERIC",
    )
    check(
        "The current selected-line witness phase matches the PDG selected-order phase",
        abs(theta_star - theta_pdg) < 5.0e-7,
        detail=f"theta_star={theta_star:.12f}, theta_pdg={theta_pdg:.12f}",
        kind="NUMERIC",
    )
    check(
        "If delta closes at 2/9, the current selected-line target phase is fixed automatically",
        abs(wrap_to_pi(theta_star - theta_from_exact_delta)) < 1.0e-4,
        detail=f"theta_(2/9)={theta_from_exact_delta:.12f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_selected_line_phase_is_fourier_phase()
    part2_brannen_standard_phase_and_c3_shift()
    part3_numeric_current_witness()

    print()
    print("Interpretation:")
    print("  The current selected-line cyclic phase target is not a new local phase")
    print("  variable. It is the same C_3 Fourier phase already used by the")
    print("  Brannen/circulant parameterization, with only fixed orbit bookkeeping:")
    print("  the current slot orientation contributes the minus sign, and the")
    print("  standard Brannen ordering differs by one exact +2pi/3 cycle shift.")
    print("  So the live physical bridge is narrower than it looked: once an ambient")
    print("  law fixes the Brannen phase delta, the current selected-line phase")
    print("  target theta follows automatically by theta = -(delta + 2pi/3).")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
