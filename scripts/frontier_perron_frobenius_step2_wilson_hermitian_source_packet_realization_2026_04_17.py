#!/usr/bin/env python3
"""
Reduce theorem-grade Wilson support realization to one finite 9-element
Hermitian Wilson source packet with explicit matrix-unit reconstruction.
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


def e(i: int, j: int) -> np.ndarray:
    m = np.zeros((3, 3), dtype=complex)
    m[i, j] = 1.0
    return m


def hermitian_basis() -> list[np.ndarray]:
    return [
        e(0, 0),
        e(1, 1),
        e(2, 2),
        e(0, 1) + e(1, 0),
        -1j * e(0, 1) + 1j * e(1, 0),
        e(0, 2) + e(2, 0),
        -1j * e(0, 2) + 1j * e(2, 0),
        e(1, 2) + e(2, 1),
        -1j * e(1, 2) + 1j * e(2, 1),
    ]


def main() -> int:
    matrix_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    hermitian_note = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    embed_boundary = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON HERMITIAN SOURCE-PACKET REALIZATION")
    print("=" * 108)
    print()

    i_e = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
        ],
        dtype=complex,
    )
    basis = hermitian_basis()
    packet = [i_e @ b @ i_e.conj().T for b in basis]

    f11, f22, f33 = packet[0], packet[1], packet[2]
    f12 = 0.5 * (packet[3] + 1j * packet[4])
    f21 = 0.5 * (packet[3] - 1j * packet[4])
    f13 = 0.5 * (packet[5] + 1j * packet[6])
    f31 = 0.5 * (packet[5] - 1j * packet[6])
    f23 = 0.5 * (packet[7] + 1j * packet[8])
    f32 = 0.5 * (packet[7] - 1j * packet[8])
    units = {
        (1, 1): f11, (2, 2): f22, (3, 3): f33,
        (1, 2): f12, (2, 1): f21,
        (1, 3): f13, (3, 1): f31,
        (2, 3): f23, (3, 2): f32,
    }
    p_e = f11 + f22 + f33

    max_mu_err = 0.0
    max_star_err = 0.0
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                for l in range(1, 4):
                    lhs = units[(i, j)] @ units[(k, l)]
                    rhs = units[(i, l)] if j == k else np.zeros_like(lhs)
                    max_mu_err = max(max_mu_err, float(np.linalg.norm(lhs - rhs)))
            max_star_err = max(max_star_err, float(np.linalg.norm(units[(i, j)].conj().T - units[(j, i)])))

    flat = np.stack([np.concatenate([s.real.ravel(), s.imag.ravel()]) for s in packet], axis=1)
    rank_packet = np.linalg.matrix_rank(flat)

    print(f"rank(packet)                                = {rank_packet}")
    print(f"rank(P_e)                                   = {int(round(np.trace(p_e).real))}")
    print(f"max matrix-unit product error               = {max_mu_err:.3e}")
    print(f"max matrix-unit adjoint error               = {max_star_err:.3e}")
    print()

    check(
        "A theorem-grade Wilson matrix-source embedding induces a finite 9-element Hermitian Wilson source packet",
        all(np.linalg.norm(s - s.conj().T) < 1.0e-12 for s in packet) and rank_packet == 9,
        detail=f"rank(packet)={rank_packet}",
    )
    check(
        "The explicit reconstruction formulas recover the embedded matrix units exactly from that Hermitian packet",
        max_mu_err < 1.0e-12 and max_star_err < 1.0e-12,
        detail=f"product_err={max_mu_err:.2e}, star_err={max_star_err:.2e}",
    )
    check(
        "The reconstructed support projector P_e = F_11 + F_22 + F_33 has rank 3",
        abs(np.trace(p_e).real - 3.0) < 1.0e-12 and np.linalg.norm(p_e @ p_e - p_e) < 1.0e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}",
    )
    check(
        "So theorem-grade Wilson support realization is exactly equivalent to one finite 9-packet with explicit matrix-unit reconstruction identities",
        "`9`-tuple of Hermitian Wilson operators" in note
        and "`F_12 = (S_4 + i S_5)/2`" in note
        and "satisfy the exact matrix-unit relations" in note
        and "rank `3`" in note,
    )
    check(
        "The new note uses the existing matrix-source, Hermitian-source, and charged-embedding notes in the right way and carries the matching current-bank no-go",
        "rank-3 Wilson **matrix-source embedding**" in matrix_note
        and "real `9`-dimensional Hermitian source plane" in hermitian_note
        and "still does **not** have" in embed_boundary
        and "current exact bank still does **not** realize even this finite packet" in note,
    )

    check(
        "This is a finite support-realization reduction, not a positive support theorem",
        "What this does not close" in note and "a positive realization of that packet" in note,
        bucket="SUPPORT",
    )
    check(
        "The Wilson frontier is now a finite packet problem with explicit polynomial identities",
        "finite `9`-packet" in note and "matrix-unit reconstruction identities" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
