#!/usr/bin/env python3
"""Direct-dM portability batch for the matched-schedule lane.

This is the first honest portability batch for the direct-dM fallback:

  - three retained grown families
  - multiple seeds
  - exact S=0 null
  - weak-field sweep
  - both retained H values

The retained single-family Fam1 probe remains the primary artifact for
the direct-dM lane. This batch is a bounded portability test.
"""

from __future__ import annotations

import argparse
import gc
import math
from collections import defaultdict
from statistics import mean

from wave_direct_dm_matched_history_probe import FAMILIES, measure_dm


def _spread_ratio(values: list[float]) -> float:
    mags = [abs(v) for v in values if abs(v) > 1e-12]
    if not mags:
        return math.nan
    center = mean(mags)
    if center <= 1e-12:
        return math.nan
    return (max(mags) - min(mags)) / center


def _fmt_pct(value: float) -> str:
    return "n/a" if math.isnan(value) else f"{value:+.2%}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5, 0.35],
        help="H values to probe. Default: 0.5 0.35",
    )
    parser.add_argument(
        "--strengths",
        type=float,
        nargs="*",
        default=[0.0, 0.002, 0.004, 0.008],
        help="Strengths to probe. Default: 0 0.002 0.004 0.008",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="*",
        default=[0, 1],
        help="Seeds to probe. Default: 0 1",
    )
    args = parser.parse_args()

    rows = []
    print("=" * 118)
    print("WAVE DIRECT-DM PORTABILITY BATCH")
    print("=" * 118)
    print("Three retained grown families, two seeds, exact null, weak-field sweep, matched-schedule direct response")
    print()

    for label, drift, restore in FAMILIES:
        print(f"[family={label} drift={drift:.2f} restore={restore:.2f}]")
        for seed in args.seeds:
            print(f"  [seed={seed}]")
            for strength in args.strengths:
                print(f"    [strength={strength:.6f}]")
                for h_val in args.hs:
                    r = measure_dm(h_val, strength, label, drift, restore, seed=seed)
                    rows.append(r)
                    suffix = (
                        "null"
                        if abs(strength) <= 1e-12
                        else f"delta/s={r['delta_hist'] / strength:+.6f}"
                    )
                    print(
                        f"      H={h_val:.3f} "
                        f"dE={r['d_early']:+.6f} "
                        f"dL={r['d_late']:+.6f} "
                        f"delta={r['delta_hist']:+.6f} "
                        f"R={r['r_hist']:+.2%} "
                        f"{suffix}"
                    )
                    gc.collect()
            print()
        print()

    print("=" * 118)
    print("SUMMARY")
    print("=" * 118)

    null_rows = [r for r in rows if abs(r["strength"]) <= 1e-12]
    ref_rows = [r for r in rows if abs(r["strength"] - 0.004) <= 1e-12]
    nonzero_rows = [r for r in rows if r["strength"] > 0]

    if null_rows:
        max_null = max(abs(r["delta_hist"]) for r in null_rows)
        print(f"null max |delta_hist| = {max_null:.3e}")
    print()

    print("reference strength s=0.004")
    print(f"{'family':<6s} {'H':>6s} {'signs':>8s} {'R mean':>12s} {'R min':>12s} {'R max':>12s}")
    by_family_h = defaultdict(list)
    for r in ref_rows:
        by_family_h[(r["family"], r["H"])].append(r)
    for (family, h_val), group in sorted(by_family_h.items()):
        rs = [g["r_hist"] for g in group]
        signs = "".join("+" if v > 0 else "-" if v < 0 else "0" for v in rs)
        print(
            f"{family:<6s} {h_val:6.3f} {signs:>8s} "
            f"{mean(rs):+12.2%} {min(rs):+12.2%} {max(rs):+12.2%}"
        )
    print()

    print("linearity spread on |delta_hist/s| over nonzero strengths")
    print(f"{'family':<6s} {'seed':>4s} {'H':>6s} {'spread':>12s}")
    by_family_seed_h = defaultdict(list)
    for r in nonzero_rows:
        by_family_seed_h[(r["family"], r["seed"], r["H"])].append(r)
    for (family, seed, h_val), group in sorted(by_family_seed_h.items()):
        scaled = [g["delta_hist"] / g["strength"] for g in sorted(group, key=lambda x: x["strength"])]
        print(f"{family:<6s} {seed:4d} {h_val:6.3f} {_fmt_pct(_spread_ratio(scaled)):>12s}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
