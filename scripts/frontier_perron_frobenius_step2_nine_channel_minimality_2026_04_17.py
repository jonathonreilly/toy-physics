#!/usr/bin/env python3
"""
Prove that the finite nine-channel Wilson compressed-route target is
dimensionally minimal on Herm(3).
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


def hermitian_basis() -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for i in range(3):
        e = np.zeros((3, 3), dtype=complex)
        e[i, i] = 1.0
        basis.append(e)
    for i in range(3):
        for j in range(i + 1, 3):
            s = np.zeros((3, 3), dtype=complex)
            s[i, j] = 1.0
            s[j, i] = 1.0
            basis.append(s)
            a = np.zeros((3, 3), dtype=complex)
            a[i, j] = -1j
            a[j, i] = 1j
            basis.append(a)
    return basis


def gram_matrix(basis: list[np.ndarray]) -> np.ndarray:
    return np.array([[float(np.real(np.trace(a @ b))) for b in basis] for a in basis], dtype=float)


def matrix_to_basis_coords(matrix: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    gram = gram_matrix(basis)
    rhs = np.array([float(np.real(np.trace(b @ matrix))) for b in basis], dtype=float)
    return np.linalg.solve(gram, rhs)


def basis_coords_to_matrix(coords: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    for coeff, elem in zip(coords, basis):
        out = out + float(coeff) * elem
    return out


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_MINIMALITY_NOTE_2026-04-17.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    explicit = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md")
    resolvent = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md")
    matrix_embedding = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    nine_channel = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 NINE-CHANNEL MINIMALITY")
    print("=" * 108)
    print()

    basis = hermitian_basis()
    gram = gram_matrix(basis)
    check(
        "Herm(3) has a real basis of size 9 with nondegenerate Hilbert-Schmidt Gram matrix",
        len(basis) == 9 and abs(np.linalg.det(gram)) > 1e-12,
        detail=f"basis_size={len(basis)}, det(G)={np.linalg.det(gram):.1f}",
    )

    first_eight = gram[:8, :]
    singular_values = np.linalg.svd(first_eight, compute_uv=False)
    rank_eight = int(np.sum(singular_values > 1e-10))
    _, _, vh = np.linalg.svd(first_eight)
    kernel_coords = vh[-1, :]
    kernel_matrix = basis_coords_to_matrix(kernel_coords, basis)
    kernel_responses = first_eight @ kernel_coords
    check(
        "Any concrete 8-channel truncation leaves a nonzero Hermitian kernel direction and therefore cannot determine arbitrary H_e",
        rank_eight == 8
        and np.linalg.norm(kernel_coords) > 1e-10
        and np.linalg.norm(kernel_matrix) > 1e-10
        and np.linalg.norm(kernel_responses) < 1e-10,
        detail=f"rank={rank_eight}, kernel_err={np.linalg.norm(kernel_responses):.2e}",
    )

    target = np.array(
        [
            [1.2 + 0.0j, 0.3 - 0.4j, -0.8 + 0.5j],
            [0.3 + 0.4j, -0.6 + 0.0j, 0.7 + 0.2j],
            [-0.8 - 0.5j, 0.7 - 0.2j, 0.9 + 0.0j],
        ],
        dtype=complex,
    )
    coords = matrix_to_basis_coords(target, basis)
    reconstructed = basis_coords_to_matrix(coords, basis)
    check(
        "Nine independent Hermitian-basis responses reconstruct an arbitrary Herm(3) target exactly",
        np.linalg.norm(target - reconstructed) < 1e-12,
        detail=f"err={np.linalg.norm(target - reconstructed):.2e}",
    )

    target_shifted = target + 0.5 * kernel_matrix
    first_eight_target = np.array([float(np.real(np.trace(b @ target))) for b in basis[:8]], dtype=float)
    first_eight_shifted = np.array([float(np.real(np.trace(b @ target_shifted))) for b in basis[:8]], dtype=float)
    check(
        "Two distinct Hermitian targets can share the same 8-channel data while differing in the 9th direction",
        np.linalg.norm(target - target_shifted) > 1e-10
        and np.linalg.norm(first_eight_target - first_eight_shifted) < 1e-10,
        detail=f"separation={np.linalg.norm(target - target_shifted):.2e}",
    )

    check(
        "The projected-source law already states that a 3 x 3 Hermitian block is determined exactly by nine real basis responses",
        "For a `3 x 3` Hermitian block, the nine real linear responses" in projected
        and "determine `H_e` exactly" in projected,
        detail="the compressed codomain already comes with a nine-response sufficiency theorem",
    )
    check(
        "The explicit-response and resolvent notes already pin the Wilson compressed route to Herm(3) data and one operator identity",
        "`M_e := I_e^* D^(-1) I_e`" in explicit
        and "`H_e^(cand) := (M_e + M_e^*) / 2`" in explicit
        and "`H_e^(cand) = H_e`" in resolvent
        and "one operator identity" in resolvent,
        detail="the lower-bound question is now only the minimal coordinate witness size",
    )
    check(
        "The matrix-source embedding and nine-channel target notes already place that witness problem on the Wilson compressed route itself",
        "rank-3 Wilson **matrix-source embedding**" in matrix_embedding
        and "`Phi_e : Mat_3(C) -> End(H_W)`" in matrix_embedding
        and "finite **nine-channel charged Hermitian source family**" in nine_channel,
        detail="the new theorem sharpens the same Wilson-side source family, not a PMNS-native object",
    )
    check(
        "The new note states the exact lower bound m < 9 => not injective on Herm(3) and concludes that nine is minimal",
        "Let `V := Herm(3)`, viewed as a real vector space." in note
        and "`dim_R V = 9`" in note
        and "If `m < 9`, then `L` cannot be injective." in note
        and "exact minimal finite number of real response channels" in note
        and "is `9`" in note,
        detail="the note upgrades nine-channel sufficiency to nine-channel minimality",
    )
    check(
        "The new note records the review-safe consequence that eight or fewer generic channels cannot close the compressed route",
        "no honest compressed-route closure can use eight or fewer generic real channels" in note
        and "So review should reject any generic compressed-route closure claim below the" in note
        and "nine-channel threshold" in note,
        detail="the lower bound now blocks underspecified shortcut claims",
    )

    check(
        "The note stays on the Wilson compressed-route front and does not overclaim a positive bridge theorem",
        "finite Wilson compressed-route response target" in note
        and "What this does not close" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive Wilson-to-`D_-` theorem" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
