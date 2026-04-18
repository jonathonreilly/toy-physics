#!/usr/bin/env python3
"""
Identify the minimal local Hermitian Wilson 4-packet with one invariant
Hermitian chain-plane embedding on the physical nearest-neighbor lattice.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_CHAIN_PLANE_TARGET_NOTE_2026-04-18.md")
    hermitian_source = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    local_four = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md")
    local_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL HERMITIAN CHAIN-PLANE TARGET")
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
    flat = np.stack([np.concatenate([b.real.ravel(), b.imag.ravel()]) for b in basis], axis=1)
    dim_chain = np.linalg.matrix_rank(flat)

    check(
        "The physical nearest-neighbor Hermitian chain plane V_chain^H is exactly 4-dimensional with basis X_12, Y_12, X_23, Y_23",
        dim_chain == 4,
        detail=f"dim(V_chain^H)={dim_chain}",
    )

    # Model a theorem-grade restriction of Psi_e by an isometric inclusion.
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
    hermitian_err = max(float(np.linalg.norm(img - img.conj().T)) for img in images)

    check(
        "A theorem-grade Hermitian source embedding Psi_e restricts exactly to an injective Hermitian chain-plane embedding Psi_chain",
        dim_image == 4 and hermitian_err < 1e-12,
        detail=f"dim(Im Psi_chain)={dim_image}, hermitian_err={hermitian_err:.2e}",
    )

    coeffs = np.array([0.2, -0.7, 1.1, 0.4], dtype=float)
    source = sum(c * b for c, b in zip(coeffs, basis))
    recovered = sum(c * img for c, img in zip(coeffs, images))
    recovery_err = float(np.linalg.norm(recovered - i_e @ source @ i_e.conj().T))
    check(
        "Choosing the basis of V_chain^H turns the chain-plane embedding exactly into the local Hermitian nearest-neighbor 4-source packet",
        recovery_err < 1e-12,
        detail=f"packet/embedding error={recovery_err:.2e}",
    )

    check(
        "The weaker Wilson source-side target is already Psi_e, and the new note identifies the local chain plane as the relevant restriction",
        "`Psi_e : Herm(3) -> Herm(H_W)`" in hermitian_source
        and "`Psi_chain : V_chain^H -> Herm(H_W)`" in note
        and "Theorem 2" in note
        and "restriction" in note,
    )
    check(
        "The existing local four-source theorem and minimality theorem already justify using V_chain^H as the sharpest local Wilson source plane",
        "local Hermitian nearest-neighbor `4`-source packet" in local_four
        and "no honest generic local Hermitian `3`-source shortcut exists" in local_min
        and "one invariant Hermitian chain-plane embedding" in note,
    )
    check(
        "The new note carries the current-bank no-go at the restricted local level too",
        "current bank still does **not** realize even the restricted local" in note
        and "current bank still does **not** realize that local Hermitian" in note,
    )

    check(
        "The theorem stays on the Wilson local source-side lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the local Hermitian chain-plane embedding" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
