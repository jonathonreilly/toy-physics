#!/usr/bin/env python3
"""
Rho1-anchored least-distortion selector theorem for the retained `3d+1`
complement-line doublet.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import TARGET
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    LINE_A,
    LINE_B,
    compressed_local_block_from_line,
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


def anchor_loss_rho1(line: np.ndarray) -> float:
    vec = normalize_line(line)
    return float(vec[1] ** 2)


def selector_key(line: np.ndarray) -> tuple[float, float]:
    return (
        projection_frobenius_distance(line, "rho1"),
        anchor_loss_rho1(line),
    )


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 RHO1 LEAST-DISTORTION SELECTOR")
    print("=" * 118)
    print()
    print("Question:")
    print("  Once the exact retained-line solve has reduced to the rho1/rho2 orientation")
    print("  doublet, is there a canonical branch-side selector that picks the right")
    print("  member without reopening generic frame freedom?")

    lines = [LINE_A, LINE_B]
    keys = [selector_key(line) for line in lines]
    choice = min(range(len(lines)), key=lambda idx: keys[idx])
    chosen = lines[choice]
    errs = [float(np.linalg.norm(compressed_local_block_from_line(line)[2] - TARGET)) for line in lines]
    line_sep = min(
        np.linalg.norm(normalize_line(LINE_A) - normalize_line(LINE_B)),
        np.linalg.norm(normalize_line(LINE_A) + normalize_line(LINE_B)),
    )
    _h, responses, live, _qmat = compressed_local_block_from_line(chosen)
    dist = float(np.linalg.norm(live - TARGET))
    gap_to_a = min(
        np.linalg.norm(normalize_line(chosen) - normalize_line(LINE_A)),
        np.linalg.norm(normalize_line(chosen) + normalize_line(LINE_A)),
    )

    print()
    print(f"  selector key(line A)                        = ({keys[0][0]:.12f}, {keys[0][1]:.12f})")
    print(f"  selector key(line B)                        = ({keys[1][0]:.12f}, {keys[1][1]:.12f})")
    print(f"  chosen line index                           = {choice}")
    print(f"  chosen live point                           = ({live[0]:.12f}, {live[1]:.12f}, {live[2]:.12f})")
    print(f"  chosen ordered-even split                   = ({responses[3]:.12f}, {responses[5]:.12f})")
    print()

    check(
        "The retained-line problem has reduced to a rho1/rho2 orientation doublet with two explicit exact target-hitting lines",
        line_sep > 1.0e-3 and max(errs) < 1.0e-10,
        f"(sep,max_err)=({line_sep:.6f},{max(errs):.3e})",
    )
    check(
        "Projection-Frobenius distortion to the rho1 reference slice is strictly smaller for line A than for line B",
        keys[0][0] + 1.0e-6 < keys[1][0],
        f"(dA,dB)=({keys[0][0]:.6f},{keys[1][0]:.6f})",
    )
    check(
        "Preferred boundary-anchor loss is also strictly smaller for line A than for line B",
        keys[0][1] + 1.0e-6 < keys[1][1],
        f"(lossA,lossB)=({keys[0][1]:.6f},{keys[1][1]:.6f})",
    )
    check(
        "So the rho1-anchored least-distortion selector chooses line A uniquely from the exact doublet",
        choice == 0 and gap_to_a < 1.0e-12,
        f"gap_to_A={gap_to_a:.3e}",
    )
    check(
        "The selected rho1-anchored least-distortion line reproduces the observed live DM target",
        dist < 1.0e-10,
        f"dist={dist:.3e}",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  New complement-line law:")
    print("    - solve the retained `3d+1` complement-line problem on the selected")
    print("      Wilson branch")
    print("    - the exact-solve set is a rho1/rho2 orientation doublet")
    print("    - choose the member with least Grassmann projection-distortion to the")
    print("      rho1 reference slice, breaking any tie by smallest loss of the")
    print("      preferred boundary anchor `(1,0)`")
    print("    - this selects the canonical line A and lands exactly on the live DM target")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
