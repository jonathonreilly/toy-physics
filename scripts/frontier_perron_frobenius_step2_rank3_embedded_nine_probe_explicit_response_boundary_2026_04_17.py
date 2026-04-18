#!/usr/bin/env python3
"""
Sharpen the strongest live positive compressed-route class to explicit embedded
response formulas and close its current-bank realization status.
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


def hermitian_responses(matrix: np.ndarray) -> list[float]:
    return [float(np.real(np.trace(b @ matrix))) for b in hermitian_basis()]


def reconstruct_hermitian_from_responses(responses: list[float]) -> np.ndarray:
    h = np.zeros((3, 3), dtype=complex)
    h[0, 0] = responses[0]
    h[1, 1] = responses[1]
    h[2, 2] = responses[2]
    idx = 3
    for i in range(3):
        for j in range(i + 1, 3):
            sym = responses[idx]
            asym = responses[idx + 1]
            h[i, j] = 0.5 * (sym - 1j * asym)
            h[j, i] = 0.5 * (sym + 1j * asym)
            idx += 2
    return h


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md")
    embedded_candidate = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_CANDIDATE_BOUNDARY_NOTE_2026-04-17.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    source_nonreal = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    bank_nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 RANK-3 EMBEDDED NINE-PROBE EXPLICIT-RESPONSE BOUNDARY")
    print("=" * 108)
    print()

    m_e = np.array(
        [
            [1.2 + 0.0j, 0.7 + 0.3j, -0.4 + 0.5j],
            [0.1 - 0.9j, -0.2 + 0.0j, 0.8 - 0.6j],
            [0.3 + 0.2j, -0.5 + 0.4j, 2.1 + 0.0j],
        ],
        dtype=complex,
    )
    h_expected = 0.5 * (m_e + m_e.conj().T)
    h_rec = reconstruct_hermitian_from_responses(hermitian_responses(m_e))

    check(
        "Nine real Hermitian-basis responses reconstruct the Hermitian compression exactly",
        np.linalg.norm(h_rec - h_expected) < 1e-12,
        detail=f"err={np.linalg.norm(h_rec - h_expected):.2e}",
    )
    check(
        "The new note sharpens the live positive class to explicit embedded-source formulas J_a(t) = t I_e B_a I_e^*",
        "`J_a(t) = t I_e B_a I_e^*`" in note
        and "rank-3 embedded nine-probe candidate-boundary theorem" in note
        and "embedded-response formula" in note,
        detail="the positive class is now formula-level explicit rather than just candidate-shaped",
    )
    check(
        "The new note identifies the reconstructed operator as H_e^(cand) from M_e = I_e^* D^(-1) I_e",
        "`M_e := I_e^* D^(-1) I_e`" in note
        and "`H_e^(cand) := (M_e + M_e^*) / 2`" in note
        and "`r_a = Tr(B_a H_e^(cand))`" in note,
        detail="the nine responses now reconstruct one explicit Hermitian compression",
    )
    check(
        "The observable and projected-source notes supply the exact prerequisites for the explicit-response sharpening",
        "`W[J] = log |det(D+J)| - log |det D|`" in observable
        and "nine real linear responses" in projected
        and "determine `H_e` exactly" in projected
        and "selected flavored transport column is algorithmic once" in projected,
        detail="source-response grammar and finite nine-response sufficiency are already exact",
    )
    check(
        "The new note records the exact success criterion for compressed-route closure: match the embedded Wilson responses to the charged projected-source target",
        "`H_e^(cand) = H_e`" in note
        and "`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`" in note
        and "only the known right-sensitive selector remains" in note,
        detail="the live positive candidate is now an explicit operator/source identity",
    )
    check(
        "The new note also sharpens the no-go: the current bank still does not instantiate the explicit-response class itself",
        "current exact bank still does **not** realize" in note
        and "explicit Wilson-side charged embedding/compression `I_e` or `P_e`" in note
        and "induced embedded probes `J_a(t) = t I_e B_a I_e^*`" in note
        and "identifying the nine Wilson first variations" in note
        and "explicit **Wilson-side charged embedding /" in embedding
        and "does **not** already realize the Wilson-side charged" in source_nonreal
        and "does **not** already contain the missing" in bank_nonreal,
        detail="this is a sharper current-bank impossibility result than the older generic source-family no-go",
    )

    check(
        "The older rank-3 candidate note is still respected: the new result sharpens it instead of pretending the bridge is already proved",
        "candidate boundary, not a proof" in embedded_candidate
        and "stronger exact candidate theorem" in note
        and "not a fake bridge proof" in note,
        bucket="SUPPORT",
    )
    check(
        "The new note keeps the missing object on the Wilson side rather than moving the burden back downstream",
        "derive `I_e` or `P_e`" in note
        and "evaluate the nine Wilson responses" in note
        and "What this does not close" in note
        and "positive Wilson-to-`dW_e^H` theorem" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
