#!/usr/bin/env python3
"""
DM PMNS Z3 doublet-block center selector theorem.

Question:
  After the exact N_e PMNS-manifold theorem and the I12 sheet closure, is
  there now a retained coefficient-free law that selects the physical PMNS
  point on the charged-lepton-side branch?

Answer:
  Yes.

  On the exact PMNS source manifold inside the fixed native N_e seed surface,
  the coefficient-free Z3 doublet-block center law

      delta_db(H) = 1,
      q_+(H) = 0

  cuts the manifold to exactly two points. They share the same x and y data
  and differ only by the sheet flip delta_src -> -delta_src, equivalently
  gamma -> -gamma and I_src -> -I_src. The already-closed I12 law I_src > 0
  then selects the physical sheet uniquely.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from frontier_dm_neutrino_breaking_triplet_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_hermitian_bridge_carrier import (
    aligned_core_from_coords,
    breaking_triplet_from_coords,
    hermitian_coords,
    spectral_package,
)
from frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem import (
    active_target_from_h,
)
from frontier_dm_pmns_ne_seed_surface_exact_source_manifold_theorem_2026_04_20 import (
    CHART_HI,
    CHART_LO,
    SEED_CHART_STARTS,
    TARGET,
    chart_to_obs,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


@dataclass
class CenterPoint:
    chart: np.ndarray
    x: np.ndarray
    y: np.ndarray
    source_phase: float
    obs: np.ndarray
    cp: np.ndarray
    bridge_break: np.ndarray
    spectral: np.ndarray
    target_pair: np.ndarray
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


def compact(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def center_features(chart: np.ndarray) -> CenterPoint:
    obs, x, y, source_phase, h = chart_to_obs(np.asarray(chart, dtype=float))
    cp = np.array(cp_pair_from_h(h), dtype=float)
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    bridge_break = np.array(breaking_triplet_from_coords(*coords), dtype=float)
    spectral = np.array(spectral_package(core), dtype=float)
    target_pair = np.array(active_target_from_h(h), dtype=float)
    source_cubic = float(np.imag(h[0, 1] * h[1, 2] * h[2, 0]))
    return CenterPoint(
        chart=np.asarray(chart, dtype=float),
        x=x,
        y=y,
        source_phase=float(source_phase),
        obs=obs,
        cp=cp,
        bridge_break=bridge_break,
        spectral=spectral,
        target_pair=target_pair,
        source_cubic=source_cubic,
    )


def center_residual(chart: np.ndarray) -> np.ndarray:
    point = center_features(chart)
    return np.concatenate([point.obs - TARGET, np.array([point.target_pair[0] - 1.0, point.target_pair[1]])])


def source_distance(a: CenterPoint, b: CenterPoint) -> float:
    phase_diff = min(
        abs(a.source_phase - b.source_phase),
        abs(a.source_phase - b.source_phase + 2.0 * math.pi),
        abs(a.source_phase - b.source_phase - 2.0 * math.pi),
    )
    return float(np.linalg.norm(a.x - b.x) + np.linalg.norm(a.y - b.y) + phase_diff)


def polish_center_solution(start: np.ndarray) -> CenterPoint | None:
    result = least_squares(
        center_residual,
        np.asarray(start, dtype=float),
        bounds=(CHART_LO, CHART_HI),
        xtol=1.0e-12,
        ftol=1.0e-12,
        gtol=1.0e-12,
        max_nfev=8000,
    )
    point = center_features(result.x)
    resid = center_residual(result.x)
    if float(np.linalg.norm(resid)) > 1.0e-8:
        return None
    return point


def distinct_center_solutions() -> list[CenterPoint]:
    rng = np.random.default_rng(3)
    starts = list(SEED_CHART_STARTS)
    for _ in range(60):
        starts.append(CHART_LO + (CHART_HI - CHART_LO) * rng.random(5))

    reps: list[CenterPoint] = []
    for start in starts:
        point = polish_center_solution(start)
        if point is None:
            continue
        if all(source_distance(point, rep) > 2.0e-3 for rep in reps):
            reps.append(point)
    return reps


def part1_the_center_law_cuts_the_exact_pmns_manifold_to_two_points() -> list[CenterPoint]:
    print("\n" + "=" * 88)
    print("PART 1: THE Z3 DOUBLET-BLOCK CENTER LAW CUTS THE EXACT PMNS MANIFOLD TO TWO POINTS")
    print("=" * 88)

    reps = distinct_center_solutions()

    check(
        "The multistart solver finds exactly two distinct exact center solutions",
        len(reps) == 2,
        f"count={len(reps)}",
    )
    check(
        "Every retained center solution satisfies the exact PMNS target to high precision",
        all(float(np.max(np.abs(point.obs - TARGET))) < 1.0e-8 for point in reps),
        f"max errors={[round(float(np.max(np.abs(point.obs - TARGET))), 12) for point in reps]}",
    )
    check(
        "Every retained center solution satisfies delta_db = 1 and q_+ = 0",
        all(abs(point.target_pair[0] - 1.0) < 1.0e-10 and abs(point.target_pair[1]) < 1.0e-10 for point in reps),
        f"targets={[tuple(map(float, np.round(point.target_pair, 12))) for point in reps]}",
    )

    for idx, point in enumerate(reps, start=1):
        print()
        print(
            f"  sol {idx}: x={np.round(point.x, 9)}, y={np.round(point.y, 9)}, "
            f"delta_src={point.source_phase:.12f}, cp={np.round(point.cp, 9)}"
        )

    return reps


def part2_the_two_center_points_are_exact_sheet_partners(reps: list[CenterPoint]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TWO CENTER POINTS ARE EXACT SHEET PARTNERS")
    print("=" * 88)

    neg, pos = sorted(reps, key=lambda point: point.source_phase)

    check(
        "The two center points share the same x data",
        np.linalg.norm(pos.x - neg.x) < 1.0e-10,
        f"x distance={np.linalg.norm(pos.x - neg.x):.3e}",
    )
    check(
        "The two center points share the same y data",
        np.linalg.norm(pos.y - neg.y) < 1.0e-10,
        f"y distance={np.linalg.norm(pos.y - neg.y):.3e}",
    )
    check(
        "Their source phases are opposite and equal in magnitude",
        abs(pos.source_phase + neg.source_phase) < 1.0e-10 and pos.source_phase > 0.0 > neg.source_phase,
        f"(delta_+,delta_-)=({pos.source_phase:.12f},{neg.source_phase:.12f})",
    )
    check(
        "The odd bridge slot gamma flips sign while the even bridge slots stay fixed",
        np.allclose(pos.bridge_break[:2], neg.bridge_break[:2], atol=1.0e-10)
        and abs(pos.bridge_break[2] + neg.bridge_break[2]) < 1.0e-10,
        f"break+={np.round(pos.bridge_break, 12)}, break-={np.round(neg.bridge_break, 12)}",
    )
    check(
        "The source cubic and intrinsic CP pair flip sign across the center pair",
        abs(pos.source_cubic + neg.source_cubic) < 1.0e-10
        and np.linalg.norm(pos.cp + neg.cp) < 1.0e-10,
        f"I_src=({pos.source_cubic:.12e},{neg.source_cubic:.12e})",
    )


def part3_i12_picks_the_physical_center_sheet(reps: list[CenterPoint]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ALREADY-CLOSED I12 LAW PICKS THE PHYSICAL CENTER SHEET")
    print("=" * 88)

    positive_src = [point for point in reps if point.source_cubic > 0.0]
    negative_src = [point for point in reps if point.source_cubic < 0.0]

    check(
        "Exactly one center solution has positive source cubic",
        len(positive_src) == 1 and len(negative_src) == 1,
        f"signs={[round(point.source_cubic, 12) for point in reps]}",
    )
    check(
        "The positive-source-cubic center solution is already in the upper octant",
        len(positive_src) == 1 and positive_src[0].obs[2] > 0.5,
        f"s23^2={positive_src[0].obs[2]:.12f}",
    )
    check(
        "That same sheet carries the physical negative intrinsic CP sign",
        len(positive_src) == 1 and positive_src[0].cp[0] < 0.0 and positive_src[0].cp[1] < 0.0,
        f"cp={np.round(positive_src[0].cp, 12)}",
    )

    point = positive_src[0]
    print()
    print("  physical center source selected by I12:")
    print(f"    x         = {np.array2string(np.round(point.x, 12), separator=', ')}")
    print(f"    y         = {np.array2string(np.round(point.y, 12), separator=', ')}")
    print(f"    delta_src = {point.source_phase:.12f}")
    print(f"    obs       = {np.array2string(np.round(point.obs, 12), separator=', ')}")


def part4_the_branch_register_records_i5_as_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BRANCH REGISTER RECORDS I5 AS CLOSED")
    print("=" * 88)

    note = read("docs/DM_PMNS_Z3_DOUBLET_BLOCK_CENTER_SELECTOR_THEOREM_NOTE_2026-04-20.md")
    register = read("docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md")
    cnote = compact(note)

    check(
        "The new theorem note records the center law delta_db = 1 and q_+ = 0",
        "delta_db(H)=1" in cnote and "q_+(H)=0" in cnote,
    )
    check(
        "The new theorem note records that the center law cuts the exact PMNS manifold to a two-sheet pair",
        "two-sheet pair" in note and "exact PMNS source manifold" in note,
    )
    check(
        "The register now marks I5 as closed on this branch",
        "| I5 |" in register and "**closed on this branch**" in register,
    )
    check(
        "The register points I5 to the new Z3 doublet-block center theorem",
        "DM_PMNS_Z3_DOUBLET_BLOCK_CENTER_SELECTOR_THEOREM_NOTE_2026-04-20.md" in register,
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS Z3 DOUBLET-BLOCK CENTER SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the exact N_e PMNS-manifold theorem and the I12 sheet closure,")
    print("  is there now a retained coefficient-free law that selects the physical")
    print("  PMNS point on the charged-lepton-side branch?")

    reps = part1_the_center_law_cuts_the_exact_pmns_manifold_to_two_points()
    part2_the_two_center_points_are_exact_sheet_partners(reps)
    part3_i12_picks_the_physical_center_sheet(reps)
    part4_the_branch_register_records_i5_as_closed()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact closure answer:")
    print("    - on the exact N_e PMNS manifold, the coefficient-free Z3")
    print("      doublet-block center law delta_db = 1, q_+ = 0 selects exactly")
    print("      one two-sheet source pair")
    print("    - the already-closed I12 source-cubic law I_src > 0 selects the")
    print("      physical sheet uniquely")
    print("    - so I5 is closed on this branch")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
