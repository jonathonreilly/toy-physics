#!/usr/bin/env python3
"""
Koide Z3-qubit radian bridge no-go theorem.

Purpose:
  Test whether the obvious physical-base Berry / Pancharatnam constructions on
  the actual Z_3 doublet ray force the structural phase ratio 2/9 in radians.

Safe target:
  1. The natural one-step Pancharatnam phase on the projective Z_3 qubit orbit
     is pi/3, not 2/9.
  2. The three-step Bargmann invariant on that orbit has phase pi, not 2/9.
  3. On the actual selected-line CP^1 carrier, the tautological connection
     A = d theta yields a continuum of endpoint holonomies on the first branch;
     2/9 is one interior value, not a forced one.
  4. On the sign-relaxed quotient circle, the flat-holonomy family
     Hol_t = exp(i 2 pi t) likewise realizes 2/9 only by choosing t = 2/3.

This does not refute the actual-route statement "if delta is given, it is read
as a Berry holonomy on the selected line." It refutes the stronger claim that
the retained physical-base Berry geometry alone forces the numerical value
delta = 2/9.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq

from frontier_koide_selected_line_cyclic_response_bridge import (
    delta_offset,
    selected_line_small_amp,
)

PASS = 0
FAIL = 0

DELTA_TARGET = 2.0 / 9.0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


def canonical_spinor(theta: float) -> np.ndarray:
    return np.array([1.0, np.exp(-2j * theta)], dtype=complex) / math.sqrt(2.0)


def qubit_step_phase(theta: float) -> float:
    psi = canonical_spinor(theta)
    phi = canonical_spinor(theta + 2.0 * math.pi / 3.0)
    return float(np.angle(np.vdot(psi, phi)))


def bargmann_orbit_phase(theta: float) -> float:
    states = [canonical_spinor(theta + 2.0 * math.pi * k / 3.0) for k in range(3)]
    prod = 1.0 + 0.0j
    for a, b in zip(states, states[1:] + states[:1]):
        prod *= np.vdot(a, b)
    return float(np.angle(prod))


def flat_delta(t: float) -> float:
    return t / 3.0


def main() -> int:
    print("=" * 80)
    print("Koide Z3-qubit radian bridge no-go theorem")
    print("=" * 80)

    theta_samples = np.linspace(0.0, 2.0 * math.pi, 12, endpoint=False)
    step_phases = np.array([qubit_step_phase(theta) for theta in theta_samples])
    bargmann_phases = np.array([bargmann_orbit_phase(theta) for theta in theta_samples])

    check(
        "The one-step Pancharatnam phase on the Z3 qubit orbit is exactly pi/3",
        np.max(np.abs(step_phases - math.pi / 3.0)) < 1e-12,
        f"phase = {step_phases[0]:.12f}",
    )
    check(
        "Reducing that one-step phase to Brannen units gives 1/18, not 2/9",
        abs((step_phases[0] / (2.0 * math.pi * 3.0)) - (1.0 / 18.0)) < 1e-12
        and abs((step_phases[0] / (2.0 * math.pi * 3.0)) - DELTA_TARGET) > 1e-3,
        f"delta_step = {step_phases[0] / (2.0 * math.pi * 3.0):.12f}",
    )
    check(
        "The three-step Bargmann invariant of the Z3 qubit orbit has phase pi",
        np.max(np.abs(np.abs(bargmann_phases) - math.pi)) < 1e-12,
        f"phase = {bargmann_phases[0]:.12f}",
    )
    check(
        "Reducing that Bargmann phase per C3 element gives 1/6, not 2/9",
        abs((abs(bargmann_phases[0]) / (2.0 * math.pi * 3.0)) - (1.0 / 6.0)) < 1e-12
        and abs((abs(bargmann_phases[0]) / (2.0 * math.pi * 3.0)) - DELTA_TARGET) > 1e-3,
        f"delta_orbit = {abs(bargmann_phases[0]) / (2.0 * math.pi * 3.0):.12f}",
    )

    m_pos = float(brentq(lambda m: selected_line_small_amp(m)[0], -1.3, -1.2))
    m_zero = float(brentq(lambda m: selected_line_small_amp(m)[0] - selected_line_small_amp(m)[1], -0.4, -0.2))
    ms = np.linspace(m_pos + 1.0e-4, m_zero - 1.0e-4, 300)
    deltas = np.array([delta_offset(m) for m in ms], dtype=float)
    delta_alt = DELTA_TARGET + 0.01
    m_target = float(brentq(lambda m: delta_offset(m) - DELTA_TARGET, m_pos + 1.0e-4, m_zero - 1.0e-4))
    m_alt = float(brentq(lambda m: delta_offset(m) - delta_alt, m_pos + 1.0e-4, m_zero - 1.0e-4))

    check(
        "On the actual selected line the Berry offset runs through a continuum of values",
        bool(np.all(np.diff(deltas) < 0.0)) and deltas[0] > DELTA_TARGET > deltas[-1],
        f"delta-range = ({deltas[-1]:.12f}, {deltas[0]:.12f})",
    )
    check(
        "The physical value 2/9 is only one interior endpoint choice on that continuum",
        abs(delta_offset(m_target) - DELTA_TARGET) < 1e-12 and abs(delta_offset(m_alt) - delta_alt) < 1e-12,
        f"m_2/9 = {m_target:.12f}, m_alt = {m_alt:.12f}",
    )
    check(
        "So the tautological connection A = dtheta does not by itself force 2/9",
        abs(m_target - m_alt) > 1e-3,
        f"|m_2/9 - m_alt| = {abs(m_target - m_alt):.6f}",
    )

    t_target = 2.0 / 3.0
    t_near = 0.69
    hol_target = np.exp(1j * 2.0 * math.pi * t_target)
    hol_near = np.exp(1j * 2.0 * math.pi * t_near)
    check(
        "The flat-holonomy family on the sign-relaxed quotient realizes 2/9 at t = 2/3",
        abs(flat_delta(t_target) - DELTA_TARGET) < 1e-12,
        f"delta(t_target) = {flat_delta(t_target):.12f}",
    )
    check(
        "Nearby flat connections give nearby non-equal phase values",
        abs(flat_delta(t_near) - DELTA_TARGET) > 1e-3 and abs(hol_near - hol_target) > 1e-3,
        f"delta(t_near) = {flat_delta(t_near):.12f}",
    )

    print()
    print("Interpretation:")
    print("  The natural physical-base Berry constructions do not force delta = 2/9.")
    print("  The Z3 qubit step phase gives pi/3, the three-step Bargmann invariant")
    print("  gives pi, and the actual selected-line / flat-holonomy routes carry")
    print("  continuous endpoint choices. The remaining live object is therefore a")
    print("  unit bridge or equivalent physical-base quantization law, not another")
    print("  hidden selector on the retained Berry carrier.")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
