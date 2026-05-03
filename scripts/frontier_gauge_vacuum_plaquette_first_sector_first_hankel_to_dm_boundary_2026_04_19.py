#!/usr/bin/env python3
"""
Upstream-of-DM seam re-localization: the first Hankel packet (m1,m2),
equivalently the first Jacobi layer (alpha0,beta1).

Scope (conservative):
  This runner is a structural verification of the claim in
  docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_FIRST_HANKEL_TO_DM_BOUNDARY_NOTE_2026-04-19.md.
  The claim has three pieces:

    (A) downstream side: the nilpotent-chain packet-to-DM boundary already
        closes once a Wilson/PF first-layer packet is supplied;
    (B) upstream side:  the earliest Wilson-side scalar packet feeding that
        boundary is the first Hankel packet (m1,m2);
    (C) equivalently:   the first Jacobi layer (alpha0,beta1), with
        alpha0 = m1 and beta1^2 = m2 - m1^2.

  We honestly check, via the same canonical minimal-bulk-completion branch
  used by the sibling packet theorem runner:

    1. there exists one explicit Wilson-side first-layer packet (m1,m2)
       on the canonical (zero-extension / Loewner-minimal positive) branch
       feeding the boundary;
    2. that packet is equivalent to the first Jacobi layer (alpha0,beta1)
       via alpha0 = m1 and beta1^2 = m2 - m1^2;
    3. the produced packet is well-defined (positive Perron eigenvalue,
       conjugation-symmetric Perron state, beta1 > 0, finite m2);
    4. the parent DM-boundary note records that this is now the upstream
       interface that the live route still leaves open;
    5. and that the seam therefore starts exactly at the first-Hankel
       layer of K_6^env after identity-rim reduction (note text check).

  This is a minimum-scoped structural check that demonstrates the specific
  boundary the note describes. It does not attempt to close the open seam.
  It only verifies that the seam is correctly localized at the named layer.
"""

from __future__ import annotations

from pathlib import Path
import math
import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_packet_theorem_2026_04_19 import (
    selected_transfer_and_packet,
)


