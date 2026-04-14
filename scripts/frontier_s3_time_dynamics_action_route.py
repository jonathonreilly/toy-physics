#!/usr/bin/env python3
"""
Route 2 dynamics-action audit: S^3 + anomaly-forced time.

This script checks whether the retained Route-2 ingredients already support
an exact action/variational bridge from the clean kinematic background
PL S^3 x R to GR-like dynamics.

Current expectation from the retained stack:
  - S^3 topology is exact
  - anomaly-forced time is exact
  - the microscopic shell boundary action is exact on the current strong-field
    source classes
  - but there is still no exact 4D dynamics action on the product background
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
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    line = f"  [{tag}] {name}"
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
    atlas = Path("/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    s3_note = Path("/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md")
    anomaly_note = Path("/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md")
    schur_note = Path("/Users/jonreilly/Projects/Physics/docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md")
    route_note = root / "docs" / "S3_TIME_DYNAMICS_ACTION_ROUTE_NOTE.md"
    committee_note = first_existing(
        [
            root / "docs" / "S3_TIME_COMMITTEE_MEMO.md",
            root / "docs" / "S3_TIME_UNIQUENESS_ROUTE_NOTE.md",
        ]
    )

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    schur_text = read_text(schur_note)
    route_text = read_text(route_note)
    committee_text = read_text(committee_note)

    print("Route 2 dynamics-action audit: S^3 + anomaly-forced time")
    print("=" * 76)
    print("  Candidate background: PL S^3 x R")
    print("  Candidate action route: exact transfer-matrix / variational lift from the shell Schur action")
    print()

    check(
        "S^3 compactification is exact",
        "PL homeomorphic to S^3" in s3_text and "for every R >= 2" in s3_text,
        "the spatial background ingredient is theorem-grade",
    )
    check(
        "Anomaly-forced time is exact",
        "single-clock" in anomaly_text.lower() and "codimension-1" in anomaly_text.lower(),
        "the temporal ingredient is theorem-grade",
    )
    check(
        "The microscopic shell boundary action is exact on the current strong-field class",
        "schur-complement boundary action" in schur_text.lower()
        and "exact microscopic lattice boundary energy" in schur_text.lower(),
        "the current action object is exact but static",
    )
    check(
        "The atlas canonicalizes the route-2 ingredients",
        "boundary-link theorem" in atlas_text.lower()
        and "anomaly-forced time" in atlas_text.lower()
        and "restricted strong-field closure synthesis" in atlas_text.lower(),
        "the background tools are reusable and canonical",
    )
    check(
        "The route note isolates the dynamics gap cleanly",
        "dynamically blocked" in route_text and "exact dynamics bridge" in route_text,
        "the route note records the missing theorem explicitly",
    )
    check(
        "The retained stack does NOT yet contain an exact PL S^3 x R dynamics bridge",
        False,
        "the best available action object is the static shell Schur action; no exact 4D product-spacetime variational law is present",
    )

    print()
    print("Summary:")
    print("  Kinematic background: yes")
    print("  Exact static shell action: yes")
    print("  Exact GR-like dynamics bridge on PL S^3 x R: blocked")
    print("  Missing theorem: exact 4D variational / transfer-matrix action on the product background")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")

    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
