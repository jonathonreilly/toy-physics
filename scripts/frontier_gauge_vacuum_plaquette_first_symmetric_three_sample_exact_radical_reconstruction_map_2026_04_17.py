#!/usr/bin/env python3
"""
Exact radical-form reconstruction map for the first symmetric three-sample
plaquette PF target.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import sympy as sp


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


def radical_entries() -> dict[str, sp.Expr]:
    rt2 = sp.sqrt(2)
    s = sp.sqrt(2 - rt2)
    u = sp.sqrt(2 - sp.sqrt(2 + rt2))
    v = sp.sqrt(2 - sp.sqrt(2 - rt2))
    sigma = sp.sqrt(2 + rt2)
    x = sp.sqrt(2 + sp.sqrt(2 + rt2))
    y = sp.sqrt(2 + sp.sqrt(2 - rt2))
    return {
        "r": rt2,
        "s": s,
        "u": u,
        "v": v,
        "sigma": sigma,
        "x": x,
        "y": y,
        "a": -3 * s,
        "b": -3 * rt2 + 3 * u + 3 * v,
        "c": 16 + 8 * sigma - 8 * x - 8 * y,
        "d": 3 * rt2 + 3 * u - 3 * v,
        "e": 16 - 8 * sigma - 8 * x + 8 * y,
    }


def radical_sample_matrix(entries: dict[str, sp.Expr]) -> sp.Matrix:
    return sp.Matrix(
        [
            [1, entries["a"], 0],
            [1, entries["b"], entries["c"]],
            [1, entries["d"], entries["e"]],
        ]
    )


def exact_trig_sample_matrix() -> sp.Matrix:
    pi = sp.pi
    sample_angles = [
        (-13 * pi / 16, 5 * pi / 8),
        (-5 * pi / 16, -7 * pi / 16),
        (7 * pi / 16, -11 * pi / 16),
    ]
    rows: list[list[sp.Expr]] = []
    for theta1, theta2 in sample_angles:
        rows.append(
            [
                sp.Integer(1),
                6 * (sp.cos(theta1) + sp.cos(theta2) + sp.cos(theta1 + theta2)),
                8
                * (
                    2
                    + 2 * sp.cos(theta1 - theta2)
                    + 2 * sp.cos(2 * theta1 + theta2)
                    + 2 * sp.cos(theta1 + 2 * theta2)
                ),
            ]
        )
    return sp.Matrix(rows)


def instantiated_inverse(entries: dict[str, sp.Expr]) -> tuple[sp.Expr, sp.Matrix]:
    a = entries["a"]
    b = entries["b"]
    c = entries["c"]
    d = entries["d"]
    e = entries["e"]
    delta = a * c - a * e + b * e - c * d
    finv = sp.Matrix(
        [
            [(b * e - c * d) / delta, -a * e / delta, a * c / delta],
            [(c - e) / delta, e / delta, -c / delta],
            [(-b + d) / delta, (a - d) / delta, (-a + b) / delta],
        ]
    )
    return delta, finv


def max_abs_complex(matrix: sp.Matrix) -> float:
    return max(abs(complex(sp.N(matrix[i, j], 100))) for i in range(matrix.rows) for j in range(matrix.cols))


def main() -> int:
    first_three_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_RECONSTRUCTION_NOTE_2026-04-17.md"
    )
    beta6_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    entries = radical_entries()
    f_rad = radical_sample_matrix(entries)
    f_trig = exact_trig_sample_matrix()
    trig_gap = max_abs_complex(f_rad - f_trig)
    f_numeric = np.array([[float(sp.N(f_rad[i, j], 50)) for j in range(f_rad.cols)] for i in range(f_rad.rows)])

    delta, finv = instantiated_inverse(entries)
    det_abs = abs(float(sp.N(delta, 50)))
    singular_floor = float(np.min(np.linalg.svd(f_numeric, compute_uv=False)))

    coeff_vec = sp.Matrix([sp.Integer(1), sp.Rational(37, 100), sp.Rational(4, 25)])
    z_vec = f_rad * coeff_vec
    coeff_rec = finv * z_vec
    rec_gap = max_abs_complex(coeff_rec - coeff_vec)

    za, zb, zc = sp.symbols("Z_A Z_B Z_C")
    z_sym = sp.Matrix([za, zb, zc])
    coeff_map = finv * z_sym
    row_a_orbit2 = f_rad[0, 2]
    c_sign = float(sp.N(entries["c"], 50))
    e_sign = float(sp.N(entries["e"], 50))
    antipodal_gap = abs(complex(sp.N(sp.exp(-13 * sp.I * sp.pi / 16) + sp.exp(3 * sp.I * sp.pi / 16), 50)))
    chi10_a = sp.exp(5 * sp.I * sp.pi / 8)
    chi10_mod_gap = abs(abs(complex(sp.N(chi10_a, 50))) - 1.0)
    coeff_map_gap = max_abs_complex(finv * f_rad - sp.eye(3))

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE EXACT RADICAL RECONSTRUCTION MAP")
    print("=" * 104)
    print()
    print("Exact radical-form sample matrix F")
    print(f_rad)
    print()
    print("Exact determinant and reconstruction structure")
    print(f"  det(F)                                      = {sp.N(delta, 30)}")
    print(f"  |det(F)|                                    = {det_abs:.12f}")
    print(f"  smallest singular value                      = {singular_floor:.12f}")
    print(f"  max radical/trig matrix gap                 = {trig_gap:.3e}")
    print(f"  exact W_A chi_(1,1) entry                   = {row_a_orbit2}")
    print(f"  exact witness reconstruction gap            = {rec_gap:.3e}")
    print(f"  antipodal-pair gap at W_A                   = {antipodal_gap:.3e}")
    print(f"  ||chi_(1,0)(W_A)| - 1|                      = {chi10_mod_gap:.3e}")
    print(f"  exact chi_(1,1) signs c,e                   = {c_sign:.12f}, {e_sign:.12f}")
    print(f"  exact left-relation gap                     = {coeff_map_gap:.3e}")
    print()
    print("Exact coefficient map a = F^(-1) Z")
    print(coeff_map)
    print()

    check(
        "First three-sample reconstruction note already fixes the named holonomies and the first retained coefficient triple",
        "three explicit regular rational-angle marked holonomies" in first_three_note
        and "first symmetric retained coefficient triple" in first_three_note,
        bucket="SUPPORT",
    )
    check(
        "Beta=6 evaluation-seam reduction note already reduces the live plaquette seam to explicit sample-side matrix elements",
        "remaining explicit `beta = 6` problem is exactly evaluation" in beta6_note
        and "class-sector matrix elements" in beta6_note,
        bucket="SUPPORT",
    )
    check(
        "PF boundary note already records the first retained target as three named same-surface samples",
        "three same-surface marked-holonomy sample values" in pf_note
        or "Z_6^env(W_A)" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "The exact radical-form matrix matches the exact trig-evaluated sample matrix at the named pi/16 holonomies",
        trig_gap < 1.0e-80,
        detail=f"max gap={trig_gap:.3e}",
    )
    check(
        "The first named sample annihilates the chi_(1,1) orbit exactly",
        row_a_orbit2 == 0,
        detail=f"F_(A,2)={row_a_orbit2}",
    )
    check(
        "The W_A decoupling is structural: the torus spectrum contains an antipodal pair so |chi_(1,0)(W_A)| = 1",
        antipodal_gap < 1.0e-40 and chi10_mod_gap < 1.0e-15,
        detail=f"antipodal gap={antipodal_gap:.3e}, ||chi10|-1|={chi10_mod_gap:.3e}",
    )
    check(
        "The structured inverse formula is an exact identity for the explicit radical-form matrix",
        coeff_map_gap < 1.0e-80,
        detail=f"max |F^(-1)F-I|={coeff_map_gap:.3e}",
    )
    check(
        "The exact radical-form three-sample matrix is invertible",
        det_abs > 1.0,
        detail=f"|det(F)|={det_abs:.12f}",
    )
    check(
        "The two non-decoupled chi_(1,1) rows have opposite exact sign",
        c_sign > 1.0e-12 and e_sign < -1.0e-12,
        detail=f"c={c_sign:.12f}, e={e_sign:.12f}",
    )
    check(
        "The exact radical-form reconstruction map recovers the witness coefficient triple exactly",
        rec_gap < 1.0e-80,
        detail=f"max reconstruction gap={rec_gap:.3e}",
    )
    check(
        "So the first retained beta=6 PF seam is exactly evaluation of Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C) followed by a fixed algebraic map with no further universal linear collapse on this witness sector",
        trig_gap < 1.0e-80 and det_abs > 1.0 and rec_gap < 1.0e-80 and coeff_map_gap < 1.0e-80,
        detail="the matrix and inverse are explicit before any beta=6 integral is evaluated",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
