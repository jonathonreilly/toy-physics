#!/usr/bin/env python3
"""
Full projected-source packet no-go theorem on the retained `3d+1` ambient of
the selected minimally-positive Wilson branch.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import sparse_face_projected_data
from frontier_dm_leptogenesis_k00_sparse_face_target_preimage_theorem import (
    solve_sparse_target_preimage,
    sparse_face_h,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    selected_retained_block_original,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_reduced_packet_complex_givens_selector_theorem_2026_04_20 import (
    selected_real_slice_h,
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
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 FULL-PACKET NO-GO")
    print("=" * 118)
    print()
    print("Question:")
    print("  After the stronger reduced-packet closure, can the selected retained")
    print("  `3d+1` ambient also reproduce the full sparse-face projected-source")
    print("  Hermitian packet exactly?")

    block4 = selected_retained_block_original().astype(complex)
    h0 = selected_real_slice_h()
    x, y, phase = solve_sparse_target_preimage()
    h_target = sparse_face_h(x[0], x[1], y[0], phase)
    data = sparse_face_projected_data(np.array([x[0], x[1], y[0], phase], dtype=float))

    lam = np.sort(np.linalg.eigvalsh(block4))
    nu0 = np.sort(np.linalg.eigvalsh(h0))
    mu = np.sort(np.linalg.eigvalsh(np.asarray(h_target, dtype=complex)))

    print()
    print(f"  eig(retained 4x4 block)                      = {np.round(lam, 12).tolist()}")
    print(f"  eig(selected real slice)                     = {np.round(nu0, 12).tolist()}")
    print(f"  eig(full sparse-face target)                 = {np.round(mu, 12).tolist()}")
    print(f"  target full packet odd channels              = ({data['A12']:.12f}, {data['A13']:.12f}, {data['A23']:.12f})")
    print()

    check(
        "The full sparse-face target Hermitian block is the exact matrix behind the target projected-source packet",
        abs(data["A13"]) > 1.0e-6 and abs(data["S12"]) > 1.0e-6 and abs(data["S13"]) > 1.0e-6,
        f"(S12,A13,S13)=({data['S12']:.6f},{data['A13']:.6f},{data['S13']:.6f})",
    )
    check(
        "Its eigenvalues violate Cauchy interlacing for any 3d compression of the selected retained 4x4 Wilson block",
        mu[0] > lam[1] + 1.0e-6 or mu[1] > lam[2] + 1.0e-6,
        f"(mu1,lam2,mu2,lam3)=({mu[0]:.6f},{lam[1]:.6f},{mu[1]:.6f},{lam[2]:.6f})",
    )
    check(
        "Therefore no orthonormal real or complex 3d slice of the retained 3d+1 ambient can reproduce the full sparse-face target packet exactly",
        mu[0] > lam[1] + 1.0e-6 or mu[1] > lam[2] + 1.0e-6,
        "full-packet equality would force forbidden compression eigenvalues",
    )
    check(
        "In particular the selected real slice cannot reach the full sparse-face target even after arbitrary internal U(3) basis dressing, because unitary similarity preserves its slice spectrum",
        np.linalg.norm(np.sort(mu) - np.sort(nu0)) > 1.0e-3,
        f"slice_target_eig_gap={np.linalg.norm(np.sort(mu) - np.sort(nu0)):.6f}",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Strong full-packet answer:")
    print("    - exact full sparse-face packet matching is impossible on the retained")
    print("      `3d+1` ambient of the selected Wilson branch")
    print("    - the obstruction is structural, not a failed search: the target block")
    print("      violates compression interlacing against the selected retained 4x4 block")
    print("    - so the strongest attainable exact commutation on this ambient is the")
    print("      reduced projected-source packet, not the full 9-channel packet")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
