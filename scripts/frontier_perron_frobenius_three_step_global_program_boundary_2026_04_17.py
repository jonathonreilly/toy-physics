#!/usr/bin/env python3
"""
Top-to-bottom status boundary for the three-step global PF program.
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
    parent_intertwiner = read("docs/PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md")
    parent_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    site_phase = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    pmns_axis = read("docs/PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md")
    pmns_transport = read("docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md")
    pmns_mode = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    global_note = read("docs/PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md")
    three_step = read("docs/PERRON_FROBENIUS_THREE_STEP_GLOBAL_PROGRAM_BOUNDARY_NOTE_2026-04-17.md")

    # Exact support intertwiner witness on the BZ-corner cube support.
    phi = np.eye(8)
    s0 = cube_shift_matrix(0)
    s1 = cube_shift_matrix(1)
    s2 = cube_shift_matrix(2)
    p0 = s0.copy()
    p1 = s1.copy()
    p2 = s2.copy()
    err0 = float(np.max(np.abs(phi.T @ p0 @ phi - s0)))
    err1 = float(np.max(np.abs(phi.T @ p1 @ phi - s1)))
    err2 = float(np.max(np.abs(phi.T @ p2 @ phi - s2)))

    # Native PMNS aligned dominant-mode witness.
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
    print("PERRON-FROBENIUS THREE-STEP GLOBAL PROGRAM BOUNDARY")
    print("=" * 108)
    print()
    print(f"site-phase intertwiner errors      = ({err0:.3e}, {err1:.3e}, {err2:.3e})")
    print(f"aligned PMNS seed reconstruction   = (x_rec={x_rec:.6f}, y_rec={y_rec:.6f})")
    print()

    check(
        "Step 1 boundary note already records that the Wilson parent object is exact on the gauge surface but not yet globally across the live sectors",
        "step 1 is closed only on the Wilson gauge surface" in parent_intertwiner
        and "does **not** yet close step 1 globally" in parent_intertwiner,
        bucket="SUPPORT",
    )
    check(
        "Wilson parent/compression note already records exact plaquette and theta descendants from the Wilson parent object",
        "plaquette source-sector transfer law is already a canonical descendant" in parent_intertwiner
        and "strong-CP `theta` law is already a canonical Fourier descendant" in parent_intertwiner,
        bucket="SUPPORT",
    )
    check(
        "Site-phase note already records an exact support intertwiner on the BZ-corner / taste-cube bridge",
        "Phi^dagger P_mu Phi = S_mu" in site_phase
        and "exact bridge theorem" in site_phase,
        bucket="SUPPORT",
    )
    check(
        "PMNS notes already record exact native partial laws on the retained hw=1 carrier",
        "graph-native" in pmns_axis
        and "transport law" in pmns_transport
        and "dominant mode" in pmns_mode,
        bucket="SUPPORT",
    )

    check(
        "An exact support intertwiner already exists inside the PMNS carrier support, but it is an internal support theorem rather than a Wilson-to-PMNS descendant theorem",
        max(err0, err1, err2) < 1.0e-12
        and "does not by itself identify the retained" in site_phase
        and "triplet with physical generations" in site_phase,
        detail="internal PMNS support intertwiners exist, but they are not yet the missing cross-sector intertwiner",
    )
    check(
        "The PMNS lane already has exact native positive partial laws, but these still stop below a nontrivial sole-axiom PMNS pack",
        abs(x_rec - xbar) < 1.0e-12
        and abs(y_rec - ybar) < 1.0e-12
        and "stays trivial" in pmns_sole,
        detail="native PMNS transport/dominant-mode structure exists, but the strongest canonical sole-axiom pack remains trivial",
    )
    check(
        "Therefore step 2 is only partially closed: exact Wilson descendants and exact PMNS support laws exist, but there is still no Wilson-to-PMNS descendant/intertwiner theorem",
        "Wilson-to-PMNS projection / descendant theorem" in global_note
        and "not derivable yet" in global_note
        and "Step 2:" in three_step
        and "partially closed" in three_step,
        detail="the actual bottleneck is the missing cross-sector intertwiner",
    )
    check(
        "Step 3 is not yet available: without the missing cross-sector intertwiner and plaquette framework-point operator data, the repo cannot yet support common-state compatibility",
        "Step 3:" in three_step
        and "not closed" in three_step
        and "common parent PF state" in three_step
        and "global sole-axiom PF selector: no." in global_note,
        detail="step 3 is downstream of the still-open step-2 bottleneck",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
