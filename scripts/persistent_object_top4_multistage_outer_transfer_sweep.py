#!/usr/bin/env python3
"""One-ring-farther transfer sweep beyond the widened top4 multistage pocket."""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.persistent_object_top3_multistage_probe import Case, _run_case  # noqa: E402


TOP_KEEP = 4

OUTER_CASES = (
    Case("source0p50", 6, 3, 0.50),
    Case("source2p85", 6, 3, 2.85),
    Case("width6", 6, 6, 2.0),
    Case("length3", 3, 3, 2.0),
    Case("length9", 9, 3, 2.0),
)

CASE_BY_LABEL = {case.label: case for case in OUTER_CASES}


def _parse_cases(case_labels: str | None) -> tuple[Case, ...]:
    if not case_labels:
        return OUTER_CASES
    labels = [label.strip() for label in case_labels.split(",") if label.strip()]
    unknown = [label for label in labels if label not in CASE_BY_LABEL]
    if unknown:
        raise SystemExit(f"unknown case labels: {', '.join(unknown)}")
    return tuple(CASE_BY_LABEL[label] for label in labels)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top-keep",
        type=int,
        default=TOP_KEEP,
        help="Compact object width to retain per update.",
    )
    parser.add_argument(
        "--case-labels",
        default="",
        help="Comma-separated case labels. Defaults to the full beyond-pocket sweep.",
    )
    args = parser.parse_args()
    cases = _parse_cases(args.case_labels)

    t0 = time.time()
    print("=" * 140)
    print("PERSISTENT OBJECT TOP4 MULTISTAGE OUTER TRANSFER SWEEP")
    print("  one ring farther than the widened exact-lattice pocket on the retained multistage floor")
    print("=" * 140)
    print(f"top_keep={args.top_keep}, cases={','.join(case.label for case in cases)}")
    print()

    passes = 0
    for case in cases:
        row = _run_case(case, args.top_keep)
        passes += int(row.admissible)
        overlap_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_mean_overlap) + "]"
        carry_mean_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_carry_mean) + "]"
        carry_min_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_carry_min) + "]"
        alpha_str = "[" + ",".join(
            f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.stage_alpha
        ) + "]"
        print(f"CASE: {case.label}  (W={case.phys_w}, L={case.phys_l}, source_z={case.source_z})")
        print(f"  stage_mean_overlap  = {overlap_str}")
        print(f"  carry_mean          = {carry_mean_str}")
        print(f"  carry_min           = {carry_min_str}")
        print(f"  stage_alpha         = {alpha_str}")
        print(f"  max_kappa_drift     = {row.max_kappa_drift:.3%}")
        print(f"  admissible          = {row.admissible}")
        print()

    print("SUMMARY")
    print(f"  top{args.top_keep} multistage-admissible on {passes}/{len(cases)} beyond-pocket cases")
    print()
    print("SAFE READ")
    print(
        f"  - If top{args.top_keep} survives most of this ring, the exact-lattice route is leaving the widened pocket."
    )
    print(
        f"  - If top{args.top_keep} collapses quickly here, the current route should be parked as a widened-pocket multistage positive only."
    )
    print("  - This is still a bounded exact-lattice transfer sweep, not matter closure.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
