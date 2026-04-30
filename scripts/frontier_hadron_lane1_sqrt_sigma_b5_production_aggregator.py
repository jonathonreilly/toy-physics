#!/usr/bin/env python3
"""Aggregate the B5 production-ladder JSONL checkpoint.

This runner is intentionally a checkpoint gate, not a closure proof.  It
summarizes the current production records, checks that the data are finite,
and verifies that the branch still refuses B5 promotion while the required
multi-volume ladder is incomplete.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import statistics
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSONL = ROOT / "outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_production_2026-04-30.jsonl"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--min-checkpoint-records", type=int, default=100)
    parser.add_argument("--required-volumes", default="8,12,16")
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def mean_stderr(values: list[float]) -> tuple[float, float]:
    mean = sum(values) / len(values)
    stderr = statistics.stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0
    return mean, stderr


def part1_data_summary(rows: list[dict[str, Any]], min_records: int) -> dict[int, list[dict[str, Any]]]:
    section("Part 1: production JSONL summary")
    by_volume: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_volume[int(row["L"])].append(row)

    for L, group in sorted(by_volume.items()):
        last = group[-1]
        print(
            f"  L={L}: n={len(group)}, last_measurement={last['measurement_index']}, "
            f"last_sweeps={last['sweeps_completed']}, acceptance={last['acceptance']:.3f}"
        )
        for key in ("plaquette", "W11", "W12", "W22", "chi22"):
            values = [float(row[key]) for row in group if row[key] is not None]
            mean, stderr = mean_stderr(values)
            print(f"    {key}: {mean:.8f} +/- {stderr:.8f}")

    check("production JSONL is non-empty", len(rows) > 0, f"records={len(rows)}")
    check(
        "all records come from the production profile",
        all(row.get("profile") == "production" for row in rows),
    )
    check(
        "L=8 has reached the checkpoint minimum",
        len(by_volume.get(8, [])) >= min_records,
        f"L8 records={len(by_volume.get(8, []))}, minimum={min_records}",
    )
    check(
        "all primary observables are finite",
        all(
            math.isfinite(float(row[key]))
            for row in rows
            for key in ("plaquette", "W11", "W12", "W22", "acceptance")
        ),
    )
    check(
        "all non-null chi22 values are finite",
        all(row["chi22"] is not None and math.isfinite(float(row["chi22"])) for row in rows),
    )
    return by_volume


def part2_closure_gate(by_volume: dict[int, list[dict[str, Any]]], required: set[int]) -> None:
    section("Part 2: production closure gate")
    present = set(by_volume)
    missing = sorted(required - present)
    print(f"  required volumes: {sorted(required)}")
    print(f"  present volumes:  {sorted(present)}")
    print(f"  missing volumes:  {missing}")

    check("L=8 production records exist", 8 in present)
    check(
        "required production ladder is still incomplete",
        bool(missing),
        f"missing volumes={missing}",
    )
    check(
        "B5 closure gate remains open",
        not required.issubset(present),
        "multi-volume production ladder incomplete",
    )


def part3_artifact_checks() -> None:
    section("Part 3: artifact checks")
    note = read("docs/HADRON_LANE1_SQRT_SIGMA_B5_PRODUCTION_CHECKPOINT_NOTE_2026-04-30.md")
    handoff = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/HANDOFF.md")
    certificate = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/CLAIM_STATUS_CERTIFICATE.md")

    check(
        "checkpoint note states no B5 promotion",
        "not B5 closure" in note and "L=12" in note and "L=16" in note,
    )
    check(
        "branch-local handoff includes production checkpoint aggregator",
        "HADRON_LANE1_SQRT_SIGMA_B5_PRODUCTION_CHECKPOINT_NOTE_2026-04-30.md" in handoff
        and "frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py" in handoff,
    )
    check(
        "claim-status certificate remains bounded support",
        "actual_current_surface_status: bounded-support" in certificate
        and "proposal_allowed: false" in certificate,
    )


def main() -> int:
    args = parse_args()
    required = {int(item.strip()) for item in args.required_volumes.split(",") if item.strip()}

    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B5 PRODUCTION CHECKPOINT AGGREGATOR")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the current production ladder data close B5?")
    print()
    print("Answer:")
    print("  No. It is a useful production checkpoint; the required")
    print("  multi-volume ladder is still incomplete.")

    rows = load_rows(args.jsonl)
    by_volume = part1_data_summary(rows, args.min_checkpoint_records)
    part2_closure_gate(by_volume, required)
    part3_artifact_checks()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
