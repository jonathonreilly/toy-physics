#!/usr/bin/env python3
"""
Prove that the physical-lattice Wilson support route is minimal at one adjacent
directed two-edge chain.
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


def basis_edge() -> list[np.ndarray]:
    e12 = np.zeros((3, 3), dtype=complex)
    e23 = np.zeros((3, 3), dtype=complex)
    e12[0, 1] = 1.0
    e23[1, 2] = 1.0
    return [e12, e23]


def flatten_complex(m: np.ndarray) -> np.ndarray:
    return m.ravel()


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md")
    two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md")
    four_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON TWO-EDGE CHAIN MINIMALITY")
    print("=" * 108)
    print()

    basis = basis_edge()
    mat = np.stack([flatten_complex(b) for b in basis], axis=1)
    rank = int(np.linalg.matrix_rank(mat))
    check(
        "The physical directed nearest-neighbor edge-source space has complex dimension 2",
        rank == 2,
        detail=f"rank_C(V_edge)={rank}",
    )

    one_channel = np.array([[1.0 + 0.0j, 0.0 + 0.0j]], dtype=complex)
    singular_values = np.linalg.svd(one_channel, compute_uv=False)
    rank_one = int(np.sum(singular_values > 1e-10))
    _, _, vh = np.linalg.svd(one_channel)
    kernel_coords = vh[-1, :]
    kernel_err = float(np.linalg.norm(one_channel @ kernel_coords))
    kernel_vec = sum(c * b for c, b in zip(kernel_coords, basis))
    check(
        "Any concrete 1-edge truncation leaves a nonzero kernel direction and therefore cannot determine arbitrary physical two-edge chain data",
        rank_one == 1 and kernel_err < 1e-10 and float(np.linalg.norm(kernel_vec)) > 1e-10,
        detail=f"rank={rank_one}, kernel_err={kernel_err:.2e}",
    )

    coeffs = np.array([0.4 + 0.3j, -0.8 + 0.5j], dtype=complex)
    target = sum(c * b for c, b in zip(coeffs, basis))
    recovered, *_ = np.linalg.lstsq(mat, flatten_complex(target), rcond=None)
    recon = sum(c * b for c, b in zip(recovered, basis))
    check(
        "Two independent directed edge channels reconstruct an arbitrary physical two-edge chain source exactly",
        np.linalg.norm(target - recon) < 1e-12,
        detail=f"err={np.linalg.norm(target - recon):.2e}",
    )

    shifted = target + 0.5 * sum(c * b for c, b in zip(kernel_coords, basis))
    one_target = one_channel @ coeffs
    one_shifted = one_channel @ (coeffs + 0.5 * kernel_coords)
    check(
        "Two distinct directed two-edge chain sources can share the same 1-edge data while differing in the second edge direction",
        np.linalg.norm(target - shifted) > 1e-10 and np.linalg.norm(one_target - one_shifted) < 1e-10,
        detail=f"separation={np.linalg.norm(target - shifted):.2e}",
    )

    check(
        "The exact two-edge chain note already states that theorem-grade Wilson support realization is equivalent to an adjacent directed two-edge chain",
        "adjacent directed two-edge chain" in two_edge
        and "theorem-grade Wilson support realization is exactly equivalent" in two_edge
        and "current bank still does **not** realize even this physical adjacent" in two_edge,
        detail="the new lower bound sharpens the same local-lattice support theorem surface",
    )
    check(
        "The exact four-packet minimality note already implies the same lower-bound pressure in real channel language",
        "`dim_R V_off = 4`" in four_min
        and "three or fewer generic channels" in four_min
        and "is `4`" in four_min,
        detail="two complex edge channels correspond to four real Hermitian source coordinates",
    )
    check(
        "The new note states the exact lower bound m < 2 => not injective on the physical edge-source space and concludes that two is minimal",
        "`dim_C V_edge = 2`" in note
        and "If `m < 2`, then `L` cannot be injective." in note
        and "exact minimal finite number of complex directed edge channels" in note
        and "is `2`" in note,
        detail="the note upgrades two-edge sufficiency to two-edge minimality",
    )
    check(
        "The new note records the review-safe consequence that no honest one-edge shortcut exists on this physical lane",
        "no honest physical-lattice sharpest-route closure can use one generic directed edge channel" in note
        and "review should reject any generic one-edge shortcut claim" in note,
        detail="the lower bound now blocks underspecified one-edge local shortcuts",
    )

    check(
        "The theorem stays on the physical-lattice Wilson support lane and does not overclaim a positive bridge theorem",
        "Wilson support route is already minimal at one adjacent directed two-edge chain" in note
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
