#!/usr/bin/env python3
"""
Koide Brannen-phase endpoint pullback.

Companion to:
docs/KOIDE_BRANNEN_PHASE_ENDPOINT_PULLBACK_NOTE_2026-04-21.md

This runner composes the existing exact selected-line phase law with the new
selected-line / Brannen orbit bridge. The result is a direct pullback:

  ambient Brannen phase delta
    -> selected-line cyclic phase theta = -(delta + 2 pi / 3)
    -> selected-line scalar bridge kappa(delta)
    -> reachable-slot ratio r(delta)
    -> unique first-branch endpoint m(delta).

This does not prove which ambient law fixes delta. It proves that once delta is
fixed, the current selected-line endpoint target is no longer independent.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from frontier_koide_selected_line_brannen_phase_orbit_bridge_2026_04_21 import (
    wrap_to_pi,
)
from frontier_koide_selected_line_cyclic_phase_target_2026_04_20 import (
    physical_selected_point,
    positivity_threshold,
    selected_line_theta,
)
from frontier_koide_selected_line_cyclic_response_bridge import (
    selected_line_kappa,
    selected_line_small_amp,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)


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


def theta_from_delta(delta: float) -> float:
    return wrap_to_pi(-(delta + 2.0 * math.pi / 3.0))


def kappa_from_delta(delta: float) -> float:
    theta = theta_from_delta(delta)
    return math.sqrt(6.0) * math.sin(theta) / (2.0 - SQRT2 * math.cos(theta))


def ratio_from_delta(delta: float) -> float:
    kappa = kappa_from_delta(delta)
    return (1.0 - kappa) / (1.0 + kappa)


def endpoint_from_delta(delta: float) -> float:
    kappa = kappa_from_delta(delta)
    m_pos = positivity_threshold()
    return float(brentq(lambda m: selected_line_kappa(m) - kappa, m_pos + 1.0e-4, 0.0))


def part1_exact_pullback_formula() -> None:
    print("=" * 88)
    print("PART 1: the selected-line scalar bridge is an exact pullback of the Brannen phase")
    print("=" * 88)

    delta = sp.symbols("delta", real=True)
    theta = -(delta + 2 * sp.pi / 3)
    kappa_theta = sp.sqrt(6) * sp.sin(theta) / (2 - sp.sqrt(2) * sp.cos(theta))
    kappa_delta = sp.simplify(sp.trigsimp(kappa_theta))
    target = -sp.sqrt(6) * sp.cos(delta + sp.pi / 6) / (2 + sp.sqrt(2) * sp.sin(delta + sp.pi / 6))

    check(
        "The orbit bridge plus cyclic phase law give one exact pullback kappa(delta)",
        sp.simplify(kappa_delta - target) == 0,
        detail=f"kappa(delta)={kappa_delta}",
    )
    check(
        "The reachable-slot ratio is therefore fixed by r(delta) = (1-kappa(delta))/(1+kappa(delta))",
        sp.simplify((1 - kappa_delta) / (1 + kappa_delta) - (1 - target) / (1 + target)) == 0,
    )


def part2_first_branch_endpoint_uniqueness() -> None:
    print()
    print("=" * 88)
    print("PART 2: on the current physical branch, delta fixes a unique selected-line endpoint")
    print("=" * 88)

    delta_samples = [0.20, 2.0 / 9.0, 0.24]
    ok_theta = True
    ok_kappa = True
    ok_m = True
    details = []

    for delta in delta_samples:
        theta = theta_from_delta(delta)
        kappa = kappa_from_delta(delta)
        m = endpoint_from_delta(delta)
        theta_rec = selected_line_theta(m)
        kappa_rec = selected_line_kappa(m)
        details.append(f"delta={delta:.6f}->m={m:.9f}")
        ok_theta &= abs(wrap_to_pi(theta_rec - theta)) < 1.0e-9
        ok_kappa &= abs(kappa_rec - kappa) < 1.0e-12
        ok_m &= positivity_threshold() < m < 0.0

    check(
        "For physical Brannen-phase values near the current window, theta(delta) lands on the first selected-line branch",
        ok_theta and ok_m,
        detail="; ".join(details),
        kind="NUMERIC",
    )
    check(
        "The pulled-back endpoint reproduces the same selected-line scalar bridge exactly",
        ok_kappa,
        detail="first-branch root of kappa(m)=kappa(delta)",
        kind="NUMERIC",
    )


def part3_delta_2_over_9_current_witness() -> None:
    print()
    print("=" * 88)
    print("PART 3: the 2/9 phase support route lands on the current selected-line witness window")
    print("=" * 88)

    delta = 2.0 / 9.0
    theta = theta_from_delta(delta)
    kappa = kappa_from_delta(delta)
    ratio = ratio_from_delta(delta)
    m = endpoint_from_delta(delta)

    m_star, _ = physical_selected_point()
    theta_star = selected_line_theta(m_star)
    kappa_star = selected_line_kappa(m_star)
    amp = selected_line_small_amp(m)
    q = float(np.sum(amp * amp) / (np.sum(amp) ** 2))

    check(
        "delta = 2/9 fixes the selected-line target phase automatically",
        abs(wrap_to_pi(theta_star - theta)) < 1.0e-4,
        detail=f"theta(2/9)={theta:.12f}, theta_*={theta_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "delta = 2/9 fixes the current selected-line scalar bridge to current-witness precision",
        abs(kappa - kappa_star) < 2.0e-5,
        detail=f"kappa(2/9)={kappa:.12f}, kappa_*={kappa_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "delta = 2/9 pulls back to the same first-branch endpoint window",
        abs(m - m_star) < 5.0e-5 and abs(q - 2.0 / 3.0) < 1.0e-12,
        detail=f"m(2/9)={m:.12f}, m_*={m_star:.12f}, r(2/9)={ratio:.12f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_exact_pullback_formula()
    part2_first_branch_endpoint_uniqueness()
    part3_delta_2_over_9_current_witness()

    print()
    print("Interpretation:")
    print("  The selected-line endpoint target is now an explicit pullback of the")
    print("  ambient Brannen phase. Once delta is fixed, the current exact stack")
    print("  already fixes theta, the selected-line scalar bridge kappa, the")
    print("  reachable-slot ratio r = w/v, and the unique first-branch endpoint m.")
    print("  So the remaining open bridge is narrower than 'ambient phase plus")
    print("  separate endpoint law': it is now just the ambient law selecting the")
    print("  physical Brannen phase itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
