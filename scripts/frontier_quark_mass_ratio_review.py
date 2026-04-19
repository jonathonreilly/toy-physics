#!/usr/bin/env python3
"""
Reviewer-facing bundle runner for the live quark mass-ratio lane.

Status:
  review-ready bundle runner on current main

Safe claim:
  This script replays the current down-type and up-type quark mass-ratio
  runners, preserves their audit output, and prints a packet-level summary.
  It does not introduce a new derivation or upgrade the bounded status of the
  underlying lanes.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


TOTAL_RE = re.compile(r"TOTAL:\s+PASS=(\d+),\s+FAIL=(\d+)")


@dataclass(frozen=True)
class RunnerSpec:
    label: str
    relative_path: str


@dataclass(frozen=True)
class RunnerResult:
    label: str
    relative_path: str
    returncode: int
    pass_count: int
    fail_count: int
    parsed_total: bool


RUNNERS = (
    RunnerSpec(
        label="Phase 1: down-type CKM dual",
        relative_path="scripts/frontier_mass_ratio_ckm_dual.py",
    ),
    RunnerSpec(
        label="Phase 2: up-type CKM inversion",
        relative_path="scripts/frontier_mass_ratio_up_sector.py",
    ),
)


def run_runner(repo_root: Path, spec: RunnerSpec) -> RunnerResult:
    runner_path = repo_root / spec.relative_path
    print("=" * 72)
    print(f"QUARK PACKET SUBRUNNER: {spec.label}")
    print(f"PATH: {spec.relative_path}")
    print("=" * 72)

    completed = subprocess.run(
        [sys.executable, str(runner_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    stdout = completed.stdout.rstrip()
    stderr = completed.stderr.rstrip()

    if stdout:
        print(stdout)

    if stderr:
        print("\n[stderr]")
        print(stderr)

    match = TOTAL_RE.search(completed.stdout)
    parsed_total = match is not None
    pass_count = int(match.group(1)) if match else 0
    fail_count = int(match.group(2)) if match else 1

    if completed.returncode != 0 and fail_count == 0:
        fail_count = 1

    if not parsed_total:
        print("\n  [FAIL] bundle parser could not find a TOTAL line")

    return RunnerResult(
        label=spec.label,
        relative_path=spec.relative_path,
        returncode=completed.returncode,
        pass_count=pass_count,
        fail_count=fail_count,
        parsed_total=parsed_total,
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    print("=" * 72)
    print("  FRONTIER: Quark Mass-Ratio Review Packet")
    print("=" * 72)
    print("  Scope:")
    print("    replay the live down-type and up-type quark mass-ratio runners")
    print("    keep their raw audit output intact")
    print("    summarize the honest packet endpoint on current main")

    results = [run_runner(repo_root, spec) for spec in RUNNERS]

    total_pass = sum(result.pass_count for result in results)
    total_fail = sum(result.fail_count for result in results)
    bundle_ok = all(
        result.returncode == 0 and result.parsed_total and result.fail_count == 0
        for result in results
    )

    print("\n" + "=" * 72)
    print("QUARK MASS-RATIO PACKET SUMMARY")
    print("=" * 72)

    for result in results:
        print(
            f"  {result.label}: PASS={result.pass_count} FAIL={result.fail_count} "
            f"(runner: {result.relative_path})"
        )

    print()
    print("  Honest endpoint on current main:")
    print("    down-type lane is the strongest quark-side result and replays cleanly")
    print("    up-type extension is live but remains bounded on the partition")
    print("    m_u/m_c lands near observation on the comparator partition")
    print("    m_c/m_t remains low by about one order of magnitude under the")
    print("    current CP-orthogonal combination rule")
    print()
    if bundle_ok:
        print("  Packet status: review-ready quark mass-ratio bundle")
    else:
        print("  Packet status: bundle replay failed; inspect subrunner output above")

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={total_pass}, FAIL={total_fail}")
    print("=" * 72)

    return 0 if bundle_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
