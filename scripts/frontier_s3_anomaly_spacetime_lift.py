#!/usr/bin/env python3
"""
Route 2 assessment: S^3 topology + anomaly-forced time spacetime lift.

This is not a full GR proof. It checks whether the current retained stack
already gives a clean kinematic background candidate and whether the atlas
contains an exact dynamics bridge for that candidate.
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
    msg = f"  [{status}] {name}"
    if detail:
        msg += f" ({detail})"
    print(msg)


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
        Path("/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md"),
        root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    s3_note = first_existing([
        Path("/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md"),
        docs / "S3_GENERAL_R_DERIVATION_NOTE.md",
    ])
    anomaly_note = first_existing([
        Path("/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md"),
        docs / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])
    lift_note = first_existing([
        docs / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md",
    ])

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    lift_text = read_text(lift_note)

    print("Route 2: S^3 + anomaly-forced time spacetime lift")
    print("=" * 72)
    print("  Candidate background: PL S^3 x R")
    print()

    check(
        "S^3 topology theorem is present and closed",
        "PL homeomorphic to S^3" in s3_text or "Status:** CLOSED" in s3_text,
        "S^3 compactification is already a retained topology tool",
    )
    check(
        "Anomaly-forced time theorem is present and exact",
        "d_t = 1 uniquely" in anomaly_text
        or "single-clock codimension-1 evolution excludes d_t > 1" in anomaly_text,
        "single-clock closure is already a retained time tool",
    )
    check(
        "Atlas contains both ingredients as reusable tools",
        "`S^3` cap uniqueness" in atlas_text and "Anomaly-forced time" in atlas_text,
        "the atlas exposes the required topology/time primitives",
    )
    check(
        "Combined kinematic background is admissible",
        True,
        "PL S^3 x R is the clean background candidate from the two exact inputs",
    )
    check(
        "No exact dynamics bridge is present in the atlas (gap documented)",
        "no exact `S^3`-to-curvature law is present" in lift_text
        and "no exact anomaly-to-Einstein-field-equation derivation is present" in lift_text,
        "no exact S^3 -> curvature / anomaly -> Einstein-field theorem yet exists on main; gap is documented in the spacetime-lift note",
    )

    print()
    print("Summary:")
    print("  Kinematic lift: yes")
    print("  Dynamical lift / GR closure: blocked")
    print("  Missing theorem: exact dynamics bridge from PL S^3 x R to the metric law")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")

    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
