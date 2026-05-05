#!/usr/bin/env python3
"""Second-ring transfer sweep for the blended-readout compact object lane.

The first blended-readout sweep established that the exact-lattice top3 compact
object stays admissible across the full nearby family under one retained
readout architecture.

The next honest question is:

  Does that same top3 + blend=0.25 branch survive one ring farther out, or
  does the current positive stop at the immediate neighborhood?
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import os
import sys
import time
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.persistent_object_blended_readout_transfer_sweep import (
    BLEND,
    ModeResult,
    _run_mode,
)


@dataclass(frozen=True)
class Case:
    label: str
    phys_l: int
    phys_w: int
    source_z: float


OUTER_CASES = (
    Case("source1.0", 6, 3, 1.0),
    Case("source2.75", 6, 3, 2.75),
    Case("width5", 6, 5, 2.0),
    Case("length4", 4, 3, 2.0),
    Case("length8", 8, 3, 2.0),
)


def _print_row(row: ModeResult) -> None:
    alpha_str = "[" + ",".join(
        f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.step_alpha
    ) + "]"
    print(
        f"{row.label:>8s} {row.min_overlap:8.3f} {row.mean_overlap:8.3f} "
        f"{row.mean_detector_eff:9.2f} {row.mean_capture:8.3f} "
        f"{row.max_kappa_drift:10.3%} {alpha_str:>24s} {str(row.admissible):>6s}"
    )


def main() -> None:
    t0 = time.time()
    print("=" * 126)
    print("PERSISTENT OBJECT BLENDED READOUT OUTER TRANSFER SWEEP")
    print("  second-ring transfer of the exact-lattice top3 compact object under the retained blended readout")
    print("=" * 126)
    print(f"fixed blended readout: blend={BLEND:.2f}")
    print()

    top2_pass = 0
    top3_pass = 0

    for case in OUTER_CASES:
        print(
            f"CASE: {case.label}  (h=0.25, W={case.phys_w}, L={case.phys_l}, source_z={case.source_z})"
        )
        print(
            f"{'mode':>8s} {'min_ov':>8s} {'mean_ov':>8s} {'det_eff':>9s} "
            f"{'capture':>8s} {'max_drift':>10s} {'step α':>24s} {'adm':>6s}"
        )
        print("-" * 106)

        top2 = _run_mode(case, 2)
        top3 = _run_mode(case, 3)
        _print_row(top2)
        _print_row(top3)

        top2_pass += int(top2.admissible)
        top3_pass += int(top3.admissible)

        if top2.admissible:
            verdict = "top2 outer bridge"
        elif top3.admissible:
            verdict = "top3 outer bridge"
        else:
            verdict = "outer transfer closed"
        print(f"  verdict: {verdict}")
        print()

    total_cases = len(OUTER_CASES)
    print("SUMMARY")
    print(f"  top2 admissible on {top2_pass}/{total_cases} cases")
    print(f"  top3 admissible on {top3_pass}/{total_cases} cases")
    print()
    print("SAFE READ")
    print("  - If top3 survives most or all of this second ring, the compact-object lane is leaving the immediate neighborhood.")
    print("  - If top3 collapses quickly here, the current positive should be read as a bounded local-family result.")
    print("  - This is still a bounded exact-lattice transfer sweep, not matter closure.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
