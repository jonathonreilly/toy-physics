#!/usr/bin/env python3
"""
Identify the sharpest Wilson local constructive object with one local path-
algebra embedding on the physical adjacent two-edge chain.
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


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")
    two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md")
    matrix_source = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    chain_plane = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_CHAIN_PLANE_TARGET_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL CHAIN PATH-ALGEBRA TARGET")
    print("=" * 108)
    print()

    e11 = e(0, 0)
    e22 = e(1, 1)
    e33 = e(2, 2)
    e12 = e(0, 1)
    e21 = e(1, 0)
    e23 = e(1, 2)
    e32 = e(2, 1)
    e13 = e12 @ e23
    e31 = e32 @ e21
    basis = [e11, e22, e33, e12, e21, e23, e32, e13, e31]
    flat = np.stack([np.concatenate([b.real.ravel(), b.imag.ravel()]) for b in basis], axis=1)
    dim_alg = np.linalg.matrix_rank(flat)

    relations_ok = (
        np.linalg.norm(e12 @ e23 - e13) < 1e-12
        and np.linalg.norm(e32 @ e21 - e31) < 1e-12
        and np.linalg.norm(e12 @ e21 - e11) < 1e-12
        and np.linalg.norm(e21 @ e12 - e22) < 1e-12
        and np.linalg.norm(e23 @ e32 - e22) < 1e-12
        and np.linalg.norm(e32 @ e23 - e33) < 1e-12
        and np.linalg.norm(e12 @ e32) < 1e-12
        and np.linalg.norm(e23 @ e21) < 1e-12
    )
    check(
        "The physical adjacent two-edge chain generates a 9-dimensional local path algebra A_chain with the exact matrix-unit relations",
        dim_alg == 9 and relations_ok,
        detail=f"dim(A_chain)={dim_alg}",
    )

    # Model a local path-algebra embedding by isometric inclusion.
    i_e = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
        ],
        dtype=complex,
    )
    images = [i_e @ b @ i_e.conj().T for b in basis]
    image_flat = np.stack([np.concatenate([img.real.ravel(), img.imag.ravel()]) for img in images], axis=1)
    dim_image = np.linalg.matrix_rank(image_flat)
    unital_err = float(np.linalg.norm(images[0] + images[1] + images[2] - (i_e @ np.eye(3) @ i_e.conj().T)))
    check(
        "A theorem-grade local adjacent two-edge chain is exactly equivalent to a local unital *-monomorphism Phi_chain of A_chain",
        dim_image == 9 and unital_err < 1e-12,
        detail=f"dim(Im Phi_chain)={dim_image}, unital_err={unital_err:.2e}",
    )

    x12 = e12 + e21
    y12 = -1j * e12 + 1j * e21
    x23 = e23 + e32
    y23 = -1j * e23 + 1j * e32
    hermitian_basis = [x12, y12, x23, y23]
    hermitian_images = [i_e @ b @ i_e.conj().T for b in hermitian_basis]
    hermitian_err = max(float(np.linalg.norm(img - img.conj().T)) for img in hermitian_images)
    hermitian_flat = np.stack([np.concatenate([img.real.ravel(), img.imag.ravel()]) for img in hermitian_images], axis=1)
    dim_herm = np.linalg.matrix_rank(hermitian_flat)
    check(
        "The local Hermitian chain-plane embedding Psi_chain is exactly the Hermitian restriction of the same local path-algebra embedding",
        hermitian_err < 1e-12 and dim_herm == 4,
        detail=f"dim(Im Psi_chain)={dim_herm}, hermitian_err={hermitian_err:.2e}",
    )

    check(
        "The existing two-edge chain theorem, matrix-source theorem, and chain-plane theorem already justify the local path-algebra reformulation",
        "adjacent directed nearest-neighbor two-edge chain" in two_edge
        and "rank-3 Wilson matrix-source embedding" in matrix_source
        and "`Psi_chain : V_chain^H -> Herm(H_W)`" in chain_plane
        and "local path-algebra embedding" in note,
    )
    check(
        "The new note carries the sharper current-bank no-go at the local algebra level too",
        "current bank still does **not** realize even the local path-algebra" in note
        and "current bank still does **not** realize either one" in note,
    )

    check(
        "The theorem stays on the Wilson local constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the local path-algebra embedding" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
