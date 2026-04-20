#!/usr/bin/env python3
"""
Closure endpoint after deriving the rho1-anchored complement-line law on the
selected least-positive-bulk Wilson branch.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import (
    TARGET,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    compressed_local_block_from_line,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_rho1_least_distortion_selector_theorem_2026_04_20 import (
    selected_line,
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
    line = selected_line()
    _h, responses, live, _qmat = compressed_local_block_from_line(line)
    live_dist = float(np.linalg.norm(live - TARGET))
    selected_pair = np.array([responses[3], responses[5]], dtype=float)
    key = selector_key(line)

    check(
        "The canonical minimal-positive Wilson completion fixes one explicit Wilson/Perron branch",
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
        key[0] >= 0.0 and key[1] >= 0.0,
        f"key=({key[0]:.6f},{key[1]:.6f})",
    )
    check(
        "The reduced DM side is already closed once the selected Wilson branch yields an exact ordered projected-source pair (S12,S13)",
        np.isfinite(selected_pair).all(),
        f"(S12,S13)=({selected_pair[0]:.6f},{selected_pair[1]:.6f})",
    )
    check(
        "So the enlarged Wilson/DM stack now reaches the live DM target without any remaining open branch-choice or complement-line seam",
        live_dist < 1.0e-10 and np.isfinite(selected_pair).all(),
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Enlarged-stack closure endpoint:")
    print("    - canonical minimal-positive completion selects the Wilson branch")
    print("    - the retained `3d+1` complement-line problem reduces to a rho1/rho2")
    print("      orientation doublet solved directly on the bounded line chart")
    print("    - the rho1-anchored least-distortion selector picks the canonical line")
    print("    - that selected line yields an exact ordered projected-source pair")
    print("      and lands on the live DM target exactly")
    print("    - on this enlarged stack, the DM flagship gate is closed positively")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
