#!/usr/bin/env python3
"""
Explicit positive rank-one transfer realization of the completed first-sector
plaquette triple Z_min.

This is new machinery beyond the current explicit spatial_pair witness family:

  1. the completed triple Z_min already determines one exact retained
     first-symmetric coefficient vector;
  2. that coefficient vector can be realized exactly as the propagated boundary
     vector of one explicit positive self-adjoint conjugation-symmetric
     rank-one transfer operator;
  3. so existence of a class-sector transfer realization is no longer open.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import sympy as sp

from frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17 import (
    sample_angle_units,
)
from frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17 import (
    radical_entries,
    sample_matrix,
    su3_partition_sum,
)
from frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17 import (
    evaluation_matrix,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def completed_sector_data() -> tuple[np.ndarray, np.ndarray]:
    entries = radical_entries()
    f_mat = sample_matrix(entries)
    f_inv = sp.simplify(f_mat.inv())
    z_1plaq, _mode_cutoff = su3_partition_sum(6.0)
    z_loc = sp.Matrix(
        [
            sp.N(sp.exp(entries["a"] / 3) / z_1plaq, 80),
            sp.N(sp.exp(entries["b"] / 3) / z_1plaq, 80),
            sp.N(sp.exp(entries["d"] / 3) / z_1plaq, 80),
        ]
    )
    a_loc = sp.N(f_inv * z_loc, 80)
    a00 = float(sp.N(a_loc[0], 50))
    a10 = float(sp.N(a_loc[1], 50))
    z_min = np.array([float(sp.N(v, 50)) for v in sp.N(f_mat * sp.Matrix([a_loc[0], a_loc[1], sp.Integer(0)]), 80)], dtype=float)
    v_min = np.array([a00, a10, a10, 0.0], dtype=float)
    return v_min, z_min


def rank_one_transfer_for_vector(v: np.ndarray) -> np.ndarray:
    v0 = float(v[0])
    norm_sq = float(np.dot(v, v))
    lam = (1.0 / (v0 * (norm_sq**2))) ** (1.0 / 3.0)
    return lam * np.outer(v, v)


def main() -> int:
    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR RANK-ONE TRANSFER REALIZATION")
    print("=" * 112)
    print()
    print("Question:")
    print("  Does the explicit completed first-sector triple Z_min admit one exact")
    print("  positive class-sector transfer realization beyond the current witness")
    print("  family ansatz?")

    completion_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md"
    )
    evaluator_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    boundary_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md"
    )

    v_min, z_min = completed_sector_data()
    weights = [(0, 0), (1, 0), (0, 1), (1, 1)]
    sample_angles = [(u1 * np.pi / 16.0, u2 * np.pi / 16.0) for u1, u2 in sample_angle_units().values()]
    e_three = evaluation_matrix(weights, sample_angles)
    z_eval = np.real_if_close(e_three @ v_min).real

    t_min = rank_one_transfer_for_vector(v_min)
    e0 = np.zeros(4, dtype=float)
    e0[0] = 1.0
    propagated = np.linalg.matrix_power(t_min, 3) @ e0

    swap = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    transfer_sym_err = float(np.max(np.abs(t_min - t_min.T)))
    transfer_swap_err = float(np.max(np.abs(swap @ t_min - t_min @ swap)))
    propagated_gap = float(np.linalg.norm(propagated - v_min))
    eig_min = float(np.min(np.linalg.eigvalsh(t_min)))
    z_gap = float(np.linalg.norm(z_eval - z_min))

    print()
    print(f"  v_min                                       = {np.round(v_min, 12).tolist()}")
    print(f"  Z_min                                       = {np.round(z_min, 12).tolist()}")
    print(f"  E_3 v_min                                   = {np.round(z_eval, 12).tolist()}")
    print(f"  propagated vector T_min^3 e_0               = {np.round(propagated, 12).tolist()}")
    print(f"  transfer symmetry / swap errors             = {transfer_sym_err:.3e} / {transfer_swap_err:.3e}")
    print(f"  min eigenvalue(T_min)                       = {eig_min:.3e}")
    print()

    check(
        "The completion note already fixes one explicit completed triple Z_min and the corresponding retained first-sector coefficient data",
        "completed sample triple" in completion_note
        and "a^min" in completion_note,
    )
    check(
        "The evaluator route still identifies the live three-sample object as linear evaluation of a beta-side class-sector vector",
        "common beta-side vector" in evaluator_note
        and "fixed three-row sample operator" in evaluator_note,
    )
    check(
        "The current explicit witness-family boundary note only closes the old family ansatz, not existence of a transfer realization itself",
        "best audited scaled fit" in boundary_note
        and "still not realized exactly" in boundary_note,
    )
    check(
        "The completed first-sector vector v_min evaluates exactly to Z_min on the retained four-weight first-symmetric sector",
        z_gap < 1.0e-12,
        f"||E_3 v_min - Z_min||={z_gap:.3e}",
    )
    check(
        "One explicit positive self-adjoint conjugation-symmetric rank-one transfer operator T_min propagates e_0 exactly to v_min at depth 3",
        propagated_gap < 1.0e-12
        and transfer_sym_err < 1.0e-12
        and transfer_swap_err < 1.0e-12
        and eig_min > -1.0e-12,
        f"(prop_gap,eig_min)=({propagated_gap:.3e},{eig_min:.3e})",
    )
    check(
        "So existence of a positive class-sector transfer realization for Z_min is now explicit; what remains open is deriving or embedding the right realization from the actual Wilson/Perron framework-point packet",
        propagated_gap < 1.0e-12 and z_gap < 1.0e-12,
        f"v_min={np.round(v_min, 10).tolist()}",
    )

    print("\n" + "=" * 112)
    print("RESULT")
    print("=" * 112)
    print("  Exact constructive upgrade:")
    print("    - the completed triple Z_min already determines one exact retained")
    print("      first-sector coefficient vector v_min")
    print("    - one explicit positive self-adjoint conjugation-symmetric rank-one")
    print("      transfer operator realizes v_min exactly at depth 3")
    print("    - therefore existence of a class-sector transfer realization for Z_min")
    print("      is no longer open")
    print("    - the remaining honest seam is deriving / embedding the right")
    print("      framework-point Wilson/Perron realization, not bare existence")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
