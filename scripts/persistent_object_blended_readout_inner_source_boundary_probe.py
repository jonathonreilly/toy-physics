#!/usr/bin/env python3
"""Inner-source boundary probe for the widened blended-readout compact lane."""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.persistent_object_blended_readout_transfer_sweep import _run_mode


@dataclass(frozen=True)
class Case:
    label: str
    phys_l: int
    phys_w: int
    source_z: float


CASES = (
    Case("source0.75", 6, 3, 0.75),
    Case("source1.00", 6, 3, 1.00),
    Case("source1.25", 6, 3, 1.25),
    Case("source1.50", 6, 3, 1.50),
)


def main() -> None:
    t0 = time.time()
    print("=" * 122)
    print("PERSISTENT OBJECT BLENDED READOUT INNER SOURCE BOUNDARY PROBE")
    print("  top3 compact object under the retained blended readout across the inward source boundary")
    print("=" * 122)
    print()

    passes = 0
    for case in CASES:
        row = _run_mode(case, 3)
        alpha_str = "[" + ",".join(
            f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.step_alpha
        ) + "]"
        print(
            f"{case.label:>10s}  source_z={case.source_z:>4.2f}  "
            f"min_ov={row.min_overlap:0.3f}  mean_ov={row.mean_overlap:0.3f}  "
            f"capture={row.mean_capture:0.3f}  max_drift={row.max_kappa_drift:0.3%}  "
            f"step_alpha={alpha_str}  admissible={row.admissible}"
        )
        passes += int(row.admissible)

    print()
    print("SUMMARY")
    print(f"  top3 admissible on {passes}/{len(CASES)} inward-source boundary rows")
    print()
    print("SAFE READ")
    print("  - If the lane reopens quickly above source1.0, the second-ring miss is a mapped inner-source boundary rather than a broad collapse.")
    print("  - If it stays closed across several inward rows, the widened regime remains source-placement fragile.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