ROOT = Path(__file__).resolve().parents[1]

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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR FIRST-HANKEL TO DM BOUNDARY")
    print("=" * 118)
    print()
    print("Question:")
    print("  Where exactly does the live-route seam between the Wilson side and the")
    print("  already-closed nilpotent-chain packet-to-DM boundary now sit?")

    boundary_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_FIRST_HANKEL_TO_DM_BOUNDARY_NOTE_2026-04-19.md"
    )

    pkg = selected_transfer_and_packet()
    alpha0 = float(pkg["alpha0"])
    beta1 = float(pkg["beta1"])
    m1 = float(pkg["m1"])
    m2 = float(pkg["m2"])
    eig = float(pkg["eig"])
    psi = np.asarray(pkg["psi"], dtype=float)
    swap = np.asarray(pkg["swap"], dtype=float)
    transfer = np.asarray(pkg["transfer"], dtype=float)

    psi_swap_err = float(np.linalg.norm(swap @ psi - psi))
    sym_err = float(np.max(np.abs(transfer - transfer.T)))
    eig_min = float(np.min(np.linalg.eigvalsh(transfer)))

    # The first Hankel packet equivalence: alpha0 = m1, beta1 = sqrt(m2 - m1^2).
    moment_alpha_gap = abs(alpha0 - m1)
    beta1_from_moments = math.sqrt(max(m2 - m1 * m1, 0.0))
    moment_beta_gap = abs(beta1 - beta1_from_moments)

    print()
    print(f"  selected (m1, m2)                           = ({m1:.12f}, {m2:.12f})")
    print(f"  selected (alpha0, beta1)                    = ({alpha0:.12f}, {beta1:.12f})")
    print(f"  beta1 from moments sqrt(m2 - m1^2)           = {beta1_from_moments:.12f}")
    print(f"  Perron eigenvalue                           = {eig:.12f}")
    print(f"  transfer symmetry / Perron-swap errors      = ({sym_err:.3e}, {psi_swap_err:.3e})")
    print(f"  min eigenvalue(T_sel)                       = {eig_min:.6e}")
    print()

    # (A) Downstream side: the parent note records the closure of the
    # packet-to-DM boundary once a Wilson/PF packet is supplied.
    check(
        "The DM-boundary note records that the nilpotent-chain packet-to-DM boundary already closes the downstream local interface once the actual Wilson/PF packet is supplied",
        "nilpotent-chain packet-to-DM boundary already closes the downstream local" in boundary_note
        and "actual Wilson/PF packet is supplied" in boundary_note,
    )

    # (B) Upstream side: the first Hankel packet is the earliest Wilson-side
    # scalar packet feeding that boundary, and it is constructively realized.
    check(
        "The DM-boundary note names the earliest Wilson-side scalar packet feeding that boundary as the first Hankel packet (m1,m2), and a canonical realization (m1,m2) is finite and well-defined",
        "first Hankel packet `(m1,m2)`" in boundary_note
        and math.isfinite(m1)
        and math.isfinite(m2)
        and m2 > m1 * m1,
        f"(m1,m2)=({m1:.6f},{m2:.6f})",
    )

    # (C) Equivalence: first Jacobi layer (alpha0, beta1) <-> first Hankel
    # packet (m1, m2) via alpha0 = m1 and beta1^2 = m2 - m1^2.
    check(
        "Equivalently (note records first Jacobi layer (alpha0,beta1)), the canonical realization satisfies alpha0 = m1 and beta1^2 = m2 - m1^2 to machine precision",
        "first Jacobi layer" in boundary_note
        and "`(alpha0,beta1)`" in boundary_note
        and moment_alpha_gap < 1.0e-12
        and moment_beta_gap < 1.0e-12
        and beta1 > 0.0,
        f"(|alpha0-m1|,|beta1-sqrt(m2-m1^2)|)=({moment_alpha_gap:.3e},{moment_beta_gap:.3e})",
    )

    # The realized packet is sane: positive Perron eigenvalue, conjugation
    # symmetric Perron state, factorized transfer operator clean.
    check(
        "The selected first-layer packet comes from a well-defined positive conjugation-symmetric factorized transfer operator with a strictly positive Perron eigenvalue",
        eig > 0.0
        and sym_err < 1.0e-10
        and psi_swap_err < 1.0e-10
        and eig_min > -1.0e-10,
        f"(eig,sym,psi_swap,eig_min)=({eig:.3e},{sym_err:.3e},{psi_swap_err:.3e},{eig_min:.3e})",
    )

    # (D) Seam localization: the parent note states the quantitative DM seam
    # now starts exactly at the first-Hankel layer of K_6^env after
    # identity-rim reduction, and that the live stack still leaves it open.
    check(
        "The DM-boundary note locates the quantitative DM seam exactly at the first-Hankel layer of K_6^env after identity-rim reduction, and records that the current stack still leaves that packet open on the live route",
        "quantitative DM seam now starts exactly at the first-Hankel layer of\n`K_6^env` after identity-rim reduction" in boundary_note
        and "current stack still leaves that packet open on the live route" in boundary_note,
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Seam localization (structural):")
    print("    - downstream packet-to-DM boundary already closes once a Wilson/PF")
    print("      packet is supplied (architectural fact recorded in the parent note)")
    print("    - upstream open object is the first Hankel packet (m1,m2),")
    print("      equivalently the first Jacobi layer (alpha0,beta1)")
    print(f"    - one canonical realization on the minimal-bulk completion branch:")
    print(f"        (m1, m2)         = ({m1:.12f}, {m2:.12f})")
    print(f"        (alpha0, beta1)  = ({alpha0:.12f}, {beta1:.12f})")
    print("    - the live-route seam therefore starts exactly at the first-Hankel")
    print("      layer of K_6^env after identity-rim reduction")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
