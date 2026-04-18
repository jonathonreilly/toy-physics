#!/usr/bin/env python3
"""
Higher-orbit underdetermination from the first sample packet
(e, W_A, W_B, W_C) on the plaquette PF lane.
"""

from __future__ import annotations

import cmath
import math
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


SAMPLES = {
    "W_A": (-13 * math.pi / 16.0, 5 * math.pi / 8.0),
    "W_B": (-5 * math.pi / 16.0, -7 * math.pi / 16.0),
    "W_C": (7 * math.pi / 16.0, -11 * math.pi / 16.0),
}

ORBITS = [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = [
        cmath.exp(1j * theta1),
        cmath.exp(1j * theta2),
        cmath.exp(-1j * (theta1 + theta2)),
    ]
    lam = [p + q, q, 0]
    num = np.array([[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    den = np.array([[x[i] ** (2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    return complex(np.linalg.det(num) / np.linalg.det(den))


def orbit_row(p: int, q: int) -> np.ndarray:
    d = dim_su3(p, q)
    mult = 1 if p == q else 2
    row = [float(mult * d * d)]
    for theta1, theta2 in SAMPLES.values():
        ch = su3_character(p, q, theta1, theta2)
        value = d * ch if p == q else 2.0 * (d * ch).real
        row.append(float(np.real_if_close(value)))
    return np.array(row, dtype=float)


def summary_matrix() -> np.ndarray:
    return np.column_stack([orbit_row(p, q) for p, q in ORBITS])


def main() -> int:
    evaluator_route_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    mtx = summary_matrix()
    rank = int(np.linalg.matrix_rank(mtx))
    nullity = len(ORBITS) - rank
    _, svals, vt = np.linalg.svd(mtx)
    kernel = vt[-1]
    kernel_resid = float(np.max(np.abs(mtx @ kernel)))
    mixed_sign = bool(np.any(kernel > 1.0e-8) and np.any(kernel < -1.0e-8))

    baseline = np.ones(len(ORBITS), dtype=float)
    eps = 0.49 / float(np.max(np.abs(kernel)))
    plus = baseline + eps * kernel
    minus = baseline - eps * kernel
    summary_plus = mtx @ plus
    summary_minus = mtx @ minus
    summary_gap = float(np.max(np.abs(summary_plus - summary_minus)))
    min_plus = float(np.min(plus))
    min_minus = float(np.min(minus))

    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE IDENTITY-PLUS-THREE-SAMPLE HIGHER-ORBIT UNDERDETERMINATION")
    print("=" * 118)
    print()
    print("Chosen higher-orbit slice")
    print(f"  orbit representatives                        = {ORBITS}")
    print(f"  summary matrix shape                         = {mtx.shape}")
    print(f"  matrix rank / nullity                        = {rank} / {nullity}")
    print(f"  singular values                              = {svals}")
    print()
    print("Kernel witness and positive perturbation pair")
    print(f"  kernel vector                                = {kernel}")
    print(f"  max |M k|                                    = {kernel_resid:.3e}")
    print(f"  epsilon                                      = {eps:.12f}")
    print(f"  min(b + eps k), min(b - eps k)               = {min_plus:.12f}, {min_minus:.12f}")
    print(f"  max summary gap                              = {summary_gap:.3e}")
    print()

    check(
        "The evaluator-route note already fixes the three named values as linear functionals of one beta-side vector",
        "`mathbf_Z_6 = E_3(v_6)`" in evaluator_route_note
        and "fixed three-row sample operator" in evaluator_route_note,
        bucket="SUPPORT",
    )
    check(
        "The truncation-envelope note already treats identity and named samples as linear functionals of the coefficient bank",
        "`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`" in envelope_note
        and "`Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`" in envelope_note,
        bucket="SUPPORT",
    )
    check(
        "The PF boundary note already records that the current route acts on one still-underdetermined beta-side vector",
        "one common beta-side vector" in pf_note
        and "still does not determine the common beta-side" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "The chosen higher-orbit slice has dimension five while the first sample packet supplies only four scalar summaries",
        mtx.shape == (4, 5),
        detail=f"shape={mtx.shape}",
    )
    check(
        "Therefore the higher-orbit summary map has nontrivial kernel on that slice",
        nullity >= 1,
        detail=f"rank={rank}, nullity={nullity}",
    )
    check(
        "Any kernel vector must have mixed sign because the identity row has strictly positive orbit weights",
        np.all(mtx[0] > 0.0) and mixed_sign,
        detail=f"identity weights={mtx[0]}",
    )
    check(
        "A strictly positive baseline can be perturbed by plus/minus epsilon times that kernel vector while remaining nonnegative",
        min_plus > 0.0 and min_minus > 0.0,
        detail=f"mins=({min_plus:.12f}, {min_minus:.12f})",
    )
    check(
        "Those two distinct nonnegative higher-orbit coefficient stacks have the same identity value and the same three named sample values",
        kernel_resid < 1.0e-10 and summary_gap < 1.0e-10,
        detail=f"kernel residual={kernel_resid:.3e}, summary gap={summary_gap:.3e}",
    )
    check(
        "So even the full first sample packet (e, W_A, W_B, W_C) does not determine the full higher-orbit beta-side coefficient stack",
        nullity >= 1 and mixed_sign and min_plus > 0.0 and min_minus > 0.0 and summary_gap < 1.0e-10,
        detail="four scalar summaries leave a nontrivial positive higher-orbit ambiguity",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
