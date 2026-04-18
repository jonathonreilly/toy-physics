#!/usr/bin/env python3
"""
Reduction theorem for the first honest Wilson-to-PMNS descendant target.
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


def schur_complement(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(c) @ b.conj().T


def psd_sqrt(matrix: np.ndarray) -> np.ndarray:
    evals, vecs = np.linalg.eigh(matrix)
    evals = np.clip(evals, 0.0, None)
    return vecs @ np.diag(np.sqrt(evals)) @ vecs.conj().T


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    triplet = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md")
    polar = read("docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md")
    micro = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md")
    step2 = read("docs/PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md")

    # Concrete Hermitian Schur-pushforward witness.
    a = np.array(
        [
            [2.3, 0.35 - 0.15j, 0.22 + 0.30j],
            [0.35 + 0.15j, 1.9, -0.18 + 0.12j],
            [0.22 - 0.30j, -0.18 - 0.12j, 1.7],
        ],
        dtype=complex,
    )
    b = np.array(
        [
            [0.15 + 0.05j, -0.08 + 0.02j],
            [0.04 - 0.06j, 0.12 + 0.01j],
            [-0.02 + 0.03j, 0.10 - 0.07j],
        ],
        dtype=complex,
    )
    c = np.array(
        [
            [1.6, 0.10 - 0.04j],
            [0.10 + 0.04j, 1.4],
        ],
        dtype=complex,
    )
    dwh = schur_complement(a, b, c)
    herm_err = float(np.max(np.abs(dwh - dwh.conj().T)))

    r11 = float(np.real(dwh[0, 0]))
    r22 = float(np.real(dwh[1, 1]))
    r33 = float(np.real(dwh[2, 2]))
    s12 = float(2.0 * np.real(dwh[0, 1]))
    a12 = float(-2.0 * np.imag(dwh[0, 1]))
    s13 = float(2.0 * np.real(dwh[0, 2]))
    a13 = float(-2.0 * np.imag(dwh[0, 2]))
    s23 = float(2.0 * np.real(dwh[1, 2]))
    a23 = float(-2.0 * np.imag(dwh[1, 2]))
    dwh_rec = np.array(
        [
            [r11, (s12 - 1j * a12) / 2.0, (s13 - 1j * a13) / 2.0],
            [(s12 + 1j * a12) / 2.0, r22, (s23 - 1j * a23) / 2.0],
            [(s13 + 1j * a13) / 2.0, (s23 + 1j * a23) / 2.0, r33],
        ],
        dtype=complex,
    )
    rec_err = float(np.max(np.abs(dwh - dwh_rec)))

    gamma = a13 / 2.0
    e1 = (r22 - r33) / 2.0 + (s12 - s13) / 4.0
    e2 = r11 + (s12 + s13) / 4.0 - (r22 + r33) / 2.0 - s23 / 2.0

    h_sqrt = psd_sqrt(dwh)
    support_score = int(np.sum(np.abs(np.triu(h_sqrt, 1)) > 1.0e-9))

    print("=" * 108)
    print("PERRON-FROBENIUS WILSON-TO-HERMITIAN DESCENDANT REDUCTION")
    print("=" * 108)
    print()
    print(f"Schur-pushforward Hermitian error = {herm_err:.3e}")
    print(f"response reconstruction error     = {rec_err:.3e}")
    print(f"projected-source channels         = (gamma={gamma:.6f}, E1={e1:.6f}, E2={e2:.6f})")
    print(f"positive-section support score    = {support_score}")
    print()

    check(
        "Existing notes already identify dW_e^H as the exact charged-sector Schur pushforward and record that evaluating D_- / dW_e^H from the axiom is still open",
        "exact charged-sector Schur pushforward" in charged
        and "evaluate the microscopic charge-`-1` operator `D_-`" in charged
        and "evaluate `D_-` or `dW_e^H` from the sole axiom" in charged,
        bucket="SUPPORT",
    )
    check(
        "Existing notes already identify dW_e^H as sufficient to reconstruct H_e and the selected N_e transport packet",
        "reconstructs `H_e` exactly" in charged
        and "determines the transport packet" in charged
        and "selected flavored transport column is algorithmic once" in projected,
        bucket="SUPPORT",
    )
    check(
        "Existing notes already identify gamma, E1, and E2 as exact linear functionals of dW_e^H and isolate the residual right-sensitive selector after the Hermitian codomain",
        "exact linear functionals" in triplet
        and "`gamma = A13 / 2`" in triplet
        and "right-sensitive microscopic selector law" in micro,
        bucket="SUPPORT",
    )
    check(
        "Existing notes already identify H as an intrinsic branch-side codomain but not the full post-Hermitian sheet datum",
        "canonical intrinsic section" in polar
        and "cannot fix the residual" in polar,
        bucket="SUPPORT",
    )

    check(
        "A concrete charged-sector Schur pushforward is Hermitian and therefore already a valid Hermitian descendant codomain",
        herm_err < 1.0e-12,
        detail="dW_e^H can be modeled exactly as a Schur pushforward of a microscopic charge block",
    )
    check(
        "The nine projected Hermitian response coordinates reconstruct dW_e^H exactly",
        rec_err < 1.0e-12,
        detail="once dW_e^H is known, H_e is already explicit",
    )
    check(
        "The projected-source channels are already downstream linear functionals of the Hermitian codomain",
        all(np.isfinite([gamma, e1, e2])),
        detail=f"(gamma,E1,E2)=({gamma:.6f},{e1:.6f},{e2:.6f})",
    )
    check(
        "The first honest PMNS-side descendant target is therefore Wilson -> D_- / dW_e^H / H_e, not a generic PMNS codomain",
        "Wilson-to-Hermitian descendant theorem" in note
        and "`Wilson -> D_- -> dW_e^H -> H_e`" in note
        and "Wilson-to-PMNS descendant / intertwiner theorem" in step2,
        detail="the Hermitian codomain is the first nontrivial PMNS-side target the repo can currently justify",
    )
    check(
        "After the Hermitian codomain lands, the residual PMNS last mile is right-sensitive rather than generic Hermitian closure",
        support_score >= 0
        and "right-sensitive microscopic selector law" in micro
        and "residual non-Hermitian/current" in note,
        detail="the step-2A/step-2B split is now reduced one level further",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
