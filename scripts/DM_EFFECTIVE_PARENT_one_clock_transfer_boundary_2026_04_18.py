#!/usr/bin/env python3
"""
Verifier for the effective-parent one-clock transfer boundary note.

The script does two things:

1. audits the exact local premises already on main:
   - pure Wilson one-clock transfer exists on the gauge side;
   - the retained strong-CP note gives the determinant-dressed action and
     positivity / reality of the determinant.
2. runs a finite toy witness showing that an exact one-clock transfer law can
   exist on an enlarged auxiliary space while scalar edge factorization of the
   determinant dressing still fails.
"""

from __future__ import annotations

import itertools
import math
import sys
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
    return (ROOT / rel_path).read_text(encoding="utf-8")


def toy_matrix(mass: float, edges: list[tuple[float, float]]) -> np.ndarray:
    (r0, s0), (r1, s1), (r2, s2) = edges
    return np.array(
        [
            [mass, r0, s2],
            [s0, mass, r1],
            [r2, s1, mass],
        ],
        dtype=float,
    )


def toy_det_formula(mass: float, edges: list[tuple[float, float]]) -> float:
    (r0, s0), (r1, s1), (r2, s2) = edges
    return (
        mass**3
        - mass * (r0 * s0 + r1 * s1 + r2 * s2)
        + r0 * r1 * r2
        + s0 * s1 * s2
    )


def transfer_block(mass: float, edge: tuple[float, float]) -> np.ndarray:
    r_t, s_t = edge
    t = np.zeros((4, 4), dtype=float)
    t[:2, :2] = np.array([[mass, -r_t * s_t], [1.0, 0.0]], dtype=float)
    t[2, 2] = r_t
    t[3, 3] = s_t
    return t


def transfer_trace(mass: float, edges: list[tuple[float, float]]) -> float:
    t_total = np.eye(4, dtype=float)
    for edge in edges:
        t_total = transfer_block(mass, edge) @ t_total
    return float(np.trace(t_total))


def mixed_third_difference(
    mass: float,
    low_edges: list[tuple[float, float]],
    high_edges: list[tuple[float, float]],
) -> float:
    total = 0.0
    for bits in itertools.product([0, 1], repeat=3):
        edges = [high_edges[i] if bits[i] else low_edges[i] for i in range(3)]
        value = math.log(toy_det_formula(mass, edges))
        total += ((-1) ** (3 - sum(bits))) * value
    return total


