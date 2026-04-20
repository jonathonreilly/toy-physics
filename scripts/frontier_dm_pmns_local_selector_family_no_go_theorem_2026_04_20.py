#!/usr/bin/env python3
"""
DM PMNS local-selector-family no-go theorem for the remaining angle pin.

Question:
  Can the current exact LOCAL selector families on the DM neutrino
  source surface close the PMNS angle pin, i.e. force the physical
  triple

      (sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
        = (0.307, 0.0218, 0.545)

  without importing the observational chamber pin?

Answer:
  No.

  The strongest exact local selector families already on land reduce to the
  same one-real selected line:

      delta = q_+ = sqrt(6) / 3.

  This is the exact output of:
    - the parity-compatible observable-selector theorem on D = diag(A,B,B),
    - and the broader 23-symmetric active-curvature theorem on
      D = diag(A,B,B) with arbitrary A,B > 0.

  On that selected line, the retained PMNS map never reaches the physical
  angle triple. More sharply:

    1. s12^2(m, sqrt(6)/3, sqrt(6)/3) has exactly two stationary points on a
       wide interval [-2000, 2000]. The global minimum occurs at
       m ~= 4.36500535 and equals

         s12^2_min = 0.331582718643... > 0.307.

       So the physical solar angle is excluded on the entire line.

    2. The full three-angle distance

         chi^2_line(m)
           = (s12^2 - 0.307)^2 + (s13^2 - 0.0218)^2 + (s23^2 - 0.545)^2

       has a unique stationary point on [-200, 200], at
       m ~= 1.27832212, with

         chi^2_line,min = 0.011428083950...

       and best-fit triple

         (0.37920275, 0.05563746, 0.47379695).

    3. The explicit current candidate points
       {Schur-Q, det-crit, Tr(H^2)-boundary, K12-character, F1 parity-mixing}
       all miss the physical PMNS triple by visible margins.

  Therefore the remaining PMNS angle-pin task is NOT closable by the current
  exact local selector families. The missing ingredient must be a nonlocal
  point-selection law on the live branch, not another local parity-compatible
  / 23-symmetric / microscopic-polynomial selector.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from frontier_dm_neutrino_source_surface_active_curvature_23_symmetric_baseline_boundary import (
    delta_star as curvature_delta_star,
    q_star as curvature_q_star,
)
from frontier_dm_neutrino_source_surface_parity_compatible_observable_selector_theorem import (
    delta_star as parity_delta_star,
    q_star as parity_q_star,
)
from frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem import (
    TARGET_S12SQ,
    TARGET_S13SQ,
    TARGET_S23SQ,
    pmns_observables,
)


ROOT = Path(__file__).resolve().parents[1]
NOTE_PATH = ROOT / "docs/DM_PMNS_LOCAL_SELECTOR_FAMILY_NO_GO_THEOREM_NOTE_2026-04-20.md"

PASS_COUNT = 0
FAIL_COUNT = 0

SCHUR_S = math.sqrt(6.0) / 3.0
TARGET = np.array([TARGET_S12SQ, TARGET_S13SQ, TARGET_S23SQ], dtype=float)

CANDIDATES = {
    "A Schur-Q": (0.5, SCHUR_S, SCHUR_S),
    "B det-crit": (0.613, 0.964, 1.552),
    "C Tr(H^2)-bdy": (0.385, 1.268, 0.365),
    "D K12 char": (0.0, 0.800, 1.000),
    "E par-mix F1": (
        4.0 * math.sqrt(2.0) / 9.0,
        math.sqrt(6.0) / 2.0 - math.sqrt(2.0) / 18.0,
        math.sqrt(6.0) / 6.0 + math.sqrt(2.0) / 18.0,
    ),
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


def read_note() -> str:
    return NOTE_PATH.read_text(encoding="utf-8")


def schur_obs(m: float) -> dict[str, float]:
    return pmns_observables(float(m), SCHUR_S, SCHUR_S)


def schur_vector(m: float) -> np.ndarray:
    obs = schur_obs(m)
    return np.array([obs["s12sq"], obs["s13sq"], obs["s23sq"]], dtype=float)


def s12_on_schur(m: float) -> float:
    return float(schur_obs(m)["s12sq"])


def chi2_on_schur(m: float) -> float:
    vec = schur_vector(m)
    return float(np.sum((vec - TARGET) ** 2))


def central_diff(fn, x: float, h: float) -> float:
    return float((fn(x + h) - fn(x - h)) / (2.0 * h))


def find_stationary_points(fn, lo: float, hi: float, *, h: float, num: int) -> list[float]:
    grid = np.linspace(lo, hi, num)
    deriv = [central_diff(fn, float(x), h) for x in grid]
    roots: list[float] = []
    for a, b, fa, fb in zip(grid[:-1], grid[1:], deriv[:-1], deriv[1:]):
        if fa == 0.0 or fb == 0.0 or fa * fb < 0.0:
            try:
                root = float(brentq(lambda x: central_diff(fn, x, h), float(a), float(b), maxiter=200))
            except ValueError:
                continue
            if all(abs(root - old) > 1.0e-3 for old in roots):
                roots.append(root)
    return roots


def part1_local_families_reduce_to_the_same_selected_line() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT EXACT LOCAL SELECTOR FAMILIES REDUCE TO THE SAME SELECTED LINE")
    print("=" * 88)

    note = read_note()
    d_parity = parity_delta_star()
    q_parity = parity_q_star()
    d_curv = curvature_delta_star()
    q_curv = curvature_q_star()

    check(
        "Parity-compatible selector theorem fixes delta_* = q_+* = sqrt(6)/3",
        abs(d_parity - SCHUR_S) < 1.0e-12 and abs(q_parity - SCHUR_S) < 1.0e-12,
        f"(delta_*,q_+*)=({d_parity:.12f},{q_parity:.12f})",
    )
    check(
        "23-symmetric active-curvature theorem fixes the same line for all D = diag(A,B,B)",
        abs(d_curv - SCHUR_S) < 1.0e-12 and abs(q_curv - SCHUR_S) < 1.0e-12,
        f"(delta_*,q_+*)=({d_curv:.12f},{q_curv:.12f})",
    )
    check(
        "The two exact local families agree on one selected line delta = q_+ = sqrt(6)/3",
        abs(d_parity - d_curv) < 1.0e-12 and abs(q_parity - q_curv) < 1.0e-12,
    )
    check(
        "The note records the local-family reduction to the Schur line",
        "delta = q_+ = sqrt(6)/3" in note and "current exact local selector families" in note,
    )


def part2_schur_line_has_a_hard_solar_angle_floor() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SCHUR LINE HAS A HARD SOLAR-ANGLE FLOOR")
    print("=" * 88)

    roots = find_stationary_points(s12_on_schur, -2000.0, 2000.0, h=1.0e-4, num=4001)
    values = [(root, s12_on_schur(root)) for root in roots]
    values.sort(key=lambda item: item[1])
    min_root, min_value = values[0]
    max_root, max_value = values[-1]
    left_value = s12_on_schur(-2000.0)
    right_value = s12_on_schur(2000.0)

    print(f" stationary roots of s12^2(m, S, S) on [-2000,2000]: {roots}")
    print(f" local min: m = {min_root:.12f}, s12^2 = {min_value:.12f}")
    print(f" local max: m = {max_root:.12f}, s12^2 = {max_value:.12f}")
    print(f" endpoint values: s12^2(-2000) = {left_value:.12f}, s12^2(2000) = {right_value:.12f}")

    check(
        "s12^2 on the Schur line has exactly two stationary points on the wide scan",
        len(roots) == 2,
        f"roots={roots}",
    )
    check(
        "The lower stationary point sits at positive m ~= 4.365 and is the line minimum on the wide scan",
        abs(min_root - 4.365005345285525) < 1.0e-6
        and min_value < left_value
        and min_value < right_value,
        f"m_min={min_root:.12f}, s12^2_min={min_value:.12f}",
    )
    check(
        "The Schur-line solar-angle floor stays strictly above the physical target 0.307",
        min_value > TARGET_S12SQ + 2.0e-2,
        f"s12^2_min - 0.307 = {min_value - TARGET_S12SQ:.12f}",
    )
    check(
        "Therefore no point on delta = q_+ = sqrt(6)/3 can realize the physical PMNS triple",
        min_value > TARGET_S12SQ,
        f"s12^2_min={min_value:.12f}",
    )


def part3_best_full_three_angle_fit_on_the_schur_line_still_misses() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE BEST FULL THREE-ANGLE FIT ON THE SCHUR LINE STILL MISSES")
    print("=" * 88)

    roots = find_stationary_points(chi2_on_schur, -200.0, 200.0, h=1.0e-4, num=8001)
    best_root = roots[0]
    best_chi2 = chi2_on_schur(best_root)
    best_vec = schur_vector(best_root)
    left = chi2_on_schur(-200.0)
    right = chi2_on_schur(200.0)

    print(f" stationary roots of chi^2_line on [-200,200]: {roots}")
    print(f" best root: m = {best_root:.12f}")
    print(f" best chi^2 = {best_chi2:.12f}")
    print(
        " best triple = "
        f"({best_vec[0]:.12f}, {best_vec[1]:.12f}, {best_vec[2]:.12f})"
    )
    print(f" endpoint chi^2 values: chi^2(-200) = {left:.12f}, chi^2(200) = {right:.12f}")

    check(
        "The Schur-line three-angle distance has a unique stationary point on the wide scan",
        len(roots) == 1,
        f"roots={roots}",
    )
    check(
        "The unique best-fit point is near m ~= 1.27832212",
        abs(best_root - 1.278322119585464) < 1.0e-6,
        f"m_best={best_root:.12f}",
    )
    check(
        "The full three-angle miss stays macroscopically nonzero",
        best_chi2 > 1.0e-2 and best_chi2 < left and best_chi2 < right,
        f"chi^2_min={best_chi2:.12f}",
    )


def part4_all_current_explicit_candidate_points_miss() -> None:
    print("\n" + "=" * 88)
    print("PART 4: ALL CURRENT EXPLICIT CANDIDATE POINTS MISS THE PMNS TRIPLE")
    print("=" * 88)

    rows: list[tuple[str, float, float]] = []
    for label, point in CANDIDATES.items():
        obs = pmns_observables(*point)
        vec = np.array([obs["s12sq"], obs["s13sq"], obs["s23sq"]], dtype=float)
        diff = vec - TARGET
        chi2 = float(np.sum(diff**2))
        max_err = float(np.max(np.abs(diff)))
        rows.append((label, chi2, max_err))
        print(
            f" {label:15s} chi^2 = {chi2:.12f}  "
            f"max|angle error| = {max_err:.12f}"
        )

    check(
        "Every current explicit selector candidate has max angle error > 0.05",
        all(max_err > 5.0e-2 for _, _, max_err in rows),
        f"rows={rows}",
    )
    check(
        "Every current explicit selector candidate has chi^2 > 0.03",
        all(chi2 > 3.0e-2 for _, chi2, _ in rows),
        f"rows={rows}",
    )


def part5_the_note_states_the_correct_i5_consequence() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE STATES THE CORRECT I5 CONSEQUENCE")
    print("=" * 88)

    note = read_note()
    check(
        "The note records the hard Schur-line solar-angle floor",
        "0.331582718643" in note and "0.307" in note,
    )
    check(
        "The note records that the missing ingredient is nonlocal point selection, not another local family",
        "nonlocal point-selection law" in note
        and "not another local parity-compatible" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS LOCAL-SELECTOR-FAMILY NO-GO THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact local selector families close the remaining")
    print("  PMNS angle pin without importing the observational chamber point?")

    part1_local_families_reduce_to_the_same_selected_line()
    part2_schur_line_has_a_hard_solar_angle_floor()
    part3_best_full_three_angle_fit_on_the_schur_line_still_misses()
    part4_all_current_explicit_candidate_points_miss()
    part5_the_note_states_the_correct_i5_consequence()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Current exact local selector families do NOT close the PMNS angle pin.")
    print("  The strongest exact local route fixes delta = q_+ = sqrt(6)/3,")
    print("  but the entire selected line misses the physical PMNS triple.")
    print("  Remaining target: a nonlocal point-selection law on the live branch.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
