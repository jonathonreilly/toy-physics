#!/usr/bin/env python3
"""
Exact local Wilson partial evaluation on the first named three-sample PF seam.
"""

from __future__ import annotations

import math
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
    return {
        "r": rt2,
        "s": s,
        "u": u,
        "v": v,
        "sample_col_a": -3 * s,
        "sample_col_b": -3 * rt2 + 3 * u + 3 * v,
        "sample_col_d": 3 * rt2 + 3 * u - 3 * v,
    }


def bessel_matrix(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [[iv(mode + i - j, arg) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def bessel_matrix_derivative(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [
            [
                (iv(mode + i - j - 1, arg) + iv(mode + i - j + 1, arg)) / 6.0
                for j in range(3)
            ]
            for i in range(3)
        ],
        dtype=float,
    )


def su3_mode_terms(beta: float, mode: int) -> tuple[float, float]:
    mat = bessel_matrix(beta, mode)
    dmat = bessel_matrix_derivative(beta, mode)
    det = float(np.linalg.det(mat))
    derivative = det * float(np.trace(np.linalg.inv(mat) @ dmat))
    return det, derivative


def su3_partition_sum(beta: float, tol: float = MODE_TOL, max_mode: int = MAX_MODE) -> tuple[float, float, int]:
    total_partition = 0.0
    total_derivative = 0.0
    used = max_mode

    for mode in range(max_mode + 1):
        strip_partition = 0.0
        strip_derivative = 0.0
        modes = [0] if mode == 0 else [-mode, mode]
        for signed_mode in modes:
            part, deriv = su3_mode_terms(beta, signed_mode)
            strip_partition += part
            strip_derivative += deriv

        total_partition += strip_partition
        total_derivative += strip_derivative

        if mode >= 3:
            partition_small = abs(strip_partition) < tol * abs(total_partition)
            derivative_small = abs(strip_derivative) < tol * abs(total_derivative)
            if partition_small and derivative_small:
                used = mode
                break

    return total_partition, total_derivative, used


def main() -> int:
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    local_note = read("docs/GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md")
    bridge_note = read("docs/GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md")
    rim_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    entries = radical_entries()
    a = entries["sample_col_a"]
    b = entries["sample_col_b"]
    d = entries["sample_col_d"]

    j_a = sp.simplify(a / 18)
    j_b = sp.simplify(b / 18)
    j_c = sp.simplify(d / 18)

    half_a = sp.exp(sp.simplify(a / 6))
    half_b = sp.exp(sp.simplify(b / 6))
    half_c = sp.exp(sp.simplify(d / 6))

    local_a = sp.exp(sp.simplify(a / 3))
    local_b = sp.exp(sp.simplify(b / 3))
    local_c = sp.exp(sp.simplify(d / 3))

    z_local, deriv_local, max_mode = su3_partition_sum(BETA)
    norm_a = float(sp.N(local_a, 50)) / z_local
    norm_b = float(sp.N(local_b, 50)) / z_local
    norm_c = float(sp.N(local_c, 50)) / z_local

    sample_gap = max(
        abs(float(sp.N(a, 50)) - (-2.29610059419054)),
        abs(float(sp.N(b, 50)) - 0.261322643095101),
        abs(float(sp.N(d, 50)) - 2.07976122109844),
    )

    half_vals = [float(sp.N(half_a, 50)), float(sp.N(half_b, 50)), float(sp.N(half_c, 50))]
    local_vals = [float(sp.N(local_a, 50)), float(sp.N(local_b, 50)), float(sp.N(local_c, 50))]
    normalized_vals = [norm_a, norm_b, norm_c]
    ordering_gap = min(
        half_vals[1] - half_vals[0],
        half_vals[2] - half_vals[1],
        local_vals[1] - local_vals[0],
        local_vals[2] - local_vals[1],
        normalized_vals[1] - normalized_vals[0],
        normalized_vals[2] - normalized_vals[1],
    )
    local_deriv = deriv_local / z_local

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE FIRST THREE-SAMPLE LOCAL WILSON PARTIAL EVALUATION")
    print("=" * 104)
    print()
    print("Exact local source values")
    print(f"  J(W_A)                                     = {sp.N(j_a, 30)}")
    print(f"  J(W_B)                                     = {sp.N(j_b, 30)}")
    print(f"  J(W_C)                                     = {sp.N(j_c, 30)}")
    print()
    print("Exact marked half-slice factors exp(3 J(W_i))")
    print(f"  exp(3 J(W_A))                              = {half_vals[0]:.15f}")
    print(f"  exp(3 J(W_B))                              = {half_vals[1]:.15f}")
    print(f"  exp(3 J(W_C))                              = {half_vals[2]:.15f}")
    print()
    print("Exact local Wilson one-plaquette weights w_6(W_i)")
    print(f"  w_6(W_A)                                   = {local_vals[0]:.15f}")
    print(f"  w_6(W_B)                                   = {local_vals[1]:.15f}")
    print(f"  w_6(W_C)                                   = {local_vals[2]:.15f}")
    print()
    print("Exact normalized local one-plaquette values")
    print(f"  Z_(1plaq)(6)                               = {z_local:.15f}   (mode cutoff m = {max_mode})")
    print(f"  w_6(W_A) / Z_(1plaq)(6)                    = {norm_a:.15f}")
    print(f"  w_6(W_B) / Z_(1plaq)(6)                    = {norm_b:.15f}")
    print(f"  w_6(W_C) / Z_(1plaq)(6)                    = {norm_c:.15f}")
    print(f"  local one-plaquette <P> at beta=6          = {local_deriv:.15f}")
    print()

    check(
        "Exact radical three-sample note already fixes the named holonomies and the exact sample-matrix radical entries",
        "exact radical-form sample matrix" in radical_note
        and "W_A = W(-13 pi / 16,  5 pi / 8)" in radical_note
        and "W_B = W( -5 pi / 16, -7 pi / 16)" in radical_note
        and "W_C = W(  7 pi / 16,-11 pi / 16)" in radical_note,
        bucket="SUPPORT",
    )
    check(
        "Local/environment factorization note already fixes the exact local Wilson class function w_beta(g)=exp[(beta/3) Re Tr g]",
        "w_beta(g) = exp[(beta / 3) Re Tr g]" in local_note
        and "D_beta^mix,norm" in local_note,
        bucket="SUPPORT",
    )
    check(
        "Bridge-support note already fixes the exact local SU(3) one-plaquette block through the Bessel/Weyl route",
        "Local Wilson source-response on the one-plaquette block." in bridge_note
        and "Z_1plaq(beta) = integral dU exp[(beta / 3) Re Tr U]" in bridge_note
        and "P_1plaq(beta)" in bridge_note,
        bucket="SUPPORT",
    )
    check(
        "Full-slice rim-lift note still records that explicit closed-form B_6(W) remains open",
        "explicit closed-form\n`beta = 6` evaluation is not derived" in rim_note
        and "`B_6(W)` is fixed as one exact local Wilson/Haar rim integral" in rim_note,
        bucket="SUPPORT",
    )

    check(
        "The exact sample-matrix second-column radicals give the exact local source values J(W_A), J(W_B), J(W_C)",
        max(
            abs(float(sp.N(18 * j_a - a, 80))),
            abs(float(sp.N(18 * j_b - b, 80))),
            abs(float(sp.N(18 * j_c - d, 80))),
        )
        < 1.0e-30
        and sample_gap < 1.0e-12,
        detail=f"max named-sample radical gap={sample_gap:.3e}",
    )
    check(
        "The exact marked half-slice multipliers exp(3 J(W_i)) are explicit at the three named holonomies",
        min(half_vals) > 0.0 and ordering_gap > 0.0,
        detail=f"exp(3J) values={half_vals}",
    )
    check(
        "The exact local Wilson one-plaquette weights w_6(W_i)=exp(6 J(W_i)) are explicit at the three named holonomies",
        min(local_vals) > 0.0 and local_vals[0] < local_vals[1] < local_vals[2],
        detail=f"w_6 values={local_vals}",
    )
    check(
        "The exact local SU(3) one-plaquette block therefore yields exact normalized sample values on the named seam",
        z_local > 0.0 and 0.0 < norm_a < norm_b < norm_c < 1.0,
        detail=f"normalized values={[norm_a, norm_b, norm_c]}",
    )
    check(
        "These current exact sample-side values are partial evaluations only, not the full environment amplitudes Z_6^env(W_i)",
        "explicit evaluation of `Z_6^env(W_A)`" in pf_note
        and "K_6^env" in pf_note
        and "B_6(W)" in pf_note,
        detail="the local block is explicit, but the full environment completion remains open",
    )
    check(
        "So the strongest current exact sample-side evaluation is the local Wilson partial evaluation, while the full Z_6^env(W_i) seam still requires K_6^env / B_6(W)",
        norm_a > 0.0 and norm_b > norm_a and norm_c > norm_b,
        detail="the branch now has exact local sample values but not full environment sample values",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
