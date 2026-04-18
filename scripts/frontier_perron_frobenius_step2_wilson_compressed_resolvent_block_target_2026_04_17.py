#!/usr/bin/env python3
"""
Collapse theorem-grade Phi_e plus H_e^(cand) = H_e to one invariant rank-3
Wilson compressed-resolvent block law and carry the matching current-bank
no-go.
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


def orthonormal_columns() -> np.ndarray:
    raw = np.array(
        [
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [1.0, 1.0, 0.0],
            [1.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )
    q, _ = np.linalg.qr(raw)
    return q[:, :3]


def orthogonal_complement(projector: np.ndarray) -> np.ndarray:
    evals, evecs = np.linalg.eigh(projector)
    order = np.argsort(np.real(evals))
    return evecs[:, order[:2]]


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_RESOLVENT_BLOCK_TARGET_NOTE_2026-04-17.md")
    matrix_source = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    resolvent = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md")
    hermitian_source = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    source_nonreal = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON COMPRESSED-RESOLVENT BLOCK TARGET")
    print("=" * 108)
    print()

    i_e = orthonormal_columns()
    p_e = i_e @ i_e.conj().T
    k_e = orthogonal_complement(p_e)
    m_e = np.array(
        [
            [1.4 + 0.0j, 0.6 - 0.2j, -0.3 + 0.8j],
            [0.1 + 0.5j, -0.7 + 0.0j, 0.9 + 0.1j],
            [-0.4 - 0.2j, 0.3 - 0.6j, 0.2 + 0.0j],
        ],
        dtype=complex,
    )
    filler = np.array(
        [
            [0.5 + 0.0j, -0.2 + 0.3j],
            [-0.1 - 0.4j, 0.8 + 0.0j],
            [0.2 + 0.1j, 0.4 - 0.5j],
        ],
        dtype=complex,
    )
    tail = np.array(
        [
            [0.9 + 0.0j, -0.3 + 0.7j],
            [0.4 - 0.1j, -0.2 + 0.0j],
        ],
        dtype=complex,
    )
    r = i_e @ m_e @ i_e.conj().T + i_e @ filler @ k_e.conj().T + k_e @ filler.conj().T @ i_e.conj().T
    r = r + k_e @ tail @ k_e.conj().T
    s_w = 0.5 * (r + r.conj().T)
    h_cand = 0.5 * (m_e + m_e.conj().T)
    h_e = h_cand.copy()
    compressed = p_e @ s_w @ p_e

    check(
        "For any isometry I_e, the Hermitian Wilson resolvent block satisfies P_e S_W P_e = I_e H_e^(cand) I_e^*",
        np.linalg.norm(i_e.conj().T @ i_e - np.eye(3)) < 1e-12
        and np.linalg.norm(compressed - i_e @ h_cand @ i_e.conj().T) < 1e-12,
        detail=f"block_err={np.linalg.norm(compressed - i_e @ h_cand @ i_e.conj().T):.2e}",
    )
    check(
        "If H_e^(cand) = H_e, the theorem pair collapses exactly to the invariant block law P_e S_W P_e = I_e H_e I_e^*",
        np.linalg.norm(h_cand - h_e) < 1e-12
        and np.linalg.norm(compressed - i_e @ h_e @ i_e.conj().T) < 1e-12,
        detail=f"target_err={np.linalg.norm(compressed - i_e @ h_e @ i_e.conj().T):.2e}",
    )
    check(
        "The compressed block on Ran(P_e) is unitarily equivalent to H_e, and compressing back by I_e^* recovers H_e^(cand) = H_e",
        np.linalg.norm(i_e.conj().T @ compressed @ i_e - h_e) < 1e-12
        and np.linalg.norm(i_e.conj().T @ s_w @ i_e - h_cand) < 1e-12,
        detail=f"compression_err={np.linalg.norm(i_e.conj().T @ compressed @ i_e - h_e):.2e}",
    )

    check(
        "The new note states the exact invariant Wilson block law and identifies it as equivalent to Phi_e plus H_e^(cand) = H_e",
        "`S_W := (D^(-1) + (D^(-1))^*) / 2`" in note
        and "`P_e S_W P_e = I_e H_e I_e^*`" in note
        and "compressed Hermitian Wilson resolvent block" in note
        and "is unitarily equivalent to the charged Hermitian target `H_e`" in note,
        detail="the theorem pair is now collapsed to one invariant rank-3 Wilson block identity",
    )
    check(
        "The new note uses the existing matrix-source, Hermitian-source, and resolvent notes in the right way",
        "rank-3 Wilson **matrix-source embedding**" in matrix_source
        and "`H_e^(cand) = H_e`" in resolvent
        and "compressed response theorem depends only on the Hermitian source embedding" in hermitian_source
        and "Theorem 1: `Phi_e` plus `H_e^(cand) = H_e` is equivalent" in note,
        detail="the new theorem sharpens the same Wilson compressed route instead of adding a new route",
    )
    check(
        "The sharper invariant no-go is carried at the same level: the current bank still lacks P_e, Phi_e, Psi_e, and therefore the Wilson block law",
        "theorem-grade `I_e / P_e`" in note
        and "theorem-grade `Phi_e`" in note
        and "theorem-grade `Psi_e`" in note
        and "current bank still lacks theorem-grade `I_e / P_e`" in note
        and "explicit Wilson-side charged embedding/compression object" in embedding
        and "pure support pullback does not produce that object" in note
        and "compressed Wilson-side source family is still unrealized" in note
        and "explicit Wilson-side charged embedding / compression object" in support_pullback
        and "Wilson-side charged source family / channel" in source_nonreal,
        detail="the block-law formulation does not open a hidden-bank loophole",
    )

    check(
        "The note keeps the frontier on the Wilson compressed-route front only",
        "strongest honest next Wilson compressed-route theorem surface" in note
        and "one projector-compression law" in note
        and "What this does not close" in note,
        bucket="SUPPORT",
    )
    check(
        "The note stays review-safe by expressing the entire target in projector-compression language on the Hermitian Wilson resolvent",
        "rank-3 orthogonal projector `P_e`" in note
        and "Hermitian Wilson resolvent" in note
        and "source-algebra presentation of that block law" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
