#!/usr/bin/env python3
"""Exploratory legacy Lorentz-symmetry test.

This is an experiment driver, not a canonical retained symmetry/causality
claim. Use `docs/START_HERE.md` and the NN light-cone note before citing it.

The model uses several local quantities on each edge:
- coordinate delay dt (NOT invariant)
- retained update sqrt(dt² - dx²) (Lorentz invariant IF boost applies)
- spent delay dt - sqrt(dt² - dx²) (NOT invariant)
- euclidean norm sqrt(dt² + dx²) (NOT invariant)

The question: does the model's action (spent delay) have any
Lorentz-like symmetry? And does this symmetry survive on the
discrete grid where boosts aren't exact?

PStack experiment: lorentz-symmetry
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    retained_update_symmetry_test,
    lorentz_boost,
    proper_time_deficit,
    action_increment_for_mode,
)


def main() -> None:
    print("=" * 72)
    print("LORENTZ SYMMETRY TEST")
    print("=" * 72)
    print()

    # =========================================================
    # TEST 1: Run the built-in symmetry test
    # =========================================================
    print("TEST 1: Built-in retained_update_symmetry_test()")
    print()
    results = retained_update_symmetry_test()
    print(f"  {'Candidate scalar':>45s}  {'max_boost_drift':>16s}  {'invariant?':>10s}")
    print(f"  {'-' * 75}")
    for r in results:
        invariant = "YES" if r.max_boost_drift < 1e-10 else "NO"
        print(f"  {r.name:>45s}  {r.max_boost_drift:16.2e}  {invariant:>10s}")

    # =========================================================
    # TEST 2: Detailed boost analysis
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: Detailed boost analysis of each scalar")
    print("=" * 72)
    print()

    dt, dx = 2.0, 1.0  # Example edge: delay=2, length=1
    velocities = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]

    print(f"  Base edge: dt={dt}, dx={dx}")
    print(f"  retained_update = sqrt(dt²-dx²) = {math.sqrt(dt**2 - dx**2):.6f}")
    print(f"  spent_delay = dt - sqrt(dt²-dx²) = {dt - math.sqrt(dt**2 - dx**2):.6f}")
    print()

    print(f"  {'velocity':>8s}  {'dt_boosted':>10s}  {'dx_boosted':>10s}  "
          f"{'retained':>10s}  {'spent':>10s}  {'euclidean':>10s}  {'coord_dt':>10s}")
    print(f"  {'-' * 72}")

    for v in velocities:
        dt_b, dx_b = lorentz_boost(dt, dx, v)
        retained = math.sqrt(max(dt_b ** 2 - dx_b ** 2, 0.0))
        spent = dt_b - retained
        euclidean = math.sqrt(dt_b ** 2 + dx_b ** 2)
        print(f"  {v:8.1f}  {dt_b:10.6f}  {dx_b:10.6f}  "
              f"{retained:10.6f}  {spent:10.6f}  {euclidean:10.6f}  {dt_b:10.6f}")

    # =========================================================
    # TEST 3: Which action modes are boost-invariant?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 3: Action mode invariance under boosts")
    print("=" * 72)
    print()

    action_modes = ["spent_delay", "coordinate_delay", "link_length"]
    dt, dx = 2.0, 1.0

    print(f"  {'mode':>20s}  ", end="")
    for v in [0.0, 0.3, 0.6, 0.9]:
        print(f"  v={v:.1f}", end="")
    print(f"  {'max_drift':>10s}  {'invariant?':>10s}")
    print(f"  {'-' * 80}")

    for mode in action_modes:
        base_action = action_increment_for_mode(dt, dx, mode, 1.0)
        max_drift = 0.0
        print(f"  {mode:>20s}  ", end="")
        for v in [0.0, 0.3, 0.6, 0.9]:
            dt_b, dx_b = lorentz_boost(dt, dx, v)
            link_len_b = abs(dx_b)
            boosted_action = action_increment_for_mode(dt_b, link_len_b, mode, 1.0)
            drift = abs(boosted_action - base_action)
            max_drift = max(max_drift, drift)
            print(f"  {boosted_action:6.4f}", end="")
        invariant = "YES" if max_drift < 1e-10 else "NO"
        print(f"  {max_drift:10.2e}  {invariant:>10s}")

    # =========================================================
    # TEST 4: Does the retained update survive on the discrete grid?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 4: Retained update on discrete grid edges")
    print("=" * 72)
    print()
    print("  On the grid, edges have specific (dx, dy) offsets:")
    print("  horizontal: (1,0), vertical: (0,1), diagonal: (1,1)")
    print("  With delay = link_length * (1 + field), the retained update is:")
    print("  sqrt(delay² - link_length²) = link_length * sqrt((1+field)² - 1)")
    print("  = link_length * sqrt(field² + 2*field)")
    print()
    print("  For small field: retained ≈ link_length * sqrt(2*field)")
    print("  For large field: retained ≈ link_length * field")
    print()

    for edge_type, link_len in [("horizontal (1,0)", 1.0),
                                  ("diagonal (1,1)", math.sqrt(2)),
                                  ("vertical (0,1)", 1.0)]:
        print(f"  {edge_type}, link_length = {link_len:.4f}:")
        for field_val in [0.0, 0.01, 0.1, 0.5, 1.0, 2.0]:
            delay = link_len * (1.0 + field_val)
            retained = math.sqrt(max(delay ** 2 - link_len ** 2, 0.0))
            spent = delay - retained
            print(f"    field={field_val:.2f}: delay={delay:.4f}, "
                  f"retained={retained:.4f}, spent={spent:.4f}, "
                  f"retained/delay={retained/delay:.4f}")
        print()

    # =========================================================
    # TEST 5: Signal speed = 1 verification
    # =========================================================
    print("=" * 72)
    print("TEST 5: Is signal speed = 1? (delay = link_length at field=0)")
    print("=" * 72)
    print()

    for link_len in [1.0, math.sqrt(2)]:
        delay_at_zero = link_len * (1.0 + 0.0)
        print(f"  link_length = {link_len:.4f}: delay(field=0) = {delay_at_zero:.4f}, "
              f"ratio = {delay_at_zero/link_len:.4f}")
        if abs(delay_at_zero / link_len - 1.0) < 1e-10:
            print(f"    → Signal speed = link_length / delay = 1.000 (exact)")
        else:
            print(f"    → Signal speed = {link_len / delay_at_zero:.4f}")

    print()
    print("  In the presence of gravity (field > 0):")
    print("  delay = link_length * (1 + field) > link_length")
    print("  → Signal slows down near massive objects (gravitational time dilation)")
    print()

    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
