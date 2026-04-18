#!/usr/bin/env python3
"""
Sharpen the compressed-route explicit-response class to a single Hermitian
resolvent-compression identity and its sharper current-bank no-go.
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


def responses(matrix: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    herm = 0.5 * (matrix + matrix.conj().T)
    return np.array([float(np.real(np.trace(b @ herm))) for b in basis], dtype=float)


def reconstruct_from_responses(resp: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    g = gram_matrix(basis)
    coeffs = np.linalg.solve(g, resp)
    out = np.zeros((3, 3), dtype=complex)
    for c, b in zip(coeffs, basis):
        out = out + c * b
    return out


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md")
    explicit = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 HERMITIAN RESOLVENT-COMPRESSION TARGET")
    print("=" * 108)
    print()

    basis = hermitian_basis()
    g = gram_matrix(basis)
    check(
        "The standard Hermitian basis has nondegenerate Hilbert-Schmidt pairing, so basis-response equality is equivalent to operator equality on Herm(3)",
        abs(np.linalg.det(g)) > 1e-12,
        detail=f"det(G)={np.linalg.det(g):.1f}",
    )

    m = np.array(
        [
            [1.3 + 0.0j, 0.4 + 0.8j, -0.5 + 0.1j],
            [0.2 - 0.6j, -0.7 + 0.0j, 0.9 - 0.4j],
            [0.5 + 0.3j, -0.2 + 0.9j, 1.1 + 0.0j],
        ],
        dtype=complex,
    )
    h = 0.5 * (m + m.conj().T)
    h_rec = reconstruct_from_responses(responses(m, basis), basis)
    check(
        "The nine embedded responses reconstruct exactly the Hermitian part of the compressed resolvent M_e",
        np.linalg.norm(h - h_rec) < 1e-12,
        detail=f"err={np.linalg.norm(h - h_rec):.2e}",
    )

    check(
        "The new note sharpens the explicit-response family to the single operator identity H_e^(cand) = H_e",
        "`H_e^(cand) := (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`" in note
        and "strongest honest next theorem surface is no longer" in note
        and "one operator identity" in note,
        detail="the compressed frontier is now stated as a single Hermitian resolvent-compression identity",
    )
    check(
        "The new note records the exact equivalence between the family identity on Herm(3), the nine basis-probe equalities, and the single operator equality",
        "the following are equivalent" in note
        and "`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`" in note
        and "`(d/dt) W[t I_e B_a I_e^*] |_(t=0) = Tr(B_a H_e)`" in note
        and "`H_e^(cand) = H_e`" in note,
        detail="the nine-probe family is only the coordinate form of the operator theorem",
    )
    check(
        "The explicit-response and projected-source notes supply the exact prerequisites for that reduction",
        "`M_e := I_e^* D^(-1) I_e`" in explicit
        and "`H_e^(cand) := (M_e + M_e^*) / 2`" in explicit
        and "nine real linear responses" in projected
        and "determine `H_e` exactly" in projected,
        detail="response-family sufficiency and Hermitian reconstruction are already exact in-bank",
    )
    check(
        "The sharper no-go is also carried at the same level: the current bank still does not realize I_e / P_e or identify H_e^(cand) with H_e",
        "current bank still does **not** realize even that sharper target" in note
        and "theorem-grade `I_e` / `P_e`" in note
        and "identification of `H_e^(cand)` with the charged projected" in note
        and "explicit Wilson-side operator `I_e` or `P_e`" in embedding
        and "does **not** already contain the missing" in nonreal,
        detail="the sharper target does not fake a bridge theorem on the present bank",
    )

    check(
        "The note keeps the frontier on the Wilson side rather than moving work back into PMNS codomain algebra",
        "still lives on the Wilson side" in note
        and "derive `I_e` or `P_e`" in note
        and "does not close" in note,
        bucket="SUPPORT",
    )
    check(
        "The note stays a theorem-surface sharpening and not a plug-in closure",
        "exact science-only theorem sharpening" in note
        and "sharper positive target theorem surface" in note
        and "sharper exact current-bank no-go" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
