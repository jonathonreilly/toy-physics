#!/usr/bin/env python3
"""
Prove that the local Hermitian Wilson source route is minimal at one
nearest-neighbor 4-source packet.
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


def real_flatten(m: np.ndarray) -> np.ndarray:
    return np.concatenate([m.real.ravel(), m.imag.ravel()])


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md")
    local_four = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md")
    four_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL HERMITIAN FOUR-SOURCE MINIMALITY")
    print("=" * 108)
    print()

    e12 = e(0, 1)
    e21 = e(1, 0)
    e23 = e(1, 2)
    e32 = e(2, 1)
    x12 = e12 + e21
    y12 = -1j * e12 + 1j * e21
    x23 = e23 + e32
    y23 = -1j * e23 + 1j * e32

    basis = [x12, y12, x23, y23]
    mat = np.stack([real_flatten(b) for b in basis], axis=1)
    rank = int(np.linalg.matrix_rank(mat))
    check(
        "The local Hermitian nearest-neighbor source space has real dimension 4",
        rank == 4,
        detail=f"rank_R(V_loc^H)={rank}",
    )

    three_channel = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype=float,
    )
    rank_three = int(np.linalg.matrix_rank(three_channel))
    _, _, vh = np.linalg.svd(three_channel)
    kernel_coords = vh[-1, :]
    kernel_err = float(np.linalg.norm(three_channel @ kernel_coords))
    kernel_vec = sum(c * b for c, b in zip(kernel_coords, basis))
    check(
        "Any concrete 3-source truncation leaves a nonzero kernel direction and therefore cannot determine arbitrary local Hermitian packet data",
        rank_three == 3 and kernel_err < 1e-10 and float(np.linalg.norm(kernel_vec)) > 1e-10,
        detail=f"rank={rank_three}, kernel_err={kernel_err:.2e}",
    )

    coeffs = np.array([0.3, -0.7, 1.1, -0.4], dtype=float)
    target = sum(c * b for c, b in zip(coeffs, basis))
    recovered, *_ = np.linalg.lstsq(mat, real_flatten(target), rcond=None)
    recon = sum(c * b for c, b in zip(recovered, basis))
    check(
        "Four independent local Hermitian sources reconstruct arbitrary local packet data exactly",
        np.linalg.norm(target - recon) < 1e-12,
        detail=f"err={np.linalg.norm(target - recon):.2e}",
    )

    check(
        "The existing local Hermitian four-source reduction note already states that the remaining constructive primitive is exactly one local Hermitian 4-source packet",
        "local Hermitian nearest-neighbor `4`-source packet" in local_four
        and "current bank still does **not** realize even this sharper local" in local_four,
    )
    check(
        "The existing four-packet minimality note already gives the same lower-bound pressure in Hermitian channel language",
        "`dim_R V_off = 4`" in four_min
        and "three or fewer generic channels" in four_min
        and "is `4`" in four_min,
    )
    check(
        "The new note states the exact lower bound m < 4 => not injective on the local Hermitian source space and concludes that four is minimal",
        "`dim_R V_loc^H = 4`" in note
        and "If `m < 4`, then `L` cannot be injective." in note
        and "exact minimal finite number of real local Hermitian source" in note
        and "is `4`" in note,
    )
    check(
        "The new note records the review-safe consequence that no honest generic local Hermitian 3-source shortcut exists",
        "no honest generic local Hermitian `3`-source shortcut exists" in note
        and "review should reject any generic `3`-source shortcut claim" in note,
    )

    check(
        "The theorem stays on the local Hermitian Wilson source lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "existence of the local Hermitian `4`-source packet on the current bank" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

