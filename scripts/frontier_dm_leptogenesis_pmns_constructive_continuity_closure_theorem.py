#!/usr/bin/env python3
"""
DM leptogenesis PMNS constructive continuity closure theorem.

Question:
  Does the constructive projected-source chamber on the fixed native N_e seed
  surface contain an exact eta/eta_obs = 1 point, or only an overshooting
  witness?

Answer:
  It contains an exact closure point.

  On the explicit interpolation family from the aligned native seed point to
  the constructive projected-source witness,

      (x,y,delta)(lambda)
        = (1-lambda) (x_seed,y_seed,0) + lambda (x_w,y_w,delta_w),

  the fixed native seed averages stay exact, the favored constructive column is
  continuous, and

      eta_1(0)  < 1 < eta_1(1).

  Therefore a lambda_* in (0,1) exists with eta_1(lambda_*) = 1. At that same
  point the projected-source triplet still satisfies gamma > 0, E1 > 0, and
  E2 > 0.

  So the constructive PMNS chamber contains an exact eta = eta_obs closure
  point on the current branch.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem import (
    WITNESS_DELTA,
    WITNESS_X,
    WITNESS_Y,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    XBAR_NE,
    YBAR_NE,
    eta_columns_from_active,
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


def seed_point() -> tuple[np.ndarray, np.ndarray, float]:
    return np.full(3, XBAR_NE, dtype=float), np.full(3, YBAR_NE, dtype=float), 0.0


def path_point(lam: float) -> tuple[np.ndarray, np.ndarray, float]:
    x_seed, y_seed, delta_seed = seed_point()
    x = (1.0 - lam) * x_seed + lam * WITNESS_X
    y = (1.0 - lam) * y_seed + lam * WITNESS_Y
    delta = (1.0 - lam) * delta_seed + lam * WITNESS_DELTA
    return x, y, float(delta)


def path_triplet(lam: float) -> dict[str, float]:
    x, y, delta = path_point(lam)
    h = canonical_h(x, y, delta)
    responses = hermitian_linear_responses(h)
    return triplet_from_projected_response_pack(responses)


def constructive_column_eta(lam: float) -> float:
    x, y, delta = path_point(lam)
    etas = eta_columns_from_active(x, y, delta)[1]
    return float(etas[1])


def part1_the_constructive_interpolation_family_stays_on_the_exact_native_seed_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CONSTRUCTIVE INTERPOLATION FAMILY STAYS ON THE FIXED SEED SURFACE")
    print("=" * 88)

    x_seed, y_seed, delta_seed = seed_point()
    x_one, y_one, delta_one = path_point(1.0)
    x_mid, y_mid, delta_mid = path_point(0.5)

    check(
        "The lambda = 0 endpoint is the exact aligned native seed point",
        np.linalg.norm(x_seed - np.full(3, XBAR_NE)) < 1e-12
        and np.linalg.norm(y_seed - np.full(3, YBAR_NE)) < 1e-12
        and abs(delta_seed) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_seed):.12f},{np.mean(y_seed):.12f})",
    )
    check(
        "The lambda = 1 endpoint is the exact constructive projected-source witness",
        np.linalg.norm(x_one - WITNESS_X) < 1e-12
        and np.linalg.norm(y_one - WITNESS_Y) < 1e-12
        and abs(delta_one - WITNESS_DELTA) < 1e-12,
        f"delta_w={delta_one:.12f}",
    )
    check(
        "Every interpolation point stays on the exact fixed native seed surface",
        abs(np.mean(x_mid) - XBAR_NE) < 1e-12
        and abs(np.mean(y_mid) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_mid):.12f},{np.mean(y_mid):.12f})",
    )


def part2_the_constructive_column_crosses_exact_closure_along_that_family() -> float:
    print("\n" + "=" * 88)
    print("PART 2: THE CONSTRUCTIVE COLUMN CROSSES EXACT CLOSURE")
    print("=" * 88)

    eta0 = constructive_column_eta(0.0)
    eta1 = constructive_column_eta(1.0)
    lam_star = brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0)
    eta_star = constructive_column_eta(lam_star)

    check(
        "On the aligned seed point the constructive column is still below exact closure",
        eta0 < 1.0,
        f"eta_1(0)={eta0:.12f}",
    )
    check(
        "On the constructive witness the same column overshoots exact closure",
        eta1 > 1.0,
        f"eta_1(1)={eta1:.12f}",
    )
    check(
        "Therefore continuity gives a lambda_* in (0,1) with eta_1(lambda_*) = 1",
        0.0 < lam_star < 1.0 and abs(eta_star - 1.0) < 1e-12,
        f"lambda_*={lam_star:.12f}",
    )

    print()
    print(f"  eta_1(0)      = {eta0:.12f}")
    print(f"  eta_1(1)      = {eta1:.12f}")
    print(f"  lambda_*      = {lam_star:.12f}")
    print(f"  eta_1(lambda_*) = {eta_star:.12f}")

    return lam_star


def part3_the_closure_point_is_still_constructive() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT CLOSURE POINT IS STILL CONSTRUCTIVE")
    print("=" * 88)

    lam_star = brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0)
    x_star, y_star, delta_star = path_point(lam_star)
    etas_star = eta_columns_from_active(x_star, y_star, delta_star)[1]
    triplet = path_triplet(lam_star)

    check(
        "The exact closure point remains genuinely off-seed and phase-oriented",
        np.linalg.norm(x_star - np.full(3, XBAR_NE)) > 1e-6
        and np.linalg.norm(y_star - np.full(3, YBAR_NE)) > 1e-6
        and abs(delta_star) > 1e-6,
        f"delta_*={delta_star:.12f}",
    )
    check(
        "At lambda_* the projected-source triplet still satisfies gamma > 0, E1 > 0, and E2 > 0",
        triplet["gamma"] > 0.0 and triplet["E1"] > 0.0 and triplet["E2"] > 0.0,
        f"(gamma,E1,E2)=({triplet['gamma']:.12f},{triplet['E1']:.12f},{triplet['E2']:.12f})",
    )
    check(
        "So the exact eta = 1 point lies inside the constructive projected-source chamber",
        abs(etas_star[1] - 1.0) < 1e-12 and triplet["gamma"] > 0.0 and triplet["E1"] > 0.0 and triplet["E2"] > 0.0,
        f"eta={np.round(etas_star, 12)}",
    )

    print()
    print(f"  x_*     = {np.round(x_star, 12)}")
    print(f"  y_*     = {np.round(y_star, 12)}")
    print(f"  delta_* = {delta_star:.12f}")
    print(f"  eta_*   = {np.round(etas_star, 12)}")


def part4_the_theorem_note_records_the_constructive_exact_closure_point() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE CONSTRUCTIVE CLOSURE THEOREM")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md")

    check(
        "The note records the aligned-seed to constructive-witness interpolation family",
        "aligned native seed point" in note and "constructive witness" in note and "lambda" in note,
    )
    check(
        "The note records the exact constructive eta = 1 consequence",
        "eta_1(0) < 1 < eta_1(1)" in note and "gamma > 0" in note and "E1 > 0" in note and "E2 > 0" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS CONSTRUCTIVE CONTINUITY CLOSURE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the constructive projected-source chamber on the fixed native N_e")
    print("  seed surface contain an exact eta/eta_obs = 1 point, or only an")
    print("  overshooting witness?")

    part1_the_constructive_interpolation_family_stays_on_the_exact_native_seed_surface()
    part2_the_constructive_column_crosses_exact_closure_along_that_family()
    part3_the_closure_point_is_still_constructive()
    part4_the_theorem_note_records_the_constructive_exact_closure_point()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact constructive answer:")
    print("    - the constructive projected-source chamber contains an exact eta = 1 point")
    print("    - it lies on the fixed native N_e seed surface")
    print("    - and it still satisfies gamma > 0, E1 > 0, E2 > 0")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
