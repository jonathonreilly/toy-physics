#!/usr/bin/env python3
"""
DM neutrino source-surface carrier-side conclusion runner.

Purpose:
  Give one honest carrier-side verdict after the full compact-branch reduction
  and the split-2 local-neighborhood exhaustion pass.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

AUTHORITY_RUNNERS = [
    (
        "global dominance obstruction",
        "scripts/frontier_dm_neutrino_source_surface_global_dominance_completeness_obstruction.py",
        "RESULT: obstruction at exact-carrier completeness / global dominance",
    ),
    (
        "split-2 local neighborhoods",
        "scripts/frontier_dm_neutrino_source_surface_split2_upper_face_local_neighborhoods_candidate.py",
        "RESULT: split-2 carrier pressure is exhausted to two explicit local",
    ),
]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def run_authority(label: str, rel_path: str, expected_fragment: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / rel_path)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    check(
        f"The {label} runner exits successfully",
        result.returncode == 0,
        f"returncode={result.returncode}",
    )
    check(
        f"The {label} runner emits its expected authority result",
        expected_fragment in result.stdout,
        expected_fragment,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE CARRIER-SIDE CONCLUSION")
    print("=" * 88)
    print()
    print("Replaying carrier-side authority spine:")

    for label, rel_path, expected_fragment in AUTHORITY_RUNNERS:
        run_authority(label, rel_path, expected_fragment)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_CARRIER_SIDE_CONCLUSION_NOTE_2026-04-18.md")
    check(
        "The carrier-side conclusion note records the verdict as obstruction rather than closure",
        "Carrier-side verdict: `obstruction`." in note,
    )
    check(
        "The carrier-side conclusion note records that the live pressure is exhausted to two explicit split-2 upper-face neighborhoods",
        "two explicit split-2 upper-face neighborhoods" in note,
    )
    check(
        "The carrier-side conclusion note records that endpoint and split-1 are no longer live carrier pressure",
        "Endpoint and split-1 are not the live carrier pressure anymore" in note,
    )
    check(
        "The carrier-side conclusion note records that interval-certified exclusion or dominance is still the remaining theorem gap",
        "interval-certified exclusion or dominance" in note,
    )

    print("\n" + "=" * 88)
    print("CARRIER-SIDE RESULT")
    print("=" * 88)
    print("  Carrier-side verdict: obstruction")
    print("  The carrier side is exhausted on the present branch to interval-style")
    print("  exclusion or dominance on two explicit split-2 upper-face neighborhoods.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
