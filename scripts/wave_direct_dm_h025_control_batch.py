#!/usr/bin/env python3
"""Run a small H=0.25 control ladder for one direct-dM family/seed pair.

This closes the biggest gap on the fine-H branch: the current H=0.25
family-pair notes are one-strength replays. This script adds the exact
S=0 null and the same weak-field ladder used on the coarse retained lane.
"""

from __future__ import annotations

import argparse
import gc
from statistics import mean

from wave_direct_dm_matched_history_probe import FAMILIES, measure_dm

STRENGTHS = (0.0, 0.002, 0.004, 0.008)


def _family_specs(label: str) -> tuple[str, float, float]:
    for family_label, drift, restore in FAMILIES:
        if family_label == label:
            return family_label, drift, restore
    raise SystemExit(f"unknown family label: {label}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", default="Fam2", help="Family label. Default: Fam2")
    parser.add_argument("--seed", type=int, default=1, help="Grow seed. Default: 1")
    parser.add_argument("--h", type=float, default=0.25, help="Resolution. Default: 0.25")
    args = parser.parse_args()

    family_label, drift, restore = _family_specs(args.family)
    rows = []

    print("=" * 108)
    print("WAVE DIRECT-DM H=0.25 CONTROL BATCH")
    print("=" * 108)
    print(f"family={family_label} drift={drift:.2f} restore={restore:.2f} seed={args.seed} H={args.h:.3f}")
    print("Exact null plus weak-field ladder on one predeclared fine-H pair")
    print()

    for strength in STRENGTHS:
        r = measure_dm(args.h, strength, family_label, drift, restore, seed=args.seed)
        rows.append(r)
        print(f"[strength={strength:.6f}]")
        print(f"  NL={r['NL']}  PW={r['PW']:.3f}  src_layer={r['src_layer']}")
        print(f"  start_z_real={r['iz_start_real']:.3f}  end_z_real={r['iz_end_real']:.3f}")
        print(f"  dM(early)    = {r['d_early']:+.6f}")
        print(f"  dM(late)     = {r['d_late']:+.6f}")
        print(f"  delta_hist   = {r['delta_hist']:+.6f}")
        print(f"  R_hist       = {r['r_hist']:+.2%}")
        if abs(strength) <= 1e-12:
            print("  null         = exact S=0 control")
        else:
            print(f"  delta_hist/s = {r['delta_hist'] / strength:+.6f}")
        print()
        gc.collect()

    null_max = max(abs(r["delta_hist"]) for r in rows if abs(r["strength"]) <= 1e-12)
    scaled = [r["delta_hist"] / r["strength"] for r in rows if r["strength"] > 0]
    spread = (max(abs(v) for v in scaled) - min(abs(v) for v in scaled)) / max(mean(abs(v) for v in scaled), 1e-12)

    print("=" * 108)
    print("SUMMARY")
    print("=" * 108)
    print(f"null max |delta_hist| = {null_max:.3e}")
    print(f"delta_hist sign pattern = {' '.join('-' if r['delta_hist'] < 0 else '+' if r['delta_hist'] > 0 else '0' for r in rows if r['strength'] > 0)}")
    print(f"|delta_hist/s| spread   = {spread:+.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
