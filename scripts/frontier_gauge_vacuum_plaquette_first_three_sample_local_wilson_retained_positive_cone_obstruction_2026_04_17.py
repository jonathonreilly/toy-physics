#!/usr/bin/env python3
"""
Local Wilson obstruction to first-symmetric retained positive-cone closure on
the named three-sample plaquette PF seam.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import sympy as sp
from scipy.special import iv


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

BETA = 6.0
MODE_TOL = 1.0e-15
MAX_MODE = 120


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


def bessel_matrix(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [[iv(mode + i - j, arg) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def su3_partition_sum(beta: float, tol: float = MODE_TOL, max_mode: int = MAX_MODE) -> tuple[float, int]:
    total_partition = 0.0
    used = max_mode

    for mode in range(max_mode + 1):
        strip_partition = 0.0
        modes = [0] if mode == 0 else [-mode, mode]
        for signed_mode in modes:
            strip_partition += float(np.linalg.det(bessel_matrix(beta, signed_mode)))

        total_partition += strip_partition

        if mode >= 3 and abs(strip_partition) < tol * abs(total_partition):
            used = mode
            break

    return total_partition, used


def max_abs_complex(matrix: sp.Matrix) -> float:
    return max(abs(complex(sp.N(matrix[i, j], 100))) for i in range(matrix.rows) for j in range(matrix.cols))


def main() -> int:
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    cone_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md"
    )
    local_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md"
    )
    rim_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )

    entries = radical_entries()
    f_mat = sample_matrix(entries)
    f_inv = sp.simplify(f_mat.inv())
    det_abs = abs(float(sp.N(f_mat.det(), 50)))

    z_1plaq, max_mode = su3_partition_sum(BETA)
    z_loc = sp.Matrix(
        [
            sp.N(sp.exp(entries["a"] / 3) / z_1plaq, 80),
            sp.N(sp.exp(entries["b"] / 3) / z_1plaq, 80),
            sp.N(sp.exp(entries["d"] / 3) / z_1plaq, 80),
        ]
    )
    coeff = sp.N(f_inv * z_loc, 80)
    rec_gap = max_abs_complex(sp.N(f_mat * coeff - z_loc, 80))

    coeff_vals = [float(sp.N(val, 50)) for val in coeff]
    sample_vals = [float(sp.N(val, 50)) for val in z_loc]
    order_gap = sample_vals[1] - sample_vals[0]
    repair = -coeff_vals[2]

    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE FIRST THREE-SAMPLE LOCAL WILSON RETAINED POSITIVE-CONE OBSTRUCTION")
    print("=" * 112)
    print()
    print("Exact first-symmetric radical sample matrix F")
    print(f_mat)
    print()
    print("Exact normalized local Wilson one-plaquette sample triple")
    print(f"  Z_loc(W_A)                                = {sample_vals[0]:.15f}")
    print(f"  Z_loc(W_B)                                = {sample_vals[1]:.15f}")
    print(f"  Z_loc(W_C)                                = {sample_vals[2]:.15f}")
    print(f"  Z_(1plaq)(6)                              = {z_1plaq:.15f}   (mode cutoff m = {max_mode})")
    print()
    print("Exact reconstructed first-symmetric retained coordinates a_loc = F^(-1) Z_loc")
    print(f"  a_loc_(0,0)                               = {coeff_vals[0]:.15f}")
    print(f"  a_loc_(1,0)                               = {coeff_vals[1]:.15f}")
    print(f"  a_loc_(1,1)                               = {coeff_vals[2]:.15f}")
    print(f"  reconstruction gap                        = {rec_gap:.3e}")
    print(f"  |det(F)|                                  = {det_abs:.12f}")
    print(f"  local order gap Z_loc(W_B)-Z_loc(W_A)     = {order_gap:.15f}")
    print(f"  minimal adjoint-channel repair            = {repair:.15f}")
    print()

    check(
        "Exact radical-map note already fixes the first-symmetric three-sample matrix and inverse reconstruction law",
        "exact radical-form sample matrix" in radical_note
        and "exact algebraic inverse map" in radical_note,
        bucket="SUPPORT",
    )
    check(
        "Positive-cone note already fixes cone membership as the exact half-space test F^(-1) Z >= 0",
        "F^(-1) Z >= 0" in cone_note and "positive cone" in cone_note,
        bucket="SUPPORT",
    )
    check(
        "Local Wilson partial-evaluation note already fixes the exact normalized local one-plaquette sample triple",
        "w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484" in local_note
        and "w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005416" in local_note
        and "w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746343" in local_note,
        bucket="SUPPORT",
    )
    check(
        "Full-slice rim-lift note still records that explicit B_6(W) remains open, so any fix must come from the nonlocal completion side",
        "What remains open is the explicit `beta = 6` evaluation problem." in rim_note
        and "explicit closed-form `B_6(W)`" in rim_note,
        bucket="SUPPORT",
    )

    check(
        "The exact local Wilson sample triple reconstructs uniquely through the radical map",
        rec_gap < 1.0e-75 and det_abs > 1.0,
        detail=f"max |F a_loc - Z_loc|={rec_gap:.3e}, |det(F)|={det_abs:.12f}",
    )
    check(
        "The reconstructed local retained coordinates have a strictly negative adjoint component",
        coeff_vals[0] > 1.0e-12 and coeff_vals[1] > 1.0e-12 and coeff_vals[2] < -1.0e-12,
        detail=(
            f"a_loc=( {coeff_vals[0]:.15f}, {coeff_vals[1]:.15f}, {coeff_vals[2]:.15f} )"
        ),
    )
    check(
        "Therefore the exact local Wilson triple lies outside the first-symmetric retained positive cone",
        coeff_vals[2] < -1.0e-12,
        detail="cone membership would require all three reconstructed retained coordinates to be nonnegative",
    )
    check(
        "The obstruction is sharper than the coarse order witness: Z_loc(W_B) > Z_loc(W_A) still holds while the cone test fails",
        order_gap > 1.0e-12 and coeff_vals[2] < -1.0e-12,
        detail=f"order gap={order_gap:.15f}, failing coordinate a_loc_(1,1)={coeff_vals[2]:.15f}",
    )
    check(
        "Any first-symmetric retained positive-type repair needs a positive adjoint-channel correction of at least -a_loc_(1,1)",
        repair > 1.0e-12,
        detail=f"minimal retained-channel repair in the adjoint coordinate={repair:.15f}",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
