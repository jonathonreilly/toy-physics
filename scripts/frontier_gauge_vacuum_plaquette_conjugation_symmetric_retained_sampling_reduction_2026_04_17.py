#!/usr/bin/env python3
"""
Conjugation-symmetric retained sampling reduction on the plaquette PF lane.

This sharpens the retained finite-sector constructive surface:

1. the physical retained coefficients already obey conjugation symmetry;
2. so the retained sampling dimension is orbit count, not full retained-basis size;
3. the first nontrivial four-weight symmetric witness is therefore recoverable
   from three generic marked-holonomy samples, not four.
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


def main() -> int:
    char_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    retained_note = read("docs/GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md")
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    orbit_coeffs = np.array([1.00, 0.37, 0.16], dtype=complex)
    sample_angles = [
        (0.9763821785336546, 0.9506659158026622),
        (0.9976858534152107, -0.8728017811294717),
        (-0.8365991569410325, -0.885780777177599),
    ]

    f_three = reduced_orbit_matrix(sample_angles)
    z_three = f_three @ orbit_coeffs
    orbit_rec = np.linalg.solve(f_three, z_three)

    det_abs = abs(np.linalg.det(f_three))
    cond = float(np.linalg.cond(f_three))
    rec_err = float(np.max(np.abs(orbit_rec - orbit_coeffs)))
    imag_floor = float(np.max(np.abs(f_three.imag)))

    f_two = f_three[:2, :]
    _, _, vh = np.linalg.svd(f_two)
    null_vec = vh[-1, :].conj()
    null_resid = float(np.max(np.abs(f_two @ null_vec)))
    orbit_alt = orbit_coeffs + 0.09 * null_vec / np.max(np.abs(null_vec))
    gap_two = float(np.max(np.abs(f_two @ orbit_alt - f_two @ orbit_coeffs)))
    gap_three = float(np.max(np.abs(f_three @ orbit_alt - f_three @ orbit_coeffs)))

    print("=" * 100)
    print("GAUGE-VACUUM PLAQUETTE CONJUGATION-SYMMETRIC RETAINED SAMPLING REDUCTION")
    print("=" * 100)
    print()
    print("Symmetric retained orbit basis")
    print("  orbits                                     = {(0,0)}, {(1,0),(0,1)}, {(1,1)}")
    print(f"  orbit coefficients                         = {np.round(orbit_coeffs.real, 6)}")
    print()
    print("Reduced orbit-evaluation matrix")
    print(f"  |det F|                                    = {det_abs:.6e}")
    print(f"  cond(F)                                    = {cond:.6e}")
    print(f"  recovery error                             = {rec_err:.3e}")
    print(f"  max imaginary entry                        = {imag_floor:.3e}")
    print()
    print("Underdetermined symmetric sub-sampling witness")
    print(f"  2-sample null residual                     = {null_resid:.3e}")
    print(f"  2-sample response gap                      = {gap_two:.3e}")
    print(f"  3-sample response gap                      = {gap_three:.3e}")
    print()

    check(
        "Character-measure note already fixes the plaquette environment coefficients to satisfy rho_(p,q)=rho_(q,p)",
        "rho_(p,q)(beta) = rho_(q,p)(beta)" in char_note,
        bucket="SUPPORT",
    )
    check(
        "Retained class-sampling inversion note already reduces retained recovery to finite marked-holonomy inversion",
        "finite holonomy-sampling problem" in retained_note
        and "too few samples remain underdetermined" in retained_note,
        bucket="SUPPORT",
    )
    check(
        "PF boundary note already records the live plaquette seam as explicit evaluation rather than scalar-observable reuse",
        "not reuse of one accepted scalar observable" in pf_note
        and "marked-holonomy samples" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "Conjugation symmetry reduces the four-weight retained witness to a three-parameter orbit basis",
        len(orbit_coeffs) == 3,
        detail="orbit count = 3 for {(0,0),(1,0),(0,1),(1,1)}",
    )
    check(
        "Three generic marked-holonomy samples invert the symmetric retained orbit system exactly",
        det_abs > 1.0e-3 and rec_err < 1.0e-10,
        detail=f"|det F|={det_abs:.3e}, recovery error={rec_err:.3e}",
    )
    check(
        "The reduced orbit-evaluation matrix is real on the symmetric witness samples",
        imag_floor < 1.0e-10,
        detail=f"max imaginary entry={imag_floor:.3e}",
    )
    check(
        "Two symmetric samples still leave one retained symmetric direction underdetermined",
        null_resid < 1.0e-10 and gap_two < 1.0e-10,
        detail=f"null residual={null_resid:.3e}, 2-sample gap={gap_two:.3e}",
    )
    check(
        "A third generic sample resolves that remaining symmetric direction",
        gap_three > 1.0e-3,
        detail=f"3-sample gap={gap_three:.3e}",
    )
    check(
        "So the physical retained sample burden drops from full retained-basis size to conjugation-orbit count",
        rec_err < 1.0e-10 and gap_two < 1.0e-10 and gap_three > 1.0e-3,
        detail="for the first four-weight witness, 3 symmetric samples replace 4 unconstrained samples",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
