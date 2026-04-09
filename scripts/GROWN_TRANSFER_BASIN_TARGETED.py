#!/usr/bin/env python3
"""Targeted narrow-basin replay around the retained grown-row positives.

This runner keeps the claim surface tiny:

- fixed-field signed-source transfer on nearby grown rows
- exact grown-row complex-action carryover on the same nearby rows

It is intentionally not a family-wide sweep. The goal is to test whether the
retained moderate-drift positives survive on a small neighborhood of nearby
grown rows.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.GROWN_TRANSFER_BASIN_SWEEP import _score_row


ROWS = [
    (0.15, 0.60),
    (0.20, 0.60),
    (0.20, 0.70),
    (0.25, 0.80),
]


def main() -> None:
    print("=" * 92)
    print("GROWN TRANSFER BASIN TARGETED")
    print("  narrow neighborhood around the retained grown-row positives")
    print("=" * 92)
    print("rows:", ROWS)
    print()
    print(
        f"{'drift':>5s} {'restore':>7s} {'zero':>12s} {'neutral':>12s} "
        f"{'plus':>12s} {'exp':>7s} {'g0':>12s} {'F0':>6s} {'F05':>6s} {'toward':>11s}"
    )
    print("-" * 104)

    survivors = 0
    for drift, restore in ROWS:
        row = _score_row(drift, restore)
        print(
            f"{drift:5.2f} {restore:7.2f} "
            f"{row.signed_zero:+12.3e} {row.signed_neutral:+12.3e} "
            f"{row.signed_single:+12.3e} {row.signed_exponent:7.3f} "
            f"{row.action_gamma0:+12.3e} {row.action_fm0:6.3f} "
            f"{row.action_fm05:6.3f} {row.action_toward!s:>11s}"
        )

        signed_ok = (
            abs(row.signed_zero) < 1e-12
            and abs(row.signed_neutral) < 1e-12
            and row.signed_single != 0.0
            and abs(row.signed_exponent - 1.0) < 0.05
        )
        complex_ok = (
            abs(row.action_gamma0) < 1e-12
            and row.action_fm0 > 0.99
            and row.action_fm05 > 0.99
        )
        if signed_ok and complex_ok:
            survivors += 1

    print()
    print("SAFE READ")
    print(f"  nearby rows surviving both observables: {survivors}/{len(ROWS)}")
    if survivors:
        print("  the retained grown-row positives survive on a narrow nearby basin")
    else:
        print("  the retained positives do not survive this nearby basin")


if __name__ == "__main__":
    main()
