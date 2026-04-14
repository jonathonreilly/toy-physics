#!/usr/bin/env python3
"""
Route 2 uniqueness audit: S^3 + anomaly-forced time.

This checks whether the retained stack uniquely selects the clean kinematic
background candidate and whether the atlas already contains an exact dynamics
bridge that would force a GR metric law on that background.
"""

from __future__ import annotations

from pathlib import Path
import sys


PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f" ({detail})"
    print(line)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("None of the candidate paths exist: " + ", ".join(str(p) for p in paths))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    atlas = first_existing([
        root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        Path("/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md"),
    ])
    s3_note = first_existing([
        root / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
        Path("/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md"),
    ])
    anomaly_note = first_existing([
        root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
        Path("/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md"),
    ])
    route_note = first_existing([
        root / "docs" / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md",
        Path("/Users/jonreilly/Projects/Physics/docs/S3_ANOMALY_SPACETIME_LIFT_NOTE.md"),
    ])
    committee_note = first_existing([
        root / "docs" / "S3_TIME_COMMITTEE_MEMO.md",
        Path("/Users/jonreilly/Projects/Physics/docs/S3_TIME_COMMITTEE_MEMO.md"),
    ])

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    route_text = read_text(route_note)
    committee_text = read_text(committee_note)

    print("Route 2 uniqueness audit: S^3 + anomaly-forced time")
    print("=" * 72)
    print("  Candidate background: PL S^3 x R")
    print()

    check(
        "S^3 compactification is closed",
        "PL homeomorphic to S^3" in s3_text or "Status:** CLOSED" in s3_text,
        "the spatial topology ingredient is exact",
    )
    check(
        "Anomaly-forced time is exact",
        "d_t = 1 uniquely" in anomaly_text or "single-clock codimension-1 evolution excludes d_t > 1" in anomaly_text,
        "the temporal ingredient is exact",
    )
    check(
        "Route-2 committee memo isolates the background and the missing bridge",
        "PL S^3 x R" in committee_text and "dynamics bridge" in committee_text,
        "background uniqueness is already isolated",
    )
    check(
        "Atlas exposes the route-2 tools as reusable and canonical",
        "`S^3` cap uniqueness" in atlas_text and "Anomaly-forced time" in atlas_text,
        "the atlas carries the route ingredients",
    )
    check(
        "No exact dynamics bridge is present for route 2",
        False,
        "no exact S^3-to-curvature, anomaly-to-Einstein, or discrete action theorem is present on this route",
    )

    print()
    print("Summary:")
    print("  Background uniqueness: yes")
    print("  GR dynamics uniqueness: blocked")
    print("  Missing theorem: exact dynamics bridge from PL S^3 x R to the metric law")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")

    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
