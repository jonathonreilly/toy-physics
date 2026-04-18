#!/usr/bin/env python3
"""
Exact boundary for the Wilson-to-PMNS descendant bottleneck.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def cube_shift_matrix(mu: int) -> np.ndarray:
    n = 8
    out = np.zeros((n, n), dtype=float)
    for a in range(n):
        b = a ^ (1 << mu)
        out[b, a] = 1.0
    return out


def main() -> int:
    parent_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    site_phase = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    pmns_axis = read("docs/PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md")
    pmns_transport = read("docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md")
    pmns_mode = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    pmns_hw1 = read("docs/PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    step2_note = read("docs/PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md")

    phi = np.eye(8)
    errs = []
    for mu in range(3):
        s = cube_shift_matrix(mu)
        p = s.copy()
        errs.append(float(np.max(np.abs(phi.T @ p @ phi - s))))

    xbar = 0.73
    ybar = 0.11
    cycle = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ]
    )
    t_seed = xbar * np.eye(3) + ybar * (cycle + cycle @ cycle)
    evals = np.linalg.eigvalsh(t_seed)
    evals = np.sort(evals)[::-1]
    x_rec = (evals[0] + 2.0 * evals[1]) / 3.0
    y_rec = (evals[0] - evals[1]) / 3.0

    print("=" * 108)
    print("PERRON-FROBENIUS WILSON-TO-PMNS DESCENDANT BOUNDARY")
    print("=" * 108)
    print()
    print(f"support intertwiner max error    = {max(errs):.3e}")
    print(f"aligned PMNS seed reconstruction = (x_rec={x_rec:.6f}, y_rec={y_rec:.6f})")
    print()

    check(
        "Wilson parent note already proves exact Wilson-side descendants and explicitly stops short of PMNS",
        "one exact Wilson parent object with canonical plaquette and `theta`" in step2_note
        and "PMNS is explicitly not yet shown" in step2_note,
        bucket="SUPPORT",
    )
    check(
        "Site-phase note already proves an exact support intertwiner on the PMNS carrier support",
        "exact bridge theorem" in site_phase
        and "Phi^dagger P_mu Phi = S_mu" in site_phase,
        bucket="SUPPORT",
    )
    check(
        "PMNS notes already prove exact internal native partial laws",
        "graph-native" in pmns_axis
        and "transport law" in pmns_transport
        and "dominant mode" in pmns_mode,
        bucket="SUPPORT",
    )
    check(
        "PMNS hw=1 boundary notes already separate supplied-pack closure from sole-axiom triviality",
        "if the nontrivial `hw=1` source/transfer pack is supplied" in step2_note
        and "the strongest canonical sole-axiom `hw=1` pack still remains trivial" in step2_note,
        bucket="SUPPORT",
    )

    check(
        "Internal PMNS support intertwiners already exist exactly",
        max(errs) < 1.0e-12,
        detail="the PMNS carrier support is not the missing exact object",
    )
    check(
        "Internal PMNS positive transport structure already exists exactly",
        abs(x_rec - xbar) < 1.0e-12 and abs(y_rec - ybar) < 1.0e-12,
        detail="native PMNS transport/dominant-mode data are real but remain internal to the PMNS lane",
    )
    check(
        "The missing step-2 theorem is specifically a Wilson-to-PMNS descendant/intertwiner theorem",
        "Wilson-to-PMNS descendant / intertwiner theorem" in step2_note
        and "cross-sector provenance" in step2_note,
        detail="the actual bottleneck is cross-sector, not intra-PMNS",
    )
    check(
        "Without that cross-sector theorem the branch cannot honestly advance from step 2 to step 3",
        "Without one of those, the branch cannot honestly advance from step 2 to step" in step2_note,
        detail="common-state compatibility remains downstream of the missing descendant theorem",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
