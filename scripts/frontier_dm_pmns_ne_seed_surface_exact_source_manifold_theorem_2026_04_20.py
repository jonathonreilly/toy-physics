#!/usr/bin/env python3
"""
DM PMNS fixed-N_e-seed-surface exact source-manifold theorem.

Question:
  On the charged-lepton-side minimal PMNS branch, does the physical PMNS angle
  triple already live on the exact fixed native N_e seed surface, and if so
  do the current exact nonlocal selector families on that surface pick it?

Answer:
  Yes to existence, no to selection.

  The fixed native N_e seed surface already contains exact realizations of the
  physical PMNS angle triple. At the verified exact points, the PMNS-angle
  Jacobian has full rank 3, so the exact preimage is a local 2-real regular
  source manifold on that surface. The current exact nonlocal seed-surface
  selector families (aligned seed, stationary effective-action branches,
  constructive eta=1 closure point, constructive witness) all miss this exact
  PMNS manifold by macroscopic chi^2. Therefore the remaining I5 object on the
  charged-lepton-side branch is a new 2-real point-selection law on the exact
  N_e PMNS source manifold.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, least_squares

from frontier_dm_leptogenesis_pmns_active_projector_reduction import active_packet_from_h
from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import path_point
from frontier_dm_leptogenesis_pmns_observable_relative_action_law import (
    XBAR_NE,
    YBAR_NE,
    build_active_from_params,
    eta_columns_from_active,
    relative_action_h,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_reduced_surface_selector_support import (
    HIGH_SOURCE_REF,
    HIGH_SOURCE_REF_Y,
    compact_chart_to_source,
)
from frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem import (
    closure_point_on_ray,
    constrained_stationary_point,
    favored_column_and_extremal_params,
)
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    eta_columns_from_active as constructive_eta_columns,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

TARGET = np.array([0.307, 0.0218, 0.545], dtype=float)
CHART_LO = np.array([1.0e-6, 1.0e-6, 1.0e-6, 1.0e-6, -math.pi], dtype=float)
CHART_HI = np.array([1.0 - 1.0e-6, 1.0 - 1.0e-6, 1.0 - 1.0e-6, 1.0 - 1.0e-6, math.pi], dtype=float)

# Diverse deterministic starts on the fixed native N_e seed chart.  Each one
# lands on an exact physical PMNS point after local polishing.
SEED_CHART_STARTS = [
    np.array([0.036052, 0.460525, 0.541825, 0.581724, -1.533871], dtype=float),
    np.array([0.102254, 0.462703, 0.493331, 0.565381, 0.789612], dtype=float),
    np.array([0.134734, 0.465282, 0.464716, 0.545577, 0.757215], dtype=float),
    np.array([0.016368, 0.459040, 0.553314, 0.620378, -0.366521], dtype=float),
    np.array([0.024419, 0.460788, 0.549077, 0.569800, -2.670784], dtype=float),
    np.array([0.168475, 0.467792, 0.431065, 0.538217, -0.635221], dtype=float),
]


@dataclass
class ExactPoint:
    chart: np.ndarray
    x: np.ndarray
    y: np.ndarray
    delta: float
    obs: np.ndarray
    chi2: float
    rank: int
    rel_action: float
    etas: np.ndarray
    source_cubic: float


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def chart_to_obs(chart: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, np.ndarray]:
    x, y, delta = compact_chart_to_source(np.asarray(chart, dtype=float))
    h = canonical_h(x, y, delta)
    packet = active_packet_from_h(h).T
    s13sq = float(packet[0, 2])
    c13sq = max(1.0 - s13sq, 1.0e-15)
    s12sq = float(packet[0, 1] / c13sq)
    s23sq = float(packet[1, 2] / c13sq)
    obs = np.array([s12sq, s13sq, s23sq], dtype=float)
    return obs, x, y, float(delta), h


def residual(chart: np.ndarray) -> np.ndarray:
    obs, _x, _y, _delta, _h = chart_to_obs(chart)
    return obs - TARGET


def chi2(chart: np.ndarray) -> float:
    r = residual(chart)
    return float(np.dot(r, r))


def finite_jacobian(fun, chart: np.ndarray, eps: float = 1.0e-6) -> np.ndarray:
    chart = np.asarray(chart, dtype=float)
    f0 = np.asarray(fun(chart), dtype=float)
    jac = np.zeros((len(f0), len(chart)), dtype=float)
    for idx in range(len(chart)):
        step = np.zeros_like(chart)
        step[idx] = eps
        jac[:, idx] = (fun(chart + step) - fun(chart - step)) / (2.0 * eps)
    return jac


def source_distance(a: ExactPoint, b: ExactPoint) -> float:
    delta_diff = min(
        abs(a.delta - b.delta),
        abs(a.delta - b.delta + 2.0 * math.pi),
        abs(a.delta - b.delta - 2.0 * math.pi),
    )
    return float(np.linalg.norm(a.x - b.x) + np.linalg.norm(a.y - b.y) + delta_diff)


def polish_exact_point(start: np.ndarray) -> ExactPoint:
    result = least_squares(
        residual,
        np.asarray(start, dtype=float),
        bounds=(CHART_LO, CHART_HI),
        xtol=1.0e-14,
        ftol=1.0e-14,
        gtol=1.0e-14,
        max_nfev=2000,
    )
    chart = np.asarray(result.x, dtype=float)
    obs, x, y, delta, h = chart_to_obs(chart)
    jac = finite_jacobian(lambda q: chart_to_obs(q)[0], chart)
    rank = int(np.linalg.matrix_rank(jac, tol=1.0e-5))
    _h_chk, _packet_chk, etas = eta_columns_from_active(x, y, delta)
    return ExactPoint(
        chart=chart,
        x=x,
        y=y,
        delta=delta,
        obs=obs,
        chi2=chi2(chart),
        rank=rank,
        rel_action=float(relative_action_h(h)),
        etas=np.asarray(etas, dtype=float),
        source_cubic=float(np.imag(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def distinct_exact_points() -> list[ExactPoint]:
    raw = [polish_exact_point(start) for start in SEED_CHART_STARTS]
    reps: list[ExactPoint] = []
    for point in raw:
        if all(source_distance(point, rep) > 5.0e-2 for rep in reps):
            reps.append(point)
    return reps


def selector_family_points() -> list[tuple[str, np.ndarray]]:
    rows: list[tuple[str, np.ndarray]] = []

    rows.append(("aligned seed", np.array([0.2, 1.0 / 6.0, 0.6], dtype=float)))

    i_star, extremal_params = favored_column_and_extremal_params()
    start = closure_point_on_ray(extremal_params, i_star)
    low_chart, _ = constrained_stationary_point(start, i_star)
    x_low, y_low, delta_low = build_active_from_params(low_chart)
    h_low = canonical_h(x_low, y_low, delta_low)
    packet_low = active_packet_from_h(h_low).T
    obs_low = np.array(
        [
            float(packet_low[0, 1] / max(1.0 - packet_low[0, 2], 1.0e-15)),
            float(packet_low[0, 2]),
            float(packet_low[1, 2] / max(1.0 - packet_low[0, 2], 1.0e-15)),
        ],
        dtype=float,
    )
    rows.append(("low-action stationary", obs_low))

    h_high = canonical_h(HIGH_SOURCE_REF, HIGH_SOURCE_REF_Y, 0.0)
    packet_high = active_packet_from_h(h_high).T
    obs_high = np.array(
        [
            float(packet_high[0, 1] / max(1.0 - packet_high[0, 2], 1.0e-15)),
            float(packet_high[0, 2]),
            float(packet_high[1, 2] / max(1.0 - packet_high[0, 2], 1.0e-15)),
        ],
        dtype=float,
    )
    rows.append(("high-action stationary", obs_high))

    lam_star = brentq(lambda lam: constructive_eta_columns(*path_point(lam))[1][1] - 1.0, 0.0, 1.0)
    x_eta, y_eta, delta_eta = path_point(lam_star)
    h_eta = canonical_h(x_eta, y_eta, delta_eta)
    packet_eta = active_packet_from_h(h_eta).T
    obs_eta = np.array(
        [
            float(packet_eta[0, 1] / max(1.0 - packet_eta[0, 2], 1.0e-15)),
            float(packet_eta[0, 2]),
            float(packet_eta[1, 2] / max(1.0 - packet_eta[0, 2], 1.0e-15)),
        ],
        dtype=float,
    )
    rows.append(("constructive eta=1", obs_eta))

    x_wit, y_wit, delta_wit = path_point(1.0)
    h_wit = canonical_h(x_wit, y_wit, delta_wit)
    packet_wit = active_packet_from_h(h_wit).T
    obs_wit = np.array(
        [
            float(packet_wit[0, 1] / max(1.0 - packet_wit[0, 2], 1.0e-15)),
            float(packet_wit[0, 2]),
            float(packet_wit[1, 2] / max(1.0 - packet_wit[0, 2], 1.0e-15)),
        ],
        dtype=float,
    )
    rows.append(("constructive witness", obs_wit))

    return rows


def part1_exact_points_exist_on_the_fixed_native_seed_surface() -> list[ExactPoint]:
    print("\n" + "=" * 88)
    print("PART 1: EXACT PHYSICAL PMNS POINTS EXIST ON THE FIXED NATIVE N_e SEED SURFACE")
    print("=" * 88)

    reps = distinct_exact_points()
    check(
        "The verifier finds at least three distinct exact PMNS points on the fixed native N_e seed surface",
        len(reps) >= 3,
        f"distinct exact points={len(reps)}",
    )
    check(
        "Every retained representative reproduces the physical PMNS angle triple to high precision",
        all(point.chi2 < 1.0e-8 for point in reps),
        f"chi2 values={[round(point.chi2, 12) for point in reps]}",
    )

    for idx, point in enumerate(reps[:3], start=1):
        print()
        print(
            f"  rep {idx}: x={np.round(point.x, 6)}, y={np.round(point.y, 6)}, "
            f"delta={point.delta:.6f}, obs={np.round(point.obs, 9)}"
        )

    return reps


def part2_the_exact_preimage_is_a_regular_two_real_source_manifold(reps: list[ExactPoint]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXACT PREIMAGE IS A REGULAR 2-REAL SOURCE MANIFOLD")
    print("=" * 88)

    check(
        "At every retained exact PMNS point the angle-map Jacobian has full rank 3",
        all(point.rank == 3 for point in reps),
        f"ranks={[point.rank for point in reps]}",
    )
    check(
        "Therefore each retained exact point lies on a local 2-real regular preimage inside the 5-real seed surface",
        all(point.rank == 3 for point in reps),
        "dim(seed surface)=5 and rank(dF)=3",
    )


def part3_current_nonlocal_selector_families_do_not_pick_the_exact_pmns_manifold() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CURRENT NONLOCAL SEED-SURFACE SELECTOR FAMILIES MISS THE MANIFOLD")
    print("=" * 88)

    rows = selector_family_points()
    misses = []
    for name, obs in rows:
        miss = float(np.sum((obs - TARGET) ** 2))
        misses.append((name, miss))
        print(f"  {name:<24s} chi^2 = {miss:.12f}, obs = {np.round(obs, 9)}")

    check(
        "Every current exact nonlocal selector-family point misses the physical PMNS triple by chi^2 > 0.03",
        all(miss > 3.0e-2 for _name, miss in misses),
        f"misses={[round(miss, 6) for _name, miss in misses]}",
    )


def part4_current_selector_observables_vary_along_the_exact_manifold(reps: list[ExactPoint]) -> None:
    print("\n" + "=" * 88)
    print("PART 4: CURRENT SELECTOR OBSERVABLES VARY ALONG THE EXACT MANIFOLD")
    print("=" * 88)

    rel_values = np.array([point.rel_action for point in reps], dtype=float)
    eta0_values = np.array([point.etas[0] for point in reps], dtype=float)
    cubic_values = np.array([point.source_cubic for point in reps], dtype=float)

    check(
        "The exact PMNS manifold carries a macroscopic relative-action spread",
        float(np.max(rel_values) - np.min(rel_values)) > 1.0,
        f"S_rel range=({np.min(rel_values):.6f},{np.max(rel_values):.6f})",
    )
    check(
        "The exact PMNS manifold carries distinct transport outputs on the favored column",
        float(np.max(eta0_values) - np.min(eta0_values)) > 5.0e-3,
        f"eta_0 range=({np.min(eta0_values):.6f},{np.max(eta0_values):.6f})",
    )
    check(
        "The exact PMNS manifold carries both source-cubic orientations",
        np.min(cubic_values) < 0.0 < np.max(cubic_values),
        f"cubic range=({np.min(cubic_values):.6e},{np.max(cubic_values):.6e})",
    )


def part5_the_note_records_the_correct_i5_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE CORRECT I5 REDUCTION")
    print("=" * 88)

    note = read("docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md")

    check(
        "The note records exact PMNS realizability on the fixed native N_e seed surface",
        "fixed native `N_e` seed surface" in note and "physical PMNS angle triple" in note,
    )
    check(
        "The note records the regular 2-real source-manifold consequence",
        "`2`-real" in note and "Jacobian" in note and "rank `3`" in note,
    )
    check(
        "The note records the current nonlocal selector-family miss",
        "aligned seed" in note and "low-action stationary" in note and "constructive witness" in note,
    )
    check(
        "The note records the sharpened I5 target as a new 2-real point-selection law",
        "new `2`-real point-selection law" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS FIXED-N_e-SEED-SURFACE EXACT SOURCE-MANIFOLD THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the physical PMNS angle triple already live on the exact fixed")
    print("  native N_e seed surface, and do the current exact nonlocal selector")
    print("  families on that surface pick it?")

    reps = part1_exact_points_exist_on_the_fixed_native_seed_surface()
    part2_the_exact_preimage_is_a_regular_two_real_source_manifold(reps)
    part3_current_nonlocal_selector_families_do_not_pick_the_exact_pmns_manifold()
    part4_current_selector_observables_vary_along_the_exact_manifold(reps)
    part5_the_note_records_the_correct_i5_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction answer:")
    print("    - the fixed native N_e seed surface already contains exact physical")
    print("      PMNS points")
    print("    - on the verified regular patch those points form a local 2-real")
    print("      source manifold")
    print("    - current exact nonlocal seed-surface selector families do not pick")
    print("      that manifold")
    print("    - so the remaining I5 object is a new 2-real point-selection law on")
    print("      the exact N_e PMNS source manifold")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
