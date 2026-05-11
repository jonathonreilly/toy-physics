#!/usr/bin/env python3
"""
Open-boundary Wilson two-body refined sweep — extends sides 11..19.

Goal:
  Reproduce the 25-run sweep documented in
  `docs/WILSON_TWO_BODY_OPEN_REFINED_NOTE_2026-04-11.md`. The parent
  `frontier_wilson_two_body_open.py` covers sides {11, 13} and d {3..6};
  this refined variant extends to sides {11, 13, 15, 17, 19} with d up
  to the largest interior separation per side, then power-law fits the
  clean attractive subset.

Hypothesis (from the note):
  On the clean attractive subset:
    - global exponent     ~ -3.669  (R^2 ~ 0.9896)
    - per-side exponents:
        side=11: -3.139   (R^2 ~ 0.9968)
        side=13: -3.313   (R^2 ~ 0.9960)
        side=15: -3.500   (R^2 ~ 0.9939)
        side=17: -3.671   (R^2 ~ 0.9920)
        side=19: -3.837   (R^2 ~ 0.9899)

  All 25 configs ATTRACT + CLEAN (SNR > 2).

Class-A assertions verify the global and per-side exponents to the
rounding precision quoted by the note, plus the all-ATTRACT-all-CLEAN
claim.

Compute: ~4 minutes wall-clock; AUDIT_TIMEOUT_SEC = 600 declared
below to avoid the 120s default ceiling.
"""

from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np

# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 600` means the
# audit-lane precompute and live audit runner allow up to 10 min of
# wall time before recording a timeout. The 120 s default ceiling is
# tight for the 25-config side=19 inclusive sweep. See
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 600

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from frontier_wilson_two_body_open import label, run_config  # noqa: E402


SIDES = (11, 13, 15, 17, 19)
G_VAL = 5.0
MU2_VAL = 0.22


