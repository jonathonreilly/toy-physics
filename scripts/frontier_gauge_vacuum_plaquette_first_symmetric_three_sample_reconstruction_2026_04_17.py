#!/usr/bin/env python3
"""
First symmetric three-sample reconstruction on the plaquette PF lane.

This turns the first symmetric retained beta=6 step into one explicit target set:

1. choose three explicit regular rational-angle holonomies;
2. build the symmetric orbit-evaluation matrix on
   {chi_(0,0), chi_(1,0)+chi_(0,1), chi_(1,1)};
3. invert it to recover the first retained coefficient triple from three
   same-surface sample values.
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


def reduced_orbit_matrix(sample_angles: list[tuple[float, float]]) -> np.ndarray:
    mat = np.zeros((len(sample_angles), 3), dtype=complex)
    for i, (theta1, theta2) in enumerate(sample_angles):
        chi_10 = su3_character(1, 0, theta1, theta2)
        chi_01 = su3_character(0, 1, theta1, theta2)
        chi_11 = su3_character(1, 1, theta1, theta2)
        mat[i, 0] = dim_su3(0, 0) * 1.0
        mat[i, 1] = dim_su3(1, 0) * chi_10 + dim_su3(0, 1) * chi_01
        mat[i, 2] = dim_su3(1, 1) * chi_11
    return mat


def min_eigenangle_gap(theta1: float, theta2: float) -> float:
    theta3 = -(theta1 + theta2)
    gaps = [
        abs(np.angle(np.exp(1j * (theta1 - theta2)))),
        abs(np.angle(np.exp(1j * (theta1 - theta3)))),
        abs(np.angle(np.exp(1j * (theta2 - theta3)))),
    ]
    return float(min(gaps))


def main() -> int:
    sym_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md"
    )
    char_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    sample_angles = [
        (-13.0 * np.pi / 16.0, 5.0 * np.pi / 8.0),
        (-5.0 * np.pi / 16.0, -7.0 * np.pi / 16.0),
        (7.0 * np.pi / 16.0, -11.0 * np.pi / 16.0),
    ]
    labels = ["A", "B", "C"]

    fmat = reduced_orbit_matrix(sample_angles)
    inv = np.linalg.inv(fmat)

    coeffs = np.array([1.00, 0.37, 0.16], dtype=complex)
    zvec = fmat @ coeffs
    coeffs_rec = inv @ zvec

    det_abs = abs(np.linalg.det(fmat))
    cond = float(np.linalg.cond(fmat))
    rec_err = float(np.max(np.abs(coeffs_rec - coeffs)))
    imag_floor = float(np.max(np.abs(fmat.imag)))
    inv_imag = float(np.max(np.abs(inv.imag)))
    row_a_orbit2 = float(abs(fmat[0, 2]))
    min_gap = min(min_eigenangle_gap(a, b) for a, b in sample_angles)

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE RECONSTRUCTION")
    print("=" * 104)
    print()
    print("Explicit regular marked-holonomy target set")
    for label, (theta1, theta2) in zip(labels, sample_angles):
        theta3 = -(theta1 + theta2)
        print(
            f"  W_{label}: (theta1, theta2, theta3)"
            f" = ({theta1/np.pi:+.6f} pi, {theta2/np.pi:+.6f} pi, {theta3/np.pi:+.6f} pi)"
        )
    print(f"  minimum eigenangle separation                = {min_gap:.6e}")
    print()
    print("Symmetric orbit-evaluation matrix on {chi_(0,0), chi_(1,0)+chi_(0,1), chi_(1,1)}")
    print(f"  |det F|                                      = {det_abs:.12f}")
    print(f"  cond(F)                                      = {cond:.12f}")
    print(f"  max imaginary entry of F                     = {imag_floor:.3e}")
    print(f"  |F_(A,2)|                                    = {row_a_orbit2:.3e}")
    print(f"  max imaginary entry of F^(-1)                = {inv_imag:.3e}")
    print(f"  reconstruction error                         = {rec_err:.3e}")
    print()
    print("Fixed reconstruction matrix F^(-1) (real to numerical tolerance)")
    print(np.round(inv.real, 12))
    print()

    check(
        "Conjugation-symmetric retained-sampling reduction note already reduces the first four-weight witness to a three-parameter orbit basis",
        "retained four-weight set" in sym_note
        and "orbit count `3`" in sym_note
        and "three generic marked-holonomy samples" in sym_note,
        bucket="SUPPORT",
    )
    check(
        "Character-measure note already fixes the physical coefficient symmetry rho_(p,q)=rho_(q,p)",
        "rho_(p,q)(beta) = rho_(q,p)(beta)" in char_note,
        bucket="SUPPORT",
    )
    check(
        "PF boundary note already records that the retained constructive target is explicit marked-holonomy sample evaluation",
        "marked-holonomy" in pf_note and "three symmetric samples" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "The three explicit marked holonomies are regular torus points with distinct eigenangles",
        min_gap > 0.25,
        detail=f"minimum eigenangle gap={min_gap:.6f}",
    )
    check(
        "The explicit three-sample symmetric orbit matrix is invertible and well-conditioned",
        det_abs > 1.0 and cond < 5.0,
        detail=f"|det F|={det_abs:.6f}, cond(F)={cond:.6f}",
    )
    check(
        "The first explicit sample annihilates the chi_(1,1) orbit contribution",
        row_a_orbit2 < 1.0e-10,
        detail=f"|F_(A,2)|={row_a_orbit2:.3e}",
    )
    check(
        "The explicit three-sample inverse reconstructs the first symmetric coefficient triple exactly",
        rec_err < 1.0e-12,
        detail=f"max reconstruction error={rec_err:.3e}",
    )
    check(
        "The explicit reconstruction matrix is real on this symmetric sample set",
        imag_floor < 1.0e-10 and inv_imag < 1.0e-10,
        detail=f"imag(F)={imag_floor:.3e}, imag(F^-1)={inv_imag:.3e}",
    )
    check(
        "So the first retained symmetric beta=6 PF target is exactly evaluation of three named same-surface sample values",
        rec_err < 1.0e-12 and cond < 5.0 and row_a_orbit2 < 1.0e-10,
        detail="evaluate Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C), then apply F^(-1)",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
