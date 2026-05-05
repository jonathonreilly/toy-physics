#!/usr/bin/env python3
"""Run one H=0.25 direct-dM matched-history validation point.

This stays intentionally small for automation use:
  - one H point at a time
  - one family / seed / strength selection
  - runtime and peak RSS reported alongside the direct-dM observables

It is the reusable support entrypoint for the current H=0.25 validation
frontier, not a batch sweeper.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import resource
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from wave_direct_dm_matched_history_probe import FAMILIES, measure_dm
from wave_retardation_continuum_limit import S_PHYS


def _family_specs(label: str) -> tuple[str, float, float]:
    for family_label, drift, restore in FAMILIES:
        if family_label == label:
            return family_label, drift, restore
    raise SystemExit(f"unknown family label: {label}")


def _rss_mb() -> float:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return raw / (1024 * 1024)
    return raw / 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--family",
        default="Fam1",
        help="Family label to run. Default: Fam1",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Grow seed for the geometry. Default: 0",
    )
    parser.add_argument(
        "--strength",
        type=float,
        default=S_PHYS,
        help="Source strength to probe. Default: S_PHYS",
    )
    parser.add_argument(
        "--h",
        type=float,
        default=0.25,
        help="Resolution to probe. Default: 0.25",
    )
    args = parser.parse_args()

    family_label, drift, restore = _family_specs(args.family)
    start = time.time()
    row = measure_dm(args.h, args.strength, family_label, drift, restore, seed=args.seed)
    elapsed = time.time() - start
    rss_mb = _rss_mb()

    print("WAVE DIRECT-DM SINGLE-POINT RUNNER")
    print(f"family={family_label} drift={drift:.2f} restore={restore:.2f}")
    print(f"seed={args.seed}")
    print(f"H={args.h:.3f}  strength={args.strength:.6f}")
    print(f"NL={row['NL']}  PW={row['PW']:.3f}  src_layer={row['src_layer']}")
    print(f"start_z_real={row['iz_start_real']:.3f}  end_z_real={row['iz_end_real']:.3f}")
    print(f"dM(early)  = {row['d_early']:+.6f}")
    print(f"dM(late)   = {row['d_late']:+.6f}")
    print(f"delta_hist = {row['delta_hist']:+.6f}")
    print(f"R_hist     = {row['r_hist']:+.2%}")
    print(f"elapsed_s  = {elapsed:.2f}")
    print(f"rss_mb     = {rss_mb:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