def d_range_for_side(side: int) -> range:
    """d from 3 up to the largest interior separation that fits.

    Symmetric placement: x_a = center - d//2, x_b = center + (d - d//2).
    Both must lie in [1, side-2] to leave a one-cell open boundary on each
    side for the open-lattice geometry to be meaningful. That gives:
      d_max = side - 3   (= largest interior separation)
    Capped at (side-1)//2 to match the note's "interior" framing.
    """
    return range(3, max(4, (side - 1) // 2 + 1))


def power_law_fit(d_arr: np.ndarray, abs_a_arr: np.ndarray) -> tuple[float, float, float]:
    """Log-log linear regression of |a_mut| vs d.

    Returns (exponent, intercept_log, R^2).
    """
    if len(d_arr) < 2:
        return float("nan"), float("nan"), float("nan")
    log_d = np.log(d_arr)
    log_a = np.log(abs_a_arr)
    # exponent = slope of log|a| vs log d
    slope, intercept = np.polyfit(log_d, log_a, 1)
    pred = slope * log_d + intercept
    ss_res = float(np.sum((log_a - pred) ** 2))
    ss_tot = float(np.sum((log_a - np.mean(log_a)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(slope), float(intercept), r2


def main() -> int:
    print("=" * 88)
    print("OPEN-BOUNDARY WILSON TWO-BODY — REFINED SWEEP")
    print(f"Sides: {SIDES}   G={G_VAL}   mu^2={MU2_VAL}")
    print("=" * 88)

    t0 = time.time()
    rows: list[dict] = []

    for side in SIDES:
        d_iter = list(d_range_for_side(side))
        for d in d_iter:
            t_cfg = time.time()
            row = run_config(side, G_VAL, MU2_VAL, d)
            mean = row["a_mutual_early_mean"]
            snr = row["snr"]
            sig, qual = label(mean, snr)
            row["signal"] = sig
            row["quality"] = qual
            rows.append(row)
            elapsed = time.time() - t_cfg
            print(
                f"side={side:2d} d={d}: a_mut={mean:+.6f} (SNR={snr:.2f}) "
                f"[{sig}] [{qual}] ({elapsed:.1f}s)"
            )

    print()
    print(f"Total compute: {time.time() - t0:.1f}s ({len(rows)} configs)")

    # ------------------------------------------------------------------
    # Aggregates
    # ------------------------------------------------------------------
    total = len(rows)
    attract = sum(1 for r in rows if r["signal"] == "ATTRACT")
    clean = sum(1 for r in rows if r["quality"] == "CLEAN")
    attract_clean = [
        r for r in rows if r["signal"] == "ATTRACT" and r["quality"] == "CLEAN"
    ]

    print()
    print("=" * 88)
    print("AGGREGATE COUNTS")
    print("=" * 88)
    print(f"  total runs:         {total}")
    print(f"  ATTRACT:            {attract}/{total}")
    print(f"  CLEAN (SNR>2):      {clean}/{total}")
    print(f"  ATTRACT and CLEAN:  {len(attract_clean)}/{total}")

    # ------------------------------------------------------------------
    # Per-side and global power-law fits on the clean attractive subset
    # ------------------------------------------------------------------
    print()
    print("=" * 88)
    print("POWER-LAW FITS ON CLEAN ATTRACTIVE SUBSET")
    print("=" * 88)

    per_side_fit: dict[int, tuple[float, float, float]] = {}
    for side in SIDES:
        sub = [r for r in attract_clean if r["side"] == side]
        if len(sub) < 2:
            print(f"  side={side}: insufficient clean rows ({len(sub)}) for fit")
            per_side_fit[side] = (float("nan"), float("nan"), float("nan"))
            continue
        d_arr = np.array([r["d"] for r in sub], dtype=float)
        abs_a_arr = np.array([abs(r["a_mutual_early_mean"]) for r in sub])
        slope, _, r2 = power_law_fit(d_arr, abs_a_arr)
        per_side_fit[side] = (slope, _, r2)
        print(f"  side={side:2d}: |a_mut| ~ d^{slope:+.3f}   (R^2 = {r2:.4f}, n={len(sub)})")

    if attract_clean:
        d_all = np.array([r["d"] for r in attract_clean], dtype=float)
        a_all = np.array([abs(r["a_mutual_early_mean"]) for r in attract_clean])
        global_slope, _, global_r2 = power_law_fit(d_all, a_all)
        print(f"  GLOBAL: |a_mut| ~ d^{global_slope:+.3f}   (R^2 = {global_r2:.4f}, n={len(attract_clean)})")
    else:
        global_slope, global_r2 = float("nan"), float("nan")

    # ------------------------------------------------------------------
    # Class-A verification asserts (verify against note's claims)
    # ------------------------------------------------------------------
    print()
    print("=" * 88)
    print("VERIFICATION ASSERTIONS")
    print("=" * 88)

    # Note's claims are quoted to 3 decimals for exponents and 4 for R^2.
    EXP_TOL = 0.005
    R2_TOL = 0.0005

    # All-ATTRACT-all-CLEAN check
    assert attract == total, (
        f"FAIL: only {attract}/{total} runs ATTRACT — note claims all should attract"
    )
    assert clean == total, (
        f"FAIL: only {clean}/{total} runs CLEAN — note claims all should be CLEAN (SNR>2)"
    )
    print(f"  PASS: {total}/{total} ATTRACT + CLEAN (matches note's 25/25 claim)")

    # Global exponent (note claims -3.669)
    expected_global_exp = -3.669
    assert math.isclose(global_slope, expected_global_exp, abs_tol=EXP_TOL), (
        f"FAIL: global exponent {global_slope:.3f} differs from "
        f"note's {expected_global_exp:.3f} by more than {EXP_TOL}"
    )
    print(
        f"  PASS: global exponent {global_slope:+.3f} matches note's "
        f"{expected_global_exp:+.3f} within tol {EXP_TOL}"
    )

    expected_global_r2 = 0.9896
    assert math.isclose(global_r2, expected_global_r2, abs_tol=R2_TOL), (
        f"FAIL: global R^2 {global_r2:.4f} differs from "
        f"note's {expected_global_r2:.4f} by more than {R2_TOL}"
    )
    print(
        f"  PASS: global R^2 {global_r2:.4f} matches note's "
        f"{expected_global_r2:.4f} within tol {R2_TOL}"
    )

    # Per-side exponents
    expected_per_side = {
        11: -3.139,
        13: -3.313,
        15: -3.500,
        17: -3.671,
        19: -3.837,
    }
    for side, exp_target in expected_per_side.items():
        slope, _, r2 = per_side_fit[side]
        if math.isnan(slope):
            print(f"  SKIP: side={side} fit is NaN")
            continue
        assert math.isclose(slope, exp_target, abs_tol=EXP_TOL), (
            f"FAIL: side={side} exponent {slope:.3f} differs from "
            f"note's {exp_target:.3f} by more than {EXP_TOL}"
        )
        print(
            f"  PASS: side={side} exponent {slope:+.3f} matches note's "
            f"{exp_target:+.3f} within tol {EXP_TOL}"
        )

    # Steeper-than-Newton check (note's main interpretive claim)
    assert global_slope < -2.0, (
        f"FAIL: global exponent {global_slope:.3f} is not steeper than "
        f"Newton's -2; note's headline claim broken"
    )
    print(
        f"  PASS: global exponent {global_slope:+.3f} is steeper than "
        f"Newton's -2 (note's headline non-Newtonian claim)"
    )

    print()
    print("=" * 88)
    print("REFINED SWEEP: PASS")
    print("=" * 88)
    return 0


if __name__ == "__main__":
    sys.exit(main())
