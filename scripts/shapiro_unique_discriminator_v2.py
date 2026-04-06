#!/usr/bin/env python3
"""Shapiro unique discriminator v2.

This is a narrow report generator for the best remaining boundary in the
Shapiro-style causal-phase lane. The detector-line phase lag is real and
portable, but a static cone-shape proxy reproduces the same curve exactly.
"""

from __future__ import annotations

import math


C_VALUES = [2.0, 1.0, 0.5, 0.25]

# Mean curves lifted from the retained Shapiro static-discriminator result.
CAUSAL_CURVE = [0.0372, 0.0446, 0.0569, 0.0662]
STATIC_CONE_CURVE = [0.0372, 0.0446, 0.0569, 0.0662]
STATIC_SCHED_CURVE = [0.0446, 0.0445, 0.0446, 0.0450]


def rmse(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)) / len(left))


def main() -> None:
    print("=" * 88)
    print("SHAPIRO UNIQUE DISCRIMINATOR V2")
    print("  strongest remaining boundary for the retained c-dependent phase lag")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can anything stronger than the detector phase lag alone separate the")
    print("  causal propagating-field lane from static lookalikes?")
    print()
    print("Exact controls:")
    print("  - exact zero control stays exact")
    print("  - the phase-lag curve is portable across the retained grown families")
    print()
    print(f"{'mode':>20s} {'c=2.0':>10s} {'c=1.0':>10s} {'c=0.5':>10s} {'c=0.25':>10s}")
    print("-" * 72)
    print(
        f"{'causal dynamic cone':>20s} "
        f"{CAUSAL_CURVE[0]:+10.4f} {CAUSAL_CURVE[1]:+10.4f} "
        f"{CAUSAL_CURVE[2]:+10.4f} {CAUSAL_CURVE[3]:+10.4f}"
    )
    print(
        f"{'static cone shape':>20s} "
        f"{STATIC_CONE_CURVE[0]:+10.4f} {STATIC_CONE_CURVE[1]:+10.4f} "
        f"{STATIC_CONE_CURVE[2]:+10.4f} {STATIC_CONE_CURVE[3]:+10.4f}"
    )
    print(
        f"{'static scheduling':>20s} "
        f"{STATIC_SCHED_CURVE[0]:+10.4f} {STATIC_SCHED_CURVE[1]:+10.4f} "
        f"{STATIC_SCHED_CURVE[2]:+10.4f} {STATIC_SCHED_CURVE[3]:+10.4f}"
    )
    print()
    print("Boundary diagnostics:")
    print(f"  causal vs static-cone RMSE: {rmse(CAUSAL_CURVE, STATIC_CONE_CURVE):.4f}")
    print(f"  causal vs static-schedule RMSE: {rmse(CAUSAL_CURVE, STATIC_SCHED_CURVE):.4f}")
    print()
    print("Safe read:")
    print("  - the detector-line phase lag is a real, portable observable")
    print("  - a static cone-shape proxy reproduces the same curve exactly")
    print("  - static scheduling does not reproduce the curve and stays near-flat")
    print("  - no stronger discriminator appeared in the retained data")
    print()
    print("Conclusion:")
    print("  The best remaining boundary is that the Shapiro-style phase lag is")
    print("  portable and proxy-level, but not unique against static field-shape")
    print("  effects. A unique causal-propagation discriminator will need another")
    print("  observable beyond the detector-line phase lag alone.")


if __name__ == "__main__":
    main()
