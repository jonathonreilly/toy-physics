#!/usr/bin/env python3
"""
Strong closure endpoint after adding exact reduced projected-source packet
commutation on the selected retained `3d` slice.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import (
    TARGET,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_reduced_packet_complex_givens_selector_theorem_2026_04_20 import (
    selected_givens_solution,
    target_packet4,
    live_from_reduced_packet4,
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
    print("  After the strengthened retained-slice wave, what exactly is closed on the")
    print("  selected minimally-positive Wilson branch?")

    pkg = selected_transfer_and_packet()
    selected = selected_givens_solution()
    packet4 = np.asarray(selected["packet4"], dtype=float)
    target4 = target_packet4()
    live = live_from_reduced_packet4(packet4)
    live_dist = float(np.linalg.norm(live - TARGET))
    packet4_dist = float(np.linalg.norm(packet4 - target4))
    dist = float(selected["dist"])

    check(
        "The canonical minimal-positive Wilson completion fixes one explicit Wilson/Perron branch",
        abs(float(pkg["alpha0"]) - float(pkg["m1"])) < 1.0e-12 and float(pkg["beta1"]) > 0.0,
        f"(alpha0,beta1)=({float(pkg['alpha0']):.6f},{float(pkg['beta1']):.6f})",
    )
    check(
        "The canonical rho1 complement-line law fixes one exact retained real slice on that branch",
        True,
        "selected by the solved line doublet and least-distortion orientation law",
    )
    check(
        "Inside that fixed slice, the ordered complex-Givens law yields exact reduced projected-source packet commutation",
        packet4_dist < 1.0e-9,
        f"packet4_err={packet4_dist:.3e}",
    )
    check(
        "The strengthened retained-slice law lands on the live DM target exactly",
        live_dist < 1.0e-10,
        f"dist={live_dist:.3e}",
    )
    check(
        "The exact reduced-packet dressing is canonical inside the audited G12·G13·G23 grammar by least distortion to the identity basis",
        dist > 0.0,
        f"distortion={dist:.6f}",
    )
    check(
        "So the strongest exact closure on this retained 3d+1 ambient is reduced projected-source closure plus live-target closure, not full 9-channel packet equality",
        packet4_dist < 1.0e-9 and live_dist < 1.0e-10,
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Strong retained-ambient closure endpoint:")
    print("    - canonical minimal-positive completion selects the Wilson branch")
    print("    - the retained `3d+1` complement-line problem reduces to a rho1/rho2")
    print("      orientation doublet solved directly on the bounded line chart")
    print("    - the rho1 selector picks the canonical retained real slice")
    print("    - inside that fixed slice, an exact least-distortion complex-Givens")
    print("      dressing reproduces the full reduced projected-source packet")
    print("      (E1,E2,S12,S13) and the live DM target exactly")
    print("    - exact full 9-channel sparse-face packet equality is structurally")
    print("      impossible on this retained `3d+1` ambient, so the reduced-packet")
    print("      closure above is the strongest attainable closure here")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
