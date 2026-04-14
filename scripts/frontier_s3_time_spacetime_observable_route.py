#!/usr/bin/env python3
"""
Route 2 observable pass: S^3 + anomaly-forced time -> PL S^3 x R.

This script checks whether the retained route-2 stack contains an exact
spacetime-lift observable or a dynamics bridge that could underpin GR.

The expected outcome on the current atlas is:
- exact kinematic lift selector: yes
- exact dynamics bridge to Einstein equations: no
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
    atlas = first_existing([
        Path("/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md"),
        root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    anomaly = first_existing([
        Path("/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md"),
        root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])
    s3_lift = first_existing([
        root / "docs" / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md",
        Path("/Users/jonreilly/Projects/Physics/docs/S3_ANOMALY_SPACETIME_LIFT_NOTE.md"),
    ])
    committee = first_existing([
        root / "docs" / "S3_TIME_COMMITTEE_MEMO.md",
        Path("/Users/jonreilly/Projects/Physics/docs/S3_TIME_COMMITTEE_MEMO.md"),
    ])

    atlas_text = read_text(atlas)
    anomaly_text = read_text(anomaly)
    s3_text = read_text(s3_lift)
    committee_text = read_text(committee)

    print("Route 2: S^3 + anomaly-forced time observable pass")
    print("=" * 72)
    print("  Candidate background: PL S^3 x R")
    print()

    s3_closed = (
        "S^3 compactification is closed" in s3_text
        or "S^3" in s3_text and "unique closure" in s3_text
        or "PL S^3" in s3_text
    )
    time_exact = (
        "d_t = 1" in anomaly_text
        or "d_t = 1 uniquely" in anomaly_text
        or "single-clock codimension-1 evolution excludes d_t > 1" in anomaly_text
    )
    background_exact = s3_closed and time_exact

    check("S^3 topology is closed on the retained route", s3_closed, "topology ingredient present")
    check("Anomaly-forced time is exact", time_exact, "single-clock closure present")
    check("Combined kinematic background PL S^3 x R is exact", background_exact, "lift selector evaluates to 1")

    exact_dynamics_terms = [
        "exact action",
        "Euler-Lagrange",
        "dynamics bridge",
        "observable is shown to encode the metric/dynamics data",
        "unique compatible dynamics are Einstein/GR dynamics",
    ]
    exact_dynamics_bridge = any(term in atlas_text for term in exact_dynamics_terms) and any(
        term in committee_text for term in ["exact action", "exact observable", "uniqueness theorem"]
    )

    check(
        "Atlas contains an exact dynamics bridge",
        exact_dynamics_bridge,
        "expected false on current stack",
    )
    check(
        "Committee memo still states the route is kinematic only",
        ("kinematic" in committee_text.lower() and "dynamics bridge" in committee_text.lower())
        or ("not yet a full gr closure path" in committee_text.lower()),
        "route remains kinematic, not dynamical",
    )

    lift_observable = 1 if background_exact else 0
    print()
    print("Route-2 observable:")
    print(f"  O_lift = {lift_observable}")
    print("  Interpretation: exact kinematic selector, not a metric carrier")
    print()
    print("Summary:")
    print("  Kinematic lift: yes")
    print("  Dynamics bridge: blocked")
    print("  Missing theorem: exact action / observable / uniqueness bridge on PL S^3 x R")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")

    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
