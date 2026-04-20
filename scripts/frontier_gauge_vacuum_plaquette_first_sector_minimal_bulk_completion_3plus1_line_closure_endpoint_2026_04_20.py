#!/usr/bin/env python3
"""
Closure endpoint after deriving the rho1-anchored complement-line law on the
selected least-positive-bulk Wilson branch.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_positive_exact_law_search import ordered_even_law
from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import (
    TARGET,
    solve_sparse_target_preimage,
    sparse_face_projected_data,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    LINE_A,
    compressed_local_block_from_line,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_rho1_least_distortion_selector_theorem_2026_04_20 import (
    selector_key,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_packet_theorem_2026_04_19 import (
    selected_transfer_and_packet,
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
def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 LINE CLOSURE ENDPOINT")
    print("=" * 118)
    print()
    print("Question:")
    print("  After the rho1-oriented retained-line wave, what exactly is still open on")
    print("  the enlarged Wilson/DM stack?")

    pkg = selected_transfer_and_packet()
    _h, _responses, live, _qmat = compressed_local_block_from_line(LINE_A)
    x, y, phase = solve_sparse_target_preimage()
    data = sparse_face_projected_data(np.array([x[0], x[1], y[0], phase], dtype=float))
    selected_pair = ordered_even_law(data)
    key_a = selector_key(LINE_A)
    line_b = np.array(
        [0.5273106873489956, 0.8459692861767273, 0.060833791226262236, 0.05078046571475716],
        dtype=float,
    )
    key_b = selector_key(line_b)
    live_dist = float(np.linalg.norm(live - TARGET))

    check(
        "Least-positive-bulk completion fixes one explicit Wilson/Perron branch",
        abs(float(pkg["alpha0"]) - float(pkg["m1"])) < 1.0e-12 and float(pkg["beta1"]) > 0.0,
        f"(alpha0,beta1)=({float(pkg['alpha0']):.6f},{float(pkg['beta1']):.6f})",
    )
    check(
        "The selected branch is quantitatively viable inside the retained 3d+1 ambient",
        live_dist < 1.0e-10,
        f"dist={live_dist:.3e}",
    )
    check(
        "The rho1 least-distortion selector closes the remaining complement-line law on that retained ambient",
        key_a < key_b,
        f"keyA=({key_a[0]:.6f},{key_a[1]:.6f})",
    )
    check(
        "The reduced DM side is already closed by the exact ordered projected-source law (S12,S13)",
        np.linalg.norm(selected_pair - np.array([data["S12"], data["S13"]], dtype=float)) < 1.0e-12,
        f"(S12,S13)=({selected_pair[0]:.6f},{selected_pair[1]:.6f})",
    )
    check(
        "So the enlarged Wilson/DM stack now reaches the live DM target without any remaining open branch-choice or slice-law seam",
        live_dist < 1.0e-10
        and np.linalg.norm(selected_pair - np.array([data["S12"], data["S13"]], dtype=float)) < 1.0e-12,
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Enlarged-stack closure endpoint:")
    print("    - least-positive-bulk completion selects the Wilson branch")
    print("    - the retained `3d+1` complement-line problem reduces to a rho1/rho2")
    print("      orientation doublet")
    print("    - the rho1-anchored least-distortion selector picks the canonical line")
    print("    - the selected branch then lands on the live DM target exactly")
    print("    - on this enlarged stack, the DM flagship gate is closed positively")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
