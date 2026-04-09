#!/usr/bin/env python3
"""Cheap alternate-family scout for the mesoscopic surrogate lane.

This is intentionally not a heavy numerical sweep. It reads the already frozen
notes for the mesoscopic-surrogate lane and answers one narrow question:

    Which already-bounded non-Gate-B family is the cheapest plausible next
    target for a more localized source object?

The scout is looking for a family where localization might matter more than on
the retained 3D h=0.5 family, without re-running a large parameter sweep.

The answer is purely a bounded recommendation, not a new physics claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class FamilyRead:
    name: str
    status: str
    why: str
    next_step: str


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def has_all(text: str, needles: tuple[str, ...]) -> bool:
    return all(needle in text for needle in needles)


def main() -> None:
    frontier = read_text("docs/MESOSCOPIC_SURROGATE_LOCALIZATION_FRONTIER_NOTE.md").lower()
    sweep_3d = read_text("docs/MESOSCOPIC_SURROGATE_LOCALIZATION_SWEEP_NOTE.md").lower()
    threshold_2d = read_text("docs/MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md").lower()
    same_family_3d = read_text("docs/SAME_FAMILY_3D_CLOSURE_NOTE.md").lower()
    asymptotic = read_text("docs/VALLEY_LINEAR_ASYMPTOTIC_BRIDGE_NOTE.md").lower()
    readiness = read_text("docs/PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md").lower()

    families = [
        FamilyRead(
            name="3D ordered-lattice h=0.5 localization frontier",
            status="closed",
            why="The frozen frontier note says the only winners are degenerate point-like cases, and topN remains the least-bad mesoscopic control once the family is meaningfully localized.",
            next_step="Do not keep sweeping this family for a sharp localization win.",
        ),
        FamilyRead(
            name="2D ordered-lattice support-threshold control",
            status="closed",
            why="The frozen threshold note says every scanned topN from 1 to 81 stayed stable, so there is no sharp support threshold to exploit.",
            next_step="Do not keep hunting a 2D support threshold.",
        ),
        FamilyRead(
            name="Retained 3D h=0.25 ordered-lattice family",
            status="recommended",
            why=(
                "The same-family 3D closure and asymptotic bridge are already frozen at h=0.25, "
                "with stronger near-Newtonian behavior and a cleaner retained continuum read than h=0.5."
            ),
            next_step=(
                "If we try a more localized source object at all, this is the cheapest bounded family that "
                "still plausibly has room for localization to matter: use non-degenerate shapes with an explicit "
                "support/capture floor."
            ),
        ),
    ]

    print("=" * 92)
    print("MESOSCOPIC SURROGATE ALTERNATE-FAMILY SCOUT")
    print("  Purpose: identify the cheapest already-bounded non-Gate-B family where")
    print("           a more localized source object might plausibly matter more than")
    print("           on the retained 3D h=0.5 family.")
    print("=" * 92)
    print()
    print("Frozen evidence check")
    print(f"  h=0.5 frontier closed? {'yes' if 'degenerate point-like localizations' in sweep_3d else 'no'}")
    print(f"  2D threshold closed? {'yes' if 'every scanned' in threshold_2d and 'stayed stable' in threshold_2d else 'no'}")
    print(f"  3D h=0.25 same-family closure present? {'yes' if 'h=0.25, w=10, l=12' in same_family_3d else 'no'}")
    print(f"  3D h=0.25 asymptotic bridge present? {'yes' if 'z>=5: -1.00' in asymptotic else 'no'}")
    print(f"  Persistent-mass readiness still open? {'yes' if 'not yet' in readiness else 'no'}")
    print()
    print("Candidate ranking")
    for idx, fam in enumerate(families, 1):
        print(f"{idx}. {fam.name} [{fam.status}]")
        print(f"   why: {fam.why}")
        print(f"   next: {fam.next_step}")
    print()
    print("Recommendation")
    print(
        "  The cheapest already-bounded family worth one more localization attempt is the retained "
        "3D h=0.25 ordered-lattice family. The retained 3D h=0.5 family is already closed as a "
        "degenerate-point-source frontier, and the 2D family is closed as 'no sharp threshold'."
    )
    print(
        "  If we do proceed, the next attempt should use only non-degenerate localized shapes "
        "(annular windows, tapered ellipsoids, or compact Gaussians) with a minimum support/capture floor."
    )
    print(
        "  If that family still cannot beat the broad topN control, the localization lane is probably "
        "done and should be frozen as a bounded negative result."
    )
    print()
    print("Useful frozen context")
    print(
        "  - 3D h=0.5 localization frontier: only degenerate point-like winners; topN remains least-bad."
    )
    print(
        "  - 2D threshold control: no sharp support threshold across topN=1..81."
    )
    print(
        "  - 3D h=0.25 ordered-lattice family: already has same-family closure and the strongest retained asymptotic bridge."
    )


if __name__ == "__main__":
    main()
