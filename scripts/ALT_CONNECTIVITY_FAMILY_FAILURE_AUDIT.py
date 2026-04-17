#!/usr/bin/env python3
"""Failure audit for the alternative connectivity family.

This diagnoses why some rows in the alt-family basin fail:
- zero-control leakage?
- neutral-cancellation leakage?
- sign-orientation flip?
- nonlinear scaling?
"""

from __future__ import annotations

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ALT_CONNECTIVITY_FAMILY_BASIN import DRIFTS, SEEDS, _measure


def main() -> None:
    print("=" * 92)
    print("ALT CONNECTIVITY FAMILY FAILURE AUDIT")
    print("=" * 92)
    reasons = {
        "zero": 0,
        "neutral": 0,
        "orientation": 0,
        "scaling": 0,
    }
    failures = []

    for drift in DRIFTS:
        for seed in SEEDS:
            zero, plus, minus, neutral, double, exponent, ok = _measure(drift, seed)
            if ok:
                continue
            if abs(zero) >= 1e-12:
                reasons["zero"] += 1
            if abs(neutral) >= 1e-12:
                reasons["neutral"] += 1
            if not (plus > 0.0 and minus < 0.0):
                reasons["orientation"] += 1
            if abs(exponent - 1.0) >= 0.05:
                reasons["scaling"] += 1
            failures.append((drift, seed, zero, plus, minus, neutral, double, exponent))

    print("Failure reasons:")
    for key in ["zero", "neutral", "orientation", "scaling"]:
        print(f"  {key:>11s}: {reasons[key]}")

    print()
    print("Representative failures:")
    for drift, seed, zero, plus, minus, neutral, double, exponent in failures[:8]:
        print(
            f"  drift={drift:.2f} seed={seed} "
            f"zero={zero:+.3e} plus={plus:+.3e} minus={minus:+.3e} "
            f"neutral={neutral:+.3e} exp={exponent:.3f}"
        )

    print()
    if reasons["orientation"] and not reasons["zero"] and not reasons["neutral"] and not reasons["scaling"]:
        print("SAFE READ")
        print("  the misses are a pure sign-orientation boundary, not a control leak")
    else:
        print("SAFE READ")
        print("  the misses involve more than sign orientation")


if __name__ == "__main__":
    main()
