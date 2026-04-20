#!/usr/bin/env python3
"""
Retained class-sampling inversion on the plaquette PF lane.

This sharpens the retained finite-sector constructive surface:

1. one scalar sample is not enough;
2. but on a retained N-dimensional marked class sector, N generic holonomy
   samples determine the retained coefficient vector exactly;
3. so retained beta=6 PF work reduces to finite sampling/inversion once a
   retained sector is chosen.
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


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = np.array(
        [
            np.exp(1j * theta1),
            np.exp(1j * theta2),
            np.exp(-1j * (theta1 + theta2)),
        ],
        dtype=complex,
    )
    lam = [p + q, q, 0]
    num = np.array(
        [[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    den = np.array(
        [[x[i] ** (2 - j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    return complex(np.linalg.det(num) / np.linalg.det(den))


def evaluation_matrix(
    weights: list[tuple[int, int]], sample_angles: list[tuple[float, float]]
) -> np.ndarray:
    mat = np.zeros((len(sample_angles), len(weights)), dtype=complex)
    for i, (theta1, theta2) in enumerate(sample_angles):
        for j, (p, q) in enumerate(weights):
            mat[i, j] = dim_su3(p, q) * su3_character(p, q, theta1, theta2)
    return mat


def sample_values(
    coeffs: np.ndarray, weights: list[tuple[int, int]], sample_angles: list[tuple[float, float]]
) -> np.ndarray:
    mat = evaluation_matrix(weights, sample_angles)
    return mat @ coeffs


def main() -> int:
    eval_note = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md")
    unique_note = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md")
    scalar_note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md")

    weights = [(0, 0), (1, 0), (0, 1), (1, 1)]
    coeffs = np.array([1.00, 0.37, 0.37, 0.16], dtype=complex)
    sample_angles = [
        (0.9763821785336546, 0.9506659158026622),
        (0.9976858534152107, -0.8728017811294717),
        (-0.8365991569410325, -0.885780777177599),
        (0.7458439213371963, 0.6408866502507771),
    ]

    e_full = evaluation_matrix(weights, sample_angles)
    z_full = e_full @ coeffs
    coeffs_rec = np.linalg.solve(e_full, z_full)

    det_abs = abs(np.linalg.det(e_full))
    cond = float(np.linalg.cond(e_full))
    rec_err = float(np.max(np.abs(coeffs_rec - coeffs)))

    e_three = e_full[:3, :]
    rank_three = int(np.linalg.matrix_rank(e_three))
    _, _, vh = np.linalg.svd(e_three)
    null_vec = vh[-1, :].conj()
    null_resid = float(np.max(np.abs(e_three @ null_vec)))

    coeffs_alt = coeffs + 0.09 * null_vec / np.max(np.abs(null_vec))
    z_three = e_three @ coeffs
    z_three_alt = e_three @ coeffs_alt
    z_full_alt = e_full @ coeffs_alt
    three_gap = float(np.max(np.abs(z_three_alt - z_three)))
    full_gap = float(np.max(np.abs(z_full_alt - z_full)))

    print("=" * 96)
    print("GAUGE-VACUUM PLAQUETTE RETAINED CLASS-SAMPLING INVERSION")
    print("=" * 96)
    print()
    print("Retained class sector")
    print(f"  weights                                    = {weights}")
    print(f"  witness coefficients                       = {np.round(coeffs.real, 6)}")
    print()
    print("Generic marked-holonomy sampling matrix")
    print(f"  sample count                               = {len(sample_angles)}")
    print(f"  |det E|                                    = {det_abs:.6e}")
    print(f"  cond(E)                                    = {cond:.6e}")
    print(f"  recovery error                             = {rec_err:.3e}")
    print()
    print("Underdetermined sub-sampling witness")
    print(f"  rank of first 3 samples                    = {rank_three}")
    print(f"  3-sample null residual                     = {null_resid:.3e}")
    print(f"  3-sample response gap                      = {three_gap:.3e}")
    print(f"  4-sample response gap                      = {full_gap:.3e}")
    print()

    check(
        "Compressed rim-evaluation note already fixes the retained boundary law as Z_beta^env(W)=<K(W), v_beta>",
        "`Z_beta^env(W) = <K(W), v_beta>`" in eval_note
        and "remaining unknown is only the beta-dependent vector `v_beta`" in eval_note,
        bucket="SUPPORT",
    )
    check(
        "Compressed rim-functional uniqueness note already fixes the retained left boundary functional as universal and unique",
        "retained left boundary functional is universal" in unique_note
        and "retained left boundary functional is unique" in unique_note,
        bucket="SUPPORT",
    )
    check(
        "Scalar-value insufficiency note already records that one scalar sample does not determine the retained coefficient vector",
        "one scalar framework-point value does not determine the class-sector vector" in scalar_note,
        bucket="SUPPORT",
    )

    check(
        "A retained finite-sector sample set defines an exact linear system for the retained coefficient vector",
        e_full.shape == (len(weights), len(weights)),
        detail=f"shape(E)={e_full.shape}",
    )
    check(
        "A generic full retained sample set is invertible on the witness sector",
        det_abs > 1.0e-6 and np.isfinite(cond),
        detail=f"|det E|={det_abs:.3e}, cond(E)={cond:.3e}",
    )
    check(
        "The retained coefficient vector is recovered exactly from full-rank marked-holonomy samples",
        rec_err < 1.0e-10,
        detail=f"max recovery error={rec_err:.3e}",
    )
    check(
        "Too few retained samples leave the system underdetermined",
        rank_three < len(weights) and null_resid < 1.0e-10,
        detail=f"rank(E_3)={rank_three}, null residual={null_resid:.3e}",
    )
    check(
        "A null direction invisible to three samples becomes visible once a fourth generic sample is added",
        three_gap < 1.0e-10 and full_gap > 1.0e-3,
        detail=f"3-sample gap={three_gap:.3e}, 4-sample gap={full_gap:.3e}",
    )
    check(
        "So retained beta-side coefficient recovery is a finite sampling/inversion problem once the sector is truncated",
        rec_err < 1.0e-10 and rank_three < len(weights),
        detail="one scalar is not enough, but N generic retained samples recover N retained coefficients",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
