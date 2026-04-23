#!/usr/bin/env python3
"""
Planck-scale horizon entropy lane verifier.

This runner encodes the current lane verdict honestly:
the admitted carrier class does not yield an exact 1/4 coefficient.
It closes instead to the Widom-Gioev-Klich class.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_bh_entropy_rt_ratio_widom import (  # noqa: E402
    fit_asymptote,
    measure_rt,
    widom_2d_diamond_straight_cut,
    widom_3d_cubic_straight_cut_monte_carlo,
)


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def main() -> None:
    print("=" * 72)
    print("Planck-Scale Horizon Entropy Lane Audit")
    print("=" * 72)
    print()
    print("Lane verdict: the current admissible carrier class does not admit an")
    print("exact 1/4 coefficient route.  The honest closure is a Widom-class")
    print("no-go / classification, not a black-hole 1/4 derivation.")
    print()

    t0 = time.time()

    print("-" * 72)
    print("Part 1. Analytic carrier coefficients")
    print("-" * 72)
    c2d = widom_2d_diamond_straight_cut()
    print(f"  c_Widom(2D) = {c2d:.10f}")
    check("2D carrier pins 1/6 exactly",
          abs(c2d - 1.0 / 6.0) < 1e-12,
          f"value = {c2d:.10f}")
    check("2D carrier is not 1/4",
          abs(c2d - 0.25) > 0.05,
          f"|1/6 - 1/4| = {abs(c2d - 0.25):.6f}")

    c3d = widom_3d_cubic_straight_cut_monte_carlo(n_samples=120_000)
    print(f"  c_Widom(3D) = {c3d:.6f}  (Monte Carlo, N = 1.2e5)")
    check("3D carrier stays well away from 1/4",
          0.08 < c3d < 0.15,
          f"value = {c3d:.6f}")

    print()
    print("-" * 72)
    print("Part 2. Small finite-L audit on the current 2D carrier")
    print("-" * 72)
    L_list = [8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64]
    print(f"  {'L':>4s} {'chi_eff':>8s} {'S_ent':>10s} {'r(L)':>10s}")
    print("  " + "-" * 38)
    records = []
    for L in L_list:
        r = measure_rt(L)
        print(f"  {r['L']:>4d} {r['chi_eff']:>8d} {r['S']:>10.4f} {r['rt']:>10.4f}")
        records.append(r)

    c_inf, a = fit_asymptote(records, L_min=32)
    dev6 = abs(c_inf - 1.0 / 6.0) / (1.0 / 6.0)
    dev4 = abs(c_inf - 0.25) / 0.25
    print()
    print(f"  tail fit: c_inf = {c_inf:.6f}, a = {a:+.4f}")
    print(f"  dev from 1/6 = {dev6:.2%}")
    print(f"  dev from 1/4 = {dev4:.2%}")

    print()
    print("-" * 72)
    print("Part 3. Verdict checks")
    print("-" * 72)
    check("tail fit is closer to 1/6 than to 1/4",
          dev6 < dev4,
          f"dev(1/6) = {dev6:.2%}, dev(1/4) = {dev4:.2%}")
    check("tail fit is acceptably near Widom 1/6",
          dev6 < 0.10,
          f"dev(1/6) = {dev6:.2%}")
    check("tail fit is not close to 1/4",
          dev4 > 0.20,
          f"dev(1/4) = {dev4:.2%}")
    check("finite-L ratio remains below 1/4 by the tail end",
          records[-1]["rt"] < 0.25,
          f"r({records[-1]['L']}) = {records[-1]['rt']:.4f}")

    check("LANE VERDICT: no exact 1/4 route on current carriers",
          abs(c2d - 1.0 / 6.0) < 1e-12 and dev4 > 0.20,
          "current carrier class closes to a sharper Widom no-go")

    print()
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print()
    print(f"Runtime: {time.time() - t0:.1f} s")

    if FAIL_COUNT:
        sys.exit(1)

    print()
    print("All checks passed.")
    print("Current admissible carriers do not give an exact 1/4 coefficient.")
    print("The retained closure is a Widom-class no-go / classification.")
    sys.exit(0)


if __name__ == "__main__":
    main()
