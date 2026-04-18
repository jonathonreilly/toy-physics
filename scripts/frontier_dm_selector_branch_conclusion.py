#!/usr/bin/env python3
"""
DM selector branch conclusion runner.

Replays the accepted branch-local authority spine and prints one unambiguous
branch result.
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
        "representation",
        "scripts/frontier_dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem.py",
        "SUMMARY: PASS=",
    ),
    (
        "observable obstruction",
        "scripts/frontier_dm_neutrino_source_surface_observable_grammar_exhaustion_obstruction.py",
        "RESULT: obstruction at observable-grammar exhaustion / intrinsic-family descent",
    ),
    (
        "global dominance obstruction",
        "scripts/frontier_dm_neutrino_source_surface_global_dominance_completeness_obstruction.py",
        "RESULT: obstruction at exact-carrier completeness / global dominance",
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
    print("DM SELECTOR BRANCH CONCLUSION")
    print("=" * 88)
    print()
    print("Replaying accepted authority spine:")

    for label, rel_path, expected_fragment in AUTHORITY_RUNNERS:
        run_authority(label, rel_path, expected_fragment)

    conclusion_note = read("docs/DM_SELECTOR_BRANCH_CONCLUSION_NOTE_2026-04-17.md")
    check(
        "The branch conclusion note records the final verdict as obstruction",
        "Final verdict: `obstruction`." in conclusion_note,
    )
    check(
        "The branch conclusion note names both exact blockers explicitly",
        "observable-grammar exhaustion / intrinsic-family descent" in conclusion_note
        and "exact-carrier completeness / global dominance" in conclusion_note,
    )
    check(
        "The branch conclusion note records the sharper compact-branch carrier picture on split-2",
        "low-slack active-boundary band" in conclusion_note,
    )
    check(
        "The branch conclusion note records the one-dimensional split-2 edge interval and preferred slack margin",
        "0 <= s < s_*" in conclusion_note and "0.215677476525" in conclusion_note,
    )
    check(
        "The branch conclusion note records that tested broad-window pressure now collapses entirely to split-2 edge data",
        "collapses entirely to that split-2 edge interval" in conclusion_note,
    )

    print("\n" + "=" * 88)
    print("BRANCH RESULT")
    print("=" * 88)
    print("  BRANCH RESULT: obstruction")
    print("  Exact blockers:")
    print("    - observable-grammar exhaustion / intrinsic-family descent")
    print("    - exact-carrier completeness / global dominance")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
