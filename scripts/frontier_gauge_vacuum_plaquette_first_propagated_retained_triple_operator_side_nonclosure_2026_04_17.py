#!/usr/bin/env python3
"""
Operator-side nonclosure at the minimal propagated plaquette target:
even exact evaluation of the propagated retained three-sample triple does not
determine the full beta-side vector or the unresolved operator-side beta=6
data on the present bank.
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

SAMPLES = {
    "W_A": (-13 * math.pi / 16.0, 5 * math.pi / 8.0),
    "W_B": (-5 * math.pi / 16.0, -7 * math.pi / 16.0),
    "W_C": (7 * math.pi / 16.0, -11 * math.pi / 16.0),
}

ORBITS = [(0, 2), (0, 3), (0, 4), (0, 5)]
BASELINE = np.ones(4, dtype=float)
EPSILON = 4.0 / 5.0


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
    x = [
        cmath.exp(1j * theta1),
        cmath.exp(1j * theta2),
        cmath.exp(-1j * (theta1 + theta2)),
    ]
    lam = [p + q, q, 0]
    num = np.array([[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    den = np.array([[x[i] ** (2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    return complex(np.linalg.det(num) / np.linalg.det(den))


def orbit_sample_row(p: int, q: int) -> np.ndarray:
    d = dim_su3(p, q)
    mult = 1 if p == q else 2
    row = []
    for theta1, theta2 in SAMPLES.values():
        ch = su3_character(p, q, theta1, theta2)
        value = d * ch if p == q else 2.0 * (d * ch).real
        row.append(float(np.real_if_close(value)))
    return np.array(row, dtype=float)


def main() -> int:
    target_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md"
    )
    evaluator_route_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    finite_packet_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md"
    )
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )

    sample_matrix = np.column_stack([orbit_sample_row(*orbit) for orbit in ORBITS])
    rank = int(np.linalg.matrix_rank(sample_matrix))
    _, _, vh = np.linalg.svd(sample_matrix)
    kernel = vh[-1]
    residual = sample_matrix @ kernel
    residual_norm = float(np.max(np.abs(residual)))
    sign_change = float(np.min(kernel)) < -1.0e-8 and float(np.max(kernel)) > 1.0e-8

    p_vec = BASELINE + EPSILON * kernel
    q_vec = BASELINE - EPSILON * kernel
    p_min = float(np.min(p_vec))
    q_min = float(np.min(q_vec))
    triple_p = sample_matrix @ p_vec
    triple_q = sample_matrix @ q_vec
    triple_gap = float(np.max(np.abs(triple_p - triple_q)))
    coeff_gap = float(np.max(np.abs(p_vec - q_vec)))

    print("=" * 124)
    print("GAUGE-VACUUM PLAQUETTE FIRST PROPAGATED RETAINED TRIPLE OPERATOR-SIDE NONCLOSURE")
    print("=" * 124)
    print()
    print(f"higher-orbit slice                           = {ORBITS}")
    print(f"sample-matrix shape                         = {sample_matrix.shape}")
    print(f"sample-matrix rank                          = {rank}")
    print(f"kernel vector                               = {kernel}")
    print(f"kernel residual max-norm                    = {residual_norm:.12e}")
    print()
    print(f"baseline                                    = {BASELINE}")
    print(f"epsilon                                     = {EPSILON:.12f}")
    print(f"P                                           = {p_vec}")
    print(f"Q                                           = {q_vec}")
    print(f"min(P), min(Q)                              = {p_min:.12f}, {q_min:.12f}")
    print(f"T_3(P)                                      = {triple_p}")
    print(f"T_3(Q)                                      = {triple_q}")
    print(f"max propagated-triple gap                   = {triple_gap:.12e}")
    print(f"max coefficient gap                         = {coeff_gap:.12f}")
    print()

    check(
        "The propagated-triple target note already identifies the three named propagated values as the minimal honest next plaquette evaluator target",
        "propagated retained three-sample output" in target_note
        and "`(Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`" in target_note,
        bucket="SUPPORT",
    )
    check(
        "The evaluator-route note already fixes the exact operator-side route as one common beta-side vector acted on by one fixed three-row operator",
        "`mathbf_Z_6 = E_3(v_6)`" in evaluator_route_note
        and "common beta-side vector" in evaluator_route_note
        and "fixed three-row sample operator" in evaluator_route_note,
        bucket="SUPPORT",
    )
    check(
        "The finite-sample nonclosure note already closes any hope that finite sample packets by themselves determine the full beta-side vector",
        "no finite sample packet" in finite_packet_note
        and "full beta-side vector `v_6`" in finite_packet_note,
        bucket="SUPPORT",
    )
    check(
        "The exact radical reconstruction-map note already shows the propagated triple determines the first retained propagated block without determining the full higher-orbit data",
        "exact algebraic map" in radical_note
        and "the three named sample values" in radical_note,
        bucket="SUPPORT",
    )

    check(
        "On the explicit four-orbit slice the propagated-triple map has codomain dimension three and domain dimension four, so rank-nullity leaves nontrivial kernel freedom",
        sample_matrix.shape == (3, 4) and rank == 3,
        detail=f"shape={sample_matrix.shape}, rank={rank}, nullity={sample_matrix.shape[1] - rank}",
    )
    check(
        "The runner exhibits an explicit kernel direction for the propagated-triple map on that slice",
        residual_norm < 1.0e-10,
        detail=f"max |T_3(k)| = {residual_norm:.12e}",
    )
    check(
        "That explicit kernel direction changes sign, so positive ambiguity can be realized around a strictly positive baseline",
        sign_change,
        detail=f"min(k)={np.min(kernel):.12f}, max(k)={np.max(kernel):.12f}",
    )
    check(
        "A strictly positive baseline plus/minus epsilon times the kernel direction stays entrywise nonnegative",
        p_min > 0.0 and q_min > 0.0,
        detail=f"min(P)={p_min:.12f}, min(Q)={q_min:.12f}",
    )
    check(
        "Those two distinct nonnegative higher-orbit coefficient stacks produce the same propagated retained triple",
        triple_gap < 1.0e-10 and coeff_gap > 1.0e-6,
        detail=f"max |T_3(P)-T_3(Q)| = {triple_gap:.12e}, max |P-Q| = {coeff_gap:.12f}",
    )
    check(
        "Therefore even exact evaluation of the propagated retained triple would still not determine the full beta-side vector or the unresolved operator-side beta=6 data on the current bank",
        triple_gap < 1.0e-10 and coeff_gap > 1.0e-6,
        detail="same propagated triple, different admissible higher-orbit coefficient stacks",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
