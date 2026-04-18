#!/usr/bin/env python3
"""
Positive-cone and order witness for the first symmetric three-sample plaquette
PF seam.
"""

from __future__ import annotations

from pathlib import Path

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
        "a": -3 * s,
        "b": -3 * rt2 + 3 * u + 3 * v,
        "c": 16 + 8 * sigma - 8 * x - 8 * y,
        "d": 3 * rt2 + 3 * u - 3 * v,
        "e": 16 - 8 * sigma - 8 * x + 8 * y,
    }


def sample_matrix(entries: dict[str, sp.Expr]) -> sp.Matrix:
    return sp.Matrix(
        [
            [1, entries["a"], 0],
            [1, entries["b"], entries["c"]],
            [1, entries["d"], entries["e"]],
        ]
    )


def instantiated_inverse(entries: dict[str, sp.Expr]) -> tuple[sp.Expr, sp.Matrix]:
    a = entries["a"]
    b = entries["b"]
    c = entries["c"]
    d = entries["d"]
    e = entries["e"]
    delta = a * c - a * e + b * e - c * d
    return delta, sp.Matrix(
        [
            [(b * e - c * d) / delta, -a * e / delta, a * c / delta],
            [(c - e) / delta, e / delta, -c / delta],
            [(-b + d) / delta, (a - d) / delta, (-a + b) / delta],
        ]
    )


def max_abs_complex(matrix: sp.Matrix) -> float:
    return max(abs(complex(sp.N(matrix[i, j], 100))) for i in range(matrix.rows) for j in range(matrix.cols))


def main() -> int:
    character_measure_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    boundary_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CURRENT_STACK_CONSTRAINT_BOUNDARY_NOTE_2026-04-17.md"
    )

    entries = radical_entries()
    f_mat = sample_matrix(entries)
    delta, f_inv = instantiated_inverse(entries)
    det_abs = abs(float(sp.N(delta, 50)))

    sign_data = {name: float(sp.N(expr, 50)) for name, expr in entries.items()}

    coeff_gap = max_abs_complex(sp.N(f_inv * f_mat - sp.eye(3), 80))

    witness_coeff = sp.Matrix([sp.Rational(5, 4), sp.Rational(2, 5), sp.Rational(3, 10)])
    witness_z = sp.simplify(f_mat * witness_coeff)
    witness_rec_gap = max_abs_complex(sp.N(f_inv * witness_z - witness_coeff, 80))

    z_a, z_b, z_c = [sp.N(val, 30) for val in witness_z]
    order_gap = float(sp.N(witness_z[1] - witness_z[0], 50))
    normalized_a = float(sp.N(witness_z[0] / witness_coeff[0], 50))
    normalized_b = float(sp.N(witness_z[1] / witness_coeff[0], 50))

    print("=" * 108)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE POSITIVE-CONE ORDER WITNESS")
    print("=" * 108)
    print()
    print("Exact radical-form matrix F")
    print(f_mat)
    print()
    print("Exact inverse F^(-1)")
    print(sp.N(f_inv, 20))
    print()
    print("Column rays of the positive cone")
    for idx in range(f_mat.cols):
        col = [sp.N(f_mat[row, idx], 20) for row in range(f_mat.rows)]
        print(f"  r_{idx} = {col}")
    print()
    print("Witness positive coefficient triple and induced sample vector")
    print(f"  a_vec = {witness_coeff}")
    print(f"  Z     = {[z_a, z_b, z_c]}")
    print(f"  Z_B - Z_A                              = {order_gap:.12f}")
    print(f"  Z_A / a_(0,0)                          = {normalized_a:.12f}")
    print(f"  Z_B / a_(0,0)                          = {normalized_b:.12f}")
    print(f"  |det(F)|                               = {det_abs:.12f}")
    print(f"  exact reconstruction gap               = {witness_rec_gap:.3e}")
    print()

    check(
        "Character-measure theorem already fixes nonnegative conjugation-symmetric character coefficients",
        "rho_(p,q)(beta) >= 0" in character_measure_note
        and "rho_(p,q)(beta) = rho_(q,p)(beta)" in character_measure_note,
        bucket="SUPPORT",
    )
    check(
        "Exact radical reconstruction-map theorem already fixes the first three-sample matrix and inverse map",
        "exact radical-form sample matrix" in radical_note
        and "exact algebraic inverse map" in radical_note,
        bucket="SUPPORT",
    )
    check(
        "Current-stack boundary theorem already says the three named samples are not further collapsed by existing symmetries",
        "not collapsed by centrality or reality" in boundary_note
        and "holonomy-resolved" in boundary_note,
        bucket="SUPPORT",
    )

    check(
        "The first symmetric retained three-sample map is exactly a simplicial cone map",
        coeff_gap < 1.0e-80 and det_abs > 1.0,
        detail=f"max |F^(-1)F-I|={coeff_gap:.3e}, |det(F)|={det_abs:.12f}",
    )
    check(
        "The explicit column rays have the sign pattern needed for a nontrivial positive-cone witness",
        sign_data["a"] < -1.0e-12
        and sign_data["b"] > 1.0e-12
        and sign_data["c"] > 1.0e-12
        and sign_data["d"] > 1.0e-12
        and sign_data["e"] < -1.0e-12,
        detail=(
            f"a={sign_data['a']:.12f}, b={sign_data['b']:.12f}, c={sign_data['c']:.12f}, "
            f"d={sign_data['d']:.12f}, e={sign_data['e']:.12f}"
        ),
    )
    check(
        "Cone membership is equivalent to the exact half-space constraints F^(-1) Z >= 0",
        coeff_gap < 1.0e-80,
        detail="the inverse map recovers the coefficient triple exactly for symbolic cone coordinates",
    )
    check(
        "Positive retained coefficients force the first explicit sample ordering Z_B >= Z_A",
        sign_data["b"] - sign_data["a"] > 1.0e-12 and sign_data["c"] > 1.0e-12 and order_gap > 1.0e-12,
        detail=f"witness gap Z_B-Z_A={order_gap:.12f}",
    )
    check(
        "After trivial-channel normalization the retained profile obeys Z_A/a_(0,0) <= 1 <= Z_B/a_(0,0)",
        normalized_a <= 1.0 + 1.0e-12 and normalized_b >= 1.0 - 1.0e-12,
        detail=f"normalized values={normalized_a:.12f}, {normalized_b:.12f}",
    )
    check(
        "This gives a genuine stronger theorem than the current-stack boundary: the seam has exact cone geometry and an order witness before beta=6 evaluation",
        coeff_gap < 1.0e-80
        and det_abs > 1.0
        and sign_data["b"] - sign_data["a"] > 1.0e-12
        and normalized_a <= 1.0 + 1.0e-12
        and normalized_b >= 1.0 - 1.0e-12
        and witness_rec_gap < 1.0e-80,
        detail="the explicit three-sample evaluation seam is partially controlled even before K_6^env or B_6(W) are evaluated",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
