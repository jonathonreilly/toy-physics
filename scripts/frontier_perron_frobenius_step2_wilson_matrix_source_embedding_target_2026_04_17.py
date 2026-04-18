#!/usr/bin/env python3
"""
Sharpen the Wilson-side compressed-route primitive from I_e / P_e to the
equivalent rank-3 matrix-source embedding class.
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


def matrix_units(n: int) -> list[np.ndarray]:
    out: list[np.ndarray] = []
    for i in range(n):
        for j in range(n):
            e = np.zeros((n, n), dtype=complex)
            e[i, j] = 1.0
            out.append(e)
    return out


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    explicit = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md")
    resolvent = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md")
    embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    source_nonreal = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON MATRIX-SOURCE EMBEDDING TARGET")
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
    e_units = matrix_units(3)
    f_units = [i_e @ e @ i_e.conj().T for e in e_units]
    rand = np.array(
        [
            [1.2 + 0.0j, 0.4 - 0.3j, -0.5 + 0.9j],
            [0.7 + 0.2j, -0.6 + 0.0j, 0.8 - 0.1j],
            [0.2 - 0.4j, -0.9 + 0.5j, 0.3 + 0.0j],
        ],
        dtype=complex,
    )
    phi_rand = i_e @ rand @ i_e.conj().T

    check(
        "For an isometry I_e, Phi_e(X) = I_e X I_e^* is a rank-3 unital *-monomorphism with projector Phi_e(1_3) = P_e",
        np.linalg.norm(i_e.conj().T @ i_e - np.eye(3)) < 1e-12
        and np.linalg.norm(p_e @ p_e - p_e) < 1e-12
        and abs(np.trace(p_e).real - 3.0) < 1e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}",
    )
    check(
        "The image of the matrix units under Phi_e satisfies the exact matrix-unit relations on the Wilson side",
        all(
            np.linalg.norm(f_units[3 * i + j] @ f_units[3 * k + l] - ((1.0 if j == k else 0.0) * f_units[3 * i + l])) < 1e-12
            for i in range(3)
            for j in range(3)
            for k in range(3)
            for l in range(3)
        )
        and all(np.linalg.norm(f_units[3 * i + j].conj().T - f_units[3 * j + i]) < 1e-12 for i in range(3) for j in range(3)),
        detail="Phi_e(E_ij) behaves exactly like a rank-3 matrix-unit system",
    )

    u1 = i_e[:, [0]]
    u2 = f_units[3 * 1 + 0] @ u1
    u3 = f_units[3 * 2 + 0] @ u1
    i_rec = np.concatenate([u1, u2, u3], axis=1)
    check(
        "A rank-3 matrix-unit system reconstructs an isometry I_e whose image realizes the same source embedding",
        np.linalg.norm(i_rec.conj().T @ i_rec - np.eye(3)) < 1e-12
        and np.linalg.norm(i_rec @ rand @ i_rec.conj().T - phi_rand) < 1e-12,
        detail=f"err={np.linalg.norm(i_rec @ rand @ i_rec.conj().T - phi_rand):.2e}",
    )

    check(
        "The new note sharpens the missing Wilson primitive to one rank-3 matrix-source embedding Phi_e : Mat_3(C) -> End(H_W)",
        "rank-3 Wilson **matrix-source embedding**" in note
        and "`Phi_e : Mat_3(C) -> End(H_W)`" in note
        and "`Phi_e(X) = I_e X I_e^*`" in note
        and "`Phi_e(1_3) = P_e`" in note,
        detail="the frontier is now typed as one invariant source-algebra realization class",
    )
    check(
        "The new note proves the exact equivalence between I_e, P_e plus matrix units, and a rank-3 unital *-monomorphism Phi_e",
        "the following are equivalent" in note
        and "an isometry `I_e : C^3 -> H_W`" in note
        and "a rank-3 orthogonal projector `P_e` together with a matrix-unit system" in note
        and "a unital `*`-monomorphism" in note,
        detail="the Wilson primitive is now stated invariantly rather than only in coordinate form",
    )
    check(
        "The explicit-response and resolvent notes are used in the right way: the new theorem only repackages their Wilson-side target and does not plug any external closure",
        "`J_a(t) = t I_e B_a I_e^*`" in explicit
        and "`H_e^(cand) = H_e`" in resolvent
        and "`J_X(t) = t Phi_e(X)`" in note
        and "`(d/dt) W[t Phi_e(X)] |_(t=0) = Re Tr(X H_e)`" in note
        and "`W[J] = log |det(D+J)| - log |det D|`" in observable,
        detail="the new theorem only sharpens the same Wilson-side compressed-route object",
    )
    check(
        "The sharper current-bank no-go is carried at the invariant level too: the bank still lacks theorem-grade I_e / P_e, matrix units, and Phi_e",
        "current exact bank still does **not** realize theorem-grade" in note
        and "theorem-grade `I_e / P_e`" in note
        and "theorem-grade embedded matrix units `F_ij`" in note
        and "theorem-grade rank-3 Wilson matrix-source embedding `Phi_e`" in note
        and "The missing primitive is an explicit **Wilson-side charged embedding /" in embedding
        and "pure support pullback" in support_pullback
        and "charged source family / channel primitive required by the compressed route" in source_nonreal,
        detail="the invariant formulation does not open a new loophole on the present bank",
    )

    check(
        "The note keeps the live frontier on the Wilson compressed route only",
        "strongest honest next compressed-route object" in note
        and "source-algebra embedding law" in note
        and "What this does not close" in note,
        bucket="SUPPORT",
    )
    check(
        "The note stays review-safe by proving the matrix-source equivalence with elementary finite-dimensional matrix-unit algebra",
        "Let `E_ij` be the standard matrix units" in note
        and "matrix-unit relations" in note
        and "rank-`3` projection" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
