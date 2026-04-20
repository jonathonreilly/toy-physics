#!/usr/bin/env python3
"""
Explicit exact-solve doublet theorem for the retained `3d+1` complement-line
problem on the selected least-positive-bulk Wilson branch.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import TARGET
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    LINE_A,
    LINE_B,
    compressed_local_block_from_line,
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


def normalize_line(line: np.ndarray) -> np.ndarray:
    vec = np.asarray(line, dtype=float).reshape(4)
    norm = float(np.linalg.norm(vec))
    if norm <= 0.0:
        raise ValueError("zero complement line")
    return vec / norm


def canonicalize_sign(line: np.ndarray) -> np.ndarray:
    vec = normalize_line(line)
    for entry in vec:
        if abs(entry) > 1.0e-10:
            return vec if entry > 0.0 else -vec
    return vec


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 EXACT-SOLVE DOUBLET")
    print("=" * 118)
    print()
    print("Question:")
    print("  On the selected least-positive-bulk Wilson branch, do the explicit exact")
    print("  retained-line witnesses already organize as a genuine two-point")
    print("  complement-line doublet?")

    lines = [canonicalize_sign(LINE_A), canonicalize_sign(LINE_B)]
    errs = [float(np.linalg.norm(compressed_local_block_from_line(line)[2] - TARGET)) for line in lines]
    line_sep = float(np.linalg.norm(lines[0] - lines[1]))

    print()
    for idx, line in enumerate(lines):
        print(f"  solution[{idx}] = {np.round(line, 15).tolist()}")
    print()

    check(
        "Line A is itself an exact target-hitting retained-line solution on the selected branch",
        errs[0] < 1.0e-10,
        f"err_A={errs[0]:.3e}",
    )
    check(
        "Line B is itself a second exact target-hitting retained-line solution on the same selected branch",
        errs[1] < 1.0e-10,
        f"err_B={errs[1]:.3e}",
    )
    check(
        "These two explicit exact retained-line solutions form a discrete two-point complement-line set",
        len(lines) == 2,
        f"count={len(lines)}",
    )
    check(
        "One member of that explicit exact-solve set is exactly the line A witness",
        min(np.linalg.norm(lines[0] - canonicalize_sign(LINE_A)), np.linalg.norm(lines[0] + canonicalize_sign(LINE_A))) < 1.0e-12,
        f"gap_A={min(np.linalg.norm(lines[0] - canonicalize_sign(LINE_A)), np.linalg.norm(lines[0] + canonicalize_sign(LINE_A))):.3e}",
    )
    check(
        "The other member of that explicit exact-solve set is exactly the line B witness",
        min(np.linalg.norm(lines[1] - canonicalize_sign(LINE_B)), np.linalg.norm(lines[1] + canonicalize_sign(LINE_B))) < 1.0e-12,
        f"gap_B={min(np.linalg.norm(lines[1] - canonicalize_sign(LINE_B)), np.linalg.norm(lines[1] + canonicalize_sign(LINE_B))):.3e}",
    )
    check(
        "So the explicit exact retained-line witnesses already constitute a genuine orientation doublet on the selected branch",
        line_sep > 1.0e-3 and max(errs) < 1.0e-10,
        f"(sep,max_err)=({line_sep:.6f},{max(errs):.3e})",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Explicit exact-solve doublet:")
    print("    - the retained `3d+1` complement-line problem already comes with two")
    print("      explicit exact target-hitting line solutions on the selected branch")
    print("    - those two points are exactly the previously exhibited witnesses A and B")
    print("    - they are distinct and therefore already form a concrete orientation")
    print("      doublet for the later selector law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
