#!/usr/bin/env python3
"""Multistage transfer sweep across the widened local pocket."""

from __future__ import annotations

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.persistent_object_top3_multistage_probe import Case, _run_case  # noqa: E402


TOP_KEEP = 4

CASES = (
    Case("baseline", 6, 3, 2.0),
    Case("source0p75", 6, 3, 0.75),
    Case("source1p00", 6, 3, 1.00),
    Case("source1p25", 6, 3, 1.25),
    Case("source1p50", 6, 3, 1.50),
    Case("source2p50", 6, 3, 2.50),
    Case("source2p75", 6, 3, 2.75),
    Case("width4", 6, 4, 2.0),
    Case("width5", 6, 5, 2.0),
    Case("length4", 4, 3, 2.0),
    Case("length5", 5, 3, 2.0),
    Case("length7", 7, 3, 2.0),
    Case("length8", 8, 3, 2.0),
)

CASE_BY_LABEL = {case.label: case for case in CASES}


def _parse_cases(case_labels: str | None) -> tuple[Case, ...]:
    if not case_labels:
        return CASES
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
        help="Comma-separated case labels. Defaults to the full widened local pocket.",
    )
    args = parser.parse_args()
    cases = _parse_cases(args.case_labels)

    t0 = time.time()
    print("=" * 138)
    print("PERSISTENT OBJECT MULTISTAGE TRANSFER SWEEP")
    print("  widened local-pocket transfer of the retained multistage compact-object floor")
    print("=" * 138)
    print(f"top_keep={args.top_keep}, cases={','.join(case.label for case in cases)}")
    print()

    passes = 0
    for case in cases:
        row = _run_case(case, args.top_keep)
        passes += int(row.admissible)
        overlap_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_mean_overlap) + "]"
        carry_mean_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_carry_mean) + "]"
        alpha_str = "[" + ",".join(
            f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.stage_alpha
        ) + "]"
        print(f"CASE: {case.label}  (W={case.phys_w}, L={case.phys_l}, source_z={case.source_z})")
        print(f"  stage_mean_overlap  = {overlap_str}")
        print(f"  carry_mean          = {carry_mean_str}")
        print(f"  stage_alpha         = {alpha_str}")
        print(f"  max_kappa_drift     = {row.max_kappa_drift:.3%}")
        print(f"  admissible          = {row.admissible}")
        print()

    print("SUMMARY")
    print(f"  top{args.top_keep} multistage-admissible on {passes}/{len(cases)} listed widened-pocket cases")
    print()
    print("SAFE READ")
    print(
        f"  - If top{args.top_keep} stays open across most of this pocket, the exact-lattice route now has a real transferable multistage floor."
    )
    print(f"  - If top{args.top_keep} collapses on the boundary rows, the floor is real but still pocket-limited.")
    print("  - This is still a bounded exact-lattice transfer sweep, not matter closure.")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
