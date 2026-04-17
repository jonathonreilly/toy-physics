#!/usr/bin/env python3
"""Minimal H=0.25 feasibility probe for the direct-dM matched-history lane.

This is intentionally tiny:
  - one family / one geometry setup
  - one strength
  - one H point: 0.25

The probe measures whether the existing matched-history direct-dM harness is
practical enough at H=0.25 on this workstation without modifying the main
lane.
"""

from __future__ import annotations

import argparse
import resource
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from wave_direct_dm_matched_history_probe import measure_dm
from wave_retardation_continuum_limit import S_PHYS


def _rss_mb() -> float:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return raw / (1024 * 1024)
    return raw / 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strength",
        type=float,
        default=S_PHYS,
        help="Source strength to probe. Default: S_PHYS",
    )
    args = parser.parse_args()

    start = time.time()
    family_label, drift, restore = ("Fam1", 0.20, 0.70)
    row = measure_dm(0.25, args.strength, family_label, drift, restore)
    elapsed = time.time() - start
    rss_mb = _rss_mb()

    print("WAVE DIRECT-DM H=0.25 FEASIBILITY PROBE")
    print(f"family={family_label} drift={drift:.2f} restore={restore:.2f}")
    print(f"H=0.25  strength={args.strength:.6f}")
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
