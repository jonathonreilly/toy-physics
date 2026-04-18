#!/usr/bin/env python3
"""
DM neutrino source-surface bundle-window trichotomy candidate.

Question:
  On the compact branch, what is the sharpest shared statement about the three
  rival `m` windows when they are viewed directly on the explicit exact
  shift-quotient bundle?

Answer:
  The three windows do not behave the same on the broad exact bundle box.

  Endpoint and split-1 both have boundary-controlled broad-box minima well
  above the preferred recovered floor, while split-2 also has a
  boundary-controlled broad-box minimum but it lies below the preferred floor.

  So broad exact-bundle dominance is not the right carrier-side theorem target:
  it would fail already on split-2. The remaining useful theorem target must
  use the finer exact carrier restriction, not the broad quotient bundle alone.

Boundary:
  This is still a numerical candidate on broad exact-bundle boxes plus local
  boundary-control checks, not an interval-certified theorem.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT, repair_from_slack_point
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

WINDOWS = {
    "endpoint": (-1.899713, -1.87),
    "split_1": (-1.16, -1.10),
    "split_2": (-0.19, -0.14),
}
CORE_DELTA = (-2.5, 2.5)
CORE_R31 = (0.5, 4.0)

EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_MINIMA = {
    "endpoint": np.array([-1.87, 1.14568951, 0.5], dtype=float),
    "split_1": np.array([-1.1, 1.08840241, 0.5], dtype=float),
    "split_2": np.array([-0.14, 0.99704993, 0.5], dtype=float),
}
EXPECTED_MIN_REPAIRS = {
    "endpoint": 3.0275559194088237,
    "split_1": 2.3086034009138245,
    "split_2": 1.5004424916582041,
}


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


def bundle_repair(m: float, delta: float, r31: float) -> float:
    h, _pars = quotient_gauge_h(float(m), float(delta), float(r31))
    return max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))


def optimize_window(name: str) -> tuple[np.ndarray, float]:
    res = differential_evolution(
        lambda z: bundle_repair(*map(float, z)),
        [WINDOWS[name], CORE_DELTA, CORE_R31],
        seed=0,
        polish=True,
        maxiter=120,
        popsize=15,
        tol=1.0e-7,
    )
    return np.asarray(res.x, dtype=float), float(res.fun)


def directional_signature(point: np.ndarray, step: float = 1.0e-3) -> tuple[float, float, float]:
    m, delta, r31 = map(float, point)
    base = bundle_repair(m, delta, r31)
    dm = bundle_repair(m - step, delta, r31) - base
    dr = bundle_repair(m, delta, r31 + step) - base
    sec_delta = bundle_repair(m, delta + step, r31) - 2.0 * base + bundle_repair(m, delta - step, r31)
    return float(dm), float(dr), float(sec_delta)


def part1_the_three_broad_bundle_minima_are_boundary_controlled() -> tuple[float, dict[str, np.ndarray], dict[str, float]]:
    print("\n" + "=" * 88)
    print("PART 1: THE THREE BROAD-BUNDLE MINIMA ARE BOUNDARY-CONTROLLED")
    print("=" * 88)

    pref = float(repair_from_slack_point(PREFERRED_RECOVERED_LIFT))
    points: dict[str, np.ndarray] = {}
    values: dict[str, float] = {}

    check(
        "The preferred recovered floor is unchanged on the compact branch",
        abs(pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"preferred={pref:.12f}",
    )

    for name in WINDOWS:
        point, value = optimize_window(name)
        points[name] = point
        values[name] = value
        expected_point = EXPECTED_MINIMA[name]
        expected_value = EXPECTED_MIN_REPAIRS[name]

        check(
            f"The {name} broad-box minimizer is reproduced stably by global refinement",
            np.linalg.norm(point - expected_point) < 5.0e-6 and abs(value - expected_value) < 1.0e-9,
            f"(point,value)=({np.round(point, 8)},{value:.12f})",
        )
        check(
            f"The {name} broad-box minimizer sits on the upper-m / lower-r31 boundary corner of its box",
            abs(point[0] - WINDOWS[name][1]) < 1.0e-9 and abs(point[2] - CORE_R31[0]) < 1.0e-9,
            f"point={np.round(point, 12)}",
        )

    return pref, points, values


def part2_endpoint_and_split1_are_dominated_but_split2_is_not(
    pref: float,
    values: dict[str, float],
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: ENDPOINT AND SPLIT-1 ARE DOMINATED, BUT SPLIT-2 IS NOT")
    print("=" * 88)

    gaps = {name: values[name] - pref for name in WINDOWS}

    check(
        "The endpoint broad-box minimum stays safely above the preferred recovered floor",
        gaps["endpoint"] > 0.0,
        f"endpoint_gap={gaps['endpoint']:.12e}",
    )
    check(
        "The split-1 broad-box minimum also stays safely above the preferred recovered floor",
        gaps["split_1"] > 0.0,
        f"split1_gap={gaps['split_1']:.12e}",
    )
    check(
        "The split-2 broad-box minimum falls below the preferred recovered floor on the same exact bundle domain",
        gaps["split_2"] < 0.0,
        f"split2_gap={gaps['split_2']:.12e}",
    )
    check(
        "So broad exact-bundle dominance cannot be the right global carrier-side theorem target",
        gaps["endpoint"] > 0.0 and gaps["split_1"] > 0.0 and gaps["split_2"] < 0.0,
        f"gaps={ {k: round(v, 9) for k, v in gaps.items()} }",
    )

    print()
    for name in WINDOWS:
        print(f"  {name:8s}: repair={values[name]:.12f}  gap={gaps[name]:.12e}")


def part3_all_three_broad_box_minima_are_locally_boundary_controlled(
    points: dict[str, np.ndarray]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: ALL THREE BROAD-BOX MINIMA ARE LOCALLY BOUNDARY-CONTROLLED")
    print("=" * 88)

    signatures = {name: directional_signature(point) for name, point in points.items()}

    for name, (dm, dr, sec_delta) in signatures.items():
        check(
            f"The {name} broad-box minimizer increases when moved inward in m and r31, with positive delta curvature",
            dm > 0.0 and dr > 0.0 and sec_delta > 0.0,
            f"(dm,dr,sec_delta)=({dm:.12e},{dr:.12e},{sec_delta:.12e})",
        )

    check(
        "So the broad-bundle split between endpoint/split-1 and split-2 is about floor level, not about missing local control",
        all(dm > 0.0 and dr > 0.0 and sec > 0.0 for dm, dr, sec in signatures.values()),
        f"signatures={ {k: tuple(round(v, 9) for v in vals) for k, vals in signatures.items()} }",
    )


def part4_the_note_records_the_window_trichotomy(values: dict[str, float], pref: float) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE WINDOW TRICHOTOMY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_BUNDLE_WINDOW_TRICHOTOMY_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the three broad-box minima and their comparison to the preferred floor",
        f"{values['endpoint']:.12f}" in note
        and f"{values['split_1']:.12f}" in note
        and f"{values['split_2']:.12f}" in note
        and f"{pref:.12f}" in note,
    )
    check(
        "The note records the key conclusion that broad exact-bundle dominance fails already on split-2",
        "broad exact-bundle dominance is not the right carrier-side theorem target" in note
        and "split-2" in note,
    )
    check(
        "The note keeps the boundary honest: this is a candidate, not theorem closure",
        "not an interval-certified theorem" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE BUNDLE-WINDOW TRICHOTOMY CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  What is the sharpest shared statement about endpoint, split-1, and split-2")
    print("  when they are viewed directly on the broad exact shift-quotient bundle?")

    pref, points, values = part1_the_three_broad_bundle_minima_are_boundary_controlled()
    part2_endpoint_and_split1_are_dominated_but_split2_is_not(pref, values)
    part3_all_three_broad_box_minima_are_locally_boundary_controlled(points)
    part4_the_note_records_the_window_trichotomy(values, pref)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Broad exact-bundle window trichotomy:")
    print("    - endpoint: boundary-controlled and above the preferred floor")
    print("    - split-1: boundary-controlled and above the preferred floor")
    print("    - split-2: boundary-controlled but below the preferred floor")
    print("  RESULT: broad exact-bundle dominance is insufficient; the finer exact")
    print("  carrier restriction is doing real work on the carrier side.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
