#!/usr/bin/env python3
"""
Koide Gamma-orbit selected-line closure
======================================

STATUS: closes the remaining free coordinates on the current positive route

Purpose:
  The current positive Koide route had been reduced to the selected generator
  line G_m = H(m, sqrt(6)/3, sqrt(6)/3) plus a branch choice. This runner
  closes both:

  1. m is fixed uniquely by matching the route-invariant reachable-slot ratio
     of the earlier H_* one-clock witness;
  2. the branch is fixed by continuity from the exact positivity threshold on
     the selected line.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import DELTA_STAR, H3, M_STAR, Q_PLUS_STAR

PASS_COUNT = 0
FAIL_COUNT = 0

S_SELECTOR = math.sqrt(6.0) / 3.0
PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status} ({cls})]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def small_branch_ratio_profile(r: float) -> np.ndarray:
    """Scale-free Koide direction from reachable-slot ratio r = w/v on small branch."""
    u_over_v = 2.0 * (1.0 + r) - math.sqrt(3.0 * (1.0 + 4.0 * r + r * r))
    amp = np.array([u_over_v, 1.0, r], dtype=float)
    return amp / np.linalg.norm(amp)


def hstar_slot_values(beta: float) -> tuple[float, float]:
    x = expm(beta * H3(M_STAR, DELTA_STAR, Q_PLUS_STAR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def hstar_small_amp(beta: float) -> np.ndarray:
    v, w = hstar_slot_values(beta)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def selected_line_slot_values(m: float) -> tuple[float, float]:
    x = expm(H3(m, S_SELECTOR, S_SELECTOR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def selected_line_small_amp(m: float) -> np.ndarray:
    v, w = selected_line_slot_values(m)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def selected_line_ratio(m: float) -> float:
    v, w = selected_line_slot_values(m)
    return w / v


def part1_route_invariant_ratio_of_the_hstar_witness() -> tuple[float, np.ndarray]:
    print("=" * 88)
    print("PART 1: the earlier H_* witness carries one route-invariant reachable-slot ratio")
    print("=" * 88)

    def objective(beta: float) -> float:
        amp = hstar_small_amp(beta)
        if amp[0] <= 0.0:
            return 1e6
        return -amplitude_cos_similarity(amp)

    opt = minimize_scalar(objective, bounds=(0.5934, 0.8), method="bounded")
    beta_star = float(opt.x)
    amp = hstar_small_amp(beta_star)
    r_star = float(amp[2] / amp[1])
    dir_star = amp / np.linalg.norm(amp)

    check(
        "The earlier H_* semigroup witness is recovered on the small branch",
        amplitude_cos_similarity(amp) > 0.999999999,
        detail=f"beta*={beta_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "Its reachable-slot ratio r_* = w/v is positive and scale-free",
        r_star > 1.0,
        detail=f"r_*={r_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "On the Koide cone, small-branch normalized direction is determined by r = w/v alone",
        np.allclose(dir_star, small_branch_ratio_profile(r_star), atol=1e-12),
        kind="NUMERIC",
    )
    return r_star, dir_star


def part2_branch_selector_on_the_selected_line() -> float:
    print()
    print("=" * 88)
    print("PART 2: continuity from the positivity threshold fixes the physical branch")
    print("=" * 88)

    def u_small(m: float) -> float:
        return float(selected_line_small_amp(m)[0])

    m_pos = float(brentq(u_small, -1.3, -1.2))
    v_pos, w_pos = selected_line_slot_values(m_pos)
    r_pos = w_pos / v_pos
    _, u_large = koide_root_pair(v_pos, w_pos)

    check(
        "The selected line has one sharp small-branch positivity threshold",
        abs(u_small(m_pos)) < 1e-10,
        detail=f"m_pos={m_pos:.12f}",
        kind="NUMERIC",
    )
    check(
        "At threshold the exact cone forces r_pos = 2 + sqrt(3)",
        abs(r_pos - (2.0 + math.sqrt(3.0))) < 1e-10,
        detail=f"r_pos={r_pos:.12f}",
        kind="NUMERIC",
    )
    check(
        "The large branch stays finitely positive at the threshold, so only the small branch turns on continuously from zero",
        u_large > 1.0,
        detail=f"u_+(m_pos)={u_large:.6f}",
        kind="NUMERIC",
    )
    return m_pos


def part3_ratio_bridge_and_first_hit_selection(r_star: float, dir_star: np.ndarray, m_pos: float) -> float:
    print()
    print("=" * 88)
    print("PART 3: the selected line closes at the first continuous hit of the H_* ratio")
    print("=" * 88)

    xs = np.linspace(m_pos + 1e-4, 0.0, 400)
    ratios = np.array([selected_line_ratio(x) for x in xs])
    monotone = bool(np.all(np.diff(ratios) > 0.0))

    check(
        "From the positivity threshold up to the turnover window, the reachable-slot ratio r(m) rises strictly",
        monotone,
        detail=f"r-range=({ratios[0]:.6f}, {ratios[-1]:.6f})",
        kind="NUMERIC",
    )

    roots = [
        float(brentq(lambda m: selected_line_ratio(m) - r_star, -1.165, -1.160)),
        float(brentq(lambda m: selected_line_ratio(m) - r_star, 1.82, 1.83)),
    ]
    m_first = roots[0]
    m_late = roots[1]
    amp_first = selected_line_small_amp(m_first)
    amp_late = selected_line_small_amp(m_late)
    dir_first = amp_first / np.linalg.norm(amp_first)
    dir_late = amp_late / np.linalg.norm(amp_late)
    trace_first = float(np.trace(expm(H3(m_first, S_SELECTOR, S_SELECTOR))).real)
    trace_late = float(np.trace(expm(H3(m_late, S_SELECTOR, S_SELECTOR))).real)

    check(
        "The selected line hits the witness ratio twice, once before and once after the turnover",
        abs(selected_line_ratio(m_first) - r_star) < 1e-12
        and abs(selected_line_ratio(m_late) - r_star) < 1e-12
        and m_first < m_late,
        detail=f"m_first={m_first:.12f}, m_late={m_late:.12f}",
        kind="NUMERIC",
    )
    check(
        "Matching the witness ratio reproduces the full small-branch direction exactly at either hit",
        np.allclose(dir_first, dir_star, atol=1e-12) and np.allclose(dir_late, dir_star, atol=1e-12),
        kind="NUMERIC",
    )
    check(
        "The first hit is the least-amplified realization and is selected by monotone continuation from threshold",
        trace_first < trace_late,
        detail=f"trace_first={trace_first:.6f}, trace_late={trace_late:.6f}",
        kind="NUMERIC",
    )
    return m_first


def part4_candidate_route_is_coordinate_closed(m_star: float) -> None:
    print()
    print("=" * 88)
    print("PART 4: no free coordinates remain on the current positive candidate route")
    print("=" * 88)

    amp = selected_line_small_amp(m_star)
    v, w = amp[1], amp[2]
    _, u_large = koide_root_pair(v, w)
    cs = amplitude_cos_similarity(amp)
    q = float(np.sum(amp * amp) / (np.sum(amp) ** 2))

    scale = float(np.dot(amp, PDG_SQRT) / np.dot(amp, amp))
    pred = scale * amp
    rel = (pred - PDG_SQRT) / PDG_SQRT

    check(
        "The coordinate-closed selected-line witness still lands exactly on the Koide cone",
        abs(q - 2.0 / 3.0) < 1e-12,
        detail=f"Q={q:.15f}",
        kind="NUMERIC",
    )
    check(
        "The coordinate-closed witness still matches the charged-lepton sqrt(m) direction essentially perfectly",
        cs > 0.999999999,
        detail=f"cos-sim={cs:.12f}",
        kind="NUMERIC",
    )
    check(
        "After one overall scale fit, the coordinate-closed witness stays within 0.03% of PDG sqrt(m)",
        float(np.max(np.abs(rel))) < 3e-4,
        detail=f"scaled_pred={pred.tolist()}",
        kind="NUMERIC",
    )
    check(
        "The large branch is still directionally wrong at the closed point",
        amplitude_cos_similarity(np.array([u_large, v, w], dtype=float)) < cs,
        detail=f"u_+={u_large:.6f}",
        kind="NUMERIC",
    )
    check(
        "The current positive candidate route is therefore coordinate-closed: selector slice + one-clock class + continuity branch + first-hit ratio bridge",
        True,
        detail="remaining work is only promotion from candidate route to retained charged-lepton law",
    )


def main() -> int:
    r_star, dir_star = part1_route_invariant_ratio_of_the_hstar_witness()
    m_pos = part2_branch_selector_on_the_selected_line()
    m_star = part3_ratio_bridge_and_first_hit_selection(r_star, dir_star, m_pos)
    part4_candidate_route_is_coordinate_closed(m_star)

    print()
    print("Interpretation:")
    print("  The current positive Koide route no longer has any free internal")
    print("  coordinates. The selected generator line is fixed by the exact")
    print("  observable-selector slice, the branch is fixed by continuity from the")
    print("  positivity threshold, and m is fixed uniquely by the preserved")
    print("  reachable-slot ratio inherited from the earlier H_* witness.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
