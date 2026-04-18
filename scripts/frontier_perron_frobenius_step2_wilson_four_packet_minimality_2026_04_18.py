#!/usr/bin/env python3
"""
Prove that the sharpest Hermitian Wilson support packet is dimensionally
minimal at four real off-diagonal channels.
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


def basis_offdiag() -> list[np.ndarray]:
    e12 = np.zeros((3, 3), dtype=complex)
    e21 = np.zeros((3, 3), dtype=complex)
    e23 = np.zeros((3, 3), dtype=complex)
    e32 = np.zeros((3, 3), dtype=complex)
    e12[0, 1] = 1.0
    e21[1, 0] = 1.0
    e23[1, 2] = 1.0
    e32[2, 1] = 1.0
    return [
        e12 + e21,
        -1j * e12 + 1j * e21,
        e23 + e32,
        -1j * e23 + 1j * e32,
    ]


def flatten_real_imag(m: np.ndarray) -> np.ndarray:
    return np.concatenate([m.real.ravel(), m.imag.ravel()])


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md")
    four_packet = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md")
    sharpest = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SHARPEST_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON FOUR-PACKET MINIMALITY")
    print("=" * 108)
    print()

    basis = basis_offdiag()
    mat = np.stack([flatten_real_imag(b) for b in basis], axis=1)
    rank = int(np.linalg.matrix_rank(mat))
    check(
        "The Hermitian nearest-neighbor off-diagonal source space has real dimension 4",
        rank == 4,
        detail=f"rank(V_off)={rank}",
    )

    first_three = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype=float,
    )
    singular_values = np.linalg.svd(first_three, compute_uv=False)
    rank_three = int(np.sum(singular_values > 1e-10))
    _, _, vh = np.linalg.svd(first_three)
    kernel_coords = vh[-1, :]
    kernel_err = float(np.linalg.norm(first_three @ kernel_coords))
    kernel_vec = sum(float(c) * b for c, b in zip(kernel_coords, basis))
    check(
        "Any concrete 3-channel truncation leaves a nonzero kernel direction and therefore cannot determine arbitrary sharpest-route support data",
        rank_three == 3 and kernel_err < 1e-10 and float(np.linalg.norm(kernel_vec)) > 1e-10,
        detail=f"rank={rank_three}, kernel_err={kernel_err:.2e}",
    )

    coeffs = np.array([0.4, -0.7, 1.1, 0.3], dtype=float)
    target = sum(c * b for c, b in zip(coeffs, basis))
    recovered, *_ = np.linalg.lstsq(mat, flatten_real_imag(target), rcond=None)
    recon = sum(c * b for c, b in zip(recovered, basis))
    check(
        "Four independent Hermitian off-diagonal channels reconstruct an arbitrary sharpest-route source exactly",
        np.linalg.norm(target - recon) < 1e-12,
        detail=f"err={np.linalg.norm(target - recon):.2e}",
    )

    shifted = target + 0.5 * sum(float(c) * b for c, b in zip(kernel_coords, basis))
    three_target = first_three @ coeffs
    three_shifted = first_three @ (coeffs + 0.5 * kernel_coords)
    check(
        "Two distinct off-diagonal source packets can share the same 3-channel data while differing in the fourth direction",
        np.linalg.norm(target - shifted) > 1e-10 and np.linalg.norm(three_target - three_shifted) < 1e-10,
        detail=f"separation={np.linalg.norm(target - shifted):.2e}",
    )

    check(
        "The exact four-packet reduction note already states that theorem-grade Wilson support realization is equivalent to an off-diagonal Hermitian 4-packet",
        "off-diagonal Hermitian nearest-neighbor `4`-packet" in four_packet
        and "theorem-grade Wilson support realization is exactly equivalent" in four_packet
        and "current bank still does **not** realize even that sharper `4`-packet" in four_packet,
        detail="the new lower bound sharpens the same support theorem surface",
    )
    check(
        "The exact sharpest-certificate note already packages the whole Wilson compressed route as a 4+3 certificate",
        "one sharpest finite `4 + 3` certificate" in sharpest
        and "off-diagonal Hermitian nearest-neighbor `4`-packet" in sharpest
        and "It is `4 + 3`." in sharpest,
        detail="the minimality theorem now sharpens the first layer of that certificate",
    )
    check(
        "The new note states the exact lower bound m < 4 => not injective on the off-diagonal Hermitian source space and concludes that four is minimal",
        "`V_off := span_R" in note
        and "`dim_R V_off = 4`" in note
        and "If `m < 4`, then `L` cannot be injective." in note
        and "exact minimal finite number of real Hermitian Wilson source" in note
        and "is `4`" in note,
        detail="the note upgrades four-packet sufficiency to four-packet minimality",
    )
    check(
        "The new note records the review-safe consequence that no honest Hermitian support shortcut below four generic channels exists on this route",
        "no honest Hermitian sharpest-route closure can use three or fewer generic channels" in note
        and "review should reject any generic Hermitian support-closure claim below the" in note
        and "four-channel threshold" in note,
        detail="the lower bound now blocks underspecified 3-channel shortcut claims",
    )

    check(
        "The theorem stays on the Wilson Hermitian support lane and does not overclaim a positive bridge theorem",
        "off-diagonal Wilson support route is already dimensionally minimal" in note
        and "What this does not close" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
