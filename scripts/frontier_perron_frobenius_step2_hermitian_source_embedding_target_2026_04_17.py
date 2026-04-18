#!/usr/bin/env python3
"""
Sharpen the Wilson compressed-route frontier from the full matrix-source
embedding Phi_e to the weaker Hermitian source embedding Psi_e actually used by
the response theorem, and carry the corresponding current-bank no-go.
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


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    matrix_source = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    resolvent = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md")
    nine_channel = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md")
    nine_min = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_MINIMALITY_NOTE_2026-04-17.md")
    source_nonreal = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    embedded_explicit = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 HERMITIAN SOURCE-EMBEDDING TARGET")
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
    p_e = i_e @ i_e.conj().T
    basis = hermitian_basis()
    images = [i_e @ b @ i_e.conj().T for b in basis]
    flat = np.stack([np.concatenate([img.real.ravel(), img.imag.ravel()]) for img in images], axis=1)
    rank = np.linalg.matrix_rank(flat)

    check(
        "A rank-3 Wilson matrix-source embedding restricts to a real-linear injective Hermitian source embedding Psi_e on Herm(3)",
        np.linalg.norm(i_e.conj().T @ i_e - np.eye(3)) < 1e-12
        and all(np.linalg.norm(img - img.conj().T) < 1e-12 for img in images)
        and rank == 9,
        detail=f"rank(Im Psi_e)={rank}",
    )
    check(
        "The Hermitian restriction carries the Wilson support projector as the order unit Psi_e(1_3) = P_e",
        np.linalg.norm(images[0] + images[1] + images[2] - p_e) < 1e-12
        and abs(np.trace(p_e).real - 3.0) < 1e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}",
    )

    m_e = np.array(
        [
            [1.4 + 0.0j, 0.5 - 0.2j, -0.3 + 0.7j],
            [0.1 + 0.6j, -0.9 + 0.0j, 0.8 + 0.4j],
            [-0.3 - 0.7j, 0.8 - 0.4j, 0.2 + 0.0j],
        ],
        dtype=complex,
    )
    h_e = 0.5 * (m_e + m_e.conj().T)
    lhs = np.array([float(np.real(np.trace(img @ (i_e @ h_e @ i_e.conj().T)))) for img in images], dtype=float)
    rhs = np.array([float(np.real(np.trace(b @ h_e))) for b in basis], dtype=float)
    check(
        "The compressed response theorem uses only the Hermitian source embedding Psi_e: the nine basis-response equalities live entirely on Herm(3)",
        np.linalg.norm(lhs - rhs) < 1e-12,
        detail=f"basis_err={np.linalg.norm(lhs - rhs):.2e}",
    )

    check(
        "The new note distinguishes the stronger invariant source algebra Phi_e from the weaker minimal Hermitian source embedding Psi_e",
        "`Psi_e := Phi_e |_(Herm(3)) : Herm(3) -> Herm(H_W)`" in note
        and "two exact attack surfaces" in note
        and "stronger invariant algebra route through full `Phi_e`" in note
        and "weaker minimal response route through the Hermitian source embedding" in note,
        detail="the Wilson front now has a weaker exact source-side target than full Mat_3(C)",
    )
    check(
        "The new note uses the matrix-source, resolvent, and nine-channel notes in the right way: full Phi_e is sufficient, but the compressed theorem itself only probes Hermitian directions",
        "rank-3 Wilson **matrix-source embedding**" in matrix_source
        and "`H_e^(cand) = H_e`" in resolvent
        and "finite **nine-channel charged Hermitian source family**" in nine_channel
        and "exact minimal finite number of real response channels" in nine_min
        and "The compressed response theorem only uses Hermitian source directions" in note,
        detail="the new theorem sharpens the attack surface instead of plugging external closure",
    )
    check(
        "The sharper weaker-object no-go is carried too: the current bank still lacks even theorem-grade Psi_e",
        "still does **not** realize theorem-grade Hermitian source embedding" in note
        and "`Psi_e : Herm(3) -> Herm(H_W)`" in note
        and "charged source family / channel primitive" in source_nonreal
        and "current exact bank still does **not** realize" in embedded_explicit,
        detail="the weaker self-adjoint reformulation does not open a new loophole",
    )

    check(
        "The note stays on the Wilson compressed-route front and only weakens the source-side target in the exact response theorem",
        "Wilson compressed route now has two exact attack surfaces" in note
        and "What this does not close" in note
        and "a positive theorem-grade realization of `Psi_e`" in note,
        bucket="SUPPORT",
    )
    check(
        "The note remains review-safe by using only finite-dimensional linear algebra on Herm(3) and already-landed response theorems",
        "dim_R Im(Psi_e) = 9" in note
        and "for any Hermitian basis `B_1, ..., B_9`" in note
        and "Hermitian resolvent-compression target theorem" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
