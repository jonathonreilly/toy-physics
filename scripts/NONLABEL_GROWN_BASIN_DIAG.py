#!/usr/bin/env python3
"""Tiny basin diagnostic for the grown-row non-label signed-source transfer.

This is the fast follow-up to NONLABEL_GROWN_BASIN_SWEEP.py. It checks only
seed 0 across the minimal 3x3 neighborhood around the retained grown row so we
can tell quickly whether the geometry-sector transfer is a small basin or just
the single retained row.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.NONLABEL_GROWN_BASIN_SWEEP import (
    DRIFTS,
    RESTORES,
    RowResult,
    _build_geometry_sector_grown,
    _measure_family,
    grow,
)


SEED = 0


def main() -> None:
    print("=" * 88)
    print("NON-LABEL GROWN BASIN DIAG")
    print(f"  seed={SEED}, drifts={DRIFTS}, restores={RESTORES}")
    print("=" * 88)
    rows: list[RowResult] = []
    for drift in DRIFTS:
        for restore in RESTORES:
            pos, adj, layers = grow(drift, restore, SEED)
            sector_adj = _build_geometry_sector_grown(pos, layers)
            zero, plus, minus, neutral, double, exponent = _measure_family(pos, sector_adj, layers)
            row = RowResult(
                drift=drift,
                restore=restore,
                seed=SEED,
                zero=zero,
                plus=plus,
                minus=minus,
                neutral=neutral,
                double=double,
                exponent=exponent,
            )
            rows.append(row)
            print(
                f"{drift:>4.2f} {restore:>4.2f} | "
                f"zero={zero:+.3e} plus={plus:+.3e} minus={minus:+.3e} "
                f"neutral={neutral:+.3e} double={double:+.3e} exp={exponent:>5.3f} "
                f"{'YES' if row.signed_ok else 'no'}"
            )

    passed = [r for r in rows if r.signed_ok]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        print("  this is a bounded positive basin on seed 0")
    else:
        print("  this is a clean no-go on seed 0")


if __name__ == "__main__":
    main()
