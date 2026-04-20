#!/usr/bin/env python3
"""
DM PMNS Z3 doublet-block center positive-sheet no-go theorem.

Question:
  Does the coefficient-free center law

      delta_db(H) = 1,
      q_+(H) = 0,

  together with the already-closed sheet selector I_src(H) > 0, close the
  remaining PMNS angle-pin I5 on the fixed native N_e seed surface?

Answer:
  No.

  On the fixed native N_e seed surface, the positive-sheet center system still
  has many distinct exact solutions. The center pair has rank 2 on the
  verified patch, so the locus is locally 3-real, and the PMNS angle triple
  varies macroscopically along it. The center law is therefore useful only as
  a conditional cut on the exact PMNS target manifold, not as a native I5
  closure by itself.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from frontier_dm_pmns_ne_seed_surface_exact_source_manifold_theorem_2026_04_20 import (
    CHART_HI,
    CHART_LO,
    SEED_CHART_STARTS,
    TARGET,
    chart_to_obs,
)
from frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem import (
    active_target_from_h,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


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


def center_features(chart: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    obs, _x, _y, _delta_src, h = chart_to_obs(np.asarray(chart, dtype=float))
    delta_db, q_plus = active_target_from_h(h)
    source_cubic = float(np.imag(h[0, 1] * h[1, 2] * h[2, 0]))
    return obs, float(delta_db), float(q_plus), source_cubic


def center_residual(chart: np.ndarray) -> np.ndarray:
    _obs, delta_db, q_plus, _cubic = center_features(chart)
    return np.array([delta_db - 1.0, q_plus], dtype=float)


def center_target_residual(chart: np.ndarray) -> np.ndarray:
    obs, delta_db, q_plus, _cubic = center_features(chart)
    return np.concatenate([obs - TARGET, np.array([delta_db - 1.0, q_plus], dtype=float)])


def finite_jacobian(fun, chart: np.ndarray, eps: float = 1.0e-6) -> np.ndarray:
    chart = np.asarray(chart, dtype=float)
    f0 = np.asarray(fun(chart), dtype=float)
    jac = np.zeros((len(f0), len(chart)), dtype=float)
    for idx in range(len(chart)):
        step = np.zeros_like(chart)
        step[idx] = eps
        jac[:, idx] = (fun(chart + step) - fun(chart - step)) / (2.0 * eps)
    return jac


def collect_positive_center_points() -> list[dict[str, np.ndarray | float | int]]:
    rng = np.random.default_rng(7)
    starts = list(SEED_CHART_STARTS)
    for _ in range(18):
        starts.append(CHART_LO + (CHART_HI - CHART_LO) * rng.random(5))

    reps: list[dict[str, np.ndarray | float | int]] = []
    for start in starts:
        result = least_squares(
            center_residual,
            np.asarray(start, dtype=float),
            bounds=(CHART_LO, CHART_HI),
            xtol=1.0e-12,
            ftol=1.0e-12,
            gtol=1.0e-12,
            max_nfev=3000,
        )
        obs, delta_db, q_plus, source_cubic = center_features(result.x)
        if np.linalg.norm([delta_db - 1.0, q_plus]) > 1.0e-8 or source_cubic <= 0.0:
            continue
        chart = np.asarray(result.x, dtype=float)
        if all(np.linalg.norm(chart - rep["chart"]) > 1.0e-3 for rep in reps):
            jac = finite_jacobian(center_residual, chart)
            reps.append(
                {
                    "chart": chart,
                    "obs": obs,
                    "delta_db": delta_db,
                    "q_plus": q_plus,
                    "source_cubic": source_cubic,
                    "rank": int(np.linalg.matrix_rank(jac, tol=1.0e-5)),
                }
            )
    return reps


def collect_conditional_center_pairs() -> list[dict[str, np.ndarray | float]]:
    rng = np.random.default_rng(5)
    starts = list(SEED_CHART_STARTS)
    for _ in range(10):
        starts.append(CHART_LO + (CHART_HI - CHART_LO) * rng.random(5))

    reps: list[dict[str, np.ndarray | float]] = []
    for start in starts:
        result = least_squares(
            center_target_residual,
            np.asarray(start, dtype=float),
            bounds=(CHART_LO, CHART_HI),
            xtol=1.0e-11,
            ftol=1.0e-11,
            gtol=1.0e-11,
            max_nfev=4000,
        )
        if float(np.linalg.norm(center_target_residual(result.x))) > 1.0e-8:
            continue
        obs, _delta_db, _q_plus, source_cubic = center_features(result.x)
        _obs2, x, y, delta_src, _h = chart_to_obs(result.x)
        item = np.concatenate([x, y, [delta_src]])
        if all(np.linalg.norm(item - rep["item"]) > 1.0e-4 for rep in reps):
            reps.append(
                {
                    "item": item,
                    "obs": obs,
                    "x": x,
                    "y": y,
                    "delta_src": float(delta_src),
                    "source_cubic": source_cubic,
                }
            )
    return reps


def part1_positive_sheet_center_locus_is_not_a_point_selector() -> list[dict[str, np.ndarray | float | int]]:
    print("\n" + "=" * 88)
    print("PART 1: THE POSITIVE-SHEET CENTER LAW IS NOT A POINT SELECTOR")
    print("=" * 88)

    reps = collect_positive_center_points()
    obs = np.array([rep["obs"] for rep in reps], dtype=float)

    check(
        "The verifier finds many distinct positive-sheet center solutions",
        len(reps) >= 8,
        f"count={len(reps)}",
    )
    check(
        "Every retained representative satisfies the exact center law delta_db = 1, q_+ = 0",
        all(abs(float(rep["delta_db"]) - 1.0) < 1.0e-10 and abs(float(rep["q_plus"])) < 1.0e-10 for rep in reps),
    )
    check(
        "Every retained representative lies on the positive I_src sheet",
        all(float(rep["source_cubic"]) > 0.0 for rep in reps),
        f"cubic values={[round(float(rep['source_cubic']), 9) for rep in reps[:6]]}",
    )
    check(
        "The PMNS angle triple varies macroscopically across the positive-sheet center locus",
        float(obs[:, 0].max() - obs[:, 0].min()) > 0.5
        and float(obs[:, 1].max() - obs[:, 1].min()) > 0.4
        and float(obs[:, 2].max() - obs[:, 2].min()) > 0.8,
        (
            f"ranges="
            f"({obs[:,0].min():.6f},{obs[:,0].max():.6f}) × "
            f"({obs[:,1].min():.6f},{obs[:,1].max():.6f}) × "
            f"({obs[:,2].min():.6f},{obs[:,2].max():.6f})"
        ),
    )

    for idx, rep in enumerate(reps[:4], start=1):
        print(f"  rep {idx}: obs={np.round(rep['obs'], 6)}, I_src={float(rep['source_cubic']):.9f}")

    return reps


def part2_center_constraints_have_rank_two_on_the_verified_patch(
    reps: list[dict[str, np.ndarray | float | int]]
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CENTER CONSTRAINTS HAVE RANK 2 ON THE VERIFIED PATCH")
    print("=" * 88)

    ranks = [int(rep["rank"]) for rep in reps[:8]]
    check(
        "At retained representative points, rank d(delta_db, q_+) = 2",
        all(rank == 2 for rank in ranks),
        f"ranks={ranks}",
    )
    check(
        "So on the verified patch the center law cuts the 5-real seed surface to a local 3-real locus",
        all(rank == 2 for rank in ranks),
        "dim(seed surface)=5 and dim(center pair)=2",
    )


def part3_conditional_intersection_with_the_exact_pmns_target_is_discrete() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CONDITIONAL VALUE — CENTER LAW CUTS THE EXACT TARGET TO A TWO-SHEET PAIR")
    print("=" * 88)

    reps = collect_conditional_center_pairs()
    reps = sorted(reps, key=lambda rep: float(rep["delta_src"]))

    check(
        "If the exact PMNS target is imposed as well, the center law yields exactly two source solutions",
        len(reps) == 2,
        f"count={len(reps)}",
    )
    check(
        "The two conditional solutions have the same x and y data",
        len(reps) == 2
        and np.linalg.norm(np.asarray(reps[0]["x"]) - np.asarray(reps[1]["x"])) < 1.0e-10
        and np.linalg.norm(np.asarray(reps[0]["y"]) - np.asarray(reps[1]["y"])) < 1.0e-10,
    )
    check(
        "They differ only by the sheet flip delta_src -> -delta_src and I_src -> -I_src",
        len(reps) == 2
        and abs(float(reps[0]["delta_src"]) + float(reps[1]["delta_src"])) < 1.0e-10
        and abs(float(reps[0]["source_cubic"]) + float(reps[1]["source_cubic"])) < 1.0e-10,
        (
            f"delta_src=({float(reps[0]['delta_src']):.12f},"
            f"{float(reps[1]['delta_src']):.12f})"
        ) if len(reps) == 2 else "",
    )


def part4_note_records_the_correct_status() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE CORRECT NO-GO STATUS")
    print("=" * 88)

    note = read("docs/DM_PMNS_Z3_DOUBLET_BLOCK_CENTER_POSITIVE_SHEET_NO_GO_THEOREM_NOTE_2026-04-20.md")
    register = read("docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md")

    check(
        "The new note states that center law + I12 does not close I5",
        "does **not** close `I5`" in note or "does **not** close I5" in note,
    )
    check(
        "The note records the local 3-real positive-sheet center locus",
        "local `3`-real" in note or "local 3-real" in note,
    )
    check(
        "The register still treats I5 as open after the center-law test",
        "| I5 |" in register and "point-selection law" in register and "retained observational input" in register,
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS Z3 DOUBLET-BLOCK CENTER POSITIVE-SHEET NO-GO THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the coefficient-free center law delta_db = 1, q_+ = 0, together")
    print("  with the already-closed I12 sign law I_src > 0, close the remaining")
    print("  PMNS angle-pin I5 on the fixed native N_e seed surface?")

    reps = part1_positive_sheet_center_locus_is_not_a_point_selector()
    part2_center_constraints_have_rank_two_on_the_verified_patch(reps)
    part3_conditional_intersection_with_the_exact_pmns_target_is_discrete()
    part4_note_records_the_correct_status()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Honest status:")
    print("    - center law + I12 leaves a positive-sheet 3-real locus and does not")
    print("      derive the PMNS target by itself")
    print("    - the center law is still useful conditionally: once the exact PMNS")
    print("      target manifold is imposed, it cuts that manifold to a two-sheet pair")
    print("    - so I5 remains open, but the live missing object is now sharper than")
    print("      before")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