def additive_fit_residual(mass: float, states: list[tuple[float, float]]) -> float:
    rows = []
    vals = []
    for idxs in itertools.product(range(len(states)), repeat=3):
        edges = [states[i] for i in idxs]
        rows.append(
            [
                1.0,
                1.0 if idxs[0] == 0 else 0.0,
                1.0 if idxs[0] == 1 else 0.0,
                1.0 if idxs[1] == 0 else 0.0,
                1.0 if idxs[1] == 1 else 0.0,
                1.0 if idxs[2] == 0 else 0.0,
                1.0 if idxs[2] == 1 else 0.0,
            ]
        )
        vals.append(math.log(toy_det_formula(mass, edges)))
    a = np.array(rows, dtype=float)
    b = np.array(vals, dtype=float)
    coeffs, _, _, _ = np.linalg.lstsq(a, b, rcond=None)
    residual = a @ coeffs - b
    return float(np.max(np.abs(residual)))


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md")
    strong_cp_note = read("docs/STRONG_CP_THETA_ZERO_NOTE.md")
    audit_note = read("docs/DM_WILSON_PARENT_CORRECTNESS_AUDIT_NOTE_2026-04-18.md")

    mass = 1.7
    sample_edges = [
        [(0.21, 0.15), (0.13, 0.24), (0.17, 0.11)],
        [(0.28, 0.16), (0.19, 0.21), (0.14, 0.27)],
        [(0.09, 0.22), (0.24, 0.18), (0.31, 0.12)],
        [(0.18, 0.09), (0.27, 0.19), (0.22, 0.14)],
    ]
    low_edges = [(0.10, 0.14), (0.11, 0.15), (0.12, 0.16)]
    high_edges = [(0.29, 0.23), (0.27, 0.24), (0.31, 0.21)]
    additive_states = [
        (0.10, 0.14),
        (0.22, 0.18),
        (0.31, 0.24),
    ]

    formula_errors = []
    transfer_errors = []
    determinants = []
    transfer_values = []
    for edges in sample_edges:
        matrix = toy_matrix(mass, edges)
        det_direct = float(np.linalg.det(matrix))
        det_formula = toy_det_formula(mass, edges)
        det_transfer = transfer_trace(mass, edges)
        determinants.append(det_direct)
        transfer_values.append(det_transfer)
        formula_errors.append(abs(det_direct - det_formula))
        transfer_errors.append(abs(det_direct - det_transfer))

    cube_dets = []
    for bits in itertools.product([0, 1], repeat=3):
        edges = [high_edges[i] if bits[i] else low_edges[i] for i in range(3)]
        cube_dets.append(toy_det_formula(mass, edges))

    third_diff = mixed_third_difference(mass, low_edges, high_edges)
    fit_residual = additive_fit_residual(mass, additive_states)

    print("=" * 88)
    print("DM EFFECTIVE PARENT ONE-CLOCK TRANSFER BOUNDARY")
    print("=" * 88)

    print("\n" + "=" * 88)
    print("PART 1: CURRENT-STACK PREMISES")
    print("=" * 88)
    check(
        "the pure-gauge plaquette lane already has an exact one-clock transfer law",
        "`Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]`" in transfer_note
        and "positive self-adjoint transfer operator `T_(L_s,beta)`" in transfer_note,
    )
    check(
        "the retained strong-CP note carries the determinant-dressed action formula",
        "Z = ∫ DU det(D[U] + m) e^{-S_Wilson[U]}" in strong_cp_note
        and "S_eff[U] = S_Wilson[U] - ln det(D[U] + m)" in strong_cp_note,
    )
    check(
        "the same strong-CP note proves positivity / reality of the retained determinant dressing",
        "det(D[U]+m) > 0" in strong_cp_note
        and "Leg C: Gauge-sector radiative non-generation" in strong_cp_note
        and "ln det(D[U]+m)` is real" in strong_cp_note,
    )
    check(
        "the audit note leaves the effective-parent route open as a genuinely new theorem target",
        "**Effective-parent route.**" in audit_note
        and "Derive an exact retained parent operator" in audit_note,
    )

    print("\n" + "=" * 88)
    print("PART 2: TOY EXACT ONE-CLOCK TRANSFER ON AN ENLARGED AUXILIARY SPACE")
    print("=" * 88)
    print(f"  mass parameter                          = {mass:.3f}")
    print(f"  determinant samples                     = {[round(v, 12) for v in determinants]}")
    print(f"  transfer-trace samples                  = {[round(v, 12) for v in transfer_values]}")
    print(f"  max direct-vs-formula error             = {max(formula_errors):.3e}")
    print(f"  max direct-vs-transfer error            = {max(transfer_errors):.3e}")
    check(
        "the toy cyclic nearest-neighbor determinant obeys the closed polynomial formula",
        max(formula_errors) < 1.0e-12,
        detail=f"max direct-vs-formula error = {max(formula_errors):.3e}",
    )
    check(
        "the same toy determinant has an exact one-clock transfer trace on a 4-state auxiliary space",
        max(transfer_errors) < 1.0e-12,
        detail=f"max direct-vs-transfer error = {max(transfer_errors):.3e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: POSITIVITY DOES NOT FORCE SCALAR EDGE FACTORIZATION")
    print("=" * 88)
    print(f"  positive determinant cube min/max       = {min(cube_dets):.12f}, {max(cube_dets):.12f}")
    print(f"  mixed third difference of log(det)      = {third_diff:.12e}")
    print(f"  best additive fit residual              = {fit_residual:.12e}")
    check(
        "the toy determinant remains strictly positive on the audited edge cube",
        min(cube_dets) > 0.0,
        detail=f"min determinant = {min(cube_dets):.6f}",
    )
    check(
        "a nonzero mixed third edge-difference of log(det) rules out exact edge-additive factorization on that cube",
        abs(third_diff) > 1.0e-8,
        detail=f"mixed third difference = {third_diff:.6e}",
    )

    check(
        "the toy transfer witness is only an auxiliary-space transfer, not a scalar one-step edge product",
        max(transfer_errors) < 1.0e-12 and abs(third_diff) > 1.0e-8,
        detail="exact one-clock transfer survives while log(det) is still not edge-additive",
        bucket="SUPPORT",
    )
    check(
        "least-squares fitting also fails to compress the toy log(det) to a constant plus one independent term per edge",
        fit_residual > 1.0e-6,
        detail=f"max additive-fit residual = {fit_residual:.6e}",
        bucket="SUPPORT",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
