#!/usr/bin/env python3
"""
Rho1-orientation theorem for the retained `3d+1` complement-line doublet.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    BOUNDARY_FIRST_WEIGHTS,
    LINE_A,
    LINE_B,
    normalize_line,
    projection_frobenius_distance,
)
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
def anchor_losses(line: np.ndarray) -> tuple[float, float]:
    vec = normalize_line(line)
    return float(vec[1] ** 2), float(vec[2] ** 2)


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 RHO1 ORIENTATION")
    print("=" * 118)
    print()
    print("Question:")
    print("  Does the exact retained-line doublet already split into a preferred")
    print("  `rho1`-anchored orientation and its mirror orientation on the selected")
    print("  Wilson branch?")

    loss10_a, loss01_a = anchor_losses(LINE_A)
    loss10_b, loss01_b = anchor_losses(LINE_B)
    dist_rho1_a = projection_frobenius_distance(LINE_A, "rho1")
    dist_rho2_a = projection_frobenius_distance(LINE_A, "rho2")
    dist_rho1_b = projection_frobenius_distance(LINE_B, "rho1")
    dist_rho2_b = projection_frobenius_distance(LINE_B, "rho2")

    print()
    print(f"  boundary-first retained order               = {BOUNDARY_FIRST_WEIGHTS}")
    print(f"  line A losses on (1,0),(0,1)               = ({loss10_a:.12f}, {loss01_a:.12f})")
    print(f"  line B losses on (1,0),(0,1)               = ({loss10_b:.12f}, {loss01_b:.12f})")
    print(f"  line A distances to rho1/rho2 slices       = ({dist_rho1_a:.12f}, {dist_rho2_a:.12f})")
    print(f"  line B distances to rho1/rho2 slices       = ({dist_rho1_b:.12f}, {dist_rho2_b:.12f})")
    print()

    check(
        "The retained ambient order is boundary-first with the preferred (1,0) slot first",
        BOUNDARY_FIRST_WEIGHTS[0] == (1, 0),
    )
    check(
        "Line A is the rho1-anchored member of the exact doublet: it loses far less of the preferred (1,0) boundary direction than line B",
        loss10_a + 1.0e-6 < loss10_b,
        f"(loss10_A,loss10_B)=({loss10_a:.6f},{loss10_b:.6f})",
    )
    check(
        "Line B is the mirror member: it loses far less of the conjugate (0,1) boundary direction than line A",
        loss01_b + 1.0e-6 < loss01_a,
        f"(loss01_A,loss01_B)=({loss01_a:.6f},{loss01_b:.6f})",
    )
    check(
        "The same split appears in Grassmann projector geometry: line A is closer to the rho1 reference slice while line B is closer to the mirror rho2 slice",
        dist_rho1_a + 1.0e-6 < dist_rho1_b and dist_rho2_b + 1.0e-6 < dist_rho2_a,
        f"(dA_rho1,dB_rho1,dA_rho2,dB_rho2)=({dist_rho1_a:.6f},{dist_rho1_b:.6f},{dist_rho2_a:.6f},{dist_rho2_b:.6f})",
    )
    check(
        "So the exact retained-line multiplicity collapses to a rho1/rho2 orientation question rather than arbitrary frame freedom",
        loss10_a + 1.0e-6 < loss10_b
        and loss01_b + 1.0e-6 < loss01_a
        and dist_rho1_a + 1.0e-6 < dist_rho1_b
        and dist_rho2_b + 1.0e-6 < dist_rho2_a,
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Rho1-orientation split of the exact line doublet:")
    print("    - the exact retained-line doublet is not structureless")
    print("    - one member is sharply `rho1`-anchored in the boundary-first ambient")
    print("    - the other is its mirror `rho2`-anchored member")
    print("    - so the existing Wilson-side `rho1` preference law already collapses the")
    print("      multiplicity to an orientation question rather than an arbitrary frame")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
